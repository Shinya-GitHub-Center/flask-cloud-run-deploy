import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select
from flask_paginate import Pagination, get_page_parameter

# Flask初期化
app = Flask(__name__)
app.config.from_pyfile("settings.py")

# DB初期化
db = SQLAlchemy()
db.init_app(app)

# モデルのインポート（DBの初期化後に行う）
from app import models

# Migrateの初期化（モデルのインポート後に行う）
basedir = os.path.dirname(os.path.dirname(__file__))
mgdir = basedir + "/db/migrations"
Migrate(app, db, directory=mgdir)


@app.route("/")
def index():
    stmt = select(models.Blogpost).order_by(models.Blogpost.id.desc())
    entries = db.session.execute(stmt).scalars().all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = entries[(page - 1) * 6 : page * 6]
    pagination = Pagination(
        page=page, total=len(entries), per_page=6, css_framework="bootstrap5"
    )
    return render_template("index.html", rows=res, pagination=pagination)


@app.route("/entries/<int:id>")
def show_entry(id):
    entry = db.session.get(models.Blogpost, id)
    return render_template("post_show.html", entry=entry)


from app.crud.views import crud

app.register_blueprint(crud)
