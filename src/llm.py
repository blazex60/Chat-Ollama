"""LM Studio OpenAI互換クライアント薄いラッパー"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, List, Dict
from openai import OpenAI

DEFAULT_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://host.docker.internal:1234/v1")


@dataclass
class LMStudioClient:
    base_url: str = DEFAULT_BASE_URL
    api_key: str | None = None  # LM Studio では必須でないことが多い

    def __post_init__(self) -> None:
        # OpenAI 互換クライアントを初期化
        self._client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key or os.getenv("OPENAI_API_KEY", "lmstudio-not-required"),
        )

    def generate_text(self, model: str, text: str) -> str:
        resp = self._client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": text}],
        )
        return resp.choices[0].message.content


# シングルトンインスタンス (app.py はこれを import)
lmstudio = LMStudioClient()

__all__ = ["lmstudio", "LMStudioClient"]