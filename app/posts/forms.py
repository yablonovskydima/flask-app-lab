from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SelectMultipleField, SubmitField, DateTimeLocalField
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
    author = SelectField('Author', coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int)
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

    def set_author_choices(self):
        from app.users.models import User
        self.author.choices = [(u.id, u.username) for u in User.query.order_by(User.username).all()]

    def set_tag_choices(self):
        from app.posts.models import Tag
        self.tags.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name).all()]
