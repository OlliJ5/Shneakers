from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, validators

class ShoeForm(FlaskForm):
    model = StringField("Shoe model")
    brand = StringField("Brand of the shoe")
    release_year = IntegerField("Release year")
    collection = SelectField("Collection", coerce=int)

    class Meta:
        csrf = False