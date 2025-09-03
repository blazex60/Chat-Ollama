FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl wget git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /llm

# 初期化スクリプトをコピー
COPY init-ollama.sh /usr/local/bin/init-ollama.sh
RUN chmod +x /usr/local/bin/init-ollama.sh

EXPOSE 11434

# bashで初期化スクリプトを実行
ENTRYPOINT ["/bin/bash", "/usr/local/bin/init-ollama.sh"]