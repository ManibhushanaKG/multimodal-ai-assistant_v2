import asyncio
import threading
import queue
import tempfile
import os

import edge_tts
import pygame


class SpeechEngine:

    def __init__(self):

        pygame.mixer.init()

        self.queue = queue.Queue()

        self.running = True

        self.thread = threading.Thread(
            target=self.worker,
            daemon=True
        )

        self.thread.start()

    def speak(self, text):

        if not text:
            return

        self.queue.put(text)

    def worker(self):

        while self.running:

            text = self.queue.get()

            if text is None:
                break

            try:
                asyncio.run(self.play(text))
            except Exception as e:
                print("Speech Error:", e)

            self.queue.task_done()

        pygame.mixer.quit()

    async def play(self, text):

        print("🔊", text)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as fp:

            filename = fp.name

        try:

            communicate = edge_tts.Communicate(
                text=text,
                voice="en-IN-NeerjaNeural"
            )

            await communicate.save(filename)

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.05)

            pygame.mixer.music.unload()

        finally:

            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except:
                    pass

    def stop(self):

        self.running = False

        self.queue.put(None)

        self.thread.join()


speech_engine = SpeechEngine()


def speak(text):
    speech_engine.speak(text)


def stop_speech():
    speech_engine.stop()