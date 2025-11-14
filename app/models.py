from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# dbインスタンスを直接作成（ファクトリパターン用）
db = SQLAlchemy()


class Blogpost(db.Model):
    __tablename__ = "posted"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.Date, default=datetime.today())
