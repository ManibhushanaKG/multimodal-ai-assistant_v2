import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.non_speaking_duration = 0.5

microphone = sr.Microphone()
initialized = False


def initialize_microphone():
    global initialized

    if initialized:
        return

    with microphone as source:
        print("🎤 Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

    initialized = True
    print("✅ Microphone Ready")


def listen_command():

    initialize_microphone()

    try:
        with microphone as source:

            print("🎤 Listening...")

            audio = recognizer.listen(
                source,
                timeout=1,
                phrase_time_limit=3
            )

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        ).lower().strip()

        print("You said:", text)

        # START COMMANDS
        start_words = [
            "hey assistant",
            "hello assistant",
            "hi assistant",
            "start assistant",
            "open assistant",
            "wake up assistant"
        ]

        # STOP COMMANDS
        stop_words = [
            "stop assistant",
            "close assistant",
            "exit assistant",
            "stop",
            "close",
            "exit"
        ]

        if any(word in text for word in start_words):
            return "start"

        if any(word in text for word in stop_words):
            return "stop"

        return ""

    except sr.UnknownValueError:
        return ""

    except sr.WaitTimeoutError:
        return ""

    except Exception as e:
        print("Voice Error:", e)
        return ""