from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

class CollectionForm(FlaskForm):
    name = StringField("Collection name", [validators.Required(), validators.Length(min=1, max=30)])
    description = TextAreaField("Description")

    class Meta:
        csrf = False