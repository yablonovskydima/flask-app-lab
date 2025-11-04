from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField("Username or Email", validators=[
        DataRequired(message="Username or Email is required.")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required."),
        Length(min=4, max=10, message="Password must be between 4 and 10 characters long.")
    ])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")
