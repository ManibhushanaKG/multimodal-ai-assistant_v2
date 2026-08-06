import cv2
import easyocr
import torch

# Initialize EasyOCR once
reader = easyocr.Reader(
    ['en'],
    gpu=torch.cuda.is_available()
)


def extract_text(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return ""

    # Enlarge image for better OCR
    image = cv2.resize(
        image,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve contrast
    gray = cv2.equalizeHist(gray)

    # Slight denoise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # OCR
    results = reader.readtext(
        gray,
        detail=0,          # Returns only text strings
        paragraph=True
    )

    print("\n========== OCR RAW ==========")
    print(results)
    print("=============================\n")

    if not results:
        return ""

    # Remove duplicates while preserving order
    seen = set()
    text = []

    for line in results:

        line = line.strip()

        if line and line not in seen:
            seen.add(line)
            text.append(line)

    final_text = " ".join(text)

    print("OCR Output:", final_text)

    return final_text