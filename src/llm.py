# LM StudioはOpenAI互換のAPIを提供
from openai import OpenAI

class lmstudio():
    def generate_text(self, selected_model, text):
        # LM StudioにホストされているAPIサーバーに接続
        client = OpenAI(base_url="http://100.65.101.114:1234/v1")

        # Gemma 3 1B モデルでテキスト生成
        response = client.chat.completions.create(
            model=selected_model,  # モデルを指定
            messages=[
                {"role": "user", "content": text}
            ],  # ユーザーからの入力メッセージ
        )
        return response.choices[0].message.content

# 生成されたテキスト応答を表示
#print(response.choices[0].message.content)