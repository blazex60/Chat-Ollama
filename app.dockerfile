FROM python:3.13-slim

# 必要最低限の OS パッケージ (git 等が不要なら削って可)
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl wget git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 依存関係のみ先にコピーしてキャッシュ活用
COPY src/requirements.txt ./requirements.txt
COPY images/ ./images/
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体
COPY src/ .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
