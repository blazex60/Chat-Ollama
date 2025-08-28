import streamlit as st
from llm import lmstudio as lm

# Sidebarの選択肢を定義する
options = ["openai/gpt-oss-20b", "qwen/qwen3-4b-thinking-2507"]
choice = st.sidebar.selectbox("Select an option", options)

# Modelを変える
lm.selected_model = choice

# テキストエリア
text_area = st.text_area('Text Area', 'Input some text here.')
# テキスト入力ボックス
text_input = st.text_input('Input', 'Input some text here.')

if st.button('Submit'):
    response = lm.generate_text(lm.selected_model, text_input)
    st.write(response)