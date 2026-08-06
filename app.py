import time

from modules.assistant import Assistant
from modules.camera_manager import CameraManager
from modules.speech import stop_speech, speak
from modules.voice_input import listen_command


VOICE_CHECK_INTERVAL = 5  # seconds


def main():

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
    # Wait for wake word
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

    last_voice_check = time.time()

    try:

        while assistant.is_running():

            # -------------------------
            # Camera (runs continuously)
            # -------------------------

            frame = camera.read()

            if frame is None:
                continue

            results = assistant.process_frame(frame)

            camera.show(results)

            # -------------------------
            # Check stop command every 5 seconds
            # -------------------------

            now = time.time()

            if now - last_voice_check >= VOICE_CHECK_INTERVAL:

                command = listen_command()

                last_voice_check = now

                if command == "stop":

                    speak("Closing assistant.")

                    assistant.stop()

                    break

            if camera.should_quit():

                assistant.stop()

    except KeyboardInterrupt:

        print("\nStopping Assistant...")

    finally:

        stop_speech()

        camera.release()

        print("Assistant Closed.")


if __name__ == "__main__":
    main()