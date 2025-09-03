from openai import OpenAI, APIConnectionError
import os, time

DEFAULT_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://host.docker.internal:1234/v1")

class lmstudio:
    def __init__(self):
        # OpenAI ライブラリは api_key が必須なのでダミー値を渡す (LM Studio 側で不要な場合でも)
        api_key = os.getenv("OPENAI_API_KEY", "lmstudio-placeholder-key")
        self._client = OpenAI(base_url=DEFAULT_BASE_URL, api_key=api_key)
        self.selected_model = None  # 選択されたモデルを保存する属性

    def list_loaded_models(self) -> list[str]:
        try:
            return [model.id for model in self._client.models.list()]
        except APIConnectionError as e:
            print(f"[Warning] LM Studio への接続に失敗しました: {e}")
            return []
        except Exception as e:
            print(f"[Warning] モデル一覧の取得に失敗しました: {e}")
            return []

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