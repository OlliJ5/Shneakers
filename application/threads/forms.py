from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators

class ThreadForm(FlaskForm):
    title = StringField("Thread title", validators=[validators.DataRequired(), validators.Length(min=3, max=40)])
    text = TextAreaField("Thread text", validators=[validators.DataRequired(), validators.Length(min=10, max=300)], render_kw={"rows":6, "cols": 40})
    category = SelectField("Category", coerce=int)

    class Meta:
        csrf = False

class ThreadEditForm(FlaskForm):
    text = TextAreaField("Edit thread's content ", [validators.DataRequired(), validators.Length(min=10)], render_kw={"rows":6, "cols": 40})

    class Meta:
        csrf = False