from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.users.models import User
from flask_login import current_user


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])

    image = FileField(
        "Update Profile Picture",
        validators=[FileAllowed(['jpg', 'png', 'jpeg'])]
    )

    submit = SubmitField("Update")

    # --- VALIDATION ---
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email is already registered.")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is already taken.")

