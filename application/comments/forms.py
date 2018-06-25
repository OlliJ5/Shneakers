from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

class CommentForm(FlaskForm):
    text = TextAreaField("Write a comment", [validators.DataRequired(), validators.Length(min=1, max=100)])

    class Meta:
        csrf = False