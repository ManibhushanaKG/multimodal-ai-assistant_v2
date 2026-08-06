import math
import time
import tkinter as tk
from typing import Callable, Optional
from gui.styles import PRIMARY_BLUE, PRIMARY_LIGHT, ACCENT_CYAN, GREEN_SUCCESS, CARD_BG


class MicPulseAnimation:
    """
    Animated Canvas widget rendering expanding concentric pulsing rings
    around a centered microphone icon for User Mode listening state.
    """

    def __init__(self, canvas: tk.Canvas, width: int = 160, height: int = 160):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.is_animating = False
        self.phase = 0.0
        self._after_id = None

    def start(self):
        if not self.is_animating:
            self.is_animating = True
            self._animate()

    def stop(self):
        self.is_animating = False
        if self._after_id:
            try:
                self.canvas.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        self.draw_idle()

    def draw_idle(self):
        """Draw static idle microphone state."""
        self.canvas.delete("pulse")
        self.canvas.delete("mic")
        r = 45
        # Inner static circle
        self.canvas.create_oval(
            self.center_x - r, self.center_y - r,
            self.center_x + r, self.center_y + r,
            fill=PRIMARY_BLUE, outline=PRIMARY_LIGHT, width=2, tags="mic"
        )
        # Mic symbol text icon
        self.canvas.create_text(
            self.center_x, self.center_y,
            text="🎤", font=("Segoe UI Emoji", 32), fill="#FFFFFF", tags="mic"
        )

    def _animate(self):
        if not self.is_animating:
            return

        self.canvas.delete("pulse")
        self.canvas.delete("mic")
        self.phase = (self.phase + 0.08) % (2 * math.pi)

        # Draw 3 expanding pulsing rings
        for i in range(3):
            wave = math.sin(self.phase - i * 0.7)
            ring_radius = 45 + max(0, wave) * 35
            alpha_val = max(0, 1.0 - (ring_radius - 45) / 35.0)

            # Color calculation for glow
            color = PRIMARY_LIGHT if i % 2 == 0 else ACCENT_CYAN
            self.canvas.create_oval(
                self.center_x - ring_radius, self.center_y - ring_radius,
                self.center_x + ring_radius, self.center_y + ring_radius,
                outline=color, width=int(3 * alpha_val + 1), tags="pulse"
            )

        # Center Mic Core
        r = 45
        self.canvas.create_oval(
            self.center_x - r, self.center_y - r,
            self.center_x + r, self.center_y + r,
            fill=PRIMARY_BLUE, outline=ACCENT_CYAN, width=3, tags="mic"
        )
        self.canvas.create_text(
            self.center_x, self.center_y,
            text="🎤", font=("Segoe UI Emoji", 32), fill="#FFFFFF", tags="mic"
        )

        self._after_id = self.canvas.after(30, self._animate)


class VoiceWaveformAnimation:
    """
    Animated multi-bar audio waveform visualizer for Assistant Speaking state.
    """

    def __init__(self, canvas: tk.Canvas, width: int = 240, height: int = 60, bar_count: int = 16):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.bar_count = bar_count
        self.is_animating = False
        self.phase = 0.0
        self._after_id = None

    def start(self):
        if not self.is_animating:
            self.is_animating = True
            self._animate()

    def stop(self):
        self.is_animating = False
        if self._after_id:
            try:
                self.canvas.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        self.canvas.delete("bar")

    def _animate(self):
        if not self.is_animating:
            return

        self.canvas.delete("bar")
        self.phase += 0.15

        spacing = self.width / (self.bar_count + 1)
        center_y = self.height / 2

        for i in range(self.bar_count):
            x = (i + 1) * spacing
            # Dynamic height using combined sine waves
            val1 = math.sin(self.phase + i * 0.4)
            val2 = math.cos(self.phase * 0.7 + i * 0.3)
            bar_h = max(6, (abs(val1 * val2) * (self.height - 12)))

            y1 = center_y - bar_h / 2
            y2 = center_y + bar_h / 2

            # Smooth gradient color transition
            color = GREEN_SUCCESS if i % 2 == 0 else ACCENT_CYAN
            self.canvas.create_line(
                x, y1, x, y2, fill=color, width=4, capstyle=tk.ROUND, tags="bar"
            )

        self._after_id = self.canvas.after(35, self._animate)


class TypingAnimation:
    """
    Simulates live streaming typewriter text effect for Assistant Spoken Response.
    """

    def __init__(self, label_widget, speed_ms: int = 25):
        self.label_widget = label_widget
        self.speed_ms = speed_ms
        self._after_id = None
        self.full_text = ""
        self.current_idx = 0

    def type_text(self, text: str, completion_callback: Optional[Callable] = None):
        self.cancel()
        self.full_text = text
        self.current_idx = 0
        self._type_step(completion_callback)

    def cancel(self):
        if self._after_id:
            try:
                self.label_widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _type_step(self, callback: Optional[Callable]):
        if self.current_idx <= len(self.full_text):
            chunk = self.full_text[:self.current_idx]
            try:
                self.label_widget.configure(text=chunk)
            except Exception:
                return
            self.current_idx += 1
            self._after_id = self.label_widget.after(
                self.speed_ms, lambda: self._type_step(callback)
            )
        else:
            if callback:
                callback()
