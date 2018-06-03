from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
  
    class Meta:
        csrf = False

class UserForm(FlaskForm):
    name = StringField("Name", [validators.DataRequired(), validators.Length(min=2)])
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=3)])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=5)])

    class Meta:
        csrf = False