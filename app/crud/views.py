from flask import Blueprint, render_template, url_for, redirect, session, current_app
from app.crud import forms
from app import models
from app.models import db
from sqlalchemy import select

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/crud/static",
)


@crud.route("/admincreate", methods=["GET", "POST"])
def login():
    form = forms.AdminForm()

    session["logged_in"] = False

    if form.validate_on_submit():
        if (
            form.username.data != current_app.config["USERNAME"]
            or form.password.data != current_app.config["PASSWORD"]
        ):
            return render_template("login.html", form=form)
        else:
            session["logged_in"] = True
            return redirect(url_for("crud.article"))

    return render_template("login.html", form=form)


@crud.route("/post", methods=["GET", "POST"])
def article():
    if not session.get("logged_in"):
        return redirect(url_for("crud.login"))

    form_art = forms.ArticlePost()

    if form_art.validate_on_submit():
        mypost = models.Blogpost(
            title=form_art.post_title.data,
            contents=form_art.post_contents.data,
        )
        db.session.add(mypost)
        db.session.commit()
        session.pop("logged_in", None)
        return redirect(url_for("index"))

    return render_template("post.html", form=form_art)


@crud.route("/admindelete", methods=["GET", "POST"])
def login_del():
    form = forms.AdminForm()
    session["logged_in"] = False
    if form.validate_on_submit():
        if (
            form.username.data != current_app.config["USERNAME"]
            or form.password.data != current_app.config["PASSWORD"]
        ):
            return render_template("login_delete.html", form=form)
        else:
            session["logged_in"] = True
            return redirect(url_for("crud.delete_entry"))
    return render_template("login_delete.html", form=form)


@crud.route("/delete", methods=["GET", "POST"])
def delete_entry():
    if not session.get("logged_in"):
        return redirect(url_for("crud.login_del"))
    stmt = select(models.Blogpost).order_by(models.Blogpost.id.desc())
    entries = db.session.execute(stmt).scalars().all()
    return render_template("delete.html", entries=entries)


@crud.route("/delete/<int:id>")
def delete(id):
    entry = db.session.get(models.Blogpost, id)
    db.session.delete(entry)
    db.session.commit()
    session.pop("logged_in", None)
    return redirect(url_for("index"))
