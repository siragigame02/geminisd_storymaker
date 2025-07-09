# ui/tabs.py

import streamlit as st
from ui.settings_tab import show_settings_tab
from ui.character_tab import show_character_tab
from ui.history_tab import show_history_tab
from ui.chat_tab import show_chat_tab


def show_tabs(config):
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 設定", "👤 キャラクター", "🗂️ 履歴", "💬 チャット"])

    with tab1:
        show_settings_tab(config)
    with tab2:
        show_character_tab()
    with tab3:
        show_history_tab()
    with tab4:
        show_chat_tab(config)
