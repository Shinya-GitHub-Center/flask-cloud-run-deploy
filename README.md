# About

こちらはFlaskアプリの勉強用リポジトリです。  
固定された管理人専用のログインIDでログインして、管理人のみが投稿・削除等ができるシンプルなブログアプリです。データベースを利用したSSR動的アプリです。

データベースなしの一番簡単なバージョン（簡単なボタンクリックによる値インクリメントのテストアプリ）で勉強したい場合は、別途[こちら](https://github.com/Shinya-GitHub-Center/flask-cloud-run-deploy/tree/v1-only-button-click)を参照してください。

- まずFlaskのシンプルな機能をローカルサーバー上で確認する
- 次に本番環境できちんと動作するか確認する（シンプルでほぼ無料で確認できるためCloud Runを利用する）

1. uv（Pythonパッケージマネージャー＆仮想環境作成ツール）があなたのローカルPCにインストールされていることが前提となります。このプロジェクトではpythonのv3.12を使用するので、事前にグローバルでuvインストールしておくとよいですね。
2. まずこのリポジトリをダウンロード後、`uv sync`コマンドにて初期化を行ってください（必要パッケージがこのプロジェクト以下の仮想環境にインストールされます）
3. VSCodeやCursorを使用して自動でPythonインタープリタが切り替わらない場合は、手動で`./.venv/bin/python`に切り替えてください。（このプロジェクト内のパッケージおよびPythonを使用するため）
4. `uv run flask --app app.main:app db init`でデータベース初期化（ローカル環境）
5. `uv run flask --app app.main:app db migrate`でマイグレーションファイル作成（ローカル環境）
6. `uv run flask --app app.main:app db upgrade`でデータベースにデータ構造を注入（ローカル環境）

Notice: Zipでダウンロードした場合は各自でGit初期化してください。また、勉強用・テスト用プロジェクトなので、特に`uv.lock`はこのリポジトリに含めていませんので、常に最新のパッケージ・モジュールを使用して勉強してください。

## 開発サーバーの起動方法
- `__init__.py`を実行しない、つまりシンプルなスクリプトとして起動する場合は、プロジェクトルートにて : `uv run app/main.py`
- `__init__.py`を実行する、つまりモジュールとして実行する場合は、プロジェクトルートにて : `uv run -m app.main`

以上どちらの場合でも（スクリプトとして実行orモジュールとして実行）、実行対象として起動するので、`__name__`は`__main__`になる。

（本番環境でgunicornコマンドで起動する場合は、パラメータにパーツとして対象オブジェクトを渡しているだけなので、`__main__`にはならない）

# ローカルでのDocker動作確認

Cloud Runにデプロイする前に、ローカルでDockerイメージをビルドして動作確認できます。

## 前提条件

Dockerがインストールされていること：
```bash
# Dockerのバージョン確認
docker --version
```

Dockerがインストールされていない場合は、[Docker公式サイト](https://docs.docker.com/get-docker/)からインストールしてください。

## 手順

### 1. Dockerイメージのビルド

プロジェクトのルートディレクトリで以下を実行：

```bash
docker build -t flask-cloud-run-deploy .
```

**パラメータの説明：**
- `-t flask-cloud-run-deploy`: イメージに`flask-cloud-run-deploy`という名前（タグ）を付ける
- `.`: 現在のディレクトリをビルドコンテキストとして使用

ビルドが成功すると、以下のようなメッセージが表示されます：
```
Successfully built xxxxxxxxxxxxx
Successfully tagged flask-cloud-run-deploy:latest
```

### 2. コンテナの起動

```bash
docker run -p 8080:8080 flask-cloud-run-deploy
```

**パラメータの説明：**
- `-p 8080:8080`: ホストのポート8080をコンテナのポート8080にマッピング
- `flask-cloud-run-deploy`: 起動するイメージ名

起動すると、gunicornのログが表示されます：
```
[2025-11-05 12:34:56 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-11-05 12:34:56 +0000] [1] [INFO] Listening at: http://0.0.0.0:8080 (1)
```

### 3. ブラウザでアクセス

ブラウザで以下のURLを開く：
```
http://localhost:8080
```

ボタンをクリックして、カウンターが増えることを確認してください！

### 4. コンテナの停止

ターミナルで `Ctrl + C` を押してコンテナを停止します。

## 便利なコマンド

### バックグラウンドで起動

```bash
# -d オプションでバックグラウンド実行
docker run -d -p 8080:8080 --name flask-app flask-cloud-run-deploy

# ログを確認
docker logs flask-app

# ログをリアルタイムで確認（フォロー）
docker logs -f flask-app

# コンテナを停止
docker stop flask-app

# コンテナを削除
docker rm flask-app
```

### イメージの確認

```bash
# ビルドしたイメージの一覧を表示
docker images | grep flask-cloud-run-deploy
```

### イメージの削除

```bash
docker rmi flask-cloud-run-deploy
```

### コンテナ内に入ってデバッグ

```bash
# コンテナを起動してシェルに入る
docker run -it --rm flask-cloud-run-deploy /bin/bash

# または実行中のコンテナに入る
docker exec -it flask-app /bin/bash
```

### コンテナ内のファイル構造を確認

```bash
docker run --rm flask-cloud-run-deploy ls -la /home/appuser
```

## Dockerのビルドキャッシュの仕組み

Dockerは効率的なビルドのために**レイヤーキャッシュ**を使用します。このプロジェクトのDockerfileは、開発効率を最大化するように設計されています。

### Dockerfileの構造とキャッシュ戦略

```dockerfile
# 1. 依存関係ファイルを先にコピー（変更頻度: 低）
COPY --chown=appuser:appuser requirements.txt .

# 2. 依存関係をインストール（時間がかかる処理）
RUN pip install --no-cache-dir -r requirements.txt

# 3. アプリケーションコードをコピー（変更頻度: 高）
COPY --chown=appuser:appuser app/ ./app/
```

**この順序が重要な理由：**
- 変更頻度が低いもの（requirements.txt）を先に処理
- 変更頻度が高いもの（app/）を後に処理
- これにより、コード変更時にpip installを再実行する必要がなくなる

### ケース1: app/の中身を変更した場合

```bash
# app/main.pyを編集してから再ビルド
docker build -t flask-cloud-run-deploy .
```

**動作：**
```
Step 7: COPY requirements.txt .
 ---> Using cache ✅（キャッシュ利用）

Step 8: RUN pip install -r requirements.txt
 ---> Using cache ✅（キャッシュ利用・高速！）

Step 9: COPY app/ ./app/
 ---> 7a8b9c0d1e2f ✨（変更を自動検知して再実行）
```

**結果：**
- ✅ 変更されたコードが自動的に新しいイメージに含まれる
- ✅ pip installはスキップされるため、ビルドが**非常に高速**
- ✅ 開発サイクルが効率的（数秒でビルド完了）

### ケース2: requirements.txtにモジュールを追加した場合

```bash
# requirements.txtを編集（例: redis==5.0.0を追加）
docker build -t flask-cloud-run-deploy .
```

**動作：**
```
Step 7: COPY requirements.txt .
 ---> 1a2b3c4d5e6f ✨（ファイル変更を自動検知）

Step 8: RUN pip install -r requirements.txt
 ---> Running in ... ✨（再実行される）
Collecting Flask==3.1.2
Collecting gunicorn==23.0.0
Collecting redis==5.0.0 ← 新規追加
Successfully installed Flask-3.1.2 gunicorn-23.0.0 redis-5.0.0

Step 9: COPY app/ ./app/
 ---> Using cache ✅（app/に変更がなければキャッシュ）
```

**結果：**
- ✅ 追加されたモジュールが自動的にインストールされる
- ✅ 全ての依存関係が正しくインストールされる
- ✅ requirements.txtが「単一の真実の情報源」として機能

### ベストプラクティス

1. **開発中の効率的なワークフロー：**
   ```bash
   # コードを編集後
   ↓
   # 高速再ビルド（pip installはスキップ）
   docker build -t flask-cloud-run-deploy .
   
   # 即座にテスト
   docker run -p 8080:8080 flask-cloud-run-deploy
   ```

2. **依存関係を追加する場合：**
   ```bash
   # requirements.txtを編集
   echo "redis==5.0.0" >> requirements.txt
   
   # 再ビルド（新しいモジュールが自動インストール）
   docker build -t flask-cloud-run-deploy .
   ```

3. **完全にクリーンな状態からビルドする場合：**
   ```bash
   # キャッシュを使わず最初から再ビルド
   docker build --no-cache -t flask-cloud-run-deploy .
   ```

## トラブルシューティング

### ポートが既に使用されている

```bash
# エラー: Bind for 0.0.0.0:8080 failed: port is already allocated
# 別のポートを使用する：
docker run -p 8081:8080 flask-cloud-run-deploy
# → http://localhost:8081 でアクセス
```

### ビルドキャッシュをクリアして再ビルド

```bash
docker build --no-cache -t flask-cloud-run-deploy .
```

### 全てのコンテナとイメージをクリーンアップ

```bash
# 停止中の全コンテナを削除
docker container prune -f

# 未使用のイメージを削除
docker image prune -a -f
```

# デプロイ設定ファイルについて

このプロジェクトでは、効率的なビルドとデプロイのために2つの除外設定ファイルを使用しています。

## `.dockerignore` と `.gcloudignore` の違い

### それぞれの役割

| ファイル | 使用タイミング | 目的 | 影響範囲 |
|---------|--------------|------|---------|
| `.dockerignore` | Dockerイメージのビルド時 | イメージサイズの最適化 | 最終的なDockerイメージの中身 |
| `.gcloudignore` | `gcloud run deploy --source .` 実行時 | ネットワーク転送量の削減 | Cloud Buildへの送信内容 |

### ローカルでのDockerテスト

```bash
docker build -t flask-cloud-run-deploy .
docker run -p 8080:8080 flask-cloud-run-deploy
```

**使用されるファイル:**
- ✅ `.dockerignore` のみ
- ❌ `.gcloudignore` は使用されない

**動作:**
```
ソースコード → [.dockerignore適用] → Dockerイメージ
```

### Cloud Runへのデプロイ

```bash
gcloud run deploy flask-cloud-run-deploy --source .
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

これにより：
1. ✅ ローカルテストが効率的（`.dockerignore`）
2. ✅ デプロイが高速（`.gcloudignore`）
3. ✅ セキュリティが向上（機密情報の除外）
4. ✅ コスト削減（転送量とビルド時間の削減）

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

# Google Cloud Run デプロイ手順

このドキュメントでは、FlaskアプリをGoogle Cloud Runにデプロイする手順を説明します。

## 前提条件

1. Google Cloudアカウント
2. Google Cloud CLIのインストール（gcloud）
3. プロジェクトの作成と課金の有効化

## 初期セットアップ

### 1. Google Cloud CLIのインストール（未インストールの場合）

https://cloud.google.com/sdk/docs/install?hl=ja

（ubuntuの場合はパッケージ形式でインストールすること）

### 2. Google Cloudの初期設定およびログイン

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

## デプロイ方法

### 方法1: Cloud Buildを使用（推奨・最も簡単）

プロジェクトのルートディレクトリで以下を実行：

```bash
gcloud run deploy flask-cloud-run-deploy \
  --source . \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated
```

or

`gcloud run deploy flask-cloud-run-deploy --platform managed --region asia-northeast1 --allow-unauthenticated --source .`

**パラメータの説明：**
- `flask-cloud-run-deploy`: サービス名（任意に変更可能）
- `--source .`: 現在のディレクトリをソースとして使用
- `--region asia-northeast1`: 東京リージョン
- `--allow-unauthenticated`: 認証なしでアクセス可能（テストアプリの場合）

#### `--source .` の動作について

`--source .` を指定すると、以下の処理が自動的に実行されます：

1. **ローカルのDockerfileを自動検出**
   - プロジェクトルートの`Dockerfile`を自動的に発見
   - `.dockerignore`の除外ルールも適用される

2. **ソースコードをGoogle Cloud Buildに送信**
   - Dockerfile、requirements.txt、app/ などが転送される
   - `.dockerignore`で除外したファイル（.git/, .venv/など）は送信されない

3. **リモートビルド（Cloud Build上）**
   - Google Cloud上でDockerイメージをビルド
   - ローカルにDockerをインストールする必要なし
   - ローカルマシンのリソースを使わない

4. **自動デプロイ**
   - ビルドしたイメージを自動的にCloud Runにデプロイ
   - 全てのプロセスが1コマンドで完結

**メリット：**
- ✅ 最もシンプル（1コマンドで完結）
- ✅ ローカルでDockerをインストール・実行する必要なし
- ✅ Dockerfileを自動検出
- ✅ リモートビルドなのでローカルマシンへの負荷なし

### 方法2: Dockerイメージを手動でビルド＆デプロイ（未テスト）

```bash
# 1. プロジェクトIDを変数に設定
PROJECT_ID=$(gcloud config get-value project)

# 2. Dockerイメージをビルドしてプッシュ
gcloud builds submit --tag gcr.io/$PROJECT_ID/flask-cloud-run-deploy

# 3. Cloud Runにデプロイ
gcloud run deploy flask-cloud-run-deploy \
  --image gcr.io/$PROJECT_ID/flask-cloud-run-deploy \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated
```

## デプロイ後

デプロイが完了すると、以下のようなURLが表示されます：

```
Service URL: https://flask-cloud-run-deploy-xxxxxxxxxx-an.a.run.app
```

このURLにアクセスして、アプリが動作することを確認してください！

## 便利なコマンド

### サービスの一覧を表示

```bash
gcloud run services list
```

### ログの確認

```bash
gcloud run services logs read flask-cloud-run-deploy --region asia-northeast1
```

### サービスの詳細情報

```bash
gcloud run services describe flask-cloud-run-deploy --region asia-northeast1
```

### サービスの削除

```bash
gcloud run services delete flask-cloud-run-deploy --region asia-northeast1
```

## トラブルシューティング

### ポートの問題

Cloud Runは環境変数`PORT`を自動的に設定します。Dockerfileで正しく設定されているか確認してください。

### ログの確認

デプロイに失敗した場合、ログを確認：

```bash
gcloud run services logs read flask-cloud-run-deploy --region asia-northeast1 --limit 50
```

### 料金の確認

Cloud Runの料金は以下で確認できます：
- [Google Cloud Console](https://console.cloud.google.com/billing)

無料枠：
- 月に2百万リクエスト
- 360,000 vCPU秒/月
- 180,000 GiB秒/月

テストアプリなら、ほぼ無料で運用できます！

## その他のリージョン

日本以外のリージョンを使用する場合：

- `us-central1` (アイオワ)
- `us-east1` (サウスカロライナ)
- `europe-west1` (ベルギー)
- `asia-east1` (台湾)

## セキュリティ設定（オプション）

認証を必要とする場合：

```bash
gcloud run deploy flask-cloud-run-deploy \
  --source . \
  --platform managed \
  --region asia-northeast1
  # --allow-unauthenticated を削除
```

これで、Google アカウントでのログインが必要になります。
