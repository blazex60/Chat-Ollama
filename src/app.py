import streamlit as st
from llm import lmstudio as lm
import re
from PIL import Image

icon = Image.open("images/icon.png")

st.set_page_config(
    page_title="省エネとは無縁の世界",
    page_icon=icon,
)

# Sidebar の選択肢を定義
try:
    options = lm.list_loaded_models()
    if not options:
        st.sidebar.error("利用可能なモデルがありません。LM Studioでモデルをロードしてください。")
        choice = None
    else:
        choice = st.sidebar.selectbox("Select an option", options)
except Exception as e:
    st.sidebar.error(f"モデル一覧の取得に失敗しました: {e}")
    choice = None

# Model を保持
lm.selected_model = choice

# テキスト入力
text_input = st.text_input("Input", "Input some text here.")

if st.button("Submit"):
    if not lm.selected_model:
        st.error("モデルが選択されていません。")
    else:
        # ストリーミングで回答を表示 (<think> は非表示)
        st.subheader("Answer")
        answer_placeholder = st.empty()

        # 生レスポンス蓄積と、<think> 除去のためのパターン
        pattern = re.compile(r"<think>([\s\S]*?)</think>", re.IGNORECASE)
        raw_chunks: list[str] = []
        cleaned_so_far = ""

        with st.spinner("Generating..."):
            try:
                stream = lm._client.chat.completions.create(
                    model=lm.selected_model,
                    messages=[{"role": "user", "content": text_input}],
                    stream=True,
                )

                # Event stream と chunk stream の両対応
                if hasattr(stream, "__enter__") and callable(getattr(stream, "__enter__")):
                    with stream as s:
                        for event in s:
                            etype = getattr(event, "type", None)
                            if etype == "chunk":
                                data = getattr(event, "data", event)
                                try:
                                    choices = getattr(data, "choices", None)
                                    if choices:
                                        delta = getattr(choices[0], "delta", None)
                                        content = getattr(delta, "content", None)
                                        if content:
                                            raw_chunks.append(content)
                                except Exception:
                                    pass
                            elif etype == "end":
                                break
                            elif etype == "error":
                                err = getattr(event, "error", None)
                                raise RuntimeError(str(err))

                            # 更新 (think を除去したものを表示)
                            raw_now = "".join(raw_chunks)
                            cleaned_now = pattern.sub("", raw_now).strip()
                            if cleaned_now != cleaned_so_far:
                                answer_placeholder.markdown(cleaned_now)
                                cleaned_so_far = cleaned_now
                else:
                    for chunk in stream:
                        content = None
                        try:
                            choices = getattr(chunk, "choices", None)
                            if choices:
                                delta = getattr(choices[0], "delta", None)
                                content = getattr(delta, "content", None)
                        except Exception:
                            content = None

                        if content:
                            raw_chunks.append(content)
                            raw_now = "".join(raw_chunks)
                            cleaned_now = pattern.sub("", raw_now).strip()
                            if cleaned_now != cleaned_so_far:
                                answer_placeholder.markdown(cleaned_now)
                                cleaned_so_far = cleaned_now
            except Exception as e:
                answer_placeholder.markdown(f"[Error] {e}")

        # ストリーミング完了後、推論過程と生レスポンスを表示
        raw = "".join(raw_chunks)
        think_blocks = pattern.findall(raw)

        if think_blocks:
            with st.expander("推論過程を表示 / 隠す", expanded=False):
                for i, block in enumerate(think_blocks, start=1):
                    st.markdown(f"**Block {i}:**")
                    st.code(block.strip(), language="markdown")

        with st.expander("Raw response (debug)"):
            st.code(raw)

