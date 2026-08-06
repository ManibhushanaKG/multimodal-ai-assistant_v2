import os
from PIL import Image, ImageDraw, ImageFont

def generate_assets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_dir = os.path.join(base_dir, "logo")
    icons_dir = os.path.join(base_dir, "icons")
    os.makedirs(logo_dir, exist_ok=True)
    os.makedirs(icons_dir, exist_ok=True)

    # 1. Generate App Logo PNG (256x256)
    img = Image.new("RGBA", (256, 256), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    # Circle gradient background
    draw.ellipse([16, 16, 240, 240], fill=(37, 99, 235, 255), outline=(6, 182, 212, 255), width=4)
    # Eye shape
    draw.ellipse([48, 88, 208, 168], fill=None, outline=(255, 255, 255, 255), width=8)
    # Pupil
    draw.ellipse([100, 100, 156, 156], fill=(6, 182, 212, 255), outline=(255, 255, 255, 255), width=4)
    # Center highlight
    draw.ellipse([118, 110, 134, 126], fill=(255, 255, 255, 255))

    logo_path = os.path.join(logo_dir, "logo.png")
    img.save(logo_path)
    print(f"Generated logo at: {logo_path}")

if __name__ == "__main__":
    generate_assets()
