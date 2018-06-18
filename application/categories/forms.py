from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField

class CategoryForm(FlaskForm):
    name = StringField("Category name")

    class Meta:
        csrf = False