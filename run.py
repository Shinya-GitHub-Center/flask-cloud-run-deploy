"""
Flask application entry point
アプリケーションのエントリーポイント
"""
from app.main import app

if __name__ == "__main__":
    app.run(debug=True)
