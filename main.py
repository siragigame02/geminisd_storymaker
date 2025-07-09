# main.py

import streamlit as st
from ui.tabs import show_tabs
from config.config_loader import load_config

# ページ設定
st.set_page_config(
    page_title="小説生成支援アプリ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# アプリタイトル表示
st.title("📘 小説生成支援アプリケーション")

# 設定読み込み（存在しない場合は空辞書）
try:
    config = load_config()
except Exception as e:
    st.warning(f"設定ファイルの読み込みに失敗しました: {e}")
    config = {}

# タブ切り替えUIを表示
show_tabs(config)
