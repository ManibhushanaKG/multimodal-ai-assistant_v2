import tkinter as tk
import customtkinter as ctk
from typing import Callable, Optional
from gui.styles import (
    BG_DARK, CARD_BG, CARD_BORDER, PRIMARY_BLUE, TEXT_WHITE, TEXT_MUTED,
    ACCENT_CYAN, GREEN_SUCCESS, WARNING_AMBER, FONT_HERO, FONT_TITLE_LARGE,
    FONT_TITLE_MEDIUM, FONT_BODY_LARGE, FONT_CAPTION, CORNER_RADIUS_LARGE
)
from gui.animations import MicPulseAnimation, VoiceWaveformAnimation, TypingAnimation


class UserModeScreen(ctk.CTkFrame):
    """
    Ultra-accessible hands-free interface for blind users.
    Focuses entirely on voice interaction, large high-contrast text,
    animated microphone pulse, voice waveform, and live spoken responses.
    """

    def __init__(self, master, on_back_callback: Optional[Callable] = None, **kwargs):
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self.on_back_callback = on_back_callback

        # Top Bar (Title & Mode Switcher)
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=32, pady=(24, 0))

        self.brand_title = ctk.CTkLabel(
            self.top_bar,
            text="👁️ VisionAssist AI",
            font=FONT_TITLE_LARGE,
            text_color=TEXT_WHITE
        )
        self.brand_title.pack(side="left")

        if self.on_back_callback:
            self.back_btn = ctk.CTkButton(
                self.top_bar,
                text="← Change Mode",
                font=FONT_CAPTION,
                fg_color=CARD_BG,
                hover_color="#334155",
                width=110,
                height=32,
                corner_radius=8,
                command=self.on_back_callback
            )
            self.back_btn.pack(side="right")

        # Main Centered Container
        self.main_container = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=CORNER_RADIUS_LARGE,
            width=720,
            height=540
        )
        self.main_container.pack_propagate(False)
        self.main_container.place(relx=0.5, rely=0.52, anchor="center")

        # 1. Animated Microphone / Waveform Canvas Container
        self.anim_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.anim_frame.pack(pady=(32, 10))

        self.canvas = tk.Canvas(
            self.anim_frame,
            width=220,
            height=160,
            bg=CARD_BG,
            highlightthickness=0
        )
        self.canvas.pack()

        # Animation Drivers
        self.mic_anim = MicPulseAnimation(self.canvas, width=220, height=160)
        self.wave_anim = VoiceWaveformAnimation(self.canvas, width=220, height=160)

        # 2. Assistant Status Indicator
        self.status_pill = ctk.CTkLabel(
            self.main_container,
            text="● READY",
            font=FONT_TITLE_MEDIUM,
            text_color=TEXT_WHITE,
            fg_color=GREEN_SUCCESS,
            corner_radius=14,
            padx=16,
            pady=4
        )
        self.status_pill.pack(pady=(0, 16))

        # 3. Status Action Text ("Listening...", "Processing...", "Speaking...")
        self.state_action_label = ctk.CTkLabel(
            self.main_container,
            text="Listening for voice commands...",
            font=FONT_TITLE_MEDIUM,
            text_color=ACCENT_CYAN
        )
        self.state_action_label.pack(pady=(0, 20))

        # 4. Spoken Response Header & Text Box
        self.response_header = ctk.CTkLabel(
            self.main_container,
            text="LAST SPOKEN RESPONSE",
            font=FONT_CAPTION,
            text_color=TEXT_MUTED
        )
        self.response_header.pack(pady=(0, 6))

        self.response_box = ctk.CTkFrame(
            self.main_container,
            fg_color="#0F172A",
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=12,
            width=640,
            height=130
        )
        self.response_box.pack_propagate(False)
        self.response_box.pack(pady=(0, 24))

        self.response_label = ctk.CTkLabel(
            self.response_box,
            text='"Welcome to VisionAssist AI. I am ready to assist you."',
            font=FONT_BODY_LARGE,
            text_color=TEXT_WHITE,
            wraplength=600
        )
        self.response_label.pack(expand=True, padx=20, pady=12)

        # Typewriter Animation
        self.typewriter = TypingAnimation(self.response_label, speed_ms=25)

        # Draw default mic idle state
        self.mic_anim.draw_idle()

    # ------------------------------------------------------------------
    # State Update Handlers
    # ------------------------------------------------------------------

    def set_listening_state(self):
        """User Mode state: Listening for voice input."""
        try:
            self.status_pill.configure(text="● LISTENING", fg_color=WARNING_AMBER)
            self.state_action_label.configure(
                text="🎙️ Listening... Say 'Hey Assistant' or 'Describe the scene'"
            )
            self.wave_anim.stop()
            self.mic_anim.start()
        except Exception:
            pass

    def set_processing_state(self):
        """User Mode state: Processing AI logic."""
        try:
            self.status_pill.configure(text="● PROCESSING", fg_color="#8B5CF6")
            self.state_action_label.configure(text="⚡ Processing AI models...")
            self.mic_anim.stop()
            self.wave_anim.stop()
        except Exception:
            pass

    def set_speaking_state(self, text: str):
        """User Mode state: Assistant speaking response."""
        try:
            self.status_pill.configure(text="● SPEAKING", fg_color=PRIMARY_BLUE)
            self.state_action_label.configure(text="🔊 Speaking Response...")
            self.mic_anim.stop()
            self.wave_anim.start()
            self.typewriter.type_text(f'"{text}"')
        except Exception:
            pass

    def set_ready_state(self):
        """User Mode state: Assistant ready."""
        try:
            self.status_pill.configure(text="● READY", fg_color=GREEN_SUCCESS)
            self.state_action_label.configure(text="Ready — speak a command...")
            self.wave_anim.stop()
            self.mic_anim.stop()
            self.mic_anim.draw_idle()
        except Exception:
            pass
