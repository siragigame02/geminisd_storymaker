#!/bin/bash

# 仮想環境がある場合は有効化
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# アプリを起動
streamlit run main.py
