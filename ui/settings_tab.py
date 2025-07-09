# ui/settings_tab.py

import streamlit as st
from config.config_loader import save_config


def show_settings_tab(config: dict):
    st.subheader("🔧 GoogleAIStudio 接続設定")
    config["google_api"]["api_key"] = st.text_input(
        "APIキー", value=config["google_api"].get("api_key", ""), type="password"
    )
    config["google_api"]["model"] = st.text_input(
        "モデル名（例：gemini-2.5-pro）", value=config["google_api"].get("model", "")
    )

    st.subheader("🎨 StableDiffusion 設定")
    sd = config["stable_diffusion"]
    sd["url"] = st.text_input(
        "エンドポイントURL", value=sd.get("url", "http://127.0.0.1:7860/")
    )
    sd["checkpoint"] = st.text_input(
        "Checkpointファイル", value=sd.get("checkpoint", "")
    )
    sd["vae"] = st.text_input("VAEファイル", value=sd.get("vae", ""))
    sd["sampler"] = st.text_input("Sampler", value=sd.get("sampler", "Euler a"))
    sd["steps"] = st.slider("Sampling Steps", 1, 100, value=sd.get("steps", 20))
    sd["cfg_scale"] = st.slider(
        "CFG Scale", 1.0, 20.0, value=sd.get("cfg_scale", 4.0)
    )
    sd["seed"] = st.number_input("Seed", value=sd.get("seed", -1))
    sd["width"] = st.number_input("解像度（横）", value=sd.get("width", 1024))
    sd["height"] = st.number_input("解像度（縦）", value=sd.get("height", 1024))

    st.subheader("💾 保存先")
    config["save_paths"]["chat_logs"] = st.text_input(
        "チャットログ保存先",
        value=config["save_paths"].get("chat_logs", "outputs/logs/"),
    )
    config["save_paths"]["images"] = st.text_input(
        "画像保存先", value=config["save_paths"].get("images", "outputs/images/")
    )

    if st.button("✅ 設定を保存"):
        save_config(config)
        st.success("設定を保存しました。")
