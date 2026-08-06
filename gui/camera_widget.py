import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Optional
from gui.styles import CARD_BG, CARD_BORDER, TEXT_MUTED, CORNER_RADIUS_MEDIUM, FONT_TITLE_MEDIUM


class CameraWidget(ctk.CTkFrame):
    """
    High-performance CustomTkinter video stream widget for Developer Mode.
    Converts OpenCV BGR numpy arrays to PIL ImageTk images for live rendering.
    """

    def __init__(self, master, width: int = 640, height: int = 480, **kwargs):
        super().__init__(
            master,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=CORNER_RADIUS_MEDIUM,
            **kwargs
        )
        self.width = width
        self.height = height

        # Image Display Label
        self.display_label = ctk.CTkLabel(
            self,
            text="📷 Camera Feed Offline",
            font=FONT_TITLE_MEDIUM,
            text_color=TEXT_MUTED,
            fg_color="#000000",
            corner_radius=CORNER_RADIUS_MEDIUM
        )
        self.display_label.pack(fill="both", expand=True, padx=4, pady=4)

        self._photo_image = None

    def update_frame(self, frame_bgr):
        """Thread-safe update of camera video frame."""
        if frame_bgr is None:
            return

        try:
            # Convert OpenCV BGR -> RGB
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)

            # Get widget dimensions
            w = self.display_label.winfo_width()
            h = self.display_label.winfo_height()

            if w > 50 and h > 50:
                # Maintain aspect ratio
                pil_image.thumbnail((w, h), Image.Resampling.LANCZOS)

            # Create CTkImage for CustomTkinter
            ctk_img = ctk.CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=(pil_image.width, pil_image.height)
            )

            self.display_label.configure(image=ctk_img, text="")
            self.display_label._image = ctk_img
        except Exception as e:
            print(f"[CameraWidget] Frame update error: {e}")

    def show_offline(self, message: str = "📷 Camera Feed Offline"):
        """Displays offline placeholder state."""
        self.display_label.configure(image=None, text=message)
