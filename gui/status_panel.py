import customtkinter as ctk
from gui.styles import (
    CARD_BG, CARD_BORDER, GREEN_SUCCESS, WARNING_AMBER, DANGER_RED,
    PROCESSING_PURPLE, PRIMARY_LIGHT, TEXT_WHITE, TEXT_MUTED, FONT_BODY_BOLD,
    CORNER_RADIUS_MEDIUM, CORNER_RADIUS_SMALL
)


class StatusPanel(ctk.CTkFrame):
    """
    Status indicator widget displaying assistant system state
    (Ready, Listening, Processing, Speaking, Error) with color glow pill.
    """

    STATUS_CONFIGS = {
        "READY": {"color": GREEN_SUCCESS, "icon": "🟢", "text": "Ready"},
        "LISTENING": {"color": WARNING_AMBER, "icon": "🎙️", "text": "Listening..."},
        "PROCESSING": {"color": PROCESSING_PURPLE, "icon": "⚡", "text": "Processing AI..."},
        "SPEAKING": {"color": PRIMARY_LIGHT, "icon": "🔊", "text": "Speaking Response"},
        "ERROR": {"color": DANGER_RED, "icon": "⚠️", "text": "System Error"}
    }

    def __init__(self, master, initial_status: str = "READY", **kwargs):
        super().__init__(
            master,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=CORNER_RADIUS_MEDIUM,
            **kwargs
        )

        # Status Container Layout
        self.pill_frame = ctk.CTkFrame(
            self,
            fg_color=GREEN_SUCCESS,
            corner_radius=CORNER_RADIUS_SMALL
        )
        self.pill_frame.pack(side="left", padx=12, pady=8)

        self.status_label = ctk.CTkLabel(
            self.pill_frame,
            text="🟢 Ready",
            font=FONT_BODY_BOLD,
            text_color=TEXT_WHITE,
            padx=12,
            pady=4
        )
        self.status_label.pack()

        # Detailed state message
        self.detail_label = ctk.CTkLabel(
            self,
            text="Assistant active and monitoring environment",
            font=FONT_BODY_BOLD,
            text_color=TEXT_MUTED,
            anchor="w"
        )
        self.detail_label.pack(side="left", padx=(8, 12), fill="x", expand=True)

        self.set_status(initial_status)

    def set_status(self, status_key: str, custom_detail: str = ""):
        """Update system status display."""
        key = status_key.upper()
        config = self.STATUS_CONFIGS.get(key, self.STATUS_CONFIGS["READY"])

        self.pill_frame.configure(fg_color=config["color"])
        self.status_label.configure(text=f"{config['icon']} {config['text']}")

        if custom_detail:
            self.detail_label.configure(text=custom_detail)
        else:
            default_details = {
                "READY": "Assistant ready for voice input",
                "LISTENING": "Listening for commands...",
                "PROCESSING": "Analyzing scene & generating speech...",
                "SPEAKING": "Synthesizing voice output...",
                "ERROR": "An error occurred in AI module"
            }
            self.detail_label.configure(text=default_details.get(key, "Active"))
