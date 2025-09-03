from openai import OpenAI, APIConnectionError
import os, time

client = OpenAI(
    base_url = 'http://ollama:11434/v1',
    api_key='ollama', # required, but unused
)

class lmstudio:
    def __init__(self):
        # OpenAI ライブラリは api_key が必須なのでダミー値を渡す (ollama 側で不要な場合でも)
        self._client = OpenAI(base_url=client.base_url, api_key=client.api_key)

    def list_loaded_models(self) -> list[str]:
        return [model.id for model in self._client.models.list()]

    def generate_text(self, model: str, text: str) -> str:
        last_err: Exception | None = None
        retries = int(os.getenv("LMSTUDIO_RETRIES", "3"))
        delay = float(os.getenv("LMSTUDIO_RETRY_DELAY", "1.0"))
        for attempt in range(1, retries + 1):
            try:
                resp = self._client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": text}],
                )
                return resp.choices[0].message.content
            except APIConnectionError as e:  # ネットワーク接続失敗
                last_err = e
                if attempt < retries:
                    time.sleep(delay)
                else:
                    return (
                        "[ConnectionError] LM Studio へ接続できませんでした。\n"
                        f"BASE_URL={self._client.base_url}\n"
                        "1) ホストで LM Studio の OpenAI 互換サーバーが起動しているか (ポート1234) を確認\n"
                        "2) ブラウザで http://localhost:1234/v1/models にアクセスできるか確認\n"
                        "3) docker compose exec app curl -v http://host.docker.internal:1234/v1/models で疎通テスト\n"
                        f"詳細: {e}"
                    )
            except Exception as e:  # その他エラー
                return f"[Error] 推論失敗: {e.__class__.__name__}: {e}"  # そのまま返す

# シングルトンインスタンスを外部に提供
lmstudio = lmstudio()