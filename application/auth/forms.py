from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from application.auth.models import User
from application.validators.unique import Unique
  
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
  
    class Meta:
        csrf = False

class UserForm(FlaskForm):
    name = StringField("Name", [validators.DataRequired(), validators.Length(min=2)])
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=3), Unique(User, User.username, "Username already in use!")])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=5)])

    class Meta:
        csrf = False