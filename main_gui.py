import sys
import os

# Ensure workspace directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from controller.app_controller import AppController


def main():
    """VisionAssist AI Desktop GUI Application Main Entry Point."""
    print("=" * 60)
    print("       👁️ VisionAssist AI Desktop GUI Application")
    print("       Multimodal AI Assistant for Visually Impaired")
    print("=" * 60)

    # Initialize Master Tkinter Window
    window = MainWindow()

    # Initialize Controller Layer (MVC Architecture)
    app_controller = AppController(window)

    # Clean Graceful Shutdown Handler
    def on_closing():
        print("\n[VisionAssist AI] Shutting down application gracefully...")
        app_controller.shutdown()
        window.destroy()
        sys.exit(0)

    window.protocol("WM_DELETE_WINDOW", on_closing)

    # Launch Application Flow (Splash -> Mode Selection)
    app_controller.start()

    # Start Tkinter Event Loop
    window.mainloop()


if __name__ == "__main__":
    main()
