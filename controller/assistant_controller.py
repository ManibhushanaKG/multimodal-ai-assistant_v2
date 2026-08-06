import threading
from typing import Callable, Optional, Dict, Any, List
from backend_bridge import BackendBridge
from modules.response_generator import simplify_scene, object_sentence


class AssistantController:
    """
    Orchestrates high-level AI assistant tasks:
    linking object detections, Florence-2 captions, and EasyOCR text extractions.
    """

    def __init__(self, bridge: BackendBridge, camera_controller=None):
        self.bridge = bridge
        self.camera_controller = camera_controller

        # Callbacks for Developer Mode Cards updates
        self.on_ocr_update_callback: Optional[Callable[[str], None]] = None
        self.on_scene_update_callback: Optional[Callable[[str], None]] = None
        self.on_response_update_callback: Optional[Callable[[str], None]] = None

    def handle_describe_scene(self) -> str:
        """Triggers Florence-2 scene captioning on current frame."""
        frame = self.camera_controller.last_frame if self.camera_controller else None
        if frame is None:
            return "Camera feed is not active."

        caption = self.bridge.run_scene_caption(frame)
        if not caption:
            return "I could not analyze the scene clearly."

        if self.on_scene_update_callback:
            self.on_scene_update_callback(caption)

        # Simplify scene e.g. "bedroom", "office", "kitchen"
        scene_type = simplify_scene(caption)
        if scene_type:
            response = f"You appear to be in a {scene_type}. {caption}"
        else:
            response = caption

        if self.on_response_update_callback:
            self.on_response_update_callback(response)

        return response

    def handle_read_text(self) -> str:
        """Triggers EasyOCR text extraction on current frame."""
        frame = self.camera_controller.last_frame if self.camera_controller else None
        if frame is None:
            return "Camera feed is not active."

        extracted_text = self.bridge.run_ocr(frame)
        if not extracted_text:
            response = "No readable text was detected."
        else:
            response = f"Text says: {extracted_text}"

        if self.on_ocr_update_callback:
            self.on_ocr_update_callback(extracted_text)

        if self.on_response_update_callback:
            self.on_response_update_callback(response)

        return response

    def handle_find_object(self, target_label: str) -> str:
        """Searches currently detected YOLO objects for target label."""
        if not self.camera_controller or not self.camera_controller.latest_objects:
            return f"I cannot see any {target_label} right now."

        target_clean = target_label.lower().strip()
        matches = [
            obj for obj in self.camera_controller.latest_objects
            if target_clean in obj["label"].lower()
        ]

        if not matches:
            return f"I do not see a {target_label} in front of you."

        best = matches[0]
        desc = object_sentence(best)
        response = f"Found {best['label']}. It is {best['distance']} on your {best['position']}."

        if self.on_response_update_callback:
            self.on_response_update_callback(response)

        return response

    def handle_query_nearby(self) -> str:
        """Summarizes objects currently detected nearby."""
        if not self.camera_controller or not self.camera_controller.latest_objects:
            return "There are no objects detected nearby."

        objs = self.camera_controller.latest_objects
        descriptions = [object_sentence(o) for o in objs[:3]]
        summary = " ".join(descriptions)
        response = f"Nearby objects: {summary}"

        if self.on_response_update_callback:
            self.on_response_update_callback(response)

        return response
