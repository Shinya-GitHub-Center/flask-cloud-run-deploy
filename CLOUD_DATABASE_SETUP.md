# Google Cloud での本番データベース設定ガイド

## 概要

このアプリケーションは、環境変数を使って自動的に本番環境とローカル環境のデータベースを切り替えます。

- **ローカル環境**: SQLite（`db/blogpost.sqlite`）
- **本番環境**: Google Cloud SQL（MySQL）

## 1. Cloud SQL インスタンスの作成

### MySQL を使用する場合（本プロジェクトで使用）

```bash
# Cloud SQL インスタンスを作成
gcloud sql instances create flask-blog-db \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=asia-northeast1

# データベースを作成
gcloud sql databases create blogpost \
    --instance=flask-blog-db

# ユーザーを作成
gcloud sql users create bloguser \
    --instance=flask-blog-db \
    --password=YOUR_SECURE_PASSWORD
```

## 2. 接続文字列の取得

### MySQL の場合（本プロジェクトで使用）

```
mysql+pymysql://bloguser:YOUR_SECURE_PASSWORD@/blogpost?unix_socket=/cloudsql/PROJECT_ID:asia-northeast1:flask-blog-db
```

**PROJECT_ID** を実際の Google Cloud プロジェクトIDに置き換えてください。

## 3. 必要なパッケージの追加

`requirements.txt` には以下が既に追加されています：

### MySQL を使用する場合（本プロジェクトで使用）

```txt
pymysql>=1.1.0
cryptography>=41.0.7
```

## 4. Secret Manager での機密情報の管理（推奨）

### Secret Manager を有効化

```bash
gcloud services enable secretmanager.googleapis.com
```

### シークレットを作成

```bash
# データベース接続文字列（MySQL）
echo -n "mysql+pymysql://bloguser:YOUR_PASSWORD@/blogpost?unix_socket=/cloudsql/PROJECT_ID:asia-northeast1:flask-blog-db" | \
    gcloud secrets create gcloud-db-connection --data-file=-

# SECRET_KEY（ランダムな文字列を生成）
python3 -c "import secrets; print(secrets.token_hex(32))" | \
    gcloud secrets create flask-secret-key --data-file=-

# 管理者パスワード
echo -n "your_admin_password" | \
    gcloud secrets create admin-password --data-file=-
```

## 5. Cloud Run への環境変数の設定

### 方法 A: 環境変数として直接設定（非推奨：機密情報が含まれる場合）

```bash
gcloud run deploy flask-blog-app \
    --image gcr.io/PROJECT_ID/flask-blog-app \
    --platform managed \
    --region asia-northeast1 \
    --add-cloudsql-instances PROJECT_ID:asia-northeast1:flask-blog-db \
    --set-env-vars "GCLOUD_DB_CONNECTION=mysql+pymysql://bloguser:PASSWORD@/blogpost?unix_socket=/cloudsql/PROJECT_ID:asia-northeast1:flask-blog-db"
```

### 方法 B: Secret Manager から参照（推奨）

```bash
gcloud run deploy flask-blog-app \
    --image gcr.io/PROJECT_ID/flask-blog-app \
    --platform managed \
    --region asia-northeast1 \
    --add-cloudsql-instances PROJECT_ID:asia-northeast1:flask-blog-db \
    --set-secrets "GCLOUD_DB_CONNECTION=gcloud-db-connection:latest,SECRET_KEY=flask-secret-key:latest,ADMIN_PASSWORD=admin-password:latest" \
    --set-env-vars "ADMIN_USERNAME=admin"
```

## 6. データベースのマイグレーション

本番環境に初めてデプロイする際は、データベースのテーブルを作成する必要があります。

### Cloud Run Jobs を使用する方法

```bash
# マイグレーション用のジョブを作成
gcloud run jobs create db-migration \
    --image gcr.io/PROJECT_ID/flask-blog-app \
    --set-cloudsql-instances PROJECT_ID:asia-northeast1:flask-blog-db \
    --set-secrets "GCLOUD_DB_CONNECTION=gcloud-db-connection:latest" \
    --command "flask" \
    --args "db,upgrade"

# ジョブを実行
gcloud run jobs execute db-migration
```

### Cloud SQL Proxy を使ってローカルから実行する方法

```bash
# Cloud SQL Proxy をダウンロード
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy

# Proxy を起動（別のターミナルで）- MySQL用にポート3306を使用
./cloud_sql_proxy -instances=PROJECT_ID:asia-northeast1:flask-blog-db=tcp:3306

# 環境変数を設定して Flask からマイグレーション
export GCLOUD_DB_CONNECTION="mysql+pymysql://bloguser:PASSWORD@localhost:3306/blogpost"
cd db/migrations
alembic upgrade head
```

## 7. 動作確認

### 環境変数が正しく設定されているか確認

```bash
gcloud run services describe flask-blog-app \
    --region asia-northeast1 \
    --format "value(spec.template.spec.containers[0].env)"
```

### ログの確認

```bash
gcloud run logs read flask-blog-app --region asia-northeast1
```

## セキュリティのベストプラクティス

1. **Secret Manager を使用する**: データベース接続情報やパスワードは Secret Manager に保存
2. **最小権限の原則**: Cloud Run サービスアカウントに必要最小限の権限のみ付与
3. **Cloud SQL の認証プロキシを使用**: 公開 IP を避け、Unix ソケット経由で接続
4. **SSL/TLS を有効化**: データベース接続を暗号化
5. **定期的なバックアップ**: Cloud SQL の自動バックアップを有効化

## トラブルシューティング

### 接続エラーが発生する場合

1. Cloud SQL インスタンス名が正しいか確認
2. `--add-cloudsql-instances` フラグが設定されているか確認
3. サービスアカウントに Cloud SQL Client 権限があるか確認

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"
```

### マイグレーションエラーが発生する場合

SQLite から PostgreSQL/MySQL への移行時は、データ型の違いに注意が必要です。
必要に応じて `models.py` のカラム定義を調整してください。

## コスト最適化

- **db-f1-micro**: 無料枠対象（月間の使用量に制限あり）
- **自動スケーリング**: 使用しない時間帯はインスタンスを停止

```bash
# 開発環境では、使用しない時はインスタンスを停止
gcloud sql instances patch flask-blog-db --activation-policy=NEVER
```
