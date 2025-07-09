# sd/sd_client.py

import requests
import os
import base64
from sd.image_utils import sanitize_filename
from datetime import datetime


def generate_image(
    prompt: str, negative_prompt: str, config: dict, filename_hint: str = ""
) -> str:
    print(f"🟡 [SD prompt] {prompt}")
    sd_config = config["stable_diffusion"]
    url = sd_config.get("url", "http://127.0.0.1:7860/") + "sdapi/v1/txt2img"

    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "sampler_name": sd_config.get("sampler", "Euler a"),
        "steps": sd_config.get("steps", 20),
        "cfg_scale": sd_config.get("cfg_scale", 4.0),
        "seed": sd_config.get("seed", -1),
        "width": sd_config.get("width", 1024),
        "height": sd_config.get("height", 1024),
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        image_data = response.json()["images"][0]

        # 画像デコード
        img_bytes = base64.b64decode(image_data.split(",", 1)[-1])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = sanitize_filename(filename_hint or "output")
        filename = f"{safe_name}_{timestamp}.png"

        output_dir = config["save_paths"]["images"]
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)

        with open(output_path, "wb") as f:
            f.write(img_bytes)

        return output_path

    except Exception as e:
        raise RuntimeError(f"StableDiffusion画像生成に失敗しました: {e}")
