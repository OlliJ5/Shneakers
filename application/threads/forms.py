from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ThreadForm(FlaskForm):
    title = StringField("Thread title", [validators.DataRequired(), validators.Length(min=3)])
    text = StringField("Thread text", [validators.DataRequired(), validators.Length(min=10)])

    class Meta:
        csrf = False

class ThreadEditForm(FlaskForm):
    text = StringField("Muokkaa tekstiä ", [validators.DataRequired(), validators.Length(min=10)])

    class Meta:
        csrf = False