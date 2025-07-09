# character/character_manager.py

import json
import os


def load_characters(path: str = "character/characters.json") -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_characters(
    characters: dict, path: str = "character/characters.json"
) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(characters, f, ensure_ascii=False, indent=2)


def get_character_by_name(name: str, characters: dict) -> dict:
    return characters.get(name, {})
