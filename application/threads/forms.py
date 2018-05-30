from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ThreadForm(FlaskForm):
    title = StringField("Thread title", [validators.Length(min=3)])
    text = StringField("Thread text", [validators.Length(min=10)])

    class Meta:
        csrf = False