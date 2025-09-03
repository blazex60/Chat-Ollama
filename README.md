# 前提環境
以下のソフトウェアがインストールされていることを前提とします。

- Docker
- Python

# セットアップ手順

## 基本の立ち上げ方

1. Dockerを起動します。
2. ターミナルで以下のコマンドを実行します。
   ```
   docker compose up -d --build
   ```
3. ブラウザで http://localhost:8080 にアクセスできるか確認します。
4. 左のタブに使用可能なモデルがロードされます。
5. 画面上部のテキストボックスに質問を入力し、送信します。

## モデルの変更方法

### 方法1: .envファイルを編集
1. `.env`ファイルを開きます。
2. `OLLAMA_MODEL`の値を変更します：
   ```
   # 例: より軽量なモデルに変更
   OLLAMA_MODEL=llama3.2:3b
   ```
3. コンテナを再起動します：
   ```
   docker compose down
   docker compose up -d --build
   ```

### 方法2: 環境変数で指定
```bash
# Windows PowerShell
$env:OLLAMA_MODEL="gemma2:2b"
docker compose up -d --build

# Linux/Mac
OLLAMA_MODEL="phi3:mini" docker compose up -d --build
```

### 利用可能なモデル例
- `qwen2.5:7b` (デフォルト)
- `llama3.2:3b` (軽量)
- `gemma2:2b` (超軽量)
- `phi3:mini` (高速)
- `mistral:7b` (汎用)
- `codellama:7b` (コード生成特化)

## ログの確認
Ollamaの初期化ログ（モデルダウンロード進行状況含む）を確認：
```
docker logs first-term_subject-ollama-1 -f
```