from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CommentForm(FlaskForm):
    text = StringField("Comment", [validators.Length(min=2)])

    class Meta:
        csrf = False