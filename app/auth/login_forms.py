from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from app.users.models import User
from app import bcrypt


class LoginForm(FlaskForm):
    username = StringField("Username or Email", validators=[
        DataRequired(message="Username or Email is required.")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required."),
        Length(min=4, max=50)
    ])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

    def validate(self):
        rv = super().validate()
        if not rv:
            return False

        user = User.query.filter(
            (User.username == self.username.data) |
            (User.email == self.username.data)
        ).first()

        if not user:
            self.username.errors.append("User not found.")
            return False

        if not bcrypt.check_password_hash(user.password, self.password.data):
            self.password.errors.append("Incorrect password.")
            return False

        self.user = user
        return True
