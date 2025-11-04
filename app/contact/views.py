from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from .forms import ContactForm
import os
import logging

contact_bp = Blueprint("contact", __name__, template_folder="templates")

LOG_FILE = os.path.join("logs", "contact.log")
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        logger.info(f"Contact form submitted: {name} ({email}), {phone}, {subject}, {message}")

        flash(f"Thank you, {name}! Your message has been successfully sent.", "success")
        return redirect(url_for("contact.contact"))

    elif request.method == "POST":
        flash("Please check the form fields and try again.", "danger")

    return render_template("contact/contact_page.html", form=form)
