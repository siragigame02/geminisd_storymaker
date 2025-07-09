# ui/chat_tab.py

import streamlit as st
from chat.chat_session import send_prompt_to_google, extract_character_names
from chat.chat_storage import save_chat_log, list_chat_logs, load_chat_log
from character.character_manager import load_characters
from sd.sd_client import generate_image
from sd.image_utils import insert_image_markdown
import os
import re
import base64


def show_chat_tab(config):
    st.subheader("💬 新規チャット開始")

    # --- 新規チャット ---
    new_title = st.text_input("新しいチャットタイトル", "")
    new_prompt = st.text_area("最初のプロンプトを入力", "", height=150)

    if st.button("✨ 新規チャット送信"):
        try:
            selected_log = None
            characters = load_characters()
            char_names = list(characters.keys())
            result = send_prompt_to_google(new_prompt, config)
            st.markdown("### 📘 応答")
            st.markdown(result)

            scene_prompt = extract_scene_prompt(result)
            used_chars = extract_character_names(result, char_names)
            image_md = ""
            scene_prompt = extract_scene_prompt(result)
            for name in used_chars:
                char = characters[name]
                base_prompt = char["SD用プロンプト"]
                combined_prompt = (
                    f"{base_prompt}, {scene_prompt}"
                    if scene_prompt
                    else base_prompt
                )
                st.markdown(f"🟡 使用プロンプト: `{combined_prompt}`")
                img_path = generate_image(
                    combined_prompt,
                    char["SD Negative Prompt"],
                    config,
                    f"{new_title}_{name}",
                )
                image_md += (
                    insert_image_markdown(img_path, caption=name) + "\n\n"
                )
                from PIL import Image

                img = Image.open(img_path)
                st.image(img, caption=name)

                final_output = (
                    f"## {new_title}\n\n{result}\n\n---\n\n{image_md}"
                )
                save_chat_log(
                    new_title, final_output, config["save_paths"]["chat_logs"]
                )
            st.success("新規チャットを保存しました。")

        except Exception as e:
            st.error(f"エラー: {e}")

    st.divider()

    # --- セッション継続 ---
    st.subheader("📖 過去チャットを続ける")

    logs = list_chat_logs(config["save_paths"]["chat_logs"])
    if logs:
        selected_log = st.selectbox("履歴を選択", logs, key="select_log")
        content = load_chat_log(selected_log, config["save_paths"]["chat_logs"])
        st.markdown("### 🔁 現在の履歴")
        render_markdown_with_images(content)
        # st.markdown(content)

        continuation = st.text_area("続きの入力", "", height=150)
        if st.button("📨 続きを送信"):
            try:
                characters = load_characters()
                char_names = list(characters.keys())
                history_texts = [
                    line.strip()
                    for line in content.splitlines()
                    if line and not line.startswith("!")
                ]
                result = send_prompt_to_google(
                    continuation, config, history=history_texts[-3:]
                )  # 過去3行だけ渡す簡易対応
                st.markdown("### 📘 応答")
                st.markdown(result)
                scene_prompt = extract_scene_prompt(result)
                used_chars = extract_character_names(result, char_names)
                image_md = ""
                scene_prompt = extract_scene_prompt(result)
                for name in used_chars:
                    char = characters[name]
                    base_prompt = char["SD用プロンプト"]
                    combined_prompt = (
                        f"{base_prompt}, {scene_prompt}"
                        if scene_prompt
                        else base_prompt
                    )

                    st.markdown(f"🟡 送信プロンプト: `{combined_prompt}`")  # デバッグ表示

                    img_path = generate_image(
                        combined_prompt,
                        char["SD Negative Prompt"],
                        config,
                        f"{new_title}_{name}",
                    )

                    if os.path.exists(img_path):
                        image_md += (
                            insert_image_markdown(img_path, caption=name)
                            + "\n\n"
                        )
                        st.image(img_path, caption=f"{name} の画像", width=512)
                    else:
                        st.warning(f"⚠️ 画像が生成されませんでした: {img_path}")

                new_block = "\n\n---\n\n" + result + "\n\n---\n\n" + image_md
                full_content = content + new_block

                save_chat_log(
                    selected_log.rsplit(".", 1)[0],
                    full_content,
                    config["save_paths"]["chat_logs"],
                )
                st.success("続きを保存しました。")
                # ✅ 再実行して入力欄を再表示
                st.rerun()
            except Exception as e:
                st.error(f"エラー: {e}")
    else:
        st.info("チャット履歴がまだ存在しません。")


def extract_scene_prompt(text: str) -> str:
    """
    本文から [Prompt:○○] の形式を探し、プロンプト文を返す
    """
    match = re.search(r"\[Prompt:(.+?)\]", text, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def render_markdown_with_images(markdown_text):
    # Markdown内の画像記法を探す
    pattern = r"!\[(.*?)\]\((.*?)\)"
    last_end = 0

    for match in re.finditer(pattern, markdown_text):
        alt_text, img_path = match.groups()
        start, end = match.span()

        # マークダウンテキスト（画像の前）を表示
        st.markdown(markdown_text[last_end:start])

        # パスが存在するかをチェックして画像を表示
        if os.path.exists(img_path):
            with open(img_path, "rb") as img_file:
                img_bytes = img_file.read()

            # 画像として表示（横幅512px、クリックで拡大）
            st.image(img_bytes, caption=alt_text, width=512)
        else:
            st.warning(f"⚠️ 画像が見つかりませんでした: {img_path}")

        last_end = end

    # 残りのマークダウンテキスト（画像の後ろ）
    st.markdown(markdown_text[last_end:])
