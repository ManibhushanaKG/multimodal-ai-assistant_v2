import customtkinter as ctk
from typing import Callable
from gui.styles import (
    BG_DARK, CARD_BG, CARD_BG_HOVER, CARD_BORDER, PRIMARY_BLUE, PRIMARY_HOVER,
    TEXT_WHITE, TEXT_MUTED, ACCENT_CYAN, FONT_HERO, FONT_TITLE_LARGE, FONT_TITLE_MEDIUM,
    FONT_SUBTITLE, FONT_BODY, FONT_CAPTION, CORNER_RADIUS_LARGE, GREEN_SUCCESS
)


class ModeSelectionScreen(ctk.CTkFrame):
    """
    Mode Selection screen featuring two large centered modern interactive cards:
    User Mode (Voice Controlled) vs Developer Mode (AI Dashboard).
    """

    def __init__(
        self,
        master,
        on_select_user_mode: Callable,
        on_select_dev_mode: Callable,
        **kwargs
    ):
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self.on_select_user_mode = on_select_user_mode
        self.on_select_dev_mode = on_select_dev_mode

        # Header Title Area
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(40, 20))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="VisionAssist AI",
            font=FONT_HERO,
            text_color=TEXT_WHITE
        )
        self.title_label.pack()

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Select an execution mode to launch the application",
            font=FONT_SUBTITLE,
            text_color=TEXT_MUTED
        )
        self.subtitle_label.pack(pady=(4, 0))

        # Cards Container Frame
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(expand=True, padx=40, pady=20)

        # -------------------------------------------------------------
        # Card 1: USER MODE
        # -------------------------------------------------------------
        self.user_card = ctk.CTkFrame(
            self.cards_frame,
            fg_color=CARD_BG,
            border_color=PRIMARY_BLUE,
            border_width=2,
            corner_radius=CORNER_RADIUS_LARGE,
            width=380,
            height=340
        )
        self.user_card.pack_propagate(False)
        self.user_card.pack(side="left", padx=24, pady=10)

        # Icon
        ctk.CTkLabel(
            self.user_card, text="👤", font=("Segoe UI Emoji", 48)
        ).pack(pady=(28, 8))

        # Card Title
        ctk.CTkLabel(
            self.user_card,
            text="USER MODE",
            font=FONT_TITLE_LARGE,
            text_color=TEXT_WHITE
        ).pack(pady=2)

        # Badge
        ctk.CTkLabel(
            self.user_card,
            text="VOICE CONTROLLED",
            font=FONT_CAPTION,
            text_color=TEXT_WHITE,
            fg_color=GREEN_SUCCESS,
            corner_radius=10,
            padx=10,
            pady=2
        ).pack(pady=(0, 12))

        # Description
        ctk.CTkLabel(
            self.user_card,
            text="Hands-free voice input and output interface designed for visually impaired users. Zero mouse or keyboard required.",
            font=FONT_BODY,
            text_color=TEXT_MUTED,
            wraplength=320
        ).pack(padx=24, pady=(0, 16))

        # Launch Button
        self.user_btn = ctk.CTkButton(
            self.user_card,
            text="Launch User Mode",
            font=FONT_TITLE_MEDIUM,
            fg_color=PRIMARY_BLUE,
            hover_color=PRIMARY_HOVER,
            corner_radius=10,
            height=44,
            command=self.on_select_user_mode
        )
        self.user_btn.pack(side="bottom", fill="x", padx=24, pady=20)

        # -------------------------------------------------------------
        # Card 2: DEVELOPER MODE
        # -------------------------------------------------------------
        self.dev_card = ctk.CTkFrame(
            self.cards_frame,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=2,
            corner_radius=CORNER_RADIUS_LARGE,
            width=380,
            height=340
        )
        self.dev_card.pack_propagate(False)
        self.dev_card.pack(side="left", padx=24, pady=10)

        # Icon
        ctk.CTkLabel(
            self.dev_card, text="💻", font=("Segoe UI Emoji", 48)
        ).pack(pady=(28, 8))

        # Card Title
        ctk.CTkLabel(
            self.dev_card,
            text="DEVELOPER MODE",
            font=FONT_TITLE_LARGE,
            text_color=TEXT_WHITE
        ).pack(pady=2)

        # Badge
        ctk.CTkLabel(
            self.dev_card,
            text="DEVELOPER DASHBOARD",
            font=FONT_CAPTION,
            text_color=TEXT_WHITE,
            fg_color=PRIMARY_BLUE,
            corner_radius=10,
            padx=10,
            pady=2
        ).pack(pady=(0, 12))

        # Description
        ctk.CTkLabel(
            self.dev_card,
            text="Complete AI visual pipeline for faculty demonstration. Includes live camera feed, YOLO detections, OCR, Florence-2 captions & debug metrics.",
            font=FONT_BODY,
            text_color=TEXT_MUTED,
            wraplength=320
        ).pack(padx=24, pady=(0, 16))

        # Launch Button
        self.dev_btn = ctk.CTkButton(
            self.dev_card,
            text="Launch Developer Mode",
            font=FONT_TITLE_MEDIUM,
            fg_color=CARD_BG_HOVER,
            hover_color=PRIMARY_BLUE,
            corner_radius=10,
            height=44,
            command=self.on_select_dev_mode
        )
        self.dev_btn.pack(side="bottom", fill="x", padx=24, pady=20)
