import threading
import time
import sys

from modules.assistant import Assistant
from modules.camera_manager import CameraManager
from modules.speech import stop_speech, speak
from modules.voice_input import listen_command

# Global flag used by background voice listener
stop_requested = False


def voice_listener():
    """Runs in the background and listens only for stop commands."""
    global stop_requested

    while not stop_requested:
        command = listen_command()

        if command == "stop":
            print("🛑 Stop Assistant detected!")
            stop_requested = True
            break


def main():
    global stop_requested

    print("=" * 60)
    print("        MULTIMODAL AI ASSISTANT v2")
    print("=" * 60)

    print("\n🎤 Voice Activation Enabled")
    print("Say:")
    print(" • Hey Assistant")
    print(" • Hello Assistant")
    print(" • Start Assistant")
    print()

    # -------------------------
    # Wake Word Detection
    # -------------------------
    while True:
        command = listen_command()

        if command == "start":
            print("✅ Assistant Started")
            speak("Hello. I am ready to assist you.")
            break

        print("Wake word not detected. Try again.")

    camera = CameraManager()
    assistant = Assistant()

    # -------------------------
    # Background Stop Listener
    # -------------------------
    stop_requested = False

    listener_thread = threading.Thread(
        target=voice_listener,
        daemon=True
    )
    listener_thread.start()

    # -------------------------
    # Main Camera Loop
    # -------------------------
    try:
        while assistant.is_running():

            # Voice command requested stop
            if stop_requested:
                print("🛑 Closing VisionAssist AI...")

                speak("Closing VisionAssist AI. Goodbye!")

                # Give TTS a moment to start speaking
                time.sleep(0.5)

                assistant.stop()

                # Release resources immediately
                try:
                    camera.release()
                except:
                    pass

                try:
                    stop_speech()
                except:
                    pass

                print("Assistant Closed.")
                sys.exit(0)

            frame = camera.read()

            if frame is None:
                continue

            results = assistant.process_frame(frame)

            camera.show(results)

            # Press Q to quit
            if camera.should_quit():
                assistant.stop()
                break

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nStopping Assistant...")

    finally:
        stop_requested = True

        try:
            stop_speech()
        except:
            pass

        try:
            camera.release()
        except:
            pass

        print("Assistant Closed.")


if __name__ == "__main__":
    main()