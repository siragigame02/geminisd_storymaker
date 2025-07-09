# chat/chat_storage.py

import os
from datetime import datetime


def sanitize_filename(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in ("-_")).rstrip()


def save_chat_log(
    title: str, content: str, path: str = "chat/history/"
) -> None:
    os.makedirs(path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = sanitize_filename(title or "untitled")
    filename = f"{safe_title}.md"
    full_path = os.path.join(path, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)


def list_chat_logs(path: str = "chat/history/") -> list:
    if not os.path.exists(path):
        return []
    return [f for f in os.listdir(path) if f.endswith(".md")]


def load_chat_log(filename: str, path: str = "chat/history/") -> str:
    full_path = os.path.join(path, filename)
    if not os.path.exists(full_path):
        return ""
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()
