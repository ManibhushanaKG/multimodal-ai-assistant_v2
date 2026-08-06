import os
import time
import tempfile
import cv2
import torch
import traceback
from typing import Dict, Any, List, Tuple, Optional, Callable

# Import existing untouched backend modules
from modules.camera_manager import CameraManager
from modules.assistant import Assistant
from modules.object_detection import detect_objects
from modules.caption import generate_caption
from modules.ocr import extract_text
from modules.response_generator import build_response, simplify_scene
from modules.speech import speak, stop_speech
from modules.state_manager import StateManager
from modules.scene_memory import SceneMemory
from modules.priority import sort_objects


class BackendBridge:
    """
    Bridge layer between GUI controllers and existing backend modules.
    Never modifies backend logic; provides clean, thread-safe access.
    """

    def __init__(self):
        self.camera_manager: Optional[CameraManager] = None
        self.assistant: Optional[Assistant] = None
        self.is_active = False

    def is_gpu_available(self) -> bool:
        """Check if PyTorch detects CUDA support."""
        try:
            return torch.cuda.is_available()
        except Exception:
            return False

    def get_gpu_name(self) -> str:
        """Returns GPU device name if available, otherwise 'CPU'."""
        if self.is_gpu_available():
            return torch.cuda.get_device_name(0)
        return "CPU Execution"

    # ------------------------------------------------------------------
    # Camera Operations
    # ------------------------------------------------------------------

    def initialize_camera(self, camera_index: int = 0) -> bool:
        """Initialize camera manager."""
        try:
            if self.camera_manager:
                self.release_camera()

            # Temporarily bypass OpenCV highgui namedWindow to prevent headless OpenCV errors
            orig_named_window = getattr(cv2, "namedWindow", None)
            try:
                cv2.namedWindow = lambda *args, **kwargs: None
                self.camera_manager = CameraManager(camera_index=camera_index)
            finally:
                if orig_named_window:
                    cv2.namedWindow = orig_named_window

            return True
        except Exception as e:
            print(f"[BackendBridge] Camera Init Error: {e}")
            self.camera_manager = None
            return False

    def read_frame(self):
        """Read a frame from camera."""
        if self.camera_manager:
            return self.camera_manager.read()
        return None

    def release_camera(self):
        """Release camera hardware."""
        if self.camera_manager:
            try:
                orig_destroy = getattr(cv2, "destroyAllWindows", None)
                try:
                    cv2.destroyAllWindows = lambda *args, **kwargs: None
                    self.camera_manager.release()
                finally:
                    if orig_destroy:
                        cv2.destroyAllWindows = orig_destroy
            except Exception:
                pass
            self.camera_manager = None

    # ------------------------------------------------------------------
    # AI Pipeline Operations
    # ------------------------------------------------------------------

    def initialize_assistant(self) -> Assistant:
        """Create a new Assistant instance."""
        self.assistant = Assistant()
        self.is_active = True
        return self.assistant

    def stop_assistant(self):
        """Stop the assistant instance."""
        if self.assistant:
            self.assistant.stop()
            self.is_active = False

    def process_detection(self, frame) -> Tuple[List[str], Any, List[Dict[str, Any]], Any]:
        """
        Runs YOLO object detection on a frame.
        Returns: (labels, results, objects, annotated_frame)
        """
        try:
            labels, results, objects = detect_objects(frame)
            annotated_frame = frame.copy()
            if results and len(results) > 0:
                annotated_frame = results[0].plot()
            return labels, results, objects, annotated_frame
        except Exception as e:
            print(f"[BackendBridge] YOLO Detection Error: {e}")
            return [], None, [], frame

    def run_scene_caption(self, frame) -> str:
        """Runs Florence-2 scene captioning on a frame."""
        temp_path = None
        try:
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            cv2.imwrite(temp_path, frame)
            caption = generate_caption(temp_path)
            return caption if caption else ""
        except Exception as e:
            print(f"[BackendBridge] Florence-2 Error: {e}")
            return ""
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

    def run_ocr(self, frame) -> str:
        """Runs EasyOCR text extraction on a frame."""
        temp_path = None
        try:
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            cv2.imwrite(temp_path, frame)
            extracted_text = extract_text(temp_path)
            return extracted_text if extracted_text else ""
        except Exception as e:
            print(f"[BackendBridge] EasyOCR Error: {e}")
            return ""
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

    def build_assistant_response(
        self,
        added_objects: List[Dict[str, Any]],
        removed_objects: List[Dict[str, Any]],
        caption: str = "",
        ocr_text: str = ""
    ) -> str:
        """Generates speech text using backend response_generator."""
        return build_response(added_objects, removed_objects, caption, ocr_text)

    # ------------------------------------------------------------------
    # Speech TTS Operations
    # ------------------------------------------------------------------

    def speak(self, text: str):
        """Queue text for Edge-TTS playback."""
        if text:
            speak(text)

    def stop_speaking(self):
        """Stop current speech output."""
        try:
            stop_speech()
        except Exception as e:
            print(f"[BackendBridge] Speech Stop Error: {e}")
