import tkinter as tk
import customtkinter as ctk
from typing import Callable, Optional

from gui.styles import (
    BG_DARK,
    CARD_BG,
    CARD_BORDER,
    PRIMARY_BLUE,
    TEXT_WHITE,
    TEXT_MUTED,
    ACCENT_CYAN,
    GREEN_SUCCESS,
    WARNING_AMBER,
    FONT_TITLE_LARGE,
    FONT_TITLE_MEDIUM,
    FONT_BODY_LARGE,
    FONT_CAPTION,
    CORNER_RADIUS_LARGE,
)

from gui.animations import MicPulseAnimation, VoiceWaveformAnimation


class UserModeScreen(ctk.CTkFrame):
    """
    User mode GUI for VisionAssist AI.
    """

    def __init__(self, master, on_back_callback: Optional[Callable] = None, **kwargs):
        super().__init__(master, fg_color=BG_DARK, **kwargs)

        self.on_back_callback = on_back_callback

        # ================= TOP BAR =================

        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=32, pady=(24, 0))

        self.brand_title = ctk.CTkLabel(
            self.top_bar,
            text="👁️ VisionAssist AI",
            font=FONT_TITLE_LARGE,
            text_color=TEXT_WHITE,
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
                command=self.on_back_callback,
            )
            self.back_btn.pack(side="right")

        # ================= MAIN CARD =================

        self.main_container = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=CORNER_RADIUS_LARGE,
            width=720,
            height=560,
        )
        self.main_container.pack_propagate(False)
        self.main_container.place(relx=0.5, rely=0.52, anchor="center")

        # ================= MIC ANIMATION =================

        self.anim_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.anim_frame.pack(pady=(28, 10))

        self.canvas = tk.Canvas(
            self.anim_frame,
            width=220,
            height=160,
            bg=CARD_BG,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.mic_anim = MicPulseAnimation(self.canvas, width=220, height=160)
        self.wave_anim = VoiceWaveformAnimation(self.canvas, width=220, height=160)

        self.mic_anim.draw_idle()

        # ================= STATUS =================

        self.status_pill = ctk.CTkLabel(
            self.main_container,
            text="● READY",
            font=FONT_TITLE_MEDIUM,
            text_color=TEXT_WHITE,
            fg_color=GREEN_SUCCESS,
            corner_radius=14,
            padx=16,
            pady=4,
        )
        self.status_pill.pack(pady=(0, 16))

        self.state_action_label = ctk.CTkLabel(
            self.main_container,
            text="Ready — Speak 'Hey Assistant'",
            font=FONT_TITLE_MEDIUM,
            text_color=ACCENT_CYAN,
        )
        self.state_action_label.pack(pady=(0, 18))

        # ================= RESPONSE HEADER =================

        self.response_header = ctk.CTkLabel(
            self.main_container,
            text="LAST SPOKEN RESPONSE",
            font=FONT_CAPTION,
            text_color=TEXT_MUTED,
        )
        self.response_header.pack(pady=(0, 8))

        # ================= RESPONSE BOX =================

        self.response_box = ctk.CTkFrame(
            self.main_container,
            fg_color="#0B1535",
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=14,
            width=650,
            height=210,
        )
        self.response_box.pack_propagate(False)
        self.response_box.pack(pady=(0, 20))

        self.response_text = ctk.CTkTextbox(
            self.response_box,
            width=610,
            height=180,
            wrap="word",
            font=FONT_BODY_LARGE,
            text_color=TEXT_WHITE,
            fg_color="transparent",
            border_width=0,
        )
        self.response_text.pack(fill="both", expand=True, padx=16, pady=16)

        self.response_text.insert(
            "1.0",
            "Welcome to VisionAssist AI. I am ready to assist you.",
        )
        self.response_text.configure(state="disabled")

    # =====================================================
    # RESPONSE UPDATE
    # =====================================================

    def update_response(self, text: str):
        self.response_text.configure(state="normal")
        self.response_text.delete("1.0", "end")
        self.response_text.insert("1.0", text)
        self.response_text.see("end")
        self.response_text.configure(state="disabled")

    # =====================================================
    # STATUS STATES
    # =====================================================

    def set_listening_state(self):
        self.status_pill.configure(
            text="● LISTENING",
            fg_color=WARNING_AMBER,
        )

        self.state_action_label.configure(
            text="🎙️ Listening... Say 'Hey Assistant' or 'Stop Assistant'",
        )

        self.wave_anim.stop()
        self.mic_anim.start()

    def set_processing_state(self):
        self.status_pill.configure(
            text="● PROCESSING",
            fg_color="#8B5CF6",
        )

        self.state_action_label.configure(
            text="⚡ Processing AI models...",
        )

        self.mic_anim.stop()
        self.wave_anim.stop()

    def set_speaking_state(self, text: str):
        self.status_pill.configure(
            text="● SPEAKING",
            fg_color=PRIMARY_BLUE,
        )

        self.state_action_label.configure(
            text="🔊 Speaking Response...",
        )

        self.mic_anim.stop()
        self.wave_anim.start()

        self.update_response(f'"{text}"')

    def set_ready_state(self):
        self.status_pill.configure(
            text="● READY",
            fg_color=GREEN_SUCCESS,
        )

        self.state_action_label.configure(
            text="Ready — Speak 'Hey Assistant'",
        )

        self.wave_anim.stop()
        self.mic_anim.stop()
        self.mic_anim.draw_idle()