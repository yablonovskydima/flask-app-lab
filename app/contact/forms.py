from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional

class ContactForm(FlaskForm):
    """Contact form for sending messages to site administration."""

    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Name is required."),
            Length(min=4, max=50, message="Name must be between 4 and 50 characters long.")
        ],
        render_kw={"placeholder": "Your full name"}
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ],
        render_kw={"placeholder": "you@example.com"}
    )

    phone = StringField(
        "Phone",
        validators=[
            Optional(),
            Regexp(r'^\+380\d{9}$', message="Phone number must match +380XXXXXXXXX format.")
        ],
        render_kw={"placeholder": "+380XXXXXXXXX (optional)"}
    )

    subject = SelectField(
        "Subject",
        choices=[
            ("", "Select a subject"),
            ("general", "General question"),
            ("support", "Support request"),
            ("sales", "Sales inquiry"),
            ("feedback", "Feedback")
        ],
        validators=[DataRequired(message="Please select a subject.")]
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Message is required."),
            Length(max=500, message="Message must not exceed 500 characters.")
        ],
        render_kw={"rows": 5, "placeholder": "Write your message here..."}
    )

    submit = SubmitField("Send Message")
