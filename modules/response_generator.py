from modules.priority import sort_objects


def object_sentence(obj):

    label = obj["label"]

    position = obj["position"]

    distance = obj["distance"]

    if distance == "very close":
        return f"{label} very close {position}."

    if distance == "close":
        return f"{label} close {position}."

    if distance == "medium distance":
        return f"{label} {position}."

    return f"{label} far {position}."


def simplify_scene(caption):

    caption = caption.lower()

    if "bedroom" in caption:
        return "bedroom"

    if "bunk bed" in caption:
        return "bedroom"

    if "bed" in caption:
        return "bedroom"

    if "kitchen" in caption:
        return "kitchen"

    if "refrigerator" in caption:
        return "kitchen"

    if "office" in caption:
        return "office"

    if "desk" in caption:
        return "office"

    if "classroom" in caption:
        return "classroom"

    if "blackboard" in caption:
        return "classroom"

    if "bathroom" in caption:
        return "bathroom"

    return ""


def build_response(

        added_objects,

        removed_objects,

        caption="",

        ocr_text=""

):

    messages = []

    # --------------------------------
    # Highest priority
    # --------------------------------

    added_objects = sort_objects(added_objects)

    for obj in added_objects[:3]:

        messages.append(
            object_sentence(obj)
        )

    # --------------------------------
    # Removed objects
    # --------------------------------

    for obj in removed_objects:

        messages.append(
            f"{obj['label']} disappeared."
        )

    # --------------------------------
    # OCR
    # --------------------------------

    if ocr_text:

        messages.append(
            f"Text says {ocr_text}."
        )

    # --------------------------------
    # Florence
    # --------------------------------

    scene = simplify_scene(caption)

    if scene:

        messages.append(
            f"You appear to be in a {scene}."
        )

    return " ".join(messages)