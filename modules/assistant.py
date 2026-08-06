import time
import cv2
import tempfile
import os
import traceback

from modules.object_detection import detect_objects
from modules.caption import generate_caption
from modules.ocr import extract_text
from modules.response_generator import build_response, simplify_scene
from modules.speech import speak
from modules.state_manager import StateManager
from modules.scene_memory import SceneMemory

SCENE_UPDATE_INTERVAL = 15


class Assistant:

    def __init__(self):

        self.running = True
        self.state = StateManager()
        self.memory = SceneMemory()
        self.last_scene_update = 0

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    def process_frame(self, frame):

        labels, results, objects = detect_objects(frame)

        added_labels, removed_labels = self.state.compare(labels)

        added_objects = [
            obj for obj in objects
            if obj["label"] in added_labels
        ]

        removed_objects = [
            {"label": label}
            for label in removed_labels
        ]

        scene_to_speak = ""
        text_to_speak = ""

        current_time = time.time()

        if current_time - self.last_scene_update >= SCENE_UPDATE_INTERVAL:

            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)

            cv2.imwrite(temp_path, frame)

            print("\n========== Updating Scene ==========")

            # ---------- Florence ----------
            try:

                caption = generate_caption(temp_path)

                print("\nFlorence Caption:")
                print(caption)

                scene = simplify_scene(caption)

                if scene and self.memory.update_scene(scene):
                    scene_to_speak = scene

            except Exception:

                print("\nFlorence Error")
                traceback.print_exc()

            # ---------- OCR ----------
            try:

                text = extract_text(temp_path)

                print("\nOCR Output:")
                print(text)

                if self.memory.update_text(text):
                    text_to_speak = text

            except Exception:

                print("\nOCR Error")
                traceback.print_exc()

            if os.path.exists(temp_path):
                os.remove(temp_path)

            self.last_scene_update = current_time

        response = build_response(
            added_objects,
            removed_objects,
            scene_to_speak,
            text_to_speak
        )

        if response and self.state.should_speak():

            print("\nAssistant:")
            print(response)

            speak(response)

            self.state.update()

        return results