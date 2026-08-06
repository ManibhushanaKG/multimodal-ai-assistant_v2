import cv2


class CameraManager:

    def __init__(self, camera_index=0):

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception("Unable to open webcam.")

        self.window_name = "Multimodal AI Assistant"

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def read(self):

        ret, frame = self.cap.read()

        if not ret:
            return None

        return frame

    def show(self, results):

        if results is None:
            return

        frame = results[0].plot()

        cv2.imshow(self.window_name, frame)

    def should_quit(self):

        key = cv2.waitKey(1) & 0xFF

        return key == ord("q")

    def release(self):

        self.cap.release()

        cv2.destroyAllWindows()