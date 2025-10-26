from flask import Blueprint, render_template, request

users_bp = Blueprint(
    "users", __name__,
    template_folder="templates"
)

@users_bp.route("/hi/<name>")
def hi_user(name):
    age = request.args.get("age", 25)
    role = request.args.get("role", "User")
    return render_template("users/hi.html", name=name, age=age, role=role)

@users_bp.route("/user")
def user_page():
    return render_template("users/user_page.html")

@users_bp.route("/admin")
def admin_page():
    return render_template("users/admin_page.html")