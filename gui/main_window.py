import customtkinter as ctk
from typing import Optional, Callable
from gui.styles import (
    BG_DARK, CARD_BG, CARD_BORDER, PRIMARY_BLUE, TEXT_WHITE, TEXT_MUTED,
    FONT_TITLE_LARGE, FONT_TITLE_MEDIUM, FONT_BODY, FONT_BODY_BOLD,
    CORNER_RADIUS_MEDIUM, apply_global_theme
)
from gui.splash_screen import SplashScreen
from gui.mode_selection import ModeSelectionScreen
from gui.user_mode import UserModeScreen
from gui.developer_mode import DeveloperModeScreen


class MainWindow(ctk.CTk):
    """
    Main Master CustomTkinter Window for VisionAssist AI.
    Handles top-level screen transitions and view container management.
    """

    def __init__(self, **kwargs):
        apply_global_theme()
        super().__init__(**kwargs)

        self.title("VisionAssist AI - Multimodal Assistant for Visually Impaired")
        self.geometry("1280x800")
        self.minsize(1024, 720)
        self.configure(fg_color=BG_DARK)

        # Active View Container Frame
        self.view_container = ctk.CTkFrame(self, fg_color=BG_DARK)
        self.view_container.pack(fill="both", expand=True)

        self.current_screen: Optional[ctk.CTkFrame] = None

    def show_screen(self, screen_class, **kwargs) -> ctk.CTkFrame:
        """Destroys current view and mounts new screen instance."""
        if self.current_screen is not None:
            self.current_screen.destroy()

        self.current_screen = screen_class(self.view_container, **kwargs)
        self.current_screen.pack(fill="both", expand=True)
        return self.current_screen


class SettingsDialog(ctk.CTkToplevel):
    """
    Settings modal dialog for Developer Mode.
    Allows configuring Camera Index, Speech Speed, Confidence Threshold,
    and displaying System Info.
    """

    def __init__(self, master, current_cam_idx: int = 0, on_save_callback: Optional[Callable] = None):
        super().__init__(master)
        self.title("⚙ VisionAssist AI - Developer Settings")
        self.geometry("450x380")
        self.resizable(False, False)
        self.configure(fg_color=CARD_BG)
        self.grab_set()

        self.on_save_callback = on_save_callback

        # Title
        ctk.CTkLabel(
            self,
            text="⚙ System & Camera Settings",
            font=FONT_TITLE_LARGE,
            text_color=TEXT_WHITE
        ).pack(pady=(20, 16))

        # Camera Index Option
        cam_frame = ctk.CTkFrame(self, fg_color="transparent")
        cam_frame.pack(fill="x", padx=32, pady=8)

        ctk.CTkLabel(
            cam_frame, text="Camera Source Index:", font=FONT_BODY_BOLD, text_color=TEXT_WHITE
        ).pack(side="left")

        self.cam_opt = ctk.CTkOptionMenu(
            cam_frame,
            values=["0 (Default WebCam)", "1 (External Camera)", "2 (USB Camera)"],
            fg_color=PRIMARY_BLUE,
            width=180
        )
        self.cam_opt.set(f"{current_cam_idx} (Default WebCam)" if current_cam_idx == 0 else f"{current_cam_idx} (Camera)")
        self.cam_opt.pack(side="right")

        # YOLO Confidence Threshold
        conf_frame = ctk.CTkFrame(self, fg_color="transparent")
        conf_frame.pack(fill="x", padx=32, pady=12)

        ctk.CTkLabel(
            conf_frame, text="YOLO Detection Conf Threshold (0.65):", font=FONT_BODY, text_color=TEXT_MUTED
        ).pack(anchor="w")

        self.conf_slider = ctk.CTkSlider(conf_frame, from_=0.3, to=0.95, number_of_steps=13)
        self.conf_slider.set(0.65)
        self.conf_slider.pack(fill="x", pady=6)

        # Close / Save Button
        btn_save = ctk.CTkButton(
            self,
            text="Apply & Close",
            font=FONT_BODY_BOLD,
            fg_color=PRIMARY_BLUE,
            hover_color="#1D4ED8",
            height=40,
            command=self._on_save
        )
        btn_save.pack(side="bottom", fill="x", padx=32, pady=24)

    def _on_save(self):
        selected_str = self.cam_opt.get()
        idx = int(selected_str.split()[0])
        if self.on_save_callback:
            self.on_save_callback(idx)
        self.destroy()
