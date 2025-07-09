# config/config_loader.py

import xml.etree.ElementTree as ET
import os


def load_config(path: str = "config/config.xml") -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"設定ファイルが存在しません: {path}")

    tree = ET.parse(path)
    root = tree.getroot()

    def get_text(elem, tag):
        return elem.find(tag).text if elem.find(tag) is not None else ""

    config = {
        "google_api": {
            "api_key": get_text(root.find("google_api"), "api_key"),
            "model": get_text(root.find("google_api"), "model"),
        },
        "stable_diffusion": {
            "url": get_text(root.find("stable_diffusion"), "url"),
            "checkpoint": get_text(root.find("stable_diffusion"), "checkpoint"),
            "vae": get_text(root.find("stable_diffusion"), "vae"),
            "sampler": get_text(root.find("stable_diffusion"), "sampler"),
            "steps": int(
                get_text(root.find("stable_diffusion"), "steps") or 20
            ),
            "cfg_scale": float(
                get_text(root.find("stable_diffusion"), "cfg_scale") or 4.0
            ),
            "seed": int(get_text(root.find("stable_diffusion"), "seed") or -1),
            "width": int(
                get_text(root.find("stable_diffusion/resolution"), "width")
                or 1024
            ),
            "height": int(
                get_text(root.find("stable_diffusion/resolution"), "height")
                or 1024
            ),
        },
        "save_paths": {
            "chat_logs": get_text(root.find("save_paths"), "chat_logs"),
            "images": get_text(root.find("save_paths"), "images"),
        },
        "image_instructions": get_text(root, "image_instructions"),
    }

    # --- Safety Settings の読み込み ---
    safety_elem = root.find("safety")
    if safety_elem is not None:
        for child in safety_elem:
            config["safety_settings"][child.tag] = child.text or "BLOCK_NONE"

    return config


def save_config(data: dict, path: str = "config/config.xml") -> None:
    root = ET.Element("config")

    google_api = ET.SubElement(root, "google_api")
    ET.SubElement(google_api, "api_key").text = data["google_api"].get(
        "api_key", ""
    )
    ET.SubElement(google_api, "model").text = data["google_api"].get(
        "model", ""
    )

    sd = ET.SubElement(root, "stable_diffusion")
    ET.SubElement(sd, "url").text = data["stable_diffusion"].get("url", "")
    ET.SubElement(sd, "checkpoint").text = data["stable_diffusion"].get(
        "checkpoint", ""
    )
    ET.SubElement(sd, "vae").text = data["stable_diffusion"].get("vae", "")
    ET.SubElement(sd, "sampler").text = data["stable_diffusion"].get(
        "sampler", ""
    )
    ET.SubElement(sd, "steps").text = str(
        data["stable_diffusion"].get("steps", 20)
    )
    ET.SubElement(sd, "cfg_scale").text = str(
        data["stable_diffusion"].get("cfg_scale", 4.0)
    )
    ET.SubElement(sd, "seed").text = str(
        data["stable_diffusion"].get("seed", -1)
    )

    resolution = ET.SubElement(sd, "resolution")
    ET.SubElement(resolution, "width").text = str(
        data["stable_diffusion"].get("width", 1024)
    )
    ET.SubElement(resolution, "height").text = str(
        data["stable_diffusion"].get("height", 1024)
    )
    ET.SubElement(root, "image_instructions").text = data.get(
        "image_instructions", ""
    )

    save_paths = ET.SubElement(root, "save_paths")
    ET.SubElement(save_paths, "chat_logs").text = data["save_paths"].get(
        "chat_logs", ""
    )
    ET.SubElement(save_paths, "images").text = data["save_paths"].get(
        "images", ""
    )

    # --- Safety Settings の保存 ---
    safety = ET.SubElement(root, "safety")
    for cat, thresh in data.get("safety_settings", {}).items():
        ET.SubElement(safety, cat).text = thresh

    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)
