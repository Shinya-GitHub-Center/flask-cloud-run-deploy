#!/bin/bash

# Cloud Run デプロイスクリプト
# 使い方: ./deploy.sh

set -e

# ========== 設定値（ここを編集してください） ==========
PROJECT_ID="YOUR_PROJECT_ID"
SERVICE_NAME="utopian-food-blog"
REGION="asia-northeast1"
DB_INSTANCE_NAME="utopian-food-blog-db"
# ====================================================

# デプロイコマンド実行
gcloud run deploy ${SERVICE_NAME} \
    --source . \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --add-cloudsql-instances ${PROJECT_ID}:${REGION}:${DB_INSTANCE_NAME} \
    --set-secrets "GCLOUD_DB_CONNECTION=utopian-blog-db-connection:latest,SECRET_KEY=utopian-blog-secret-key:latest,ADMIN_PASSWORD=utopian-blog-admin-password:latest,ADMIN_USERNAME=utopian-blog-admin-username:latest" \
    --project ${PROJECT_ID}
