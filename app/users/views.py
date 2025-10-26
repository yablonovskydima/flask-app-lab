from flask import Blueprint, render_template

users_bp = Blueprint(
    "users", __name__,
    template_folder="templates"
)

@users_bp.route("/<name>")
def hi_user(name):
    return render_template("users/hi.html", name=name)
