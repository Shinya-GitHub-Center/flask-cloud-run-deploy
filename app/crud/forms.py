from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AdminForm(FlaskForm):
    username = StringField(
        "Admin Name", validators=[DataRequired(message="Required to fill out")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Required to fill out")]
    )
    submit = SubmitField(("Login"))


class ArticlePost(FlaskForm):
    post_title = StringField(
        "Title",
        validators=[
            DataRequired(message="Required to fill out"),
        ],
    )
    post_contents = TextAreaField(
        "Content",
        validators=[
            DataRequired(message="Required to fill out"),
        ],
    )
    submit = SubmitField(("Post"))
