"""
Object priorities.

Higher number = more important.
Used by the response generator to decide
what should be spoken first.
"""

HIGH_PRIORITY = {
    "person",
    "car",
    "truck",
    "bus",
    "motorcycle",
    "bicycle",
    "chair",
    "stairs",
    "door",
    "dog",
    "cat"
}

MEDIUM_PRIORITY = {
    "cell phone",
    "laptop",
    "backpack",
    "bottle",
    "cup",
    "book",
    "handbag",
    "keyboard",
    "mouse"
}

LOW_PRIORITY = {
    "tv",
    "clock",
    "plant",
    "vase",
    "potted plant",
    "remote"
}


def get_priority(label: str) -> int:
    """
    Returns:
        3 = High
        2 = Medium
        1 = Low
    """

    if label in HIGH_PRIORITY:
        return 3

    if label in MEDIUM_PRIORITY:
        return 2

    return 1


def sort_objects(objects):
    """
    Sort objects by priority.
    """

    return sorted(
        objects,
        key=lambda obj: get_priority(obj["label"]),
        reverse=True
    )