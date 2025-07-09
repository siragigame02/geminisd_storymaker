# ui/character_tab.py

import streamlit as st
from character.character_manager import load_characters, save_characters


def show_character_tab():
    st.subheader("👤 キャラクター情報管理")

    characters = load_characters()
    selected_name = st.selectbox(
        "キャラクターを選択", ["新規作成"] + list(characters.keys()), key="character_select"
    )
    is_new = selected_name == "新規作成"

    if is_new:
        char = {
            k: ""
            for k in [
                "名前",
                "年齢",
                "性別",
                "体型",
                "容姿",
                "髪型・髪色",
                "瞳の色",
                "SD用プロンプト",
                "SD Negative Prompt",
            ]
        }
    else:
        char = characters[selected_name]

    with st.form("char_form"):
        char["名前"] = st.text_input("名前", value=char["名前"])
        char["年齢"] = st.text_input("年齢", value=char["年齢"])
        char["性別"] = st.text_input("性別", value=char["性別"])
        char["体型"] = st.text_input("体型", value=char["体型"])
        char["容姿"] = st.text_area("容姿", value=char["容姿"])
        char["髪型・髪色"] = st.text_input("髪型・髪色", value=char["髪型・髪色"])
        char["瞳の色"] = st.text_input("瞳の色", value=char["瞳の色"])
        char["SD用プロンプト"] = st.text_area("SD用プロンプト", value=char["SD用プロンプト"])
        char["SD Negative Prompt"] = st.text_area(
            "SD Negative Prompt", value=char["SD Negative Prompt"]
        )

        submitted = st.form_submit_button("保存")
        if submitted:
            characters[char["名前"]] = char
            save_characters(characters)
            st.success("保存しました。")

    if not is_new and st.button("🗑 削除"):
        del characters[selected_name]
        save_characters(characters)
        st.warning("削除しました。")
