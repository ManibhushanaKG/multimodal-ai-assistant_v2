from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch

processor = None
model = None
device = None


def load_model():
    global processor, model, device

    if processor is not None and model is not None:
        return

    print("Loading Florence-2 Large (first time only)...")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    processor = AutoProcessor.from_pretrained(
        "microsoft/Florence-2-large",
        trust_remote_code=True
    )

    if device == "cuda":
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Florence-2-large",
            trust_remote_code=True,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        ).to(device)

    else:
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Florence-2-large",
            trust_remote_code=True
        ).to(device)

    model.eval()

    print(f"Florence-2 loaded successfully on {device.upper()}.")


def generate_caption(image_path):

    load_model()

    image = Image.open(image_path).convert("RGB")

    prompt = "<MORE_DETAILED_CAPTION>"

    inputs = processor(
        text=prompt,
        images=image,
        return_tensors="pt"
    )

    inputs = {
        k: (
            v.to(device, dtype=torch.float16)
            if device == "cuda" and torch.is_floating_point(v)
            else v.to(device)
        )
        for k, v in inputs.items()
    }

    with torch.inference_mode():

        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=64,
            num_beams=1,
            do_sample=False
        )

    generated_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=False
    )[0]

    parsed = processor.post_process_generation(
        generated_text,
        task=prompt,
        image_size=image.size
    )

    image.close()

    return parsed[prompt]