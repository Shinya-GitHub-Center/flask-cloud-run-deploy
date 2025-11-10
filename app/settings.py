import os

basedir = os.path.dirname(os.path.dirname(__file__))
dbdir = basedir + "/db"

# 本番環境のデータベース接続情報（環境変数から取得）
GCLOUD_DB_CONNECTION = os.environ.get("GCLOUD_DB_CONNECTION")

# データベースURIの設定
if GCLOUD_DB_CONNECTION:
    # 本番環境: Google Cloud SQL を使用
    SQLALCHEMY_DATABASE_URI = GCLOUD_DB_CONNECTION
else:
    # ローカル開発環境: SQLite を使用
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(dbdir, "blogpost.sqlite")

# セキュリティ設定
# 本番環境では環境変数から取得、ローカルではデフォルト値を使用
SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(10))

# 管理者認証情報
# 本番環境では環境変数から取得、ローカルではデフォルト値を使用
USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "0000")
