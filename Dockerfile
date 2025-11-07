# Python 3.12のスリムイメージを使用
FROM python:3.12-slim

# 必要なシステムパッケージをインストール（必要最小限）
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 非rootユーザーを作成（セキュリティのため）
RUN useradd -m -u 1000 appuser

# ユーザーのホームディレクトリを作業ディレクトリに設定
WORKDIR /home/appuser

# Pythonの依存関係をコピーしてインストール（rootで実行）
# ビルド時にrootを使うのは標準的なベストプラクティス
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー（所有者をappuserに設定）
COPY --chown=appuser:appuser app/ ./app/

# ここで非rootユーザーに切り替え
# 実行時に非rootユーザーを使うことでセキュリティを確保する
USER appuser

# Cloud Runが使用するポート（環境変数PORTから取得、デフォルトは8080）
ENV PORT=8080

# gunicornでアプリケーションを起動（JSON形式でシグナル処理を最適化）
CMD ["sh", "-c", "exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app.main:app"]
