# sd/image_utils.py

import re


def sanitize_filename(name: str) -> str:
    """
    ファイル名として使えない文字を除去・安全に整形
    """
    return re.sub(r'[\\/*?:"<>|]', "_", name)


def insert_image_markdown(image_path: str, caption: str = "") -> str:
    """
    挿絵画像を本文にMarkdown形式で挿入
    """
    return f"![{caption}]({image_path})"
