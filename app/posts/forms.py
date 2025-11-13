from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired(message="Title is required"), Length(min=3, max=100)]
    )
    content = TextAreaField(
        'Content',
        validators=[DataRequired(message="Content is required"), Length(min=10)]
    )
    enabled = BooleanField('Enabled')
    posted = DateTimeLocalField(
        'Posted',
        format='%Y-%m-%dT%H:%M',
        default=datetime.utcnow,
        validators=[DataRequired(message="Publish date is required")]
    )
    category = SelectField(
        'Category',
        choices=[
            ('NEWS', 'News'),
            ('PUBLICATION', 'Publication'),
            ('TECH', 'Tech'),
            ('OTHER', 'Other')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
