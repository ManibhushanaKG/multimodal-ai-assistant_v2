import customtkinter as ctk
from typing import Callable, Optional, Dict, Any, List
from gui.styles import (
    BG_DARK, CARD_BG, CARD_BORDER, PRIMARY_BLUE, PRIMARY_HOVER, TEXT_WHITE,
    TEXT_MUTED, GREEN_SUCCESS, WARNING_AMBER, DANGER_RED, ACCENT_CYAN,
    FONT_TITLE_MEDIUM, FONT_TITLE_LARGE, FONT_BODY_BOLD, FONT_CAPTION,
    CORNER_RADIUS_MEDIUM
)
from gui.camera_widget import CameraWidget
from gui.cards import InfoCard
from gui.status_panel import StatusPanel


class DeveloperModeScreen(ctk.CTkFrame):
    """
    Developer Mode Dashboard providing real-time visualization of the AI pipeline.
    Includes header metric pills, live camera feed with YOLO bounding boxes,
    4 real-time Info Cards, bottom control toolbar, and system status panel.
    """

    def __init__(
        self,
        master,
        on_start_callback: Callable,
        on_stop_callback: Callable,
        on_capture_callback: Callable,
        on_voice_toggle_callback: Callable,
        on_settings_callback: Callable,
        on_back_callback: Callable,
        **kwargs
    ):
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self.on_start_callback = on_start_callback
        self.on_stop_callback = on_stop_callback
        self.on_capture_callback = on_capture_callback
        self.on_voice_toggle_callback = on_voice_toggle_callback
        self.on_settings_callback = on_settings_callback
        self.on_back_callback = on_back_callback

        # -------------------------------------------------------------
        # TOP HEADER: Branding & System Status Pills
        # -------------------------------------------------------------
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=CORNER_RADIUS_MEDIUM
        )
        self.header_frame.pack(fill="x", padx=16, pady=(16, 8))

        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="💻 VisionAssist AI - Developer Dashboard",
            font=FONT_TITLE_LARGE,
            text_color=TEXT_WHITE
        )
        self.title_label.pack(side="left", padx=16, pady=12)

        # Status Badges Container (Right Side)
        self.metrics_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.metrics_container.pack(side="right", padx=16, pady=8)

        # GPU Status Badge
        self.gpu_badge = self._create_metric_badge(
            self.metrics_container, "GPU", "CPU", DANGER_RED
        )
        self.gpu_badge.pack(side="left", padx=4)

        # Camera Status Badge
        self.camera_badge = self._create_metric_badge(
            self.metrics_container, "CAM", "Offline", DANGER_RED
        )
        self.camera_badge.pack(side="left", padx=4)

        # Voice Status Badge
        self.voice_badge = self._create_metric_badge(
            self.metrics_container, "VOICE", "Idle", WARNING_AMBER
        )
        self.voice_badge.pack(side="left", padx=4)

        # FPS Counter Badge
        self.fps_badge = self._create_metric_badge(
            self.metrics_container, "FPS", "0.0", PRIMARY_BLUE
        )
        self.fps_badge.pack(side="left", padx=4)

        # Mode Back Button
        self.back_btn = ctk.CTkButton(
            self.metrics_container,
            text="← Mode Selection",
            font=FONT_CAPTION,
            fg_color="#334155",
            hover_color=PRIMARY_BLUE,
            width=110,
            height=32,
            corner_radius=8,
            command=self.on_back_callback
        )
        self.back_btn.pack(side="left", padx=(12, 0))

        # -------------------------------------------------------------
        # MAIN CONTENT AREA: Camera (Left) + 4 Info Cards Grid (Right)
        # -------------------------------------------------------------
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=16, pady=8)

        # Left Column: Large Live Camera View
        self.camera_column = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.camera_column.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.camera_widget = CameraWidget(self.camera_column, width=640, height=480)
        self.camera_widget.pack(fill="both", expand=True)

        # Right Column: 2x2 Grid of Information Cards
        self.cards_column = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.cards_column.pack(side="right", fill="both", expand=True, padx=(8, 0))

        # Configure 2x2 Grid weight
        self.cards_column.columnconfigure((0, 1), weight=1)
        self.cards_column.rowconfigure((0, 1), weight=1)

        # Card 1: Objects Card (Top Left)
        self.card_objects = InfoCard(
            self.cards_column,
            title="Objects (YOLO11)",
            icon="🎯",
            badge_text="0 Objects",
            header_color=PRIMARY_BLUE
        )
        self.card_objects.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        # Card 2: OCR Card (Top Right)
        self.card_ocr = InfoCard(
            self.cards_column,
            title="Extracted Text (EasyOCR)",
            icon="📄",
            badge_text="Idle",
            header_color=ACCENT_CYAN
        )
        self.card_ocr.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)

        # Card 3: Scene Description Card (Bottom Left)
        self.card_scene = InfoCard(
            self.cards_column,
            title="Scene Description (Florence-2)",
            icon="🖼️",
            badge_text="Idle",
            header_color="#8B5CF6"
        )
        self.card_scene.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)

        # Card 4: Assistant Response Card (Bottom Right)
        self.card_response = InfoCard(
            self.cards_column,
            title="Assistant Response",
            icon="💬",
            badge_text="Ready",
            header_color=GREEN_SUCCESS
        )
        self.card_response.grid(row=1, column=1, sticky="nsew", padx=4, pady=4)

        # -------------------------------------------------------------
        # BOTTOM BAR: Control Toolbar & Status Panel
        # -------------------------------------------------------------
        self.bottom_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_bar.pack(fill="x", padx=16, pady=(8, 16))

        # Status Panel (Left)
        self.status_panel = StatusPanel(self.bottom_bar)
        self.status_panel.pack(side="left", fill="y")

        # Toolbar Control Buttons (Right)
        self.toolbar_frame = ctk.CTkFrame(
            self.bottom_bar,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=CORNER_RADIUS_MEDIUM
        )
        self.toolbar_frame.pack(side="right", padx=(12, 0))

        # ▶ Start Button
        self.btn_start = ctk.CTkButton(
            self.toolbar_frame,
            text="▶ Start",
            font=FONT_BODY_BOLD,
            fg_color=GREEN_SUCCESS,
            hover_color="#16A34A",
            width=90,
            height=36,
            command=self.on_start_callback
        )
        self.btn_start.pack(side="left", padx=6, pady=6)

        # ■ Stop Button
        self.btn_stop = ctk.CTkButton(
            self.toolbar_frame,
            text="■ Stop",
            font=FONT_BODY_BOLD,
            fg_color=DANGER_RED,
            hover_color="#DC2626",
            width=90,
            height=36,
            command=self.on_stop_callback
        )
        self.btn_stop.pack(side="left", padx=6, pady=6)

        # 📸 Capture Button
        self.btn_capture = ctk.CTkButton(
            self.toolbar_frame,
            text="📸 Capture",
            font=FONT_BODY_BOLD,
            fg_color=PRIMARY_BLUE,
            hover_color=PRIMARY_HOVER,
            width=100,
            height=36,
            command=self.on_capture_callback
        )
        self.btn_capture.pack(side="left", padx=6, pady=6)

        # 🎤 Voice Toggle Button
        self.btn_voice = ctk.CTkButton(
            self.toolbar_frame,
            text="🎤 Voice",
            font=FONT_BODY_BOLD,
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            width=90,
            height=36,
            command=self.on_voice_toggle_callback
        )
        self.btn_voice.pack(side="left", padx=6, pady=6)

        # ⚙ Settings Button
        self.btn_settings = ctk.CTkButton(
            self.toolbar_frame,
            text="⚙ Settings",
            font=FONT_BODY_BOLD,
            fg_color="#334155",
            hover_color="#475569",
            width=100,
            height=36,
            command=self.on_settings_callback
        )
        self.btn_settings.pack(side="left", padx=6, pady=6)

    def _create_metric_badge(self, parent, label: str, value: str, bg_color: str):
        badge_frame = ctk.CTkFrame(
            parent,
            fg_color="#0F172A",
            border_color=CARD_BORDER,
            border_width=1,
            corner_radius=8
        )
        lbl = ctk.CTkLabel(
            badge_frame,
            text=f"{label}: ",
            font=FONT_CAPTION,
            text_color=TEXT_MUTED
        )
        lbl.pack(side="left", padx=(6, 2))

        val_lbl = ctk.CTkLabel(
            badge_frame,
            text=value,
            font=FONT_CAPTION,
            text_color=TEXT_WHITE,
            fg_color=bg_color,
            corner_radius=6,
            padx=6,
            pady=1
        )
        val_lbl.pack(side="left", padx=(0, 4))
        badge_frame.value_label = val_lbl
        return badge_frame

    # ------------------------------------------------------------------
    # Update API Methods
    # ------------------------------------------------------------------

    def update_gpu_status(self, device_name: str, is_gpu: bool):
        color = GREEN_SUCCESS if is_gpu else WARNING_AMBER
        self.gpu_badge.value_label.configure(text=device_name, fg_color=color)

    def update_camera_status(self, is_active: bool):
        text = "Active" if is_active else "Offline"
        color = GREEN_SUCCESS if is_active else DANGER_RED
        self.camera_badge.value_label.configure(text=text, fg_color=color)

    def update_voice_status(self, status: str):
        colors = {
            "Listening": WARNING_AMBER,
            "Speaking": PRIMARY_BLUE,
            "Idle": "#334155",
            "Off": DANGER_RED
        }
        self.voice_badge.value_label.configure(
            text=status, fg_color=colors.get(status, "#334155")
        )

    def update_fps(self, fps: float):
        self.fps_badge.value_label.configure(text=f"{fps:.1f}")

    def update_objects_card(self, objects: List[Dict[str, Any]]):
        if not objects:
            self.card_objects.update_content("No objects detected in frame.", badge_text="0 Objects")
            return

        lines = []
        for obj in objects:
            conf_pct = int(obj.get("confidence", 0) * 100)
            lines.append(
                f"• {obj.get('label', 'Unknown').capitalize()} ({conf_pct}%)\n"
                f"  Position: {obj.get('position', 'center')}, Dist: {obj.get('distance', 'medium')}\n"
            )

        text_content = "\n".join(lines)
        self.card_objects.update_content(text_content, badge_text=f"{len(objects)} Objects")

    def update_ocr_card(self, text: str):
        badge = "Extracted" if text else "No Text"
        self.card_ocr.update_content(text if text else "No text detected in scene.", badge_text=badge)

    def update_scene_card(self, caption: str):
        badge = "Updated" if caption else "Idle"
        self.card_scene.update_content(caption if caption else "Analyzing scene...", badge_text=badge)

    def update_response_card(self, response: str):
        self.card_response.update_content(response if response else "Ready.", badge_text="Active")
