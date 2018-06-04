from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

class ThreadForm(FlaskForm):
    title = StringField("Thread title", [validators.DataRequired(), validators.Length(min=3)])
    text = TextAreaField("Thread text", [validators.DataRequired(), validators.Length(min=10)], render_kw={"rows":6, "cols": 40})

    class Meta:
        csrf = False

class ThreadEditForm(FlaskForm):
    text = TextAreaField("Muokkaa tekstiä ", [validators.DataRequired(), validators.Length(min=10)], render_kw={"rows":6, "cols": 40})

    class Meta:
        csrf = False