import time


class StateManager:

    def __init__(self):

        # label -> object information
        self.objects = {}

        self.last_spoken = 0

        self.cooldown = 3

        # Seconds before removing object
        self.persistence = 2

        # Object must be detected this many consecutive frames
        self.confirm_frames = 3

    def should_speak(self):

        return (time.time() - self.last_spoken) >= self.cooldown

    def update(self):

        self.last_spoken = time.time()

    def compare(self, detected_labels):

        now = time.time()

        detected = set(detected_labels)

        added = []

        removed = []

        # --------------------------
        # Update currently detected objects
        # --------------------------

        for label in detected:

            if label not in self.objects:

                self.objects[label] = {
                    "count": 1,
                    "spoken": False,
                    "last_seen": now
                }

            else:

                self.objects[label]["count"] += 1
                self.objects[label]["last_seen"] = now

            if (
                self.objects[label]["count"] >= self.confirm_frames
                and not self.objects[label]["spoken"]
            ):

                added.append(label)
                self.objects[label]["spoken"] = True

        # --------------------------
        # Remove disappeared objects
        # --------------------------

        for label in list(self.objects.keys()):

            if label in detected:
                continue

            if now - self.objects[label]["last_seen"] > self.persistence:

                if self.objects[label]["spoken"]:
                    removed.append(label)

                del self.objects[label]

        return added, removed