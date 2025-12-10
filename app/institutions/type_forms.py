from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class InstitutionTypeForm(FlaskForm):
    type_name = StringField(
        'Type Name',
        validators=[DataRequired(message="Type name is required"), Length(min=2, max=100)]
    )
    description = TextAreaField(
        'Description',
        validators=[Length(max=500)]
    )
    submit = SubmitField('Create')
