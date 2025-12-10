from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app import db
from app.institutions.models import InstitutionType, EducationInstitution
from app.users.models import User


class EducationInstitutionForm(FlaskForm):
    name = StringField(
        'Institution Name',
        validators=[DataRequired(), Length(min=3, max=150)]
    )

    address = StringField(
        'Address',
        validators=[DataRequired(), Length(min=5, max=255)]
    )

    description = TextAreaField(
        'Description',
        validators=[Length(max=500)]
    )

    type_id = SelectField(
        'Institution Type',
        coerce=int,
        validators=[DataRequired()]
    )

    author_id = SelectField(
        'Author',
        coerce=int,
        validators=[DataRequired()]
    )

    submit = SubmitField("Create")


    def set_type_choices(self):
        self.type_id.choices = [
            (t.id, t.type_name) for t in InstitutionType.query.order_by(InstitutionType.type_name).all()
        ]

    def set_author_choices(self):
        self.author_id.choices = [
            (u.id, u.username) for u in User.query.order_by(User.username).all()
        ]
