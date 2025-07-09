# ui/history_tab.py
import streamlit as st
from chat.chat_storage import list_chat_logs, load_chat_log
import re
import os
import base64


def show_history_tab():
    st.subheader("🗂️ チャット履歴")
    from config.config_loader import load_config  # 先頭に追加

    config = load_config()
    logs = list_chat_logs(config["save_paths"]["chat_logs"])

    if not logs:
        st.info("履歴がまだありません。")
        return

    selected_log = st.selectbox("履歴を選択", logs, key="history_select")
    content = load_chat_log(selected_log, config["save_paths"]["chat_logs"])
    st.markdown(f"### 📄 {selected_log}")
    render_markdown_with_images(content)
    # st.markdown(content)


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
