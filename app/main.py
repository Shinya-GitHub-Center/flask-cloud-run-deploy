import os
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select
from app import models
from flask import request
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config.from_pyfile("settings.py")

db = SQLAlchemy()
db.init_app(app)

basedir = os.path.dirname(os.path.dirname(__file__))
mgdir = basedir + "/db/migrations"
Migrate(app, db, directory=mgdir)


@app.route("/")
def index():
    stmt = select(models.Blogpost).order_by(models.Blogpost.id.desc())
    entries = db.session.execute(stmt).scalars().all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = entries[(page - 1) * 3 : page * 3]
    pagination = Pagination(page=page, total=len(entries), per_page=3)
    return render_template("index.html", rows=res, pagination=pagination)


@app.route("/entries/<int:id>")
def show_entry(id):
    entry = db.session.get(models.Blogpost, id)
    return render_template("post_show.html", entry=entry)


from app.crud.views import crud

app.register_blueprint(crud)
