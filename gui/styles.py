import customtkinter as ctk

# Centralized Theme & Styling System for VisionAssist AI

# Color Palette (Slate Dark Theme with Vibrant Accents)
BG_DARK = "#0F172A"          # Main Window Background (Slate 900)
CARD_BG = "#1E293B"          # Info Card & Panel Background (Slate 800)
CARD_BG_HOVER = "#334155"    # Card Hover / Secondary (Slate 700)
CARD_BORDER = "#334155"      # Subtle Card Borders

# Accent Colors
PRIMARY_BLUE = "#2563EB"     # Primary Blue Action Color (Blue 600)
PRIMARY_HOVER = "#1D4ED8"    # Hover State (Blue 700)
PRIMARY_LIGHT = "#3B82F6"    # Bright Accent Blue (Blue 500)
ACCENT_CYAN = "#06B6D4"      # Cyan Accent (Cyan 500)

# Status Colors
GREEN_SUCCESS = "#22C55E"    # Ready / Active Status (Emerald 500)
WARNING_AMBER = "#F59E0B"    # Listening / Warning (Amber 500)
DANGER_RED = "#EF4444"       # Error / Stop (Red 500)
PROCESSING_PURPLE = "#8B5CF6"# AI Processing (Purple 500)

# Text Colors
TEXT_WHITE = "#FFFFFF"       # High contrast primary text
TEXT_LIGHT = "#F8FAFC"       # Near white text
TEXT_MUTED = "#94A3B8"       # Secondary caption text (Slate 400)
TEXT_DIM = "#64748B"         # Subdued text (Slate 500)

# Typography Constants
FONT_FAMILY = "Segoe UI"     # Clean, modern Windows UI font

FONT_HERO = (FONT_FAMILY, 32, "bold")
FONT_TITLE_LARGE = (FONT_FAMILY, 24, "bold")
FONT_TITLE_MEDIUM = (FONT_FAMILY, 18, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 14, "normal")
FONT_BODY_LARGE = (FONT_FAMILY, 16, "normal")
FONT_BODY_BOLD = (FONT_FAMILY, 16, "bold")
FONT_BODY = (FONT_FAMILY, 13, "normal")
FONT_CAPTION = (FONT_FAMILY, 11, "normal")

FONT_MONO = ("Consolas", 12, "normal")

# Geometry & Borders
CORNER_RADIUS_LARGE = 16
CORNER_RADIUS_MEDIUM = 12
CORNER_RADIUS_SMALL = 8


def apply_global_theme():
    """Configures default CustomTkinter appearance mode."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
