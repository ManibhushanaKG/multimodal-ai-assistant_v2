import queue
import threading


class SpeechQueue:

    def __init__(self):

        self.queue = queue.Queue()

        self.worker = None

        self.running = True

    # --------------------------------
    # Set speaker function
    # --------------------------------

    def start(self, speaker_function):

        if self.worker is not None:
            return

        self.worker = threading.Thread(
            target=self._worker,
            args=(speaker_function,),
            daemon=True
        )

        self.worker.start()

    # --------------------------------
    # Worker Thread
    # --------------------------------

    def _worker(self, speaker):

        while self.running:

            text = self.queue.get()

            if text is None:
                break

            try:
                speaker(text)

            except Exception as e:
                print("Speech Error:", e)

            self.queue.task_done()

    # --------------------------------
    # Add speech
    # --------------------------------

    def speak(self, text):

        if not text:
            return

        self.queue.put(text)

    # --------------------------------
    # Emergency Interrupt
    # --------------------------------

    def clear(self):

        while not self.queue.empty():

            try:
                self.queue.get_nowait()

                self.queue.task_done()

            except queue.Empty:
                break

    # --------------------------------
    # Stop Queue
    # --------------------------------

    def stop(self):

        self.running = False

        self.queue.put(None)

        if self.worker:

            self.worker.join()