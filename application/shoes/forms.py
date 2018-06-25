from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, validators

class ShoeForm(FlaskForm):
    model = StringField("Shoe model", [validators.Required(), validators.Length(min=1, max=30)])
    brand = StringField("Brand of the shoe", [validators.Required(), validators.Length(min=1, max=30)])
    release_year = IntegerField("Release year", [validators.Required()])
    collection = SelectField("Collection", [validators.Required()], coerce=int)

    class Meta:
        csrf = False