import time
import threading
from typing import Callable, Optional, List, Dict, Any
from backend_bridge import BackendBridge


class CameraController:
    """
    Manages non-blocking camera frame acquisition, YOLO object detection,
    and FPS measurement in a background worker thread.
    """

    def __init__(self, bridge: BackendBridge):
        self.bridge = bridge
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.camera_index = 0

        # Callbacks
        self.on_frame_callback: Optional[Callable] = None
        self.on_objects_callback: Optional[Callable] = None
        self.on_fps_callback: Optional[Callable] = None

        # State metrics
        self.current_fps = 0.0
        self.last_frame = None
        self.latest_objects: List[Dict[str, Any]] = []

    def start(self, camera_index: int = 0) -> bool:
        """Initialize camera and start capture thread."""
        if self.running:
            return True

        self.camera_index = camera_index
        success = self.bridge.initialize_camera(camera_index)
        if not success:
            return False

        self.running = True
        self.thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.thread.start()
        return True

    def stop(self):
        """Stop capture thread and release camera."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        self.thread = None
        self.bridge.release_camera()

    def _worker_loop(self):
        fps_frame_count = 0
        fps_start_time = time.time()

        while self.running:
            frame = self.bridge.read_frame()
            if frame is None:
                time.sleep(0.02)
                continue

            # Run YOLO Object Detection
            labels, results, objects, annotated_frame = self.bridge.process_detection(frame)

            self.last_frame = frame
            self.latest_objects = objects

            # Measure FPS
            fps_frame_count += 1
            now = time.time()
            elapsed = now - fps_start_time
            if elapsed >= 0.5:
                self.current_fps = fps_frame_count / elapsed
                fps_frame_count = 0
                fps_start_time = now

                if self.on_fps_callback:
                    self.on_fps_callback(self.current_fps)

            # Dispatch callbacks
            if self.on_frame_callback:
                self.on_frame_callback(annotated_frame)

            if self.on_objects_callback:
                self.on_objects_callback(objects)

            time.sleep(0.01)  # Limit CPU spinning (~30-60 FPS)
