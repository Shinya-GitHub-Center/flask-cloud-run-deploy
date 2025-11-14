# About

## [セルフ勉強用]Sorry, this repo is Japanese language only![管理人備忘録]

こちらはFlaskアプリの勉強用リポジトリです。  
固定された管理人専用のログインIDでログインして、管理人のみが投稿・削除等ができるシンプルなブログアプリです。データベースを利用したSSR動的アプリです。  
本番環境は、Google CloudのCloud Runにデプロイして、Cloud SQLのMySQLに接続する構成です。

**※セキュリティは必要最小限で構築されていますので「テスト・勉強用」のみにお使いください。**

データベースなしの一番簡単なバージョン（簡単なボタンクリックによる値インクリメントのテストアプリ）で勉強したい場合は、別途[こちら](https://github.com/Shinya-GitHub-Center/flask-cloud-run-deploy/tree/v1-only-button-click)を参照してください。

- まずFlaskのシンプルな機能をローカルサーバー上で確認する
- 次に本番環境できちんと動作するか確認する（シンプルでほぼ無料で確認できるためCloud Runを利用する）

1. uv（Pythonパッケージマネージャー＆仮想環境作成ツール）があなたのローカルPCにインストールされていることが前提となります。このプロジェクトではpythonのv3.12を使用するので、事前にグローバルでuvインストールしておくとよいですね。
2. まずこのリポジトリをダウンロード後、`uv sync`コマンドにて初期化を行ってください（必要パッケージがこのプロジェクト以下の仮想環境にインストールされます）
3. VSCodeやCursorを使用して自動でPythonインタープリタが切り替わらない場合は、手動で`./.venv/bin/python`に切り替えてください。（このプロジェクト内のパッケージおよびPythonを使用するため）
4. `uv run flask --app run:app db init`でデータベース初期化（ローカル環境）
5. `uv run flask --app run:app db migrate`でマイグレーションファイル作成（ローカル環境）
6. `uv run flask --app run:app db upgrade`でデータベースにデータ構造を注入（ローカル環境）

Notice: Zipでダウンロードした場合は各自でGit初期化してください。また、勉強用・テスト用プロジェクトなので、特に`uv.lock`はこのリポジトリに含めていませんので、常に最新のパッケージ・モジュールを使用して勉強してください。

## 開発サーバーの起動方法
- `uv run run.py`（__name__が__main__になるのでデバッグモードがオンになる）

（本番環境でgunicornコマンドで起動する場合は、パラメータにパーツとして対象オブジェクトを渡しているだけなので、__main__にはならない）

## ブログ使用方法
- コナミコマンド（↑↑↓↓←→←→BA）で管理人専用投稿画面をひらく（ログインが必要、`settings.py`のUSERNAMEとPASSWORDを参照）。タブレットの場合は、`/post`パスへ直接移動してください。
- 別コナミコマンド（←→←→BA）で管理人専用記事削除画面をひらく（ログインが必要、`settings.py`のUSERNAMEとPASSWORDを参照）。タブレットの場合は、`/delete`パスへ直接移動してください。

## Tips

- サーバーサイド（Python/Flask）: `app/__init__.py`, `app/crud/views.py`などのPythonコードはサーバー上で実行され、HTMLを生成します
- クライアントサイド（JavaScript）: static/js/scripts.jsはブラウザで実行され、DOM操作、イベント処理、動的な画面更新などを行います
- **ビュー関数の「未使用」警告について**: `@app.route()`デコレータでラップされたビュー関数（`index()`, `show_entry()`等）は、静的解析ツールで「未使用」と警告されることがありますが、これは誤検知です。これらの関数はサーバー起動時にルーティングテーブルに登録され、HTTPリクエスト受信時にFlaskフレームワークが動的に呼び出すため、コード内で直接呼ばれることはありません。警告は無視して問題ありません
### **サーバー起動時（インタープリタによる静的な処理、つまりアプリエンティティによる操作）**
```python
@app.route("/")
def index():  # ← ここで関数が「定義」され、デコレーターがルーティングテーブルに登録
    ...
```
- 関数定義を読み込み
- `@app.route()`デコレーターが関数をFlaskの内部ルーティングテーブルに登録
- **関数自体はまだ実行されない**
- 静的解析ツール「この関数、コード内で直接呼ばれてないな...」→ 警告

### **リクエスト受信時（動的な処理、サーバーが立ち上がってからのユーザーによるインタラクティブな操作によって呼び出される）**
```
ユーザー → HTTP GET / → Flask → ルーティングテーブル参照 → index()呼び出し
```
- Flaskがリクエストを受信
- URLパターンとルーティングテーブルをマッチング
- 該当する関数（`index()`や`show_entry()`）を**実行時に動的に呼び出す**

### 処理の過程で同じモジュールが読み込まれたときの挙動について
Pythonでは、すべてのインポートされたモジュールが sys.modules という辞書に保存されます。
1. **モジュールのコードは1回だけ実行される**
   - 最初のインポート時にコードが実行される
   - その後のインポートはキャッシュから参照を取得するだけ

2. **スキップではなくキャッシュ再利用**
   - インポート文自体は実行される
   - しかしモジュールのコードは再実行されない
   - キャッシュされたモジュールオブジェクトが返される

つまりデフォルトで循環インポートを防ぐような仕様になっている（以前のコードも偶然動いていたのではなく、Pythonの仕組み上正しく動いていた）。しかし、ファクトリパターンの方が設計として堅牢で保守しやすいという優位性がある。

# デプロイ設定ファイルについて

このプロジェクトでは、効率的なビルドとデプロイのために2つの除外設定ファイルを使用しています。

## `.dockerignore` と `.gcloudignore` の違い

### それぞれの役割

| ファイル | 使用タイミング | 目的 | 影響範囲 |
|---------|--------------|------|---------|
| `.dockerignore` | Dockerイメージのビルド時 | イメージサイズの最適化 | 最終的なDockerイメージの中身 |
| `.gcloudignore` | `gcloud run deploy --source .` 実行時 | ネットワーク転送量の削減 | Cloud Buildへの送信内容 |

### Cloud Runへのデプロイ

```bash
gcloud run deploy utopian-food-blog --source .
```

**使用されるファイル:**
- ✅ `.gcloudignore` と `.dockerignore` の両方

**動作:**
```
ステップ1: ローカル → Cloud Buildへ送信
  └─ .gcloudignore でフィルタ
     （.venv/, __pycache__/, .git/ などを除外）

ステップ2: Cloud Build上でDockerビルド
  └─ .dockerignore でフィルタ
     （pyproject.toml, README.md などを除外）

ステップ3: Cloud Runにデプロイ
```

## それぞれのファイルで除外するもの

### `.dockerignore` で除外（実行時に不要なファイル）

```
# プロジェクト管理ファイル
pyproject.toml
uv.lock
.python-version

# ドキュメント
README.md
*.md

# 開発ツール設定
.vscode/
.idea/
```

**理由:** これらは実行時に不要。最終的なDockerイメージのサイズを小さく保つ。

### `.gcloudignore` で除外（転送不要なファイル）

```
# 開発環境の仮想環境（サイズが大きい）
.venv/
venv/

# Gitリポジトリ（不要）
.git/

# Pythonキャッシュ（自動生成される）
__pycache__/

# ログファイル（開発用）
*.log

# 環境変数（セキュリティ）
.env
```

**理由:** これらをCloud Buildに送信するのは無駄。特に`.venv/`は数百MBになることもある。

## `.gitignore` との関係

公式ドキュメントによると：

> If a `.gcloudignore` file is absent and a `.gitignore` file is present, gcloud will use a generated Git-compatible `.gcloudignore` file that respects your .gitignored files.

つまり：
- `.gcloudignore`がない場合、`.gitignore`が自動的に使用される
- ただし、**明示的に`.gcloudignore`を作成する方が確実**

## ベストプラクティス

✅ **両方のファイルをプロジェクトルートに配置する**

```
flask-cloud-run-deploy/
├── .dockerignore      # Dockerビルド用
├── .gcloudignore      # Cloud Buildデプロイ用
├── .gitignore         # Git管理用
├── Dockerfile
└── ...
```

## 確認方法

### `.dockerignore` の動作確認

```bash
# ビルドコンテキストに含まれるファイルを確認
docker build --no-cache -t test-image . 2>&1 | grep "Sending build context"
```

### `.gcloudignore` の動作確認

```bash
# デプロイ時のログで転送されるファイルを確認
gcloud run deploy --source . --dry-run
```

# Google Cloud アカウント初期設定

このドキュメントでは、FlaskアプリをGoogle Cloud Runにデプロイする手順を説明します。

## 前提条件

1. Google Cloudアカウント
2. Google Cloud CLIのインストール（gcloud）
3. プロジェクトの作成と課金の有効化

## 初期セットアップ

### 1. Google Cloud CLIのインストール（未インストールの場合のみ）

https://cloud.google.com/sdk/docs/install?hl=ja

（ubuntuの場合はパッケージ形式でインストールすること）

### 2. Google Cloudの初期設定およびログイン（gcloud CLIを初めて使う場合のみ）

```bash
gcloud init
```

プロジェクト選択の画面まで進んだら、そこで一旦中断。（ctrl+c）

### 3. プロジェクトの設定

```bash
# 既存のプロジェクトを使用する場合
gcloud config set project YOUR_PROJECT_ID

# または新しいプロジェクトを作成
gcloud projects create YOUR_PROJECT_ID --name="Flask Test App"
gcloud config set project YOUR_PROJECT_ID
```

### 4. 必要なAPIを有効化

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

※この時点で、編集者のロールを持ったサービスアカウント`${PROJECT_NUMBER}-compute@developer.gserviceaccount.com`が自動で作成される。

# データベース初期化からデプロイまで

## 概要

このアプリケーションは、環境変数を使って自動的に本番環境とローカル環境のデータベースを切り替えます。

- **ローカル環境**: SQLite（`db/blogpost.sqlite`）
- **本番環境**: Google Cloud SQL（MySQL）

## 1. Cloud SQL インスタンスの作成

gcloudコマンドを使用するので、作業の前に`gcloud info`でターゲットのプロジェクトが選択されていることを確認してください。  
（sqladmin.googleapis.comを有効にしてくださいと言われたたYESを選択）

### MySQL を使用する場合（本プロジェクトで使用）

Cloud SQL インスタンスを作成  
`gcloud sql instances create utopian-food-blog-db --database-version=MYSQL_8_0 --tier=db-f1-micro --region=asia-northeast1`

データベースを作成  
`gcloud sql databases create blogpost --instance=utopian-food-blog-db`

ユーザーを作成  
`gcloud sql users create bloguser --instance=utopian-food-blog-db --password=YOUR_SECURE_PASSWORD`

## 2. データベースのマイグレーション

本番環境に初めてデプロイする際は、データベースのテーブルを作成する必要があります。  
※以下の方法はめんどくさいので今回はスキップ
- Cloud SQL Proxyを使ってローカルから実行する方法
- リモートコンテナの中からマイグレーションファイルをDB接続して注入する方法

### Cloud Shellを使う（最も簡単・推奨）

### 1. Cloud Shellを起動

1. ブラウザでGoogle Cloud Consoleにアクセスして、ターゲットのプロジェクトに切り替える。
2. 画面右上の「**Cloud Shellをアクティブにする**」アイコン（`>_`）をクリック
3. 画面下部にターミナルが表示される（カレントディレクトリ表示の横にプロジェクト名があるのを確認）

### 2. Cloud SQLインスタンスに接続

Cloud Shellで以下のコマンドを実行：

```bash
gcloud sql connect utopian-food-blog-db --user=bloguser
```

### 3. パスワードを入力

プロンプトが表示されたら、Cloud SQLインスタンス作成時に設定したパスワードを入力：

```
Allowlisting your IP for incoming connection for 5 minutes...done.
Connecting to database with SQL user [bloguser].Enter password:
```

パスワードを入力すると、MySQLプロンプト（`mysql>`）が表示されます。

### 4. 接続後にデータベースを選択

MySQLプロンプトが表示されたら、以下のコマンドでデータベースを選択：

```
USE blogpost;
```

### 5. テーブルを作成（マイグレーション実行）

MySQLプロンプトで以下のSQLコマンドを実行：  
（各SQLコマンドをひとつづつ実行）

```sql
-- テーブルを作成
CREATE TABLE posted (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    contents TEXT NOT NULL,
    create_at DATE
);

-- Alembicのバージョン管理テーブルを作成
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- 現在のマイグレーションバージョンを記録
INSERT INTO alembic_version (version_num) VALUES ('47d32b838e67');
```

### 6. 確認

テーブルが正しく作成されたか確認：

```sql
-- テーブル一覧を表示
SHOW TABLES;

-- postedテーブルの構造を確認
DESCRIBE posted;

-- データを確認（空のはず）
SELECT * FROM posted;
```

### 7. 終了

```sql
-- MySQLから切断
exit;
```

### 注意点

1. **接続は5分間有効**：Cloud Shellからの接続は、自動的にIPアドレスが一時的に許可リストに追加され、5分間有効です
2. **プロジェクトIDの確認**：別のプロジェクトを操作している場合は、`gcloud config set project PROJECT_ID`で切り替え
3. **パスワードを忘れた場合**：Cloud Consoleから、または`gcloud sql users set-password`でリセット可能

## 3. 接続文字列の取得

### MySQL の場合（本プロジェクトで使用）

```
mysql+pymysql://bloguser:YOUR_SECURE_PASSWORD@/blogpost?unix_socket=/cloudsql/PROJECT_ID:asia-northeast1:utopian-food-blog-db
```

**PROJECT_ID** を実際の Google Cloud プロジェクトIDに置き換えてください。

## 4. 必要なパッケージの追加

`requirements.txt` には以下が既に追加されています：

### MySQL を使用する場合（本プロジェクトで使用）

```txt
pymysql>=1.1.0
cryptography>=41.0.7
```

## 5. Secret Manager での機密情報の管理（推奨）

### Secret Manager を有効化

```bash
gcloud services enable secretmanager.googleapis.com
```

### シークレットを作成

```bash
# データベース接続文字列（MySQL）
echo -n "mysql+pymysql://bloguser:YOUR_PASSWORD@/blogpost?unix_socket=/cloudsql/PROJECT_ID:asia-northeast1:utopian-food-blog-db" | gcloud secrets create utopian-blog-db-connection --data-file=-

# SECRET_KEY（ランダムな文字列を生成）
python3 -c "import secrets; print(secrets.token_hex(32))" | gcloud secrets create utopian-blog-secret-key --data-file=-

# ブログアプリログインユーザー名
echo -n "your_login_name" | gcloud secrets create utopian-blog-admin-username --data-file=-

# ブログアプリパスワード
echo -n "your_login_password" | gcloud secrets create utopian-blog-admin-password --data-file=-
```

## 6. Cloud Buildを使用してデプロイ

Secret Manager から参照しながらデプロイする。プロジェクトのルートディレクトリで以下を実行：

```bash
gcloud run deploy utopian-food-blog \
    --source . \
    --platform managed \
    --region asia-northeast1 \
    --allow-unauthenticated \
    --add-cloudsql-instances PROJECT_ID:asia-northeast1:utopian-food-blog-db \
    --set-secrets "GCLOUD_DB_CONNECTION=utopian-blog-db-connection:latest,SECRET_KEY=utopian-blog-secret-key:latest,ADMIN_PASSWORD=utopian-blog-admin-password:latest,ADMIN_USERNAME=utopian-blog-admin-username:latest"
```

### 💡 簡単デプロイ：スクリプトを使用

毎回長いコマンドを入力する代わりに、`deploy.sh` という名前のスクリプトファイルを作って実行してもよいです：  
`chmod +x deploy.sh`を忘れずに。

（例）
```bash
#!/bin/bash

# Cloud Run デプロイスクリプト
# 使い方: ./deploy.sh

set -e

# ========== 設定値（ここを編集してください） ==========
PROJECT_ID=""
SERVICE_NAME=""
REGION=""
DB_INSTANCE_NAME=""

# Secret Manager のシークレット名
SECRET_DB_CONNECTION=""
SECRET_KEY=""
SECRET_ADMIN_PASSWORD=""
SECRET_ADMIN_USERNAME=""
# ====================================================

# デプロイコマンド実行
gcloud run deploy ${SERVICE_NAME} \
    --source . \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --add-cloudsql-instances ${PROJECT_ID}:${REGION}:${DB_INSTANCE_NAME} \
    --set-secrets "GCLOUD_DB_CONNECTION=${SECRET_DB_CONNECTION}:latest,SECRET_KEY=${SECRET_KEY}:latest,ADMIN_PASSWORD=${SECRET_ADMIN_PASSWORD}:latest,ADMIN_USERNAME=${SECRET_ADMIN_USERNAME}:latest" \
    --project ${PROJECT_ID}
```

## 7. サービスアカウントに特定の権限（ロール）のみ紐付けるバージョン（オプショナル）

### 方法1：gcloudコマンドで一括設定（推奨）

まず、プロジェクト番号を取得：

```bash
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

echo "サービスアカウント: ${SERVICE_ACCOUNT}"
```

すでに編集者のロールがアタッチされている場合は、セキュリティ的にまずこの巨大権限を削除してから、以下の最小権限をひとつづつ付与していく。

```bash
# 編集者ロールを削除（巨大権限の削除）
gcloud projects remove-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/editor"
```

必要な5つの権限を付与：

```bash
# 1. Secret Manager のシークレットアクセサー
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor"

# 2. Storage オブジェクト閲覧者（コンテナビルド時に使用）
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/storage.objectViewer"

# 3. Artifact Registry 書き込み（コンテナイメージ保存用）
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/artifactregistry.writer"

# 4. Cloud SQL クライアント
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/cloudsql.client"

# 5. ログ書き込み（エラーログ確認用）
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/logging.logWriter"
```

### 方法2：ブラウザで手動設定

ブラウザで該当プロジェクト上でサービスアカウントページを開き、まず「編集者」のロールを削除してから、`default compute service account`に以下のロールを追加：
- 「Secret Managerのシークレットアクセサー」
- 「Storage オブジェクト閲覧者」
- 「Artifact Registry 書き込み」
- 「Cloud SQL クライアント」
- 「ログ書き込み」

### 🔐 権限の説明

| ロール | 説明 |
|--------|------|
| `roles/secretmanager.secretAccessor` | Secret Managerに保存されたシークレット（パスワードや接続文字列など）を読み取る権限 |
| `roles/storage.objectViewer` | Cloud Storageからオブジェクトを読み取る権限（コンテナビルド時に必要） |
| `roles/artifactregistry.writer` | Artifact Registryにコンテナイメージを書き込む権限 |
| `roles/cloudsql.client` | Cloud SQLインスタンスへの接続権限 |
| `roles/logging.logWriter` | Cloud Loggingへのログ書き込み権限（デバッグ・監視用） |

- **対象サービスアカウント**: `PROJECT_NUMBER-compute@developer.gserviceaccount.com`（Compute Engineのデフォルトサービスアカウント）
- **スコープ**: プロジェクト全体に付与

### 💡 補足

このサービスアカウント（`*-compute@developer.gserviceaccount.com`）は、Google Cloudのデフォルトサービスアカウントで、Cloud Runなどのサービスが使用します。今回のように、Secret Managerなどの他のサービスにアクセスする場合は、明示的に権限を付与する必要があります。（編集者ロールがある場合はこれだけでOKだが、権限が大き過ぎるので注意）

## 8. 動作確認

### 環境変数が正しく設定されているか確認

```bash
gcloud run services describe utopian-food-blog \
    --region asia-northeast1 \
    --format "value(spec.template.spec.containers[0].env)"
```

### ログの確認

```bash
gcloud run logs read utopian-food-blog --region asia-northeast1
```

## 基本的なDevOps方針と改善点
- `requirements.txt`の中身やappディレクトリ内のコードを変えてデプロイするごとに、しっかりと変更点が反映されて自動デプロイしてくれる。
- しかし現時点でイメージキャッシュが全く効かないので毎回時間がかかる。（Cloud Buildのyaml設定ファイル等で制御できるらしいが、めんどくさいのでスキップ！！）
- Cloudflareプラットフォームでのデプロイ作業に慣れた後で、今回はじめてGoogleで「Workersからデータベース連携」のようなことを試したら、めんどくさ過ぎてビビった笑（いつまでたってもAPP開発に専念できない病）

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
gcloud sql instances patch utopian-food-blog-db --activation-policy=NEVER
```

## Google Cloud 認証の仕組み（勉強用）

### 認証方式の概要

Google Cloudでは、**誰が・どこで・何を**するかによって異なる認証方式が使用されます。

### 3つの主要な認証フロー

#### 1. ローカルPCからのデプロイ操作

```bash
gcloud auth login
gcloud run deploy ...
```

- **認証方式**: OAuth 2.0トークンベース
- **トークンの保存場所**: `~/.config/gcloud/`（このプロジェクト外のあなたのローカルPCホームディレクトリ以下の設定ファイル内）
- **仕組み**:
  - ブラウザでGoogleアカウントにログイン
  - **アクセストークン**（短時間有効、通常1時間）と**リフレッシュトークン**（長期間有効）を取得
  - ローカルに保存されたトークンを使ってGCP APIにリクエスト
  - トークン期限切れ時は自動的に更新
- **JSONキー**: 不要 ✅

#### 2. Cloud Build でのコンテナビルド（GCP内部）

```
gcloud run deploy 実行
  ↓
Cloud Build が裏側で起動
  ↓
Dockerイメージをビルド
  ↓
Artifact Registry に保存
```

- **認証方式**: GCPメタデータサーバー経由
- **使用するサービスアカウント**: Default Compute Service Account
- **必要な権限**:
  - `Artifact Registry Writer` - ビルドしたイメージを保存
  - `Storage Object Viewer` - ビルド時の一時ファイルにアクセス
  - `Secret Manager Secret Accessor` - シークレットを取得（必要な場合）
- **JSONキー**: 不要（メタデータサーバーから自動取得）✅

**メタデータサーバーとは**:
```bash
# GCP内部のサービスから実行すると動作する特別なエンドポイント
curl "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" \
  -H "Metadata-Flavor: Google"
# → アクセストークンが自動取得される
```

#### 3. Cloud Run 上のアプリ実行時（GCP内部）

```
デプロイされたFlaskアプリ
  ↓
Cloud SQL、Storage等にアクセス
```

- **認証方式**: GCPメタデータサーバー経由
- **使用するサービスアカウント**: Default Compute Service Account
- **必要な権限**:
  - `Cloud SQL Client` - データベースに接続
  - `Secret Manager Secret Accessor` - シークレットを取得
  - `Cloud Logging Writer` - ログを出力（任意）
- **JSONキー**: 不要（メタデータサーバーから自動取得）✅

### サービスアカウントのJSONキーファイル

#### JSONキーが不要な場合（通常の開発・本番運用）

| 環境 | 認証方法 | JSONキー |
|------|---------|---------|
| ローカルPC | `gcloud auth login` | 不要 ✅ |
| Cloud Build | メタデータサーバー | 不要 ✅ |
| Cloud Run | メタデータサーバー | 不要 ✅ |
| Compute Engine | メタデータサーバー | 不要 ✅ |

#### JSONキーが必要な場合

| 環境 | 理由 | JSONキー |
|------|------|---------|
| GitHub Actions | GCP外部からのデプロイ | 必要 ⚠️ |
| CI/CD（外部） | GCP外部からのデプロイ | 必要 ⚠️ |
| 他社クラウド | GCP外部からのアクセス | 必要 ⚠️ |
| オンプレミス | GCP外部からのアクセス | 必要 ⚠️ |

### 重要なポイント

1. **`gcloud auth login` = ユーザー認証**
   - あなた自身のGoogleアカウントで認証
   - ローカルPCからGCP操作を行う権限

2. **Default Compute Service Account = アプリ認証**
   - GCP内部で動作するサービス（Cloud Build、Cloud Run等）の認証
   - 各種リソースへのアクセス権限が必要

3. **メタデータサーバー = GCP内部の自動認証**
   - GCP内部で動作するサービスは自動的に認証情報を取得
   - JSONキーファイル不要

4. **JSONキー = GCP外部からの認証**
   - GitHub Actions等、GCP外部から操作する場合のみ必要
   - 通常の開発・運用では不要

### 確認コマンド

```bash
# 現在の認証情報を確認
gcloud auth list

# 現在のアクセストークンを表示
gcloud auth print-access-token

# プロジェクトとアカウントの設定を確認
gcloud config list

# サービスアカウントの一覧を表示
gcloud iam service-accounts list

# Cloud Run サービスの環境変数とサービスアカウントを確認
gcloud run services describe utopian-food-blog \
    --region asia-northeast1 \
    --format "value(spec.template.spec.serviceAccountName)"
```

## 便利SQLコマンド
`gcloud sql connect utopian-food-blog-db --user=bloguser`でcloud shellからログインして、`USE blogpost;`でデータベースを選択後、

- すべてのテーブルを表示 : `SHOW TABLES;`
- すべての投稿内容（レコード）を表示 : `SELECT * FROM posted;`
- データベース登録済みのすべてのユーザーを表示 : `SELECT user, host FROM mysql.user;`
- bloguserに与えられている権限を表示 : `SHOW GRANTS FOR bloguser@;`

1. ポイントは`gcloud sql users create`によってユーザーを作成しているので自動ですべてのデータベースに対して操作の権限が最初から与えられている。
2. Cloud RunからのMySQL接続方法はUnixソケット経由を使用している。（Unixソケット経由の接続では、MySQLは接続元を localhost として認識する。よってホスト名が空欄、つまりbloguser@になっていてもよい）

## Cloud SQLのアクセス制御の仕組み

### パブリックIPがある場合のセキュリティ

Cloud SQLインスタンスにパブリックIPが割り当てられていても、**承認済みネットワーク（Authorized Networks）**の設定によってアクセス制御されます。

```
パブリックIPあり = 誰でもアクセス可能 ❌ 間違い

パブリックIPあり + 承認済みネットワーク = アクセス制御 ✅ 正解
```

### デフォルトの動作

```bash
gcloud sql instances create utopian-food-blog-db \
  --database-version=MYSQL_8_0 \
  --tier=db-f1-micro \
  --region=asia-northeast1
```

このコマンドでインスタンスを作成した場合：

| 項目 | 状態 |
|-----|-----|
| パブリックIP | ✅ 割り当てられる |
| 承認済みネットワーク | 🔒 **空（デフォルト）** |
| 外部からの直接アクセス | ❌ **拒否される** |
| `gcloud sql connect`の使用 | ✅ **可能**（一時的に承認） |
| Cloud Runからの接続 | ✅ **可能**（Unixソケット経由） |

### セキュリティの仕組み

#### 1. **通常の外部アクセス**（承認済みネットワークなし）

```bash
# 承認済みネットワークに何も設定していない状態
mysql -h <PUBLIC_IP> -u bloguser -p

# 結果
ERROR 2003 (HY000): Can't connect to MySQL server on '<PUBLIC_IP>'
(Connection timed out)
```

**✅ セキュリティ的に安全** - 拒否される

#### 2. **`gcloud sql connect`を使用**

```bash
gcloud sql connect utopian-food-blog-db --user=bloguser

# 内部的な動作：
# 1. Cloud ShellのIPアドレスを取得（例：34.85.123.45）
# 2. 承認済みネットワークに一時追加：34.85.123.45/32
# 3. MySQL接続を確立
# 4. 5分後に自動削除
```

**✅ セキュリティ的に安全** - 5分間の制限付きアクセス

#### 3. **もし誰かが承認済みネットワークに `0.0.0.0/0` を追加したら**

```bash
# これをやってしまうと危険！
gcloud sql instances patch utopian-food-blog-db \
  --authorized-networks=0.0.0.0/0

# この状態だと、世界中の誰でもアクセス可能に！
```

**❌ セキュリティ的に危険** - 全世界に公開

### Cloud Runからの接続（Unixソケット経由）

```python
# Unixソケット経由の接続（承認済みネットワークの設定に関係なく動作）
DATABASE_URI = "mysql+pymysql://bloguser:pass@/blogpost?unix_socket=/cloudsql/..."
```

- 承認済みネットワークの設定に**影響されない**
- VPC内部の接続として扱われる
- **常に安全にアクセス可能**