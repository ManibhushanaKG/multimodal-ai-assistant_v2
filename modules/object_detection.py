import cv2
from ultralytics import YOLO

print("Loading YOLO11...")

model = YOLO("yolo11n.pt")
model.to("cuda")

print("YOLO Loaded!")

CONFIDENCE_THRESHOLD = 0.65


def detect_objects(frame):

    # Resize for faster inference
    frame = cv2.resize(frame, (640, 480))

    results = model(
        frame,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False,
        device=0
    )

    objects = []

    for result in results:

        for box in result.boxes:

            confidence = float(box.conf[0])

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            cls = int(box.cls[0])
            label = model.names[cls]

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            center_x = (x1 + x2) / 2

            width = x2 - x1
            height = y2 - y1
            area = width * height

            frame_width = frame.shape[1]

            if center_x < frame_width * 0.15:
                position = "far left"
            elif center_x < frame_width * 0.35:
                position = "left"
            elif center_x < frame_width * 0.45:
                position = "slightly left"
            elif center_x < frame_width * 0.55:
                position = "center"
            elif center_x < frame_width * 0.65:
                position = "slightly right"
            elif center_x < frame_width * 0.85:
                position = "right"
            else:
                position = "far right"

            if area > 90000:
                distance = "very close"
            elif area > 40000:
                distance = "close"
            elif area > 15000:
                distance = "medium distance"
            else:
                distance = "far"

            objects.append(
                {
                    "label": label,
                    "confidence": confidence,
                    "position": position,
                    "distance": distance,
                    "area": area,
                    "bbox": (x1, y1, x2, y2),
                }
            )

    labels = list(set(obj["label"] for obj in objects))

    return labels, results, objects