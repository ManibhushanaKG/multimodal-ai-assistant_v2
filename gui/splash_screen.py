import customtkinter as ctk
from typing import Callable
from gui.styles import (
    BG_DARK, CARD_BG, PRIMARY_BLUE, PRIMARY_LIGHT, ACCENT_CYAN, TEXT_WHITE,
    TEXT_MUTED, FONT_HERO, FONT_TITLE_LARGE, FONT_SUBTITLE, FONT_CAPTION,
    CORNER_RADIUS_LARGE
)


class SplashScreen(ctk.CTkFrame):
    """
    Commercial 2-second Splash Screen with branding logo, subtitle,
    technology stack pill badges, and animated progress bar.
    """

    def __init__(self, master, on_complete_callback: Callable, **kwargs):
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self.on_complete_callback = on_complete_callback
        self.progress_val = 0.0

        # Centered Container Frame
        self.container = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            corner_radius=CORNER_RADIUS_LARGE,
            border_color="#334155",
            border_width=1,
            width=540,
            height=420
        )
        self.container.pack_propagate(False)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Eye Logo Badge
        self.logo_label = ctk.CTkLabel(
            self.container,
            text="👁️",
            font=("Segoe UI Emoji", 56)
        )
        self.logo_label.pack(pady=(36, 4))

        # Title
        self.title_label = ctk.CTkLabel(
            self.container,
            text="VisionAssist AI",
            font=FONT_HERO,
            text_color=TEXT_WHITE
        )
        self.title_label.pack(pady=2)

        # Subtitle
        self.sub_label = ctk.CTkLabel(
            self.container,
            text="Multimodal AI Assistant for Visually Impaired",
            font=FONT_SUBTITLE,
            text_color=ACCENT_CYAN
        )
        self.sub_label.pack(pady=(0, 16))

        # Powered By Label
        self.powered_label = ctk.CTkLabel(
            self.container,
            text="POWERED BY",
            font=FONT_CAPTION,
            text_color=TEXT_MUTED
        )
        self.powered_label.pack(pady=(0, 6))

        # Tech Stack Badges Frame
        self.tech_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.tech_frame.pack(pady=(0, 24))

        techs = [
            ("YOLO11", "#2563EB"),
            ("Florence-2", "#8B5CF6"),
            ("EasyOCR", "#06B6D4"),
            ("Edge-TTS", "#22C55E")
        ]

        for tech, color in techs:
            pill = ctk.CTkLabel(
                self.tech_frame,
                text=tech,
                font=FONT_CAPTION,
                text_color=TEXT_WHITE,
                fg_color=color,
                corner_radius=12,
                padx=10,
                pady=3
            )
            pill.pack(side="left", padx=4)

        # Animated Loading Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            self.container,
            width=380,
            height=8,
            corner_radius=4,
            progress_color=PRIMARY_BLUE,
            fg_color="#0F172A"
        )
        self.progress_bar.pack(pady=(0, 8))
        self.progress_bar.set(0.0)

        # Status text below progress bar
        self.status_label = ctk.CTkLabel(
            self.container,
            text="Initializing AI Engine & Neural Weights...",
            font=FONT_CAPTION,
            text_color=TEXT_MUTED
        )
        self.status_label.pack()

    def start_loading(self):
        """Start 2-second splash screen loading animation sequence."""
        self.progress_val = 0.0
        self._animate_progress()

    def _animate_progress(self):
        if self.progress_val < 1.0:
            self.progress_val += 0.05
            self.progress_bar.set(self.progress_val)
            # 20 steps * 100ms = 2000ms (2 seconds)
            self.after(100, self._animate_progress)
        else:
            self.progress_bar.set(1.0)
            self.status_label.configure(text="Ready!")
            self.after(300, self.on_complete_callback)
