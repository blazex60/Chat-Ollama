import streamlit as st
from llm import lmstudio as lm
import re

# Sidebarの選択肢を定義する
options = ["openai/gpt-oss-20b", "qwen/qwen3-4b-thinking-2507"]
choice = st.sidebar.selectbox("Select an option", options)

# Modelを変える
lm.selected_model = choice

# テキスト入力ボックス
text_input = st.text_input('Input', 'Input some text here.')

if st.button('Submit'):
    raw = lm.generate_text(lm.selected_model, text_input)

    # すべての <think> ブロックを抽出 (大小文字無視 / 非貪欲)
    pattern = re.compile(r"<think>([\s\S]*?)</think>", re.IGNORECASE)
    think_blocks = pattern.findall(raw)

    # 本文用テキスト (think ブロックを除去したもの)
    cleaned = pattern.sub("", raw).strip()

    # <think> ブロックを隠す (ユーザーが開ける)
    if think_blocks:
        with st.expander("推論過程を表示 / 隠す", expanded=False):
            for i, block in enumerate(think_blocks, start=1):
                st.markdown(f"**Block {i}:**")
                # 余計な前後空白を除去しコードブロック表示
                st.code(block.strip(), language="markdown")
    else:
        # 推論ブロックがない場合もデバッグ用に開けるようにするかは任意。ここでは表示しない。
        pass

    # 回答表示
    st.subheader("Answer")
    st.write(cleaned if cleaned else "(空の応答)")

    # 任意: 生レスポンスをさらに確認したい場合 (デバッグ)
    with st.expander("Raw response (debug)"):
        st.code(raw)