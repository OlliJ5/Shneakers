from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CommentForm(FlaskForm):
    text = StringField("Comment", [validators.DataRequired(), validators.Length(min=1)])

    class Meta:
        csrf = False