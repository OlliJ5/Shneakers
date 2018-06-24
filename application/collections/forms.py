from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

class CollectionForm(FlaskForm):
    name = StringField("Collection name")
    description = TextAreaField("Description")

    class Meta:
        csrf = False