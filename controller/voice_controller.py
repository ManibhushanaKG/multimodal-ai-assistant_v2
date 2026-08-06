import time
import threading
from typing import Callable, Optional
from backend_bridge import BackendBridge


# ------------------------------------------------------------------ #
# One-time PyAudio availability check                                  #
# ------------------------------------------------------------------ #
def _check_pyaudio() -> bool:
    """Returns True if PyAudio is installed and usable."""
    try:
        import pyaudio
        pa = pyaudio.PyAudio()
        pa.terminate()
        return True
    except Exception:
        return False


def _check_speech_recognition() -> bool:
    """Returns True if speech_recognition is importable."""
    try:
        import speech_recognition as sr  # noqa: F401
        return True
    except ImportError:
        return False


_PYAUDIO_AVAILABLE = _check_pyaudio()
_SR_AVAILABLE = _check_speech_recognition()

if _SR_AVAILABLE:
    import speech_recognition as sr


class VoiceController:
    """
    Manages continuous voice command recognition, natural intent decoding,
    and voice output synthesis in a background worker thread.

    Gracefully degrades when PyAudio / speech_recognition is unavailable.
    All AI pipeline commands are decoded and dispatched here.
    """

    def __init__(self, bridge: BackendBridge, assistant_controller=None):
        self.bridge = bridge
        self.assistant_controller = assistant_controller
        self.running = False
        self.thread: Optional[threading.Thread] = None

        # Callbacks — always called via window.after(0,...) in app_controller
        self.on_status_change_callback: Optional[Callable[[str], None]] = None
        self.on_response_callback: Optional[Callable[[str], None]] = None
        self.on_recognized_text_callback: Optional[Callable[[str], None]] = None

        self.last_spoken_response = "Welcome to VisionAssist AI."

        if _SR_AVAILABLE and _PYAUDIO_AVAILABLE:
            self._recognizer = sr.Recognizer()
            self._recognizer.dynamic_energy_threshold = True
            self._recognizer.pause_threshold = 0.8
            self._recognizer.non_speaking_duration = 0.5
            print("[VoiceController] ✅ Microphone ready.")
        else:
            self._recognizer = None
            reason = "speech_recognition missing" if not _SR_AVAILABLE else "PyAudio missing"
            print(f"[VoiceController] ⚠️ Voice input disabled: {reason}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def voice_available(self) -> bool:
        return _PYAUDIO_AVAILABLE and _SR_AVAILABLE

    def start_listening(self):
        """Start continuous voice recognition background thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(
            target=self._voice_loop,
            daemon=True,
            name="VoiceListener"
        )
        self.thread.start()

    def stop_listening(self):
        """Stop voice listener thread gracefully."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        self.thread = None

    # ------------------------------------------------------------------
    # Internal: Notifiers
    # ------------------------------------------------------------------

    def _set_status(self, status: str):
        if self.on_status_change_callback:
            try:
                self.on_status_change_callback(status)
            except Exception:
                pass

    def _speak_and_notify(self, text: str):
        if not text:
            return
        self.last_spoken_response = text
        if self.on_response_callback:
            try:
                self.on_response_callback(text)
            except Exception:
                pass
        self._set_status("SPEAKING")
        self.bridge.speak(text)
        time.sleep(1.0)  # Let TTS start before listening again

    # ------------------------------------------------------------------
    # Internal: Raw Speech Transcription
    # ------------------------------------------------------------------

    def _listen_raw(self) -> str:
        """
        Listens to microphone and returns full raw transcribed text.
        Returns empty string on timeout / error.
        """
        if not self.voice_available or self._recognizer is None:
            time.sleep(5.0)   # Long sleep — no point spinning
            return ""

        try:
            with sr.Microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.3)
                print("[VoiceController] 🎤 Listening...")
                audio = self._recognizer.listen(source, timeout=5, phrase_time_limit=6)

            text = self._recognizer.recognize_google(audio, language="en-IN").lower().strip()
            print(f"[VoiceController] 🗣️  You said: '{text}'")
            return text

        except sr.UnknownValueError:
            return ""
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            err = str(e)
            # Only print once per unique error type to avoid spam
            if not hasattr(self, "_last_error") or self._last_error != err:
                self._last_error = err
                print(f"[VoiceController] Mic error: {err}")
            time.sleep(2.0)
            return ""

    # ------------------------------------------------------------------
    # Intent Recognition & Dispatch
    # ------------------------------------------------------------------

    def _dispatch_command(self, text: str) -> bool:
        """
        Matches raw transcribed text to voice commands and executes the action.
        Returns True if a command was matched and handled.
        """
        # --- Wake / Greeting ---
        if any(w in text for w in [
            "hey assistant", "hello assistant", "hi assistant",
            "hey vision", "hello vision", "ok assistant"
        ]):
            self._speak_and_notify("Hello! How can I help you?")
            return True

        # --- Describe Scene ---
        if any(w in text for w in [
            "describe", "what do you see", "look around",
            "what is around", "describe the scene", "scene description"
        ]):
            if self.assistant_controller:
                self._set_status("PROCESSING")
                reply = self.assistant_controller.handle_describe_scene()
                self._speak_and_notify(reply or "I could not analyze the scene.")
            else:
                self._speak_and_notify("Scene analysis is not ready yet.")
            return True

        # --- Read Text (OCR) ---
        if any(w in text for w in [
            "read", "read text", "what does it say",
            "read everything", "extract text", "what is written"
        ]):
            if self.assistant_controller:
                self._set_status("PROCESSING")
                reply = self.assistant_controller.handle_read_text()
                self._speak_and_notify(reply or "No readable text detected.")
            else:
                self._speak_and_notify("Text reader is not ready yet.")
            return True

        # --- Find Object ---
        if "find" in text or "where is" in text or "locate" in text:
            target = text
            for word in ["find", "where is", "locate", "the", "my", "a"]:
                target = target.replace(word, "")
            target = target.strip()
            if self.assistant_controller and target:
                self._set_status("PROCESSING")
                reply = self.assistant_controller.handle_find_object(target)
                self._speak_and_notify(reply or f"Could not find {target}.")
            else:
                self._speak_and_notify("Please say what object you want me to find.")
            return True

        # --- Query Nearby Objects ---
        if any(w in text for w in [
            "nearby", "what objects", "who is in front",
            "what is in front", "objects around",
            "what's around", "what is around me"
        ]):
            if self.assistant_controller:
                self._set_status("PROCESSING")
                reply = self.assistant_controller.handle_query_nearby()
                self._speak_and_notify(reply or "No objects detected nearby.")
            else:
                self._speak_and_notify("Object scanner is not ready.")
            return True

        # --- Repeat ---
        if "repeat" in text or "say again" in text or "say that again" in text:
            self._speak_and_notify(self.last_spoken_response)
            return True

        # --- Stop Speaking ---
        if any(w in text for w in ["stop speaking", "be quiet", "stop talking"]):
            self.bridge.stop_speaking()
            return True

        # --- Exit ---
        if any(w in text for w in [
            "exit assistant", "close assistant",
            "stop assistant", "goodbye", "bye assistant"
        ]):
            self._speak_and_notify("Closing VisionAssist AI. Goodbye!")
            self.running = False
            return True

        return False

    # ------------------------------------------------------------------
    # Main Voice Loop
    # ------------------------------------------------------------------

    def _voice_loop(self):
        """Continuous background voice listener loop."""
        if not self.voice_available:
            self._set_status("UNAVAILABLE")
            print("[VoiceController] ⚠️ Voice loop exiting — PyAudio not available.")
            # Notify user once via TTS (uses pyttsx3/edge-tts, not pyaudio)
            try:
                self.bridge.speak(
                    "Microphone not available. Voice commands disabled. "
                    "Please run the application using Python 3.11."
                )
            except Exception:
                pass
            return

        while self.running:
            self._set_status("LISTENING")

            raw_text = self._listen_raw()

            if not self.running:
                break

            if not raw_text:
                continue

            # Notify UI with transcribed text
            if self.on_recognized_text_callback:
                try:
                    self.on_recognized_text_callback(raw_text)
                except Exception:
                    pass

            self._set_status("PROCESSING")
            matched = self._dispatch_command(raw_text)

            if not matched:
                self._speak_and_notify(
                    "I did not understand that. You can say: "
                    "describe the scene, read text, find an object, or nearby objects."
                )

            self._set_status("READY")
            time.sleep(0.2)
