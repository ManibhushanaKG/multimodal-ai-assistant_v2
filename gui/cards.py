import customtkinter as ctk
from typing import Optional
from gui.styles import (
    CARD_BG, CARD_BORDER, PRIMARY_BLUE, TEXT_WHITE, TEXT_MUTED,
    FONT_TITLE_MEDIUM, FONT_BODY, FONT_CAPTION, CORNER_RADIUS_MEDIUM,
    ACCENT_CYAN, GREEN_SUCCESS
)


class InfoCard(ctk.CTkFrame):
    """
    Modern reusable info card container for Developer Mode AI pipeline visualization.
    Features header icon, title, count/status badge, and main content panel.
    All updates are thread-safe via _safe_update.
    """

    def __init__(
        self,
        master,
        title: str,
        icon: str = "ℹ️",
        badge_text: str = "",
        header_color: str = PRIMARY_BLUE,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=CORNER_RADIUS_MEDIUM,
            **kwargs
        )

        self.title_str = title
        self.header_color = header_color

        # Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=12, pady=(10, 6))

        # Icon + Title Label
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=f"{icon}  {title}",
            font=FONT_TITLE_MEDIUM,
            text_color=TEXT_WHITE,
            anchor="w"
        )
        self.title_label.pack(side="left")

        # Badge Pill
        self.badge_label = ctk.CTkLabel(
            self.header_frame,
            text=badge_text if badge_text else "Ready",
            font=FONT_CAPTION,
            text_color=TEXT_WHITE,
            fg_color=header_color,
            corner_radius=10,
            padx=8,
            pady=2
        )
        self.badge_label.pack(side="right")

        # Divider Line
        self.divider = ctk.CTkFrame(self, height=1, fg_color=CARD_BORDER)
        self.divider.pack(fill="x", padx=12, pady=(0, 8))

        # Scrollable / Text Content
        self.content_textbox = ctk.CTkTextbox(
            self,
            fg_color="transparent",
            text_color=TEXT_WHITE,
            font=FONT_BODY,
            wrap="word",
            activate_scrollbars=True
        )
        self.content_textbox.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        self.content_textbox.insert("1.0", "Waiting for data...")
        self.content_textbox.configure(state="disabled")

    def _safe_update(self, text: str, badge_text: Optional[str]):
        """Must be called on the main Tk thread."""
        try:
            self.content_textbox.configure(state="normal")
            self.content_textbox.delete("1.0", "end")
            self.content_textbox.insert("1.0", text if text else "No data detected.")
            self.content_textbox.configure(state="disabled")
            if badge_text is not None:
                self.badge_label.configure(text=badge_text)
        except Exception as e:
            print(f"[InfoCard] Update error: {e}")

    def update_content(self, text: str, badge_text: Optional[str] = None):
        """Thread-safe content update — schedules on Tk main loop."""
        try:
            self.after(0, lambda t=text, b=badge_text: self._safe_update(t, b))
        except Exception:
            pass

    def set_badge_color(self, color: str):
        """Update badge pill background color."""
        try:
            self.after(0, lambda: self.badge_label.configure(fg_color=color))
        except Exception:
            pass
