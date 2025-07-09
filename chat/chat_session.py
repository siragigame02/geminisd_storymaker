# chat/chat_session.py

import requests
from google.generativeai.types import HarmCategory, HarmBlockThreshold


def send_prompt_to_google(prompt: str, config: dict, history: list = []) -> str:

    api_key = config["google_api"].get("api_key", "")
    model = config["google_api"].get("model", "gemini-2.5-pro")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    # ✅ 画像用命令文を末尾に自動付加
    image_instruction = config.get("image_instructions", "").strip()
    if image_instruction and image_instruction not in prompt:
        prompt = f"{prompt}\n\n----\n{image_instruction.strip()}\n----"

    # ユーザープロンプトと履歴を parts に変換
    parts = [{"text": h} for h in history] + [{"text": prompt}]
    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"temperature": 0.9, "topP": 1.0, "topK": 1},
    }

    # ✅ Safety Settings を追加
    safety_raw = config.get("safety_settings", {})
    if safety_raw:
        payload["safetySettings"] = []
        for category_name, threshold_str in safety_raw.items():
            payload["safetySettings"].append(
                {"category": category_name, "threshold": threshold_str}
            )

    # 🔽 API呼び出し
    response = requests.post(url, headers=headers, json=payload)

    try:
        result = response.json()

        if "error" in result:
            raise RuntimeError(f"❌ APIエラー: {result['error'].get('message')}")

        if "candidates" not in result or not result["candidates"]:
            print("🔴 APIレスポンス内容（debug）:")
            print(response.text)
            raise RuntimeError(
                "❌ レスポンスに candidates が含まれていません。Geminiの規約違反などが含まれている可能性があります"
            )

        content = result["candidates"][0]["content"]

        if "parts" in content:
            return content["parts"][0]["text"]
        elif "text" in content:
            return content["text"]
        else:
            raise RuntimeError("❌ 'parts' も 'text' も見つかりません")

    except Exception as e:
        raise RuntimeError(f"レスポンス処理エラー: {e}")


def extract_character_names(text: str, character_list: list) -> list:
    found = []
    for name in character_list:
        if name in text:
            found.append(name)
    return found
