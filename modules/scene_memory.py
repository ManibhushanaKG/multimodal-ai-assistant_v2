import time


class SceneMemory:

    def __init__(self):

        self.scene = ""

        self.text = ""

        self.objects = set()

        self.last_scene_time = 0

        self.last_text_time = 0

    # -------------------------
    # Objects
    # -------------------------

    def update_objects(self, labels):

        previous = self.objects

        current = set(labels)

        added = current - previous

        removed = previous - current

        self.objects = current

        return list(added), list(removed)

    # -------------------------
    # Scene
    # -------------------------

    def update_scene(self, scene):

        scene = scene.strip().lower()

        if scene == self.scene:
            return False

        self.scene = scene

        self.last_scene_time = time.time()

        return True

    # -------------------------
    # OCR
    # -------------------------

    def update_text(self, text):

        text = text.strip()

        if not text:
            return False

        if text == self.text:
            return False

        self.text = text

        self.last_text_time = time.time()

        return True