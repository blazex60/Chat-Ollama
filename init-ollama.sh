#!/bin/bash

# ==================================================
# Ollama設定
# ==================================================
# 使用するモデルを指定（環境変数またはデフォルト値）
MODEL_NAME="${OLLAMA_MODEL:-qwen2.5:7b}"

# 他のモデル例：
# MODEL_NAME="llama3.2:3b"
# MODEL_NAME="gemma2:2b"
# MODEL_NAME="phi3:mini"
# MODEL_NAME="mistral:7b"
# 
# 環境変数での指定例：
# export OLLAMA_MODEL="llama3.2:3b"
# または docker-compose.yml で環境変数を設定

# ==================================================
# 初期化処理
# ==================================================

echo "=== Ollama初期化開始 ==="
echo "使用モデル: $MODEL_NAME"
echo "$(date): Ollamaサーバーを起動中..."

# Ollamaサーバーをバックグラウンドで起動
ollama serve &
OLLAMA_PID=$!

# サーバーが起動するまで待機
echo "$(date): サーバーの起動を待機中..."
sleep 10

# サーバーが正常に起動しているか確認
if ! curl -f http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "$(date): ⚠️ Ollamaサーバーの起動に失敗しました"
    exit 1
fi

echo "$(date): ✅ Ollamaサーバーが正常に起動しました"
echo "$(date): 📥 モデル $MODEL_NAME のダウンロードを開始します..."

# モデルをダウンロード（エラーハンドリング付き）
if ollama pull $MODEL_NAME; then
    echo ""
    echo "🎉 =================================="
    echo "🎉  モデルダウンロード完了！"
    echo "🎉  Model: $MODEL_NAME"
    echo "🎉  Time: $(date)"
    echo "🎉  Status: Ready for use"
    echo "🎉 =================================="
    echo ""
    
    # 利用可能なモデルを表示
    echo "📋 利用可能なモデル一覧:"
    ollama list
    echo ""
    echo "🚀 Ollamaサーバーが準備完了しました！"
    echo "🌐 API endpoint: http://localhost:11434"
else
    echo ""
    echo "❌ =================================="
    echo "❌  モデルダウンロード失敗"
    echo "❌  Model: $MODEL_NAME"
    echo "❌  Time: $(date)"
    echo "❌ =================================="
    echo ""
    exit 1
fi

# フォアグラウンドでサーバーを継続実行
echo "$(date): サーバーを継続実行中..."
wait
