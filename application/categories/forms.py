from flask_wtf import FlaskForm
from wtforms import StringField, validators
from application.categories.models import Category
from application.validators.unique import Unique

class CategoryForm(FlaskForm):
    name = StringField("Category name", [validators.Required(), Unique(Category, Category.name, "Category already exists")])

    class Meta:
        csrf = False