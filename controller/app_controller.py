import threading
from typing import Optional
from backend_bridge import BackendBridge
from controller.camera_controller import CameraController
from controller.voice_controller import VoiceController
from controller.assistant_controller import AssistantController

from gui.main_window import MainWindow, SettingsDialog
from gui.splash_screen import SplashScreen
from gui.mode_selection import ModeSelectionScreen
from gui.user_mode import UserModeScreen
from gui.developer_mode import DeveloperModeScreen


class AppController:
    """
    Master Application Controller for MVC Architecture.
    Coordinates views, controllers, backend bridge, and hardware streams.
    All cross-thread GUI updates go through window.after(0, ...) here.
    """

    def __init__(self, main_window: MainWindow):
        self.window = main_window
        self.bridge = BackendBridge()

        # Sub-controllers
        self.camera_controller = CameraController(self.bridge)
        self.assistant_controller = AssistantController(self.bridge, self.camera_controller)
        self.voice_controller = VoiceController(self.bridge, self.assistant_controller)

        # Active Mode Tracking
        self.current_mode = "SPLASH"
        self.current_cam_index = 0

    def start(self):
        """Launch application flow: Splash -> Mode Selection."""
        self._show_splash_screen()

    # ------------------------------------------------------------------
    # Screen Transitions
    # ------------------------------------------------------------------

    def _show_splash_screen(self):
        self.current_mode = "SPLASH"
        splash = self.window.show_screen(
            SplashScreen,
            on_complete_callback=self._show_mode_selection
        )
        splash.start_loading()

    def _show_mode_selection(self):
        self.camera_controller.stop()
        self.voice_controller.stop_listening()

        self.current_mode = "SELECTION"
        self.window.show_screen(
            ModeSelectionScreen,
            on_select_user_mode=self.launch_user_mode,
            on_select_dev_mode=self.launch_developer_mode
        )

    # ------------------------------------------------------------------
    # USER MODE
    # ------------------------------------------------------------------

    def launch_user_mode(self):
        """Initializes and displays User Mode (Hands-free voice UI)."""
        self.current_mode = "USER"
        user_screen: UserModeScreen = self.window.show_screen(
            UserModeScreen,
            on_back_callback=self._show_mode_selection
        )

        # Start Camera silently in background (for AI processing even in user mode)
        self.camera_controller.start(self.current_cam_index)

        # --- Wire Voice Controller Callbacks ---
        def on_status_change(status_key: str):
            """Called from background thread → safely dispatch to Tk main thread."""
            status = status_key.upper()
            try:
                if status == "LISTENING":
                    self.window.after(0, user_screen.set_listening_state)
                elif status == "PROCESSING":
                    self.window.after(0, user_screen.set_processing_state)
                elif status == "READY":
                    self.window.after(0, user_screen.set_ready_state)
            except Exception:
                pass

        def on_response(text: str):
            """Called from background thread → safely update UI on main thread."""
            try:
                self.window.after(0, lambda t=text: user_screen.set_speaking_state(t))
            except Exception:
                pass

        self.voice_controller.on_status_change_callback = on_status_change
        self.voice_controller.on_response_callback = on_response

        # Welcome announcement first, then start voice loop
        def _welcome_then_listen():
            welcome_msg = "Welcome to VisionAssist AI. I am ready to assist you. Say hey assistant to begin."
            self.bridge.speak(welcome_msg)
            try:
                self.window.after(0, lambda: user_screen.set_speaking_state(welcome_msg))
            except Exception:
                pass
            # Small delay so welcome finishes before listening starts
            import time
            time.sleep(2.5)
            try:
                self.window.after(0, user_screen.set_listening_state)
            except Exception:
                pass
            self.voice_controller.start_listening()

        threading.Thread(target=_welcome_then_listen, daemon=True).start()

    # ------------------------------------------------------------------
    # DEVELOPER MODE
    # ------------------------------------------------------------------

    def launch_developer_mode(self):
        """Initializes and displays Developer Mode (AI Dashboard UI)."""
        self.current_mode = "DEVELOPER"

        dev_screen: DeveloperModeScreen = self.window.show_screen(
            DeveloperModeScreen,
            on_start_callback=self._dev_start_pipeline,
            on_stop_callback=self._dev_stop_pipeline,
            on_capture_callback=self._dev_trigger_capture,
            on_voice_toggle_callback=self._dev_toggle_voice,
            on_settings_callback=self._dev_open_settings,
            on_back_callback=self._show_mode_selection
        )

        # GPU Status
        gpu_name = self.bridge.get_gpu_name()
        is_gpu = self.bridge.is_gpu_available()
        dev_screen.update_gpu_status(gpu_name, is_gpu)

        # --- Wire Camera Callbacks ---
        def on_frame(frame):
            try:
                self.window.after(0, lambda f=frame: dev_screen.camera_widget.update_frame(f))
            except Exception:
                pass

        def on_objects(objects):
            try:
                self.window.after(0, lambda o=objects: dev_screen.update_objects_card(o))
            except Exception:
                pass

        def on_fps(fps):
            try:
                self.window.after(0, lambda f=fps: dev_screen.update_fps(f))
            except Exception:
                pass

        self.camera_controller.on_frame_callback = on_frame
        self.camera_controller.on_objects_callback = on_objects
        self.camera_controller.on_fps_callback = on_fps

        # --- Wire Assistant Callbacks ---
        def on_ocr(text):
            try:
                self.window.after(0, lambda t=text: dev_screen.update_ocr_card(t))
            except Exception:
                pass

        def on_scene(caption):
            try:
                self.window.after(0, lambda c=caption: dev_screen.update_scene_card(c))
            except Exception:
                pass

        def on_response(resp):
            try:
                self.window.after(0, lambda r=resp: dev_screen.update_response_card(r))
            except Exception:
                pass

        self.assistant_controller.on_ocr_update_callback = on_ocr
        self.assistant_controller.on_scene_update_callback = on_scene
        self.assistant_controller.on_response_update_callback = on_response

        # --- Wire Voice Callbacks ---
        def on_voice_status(status_key: str):
            status = status_key.capitalize()
            try:
                self.window.after(0, lambda s=status: dev_screen.update_voice_status(s))
                self.window.after(0, lambda k=status_key: dev_screen.status_panel.set_status(k))
            except Exception:
                pass

        def on_voice_response(text: str):
            try:
                self.window.after(0, lambda t=text: dev_screen.update_response_card(t))
            except Exception:
                pass

        self.voice_controller.on_status_change_callback = on_voice_status
        self.voice_controller.on_response_callback = on_voice_response

        # Auto-start pipeline
        self._dev_start_pipeline()

    # ------------------------------------------------------------------
    # Developer Mode Toolbar Actions
    # ------------------------------------------------------------------

    def _dev_start_pipeline(self):
        cam_ok = self.camera_controller.start(self.current_cam_index)
        if self.window.current_screen and hasattr(self.window.current_screen, 'update_camera_status'):
            self.window.after(0, lambda: self.window.current_screen.update_camera_status(cam_ok))
        if not self.voice_controller.running:
            self.voice_controller.start_listening()

    def _dev_stop_pipeline(self):
        self.camera_controller.stop()
        self.voice_controller.stop_listening()
        if self.window.current_screen and hasattr(self.window.current_screen, 'update_camera_status'):
            self.window.after(0, lambda: self.window.current_screen.update_camera_status(False))
        if self.window.current_screen and hasattr(self.window.current_screen, 'update_voice_status'):
            self.window.after(0, lambda: self.window.current_screen.update_voice_status("Off"))

    def _dev_trigger_capture(self):
        """Manual trigger: run Florence-2 + EasyOCR on current frame."""
        def worker():
            if self.window.current_screen and hasattr(self.window.current_screen, 'status_panel'):
                self.window.after(0, lambda: self.window.current_screen.status_panel.set_status(
                    "PROCESSING", "Analyzing Scene & OCR..."))

            caption_res = self.assistant_controller.handle_describe_scene()
            ocr_res = self.assistant_controller.handle_read_text()

            parts = [p for p in [caption_res, ocr_res] if p]
            spoken = " ".join(parts)
            if spoken:
                self.bridge.speak(spoken)

            if self.window.current_screen and hasattr(self.window.current_screen, 'status_panel'):
                self.window.after(0, lambda: self.window.current_screen.status_panel.set_status(
                    "READY", "Scene Capture Completed"))

        threading.Thread(target=worker, daemon=True).start()

    def _dev_toggle_voice(self):
        if self.voice_controller.running:
            self.voice_controller.stop_listening()
            if self.window.current_screen and hasattr(self.window.current_screen, 'update_voice_status'):
                self.window.after(0, lambda: self.window.current_screen.update_voice_status("Off"))
        else:
            self.voice_controller.start_listening()
            if self.window.current_screen and hasattr(self.window.current_screen, 'update_voice_status'):
                self.window.after(0, lambda: self.window.current_screen.update_voice_status("Listening"))

    def _dev_open_settings(self):
        def on_save(new_cam_idx: int):
            if new_cam_idx != self.current_cam_index:
                self.current_cam_index = new_cam_idx
                self._dev_stop_pipeline()
                self._dev_start_pipeline()

        SettingsDialog(self.window, current_cam_idx=self.current_cam_index, on_save_callback=on_save)

    # ------------------------------------------------------------------
    # Application Shutdown
    # ------------------------------------------------------------------

    def shutdown(self):
        """Cleanup all streams and threads on application exit."""
        self.camera_controller.stop()
        self.voice_controller.stop_listening()
        try:
            self.bridge.stop_speaking()
        except Exception:
            pass
