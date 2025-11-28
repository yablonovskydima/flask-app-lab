from flask import Blueprint, render_template, redirect, url_for, session, flash, request, make_response
from app.auth.login_forms import LoginForm
from app.auth.register_forms import RegisterForm
from app.users.models import User
from app import bcrypt
from app import db

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate():
        user = form.user

        session["username"] = user.username
        session["email"] = user.email
        session["user_id"] = user.id

        flash("Login successful!", "success")
        return redirect(url_for("auth.account"))

    return render_template("auth/login.html", form=form)

@auth_bp.route("/account")
def account():
    if "username" not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for("auth.login"))

    username = session.get("username")
    email = session.get("email")
    user_id = session.get("user_id")

    users = User.query.all()
    users_count = len(users)

    return render_template(
        "auth/account.html",
        username=username,
        email=email,
        user_id=user_id,
        users=users,
        users_count=users_count
    )



@auth_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("auth.login"))

    username = session["username"]
    theme = request.cookies.get("theme", "light")

    if request.method == "POST":
        action = request.form.get("action")
        resp = make_response(redirect(url_for("auth.profile")))

        if action == "add":
            key = request.form.get("key")
            value = request.form.get("value")
            expires_raw = request.form.get("expires", "").strip()
            expires = int(expires_raw) if expires_raw.isdigit() else None

            if key and value:
                if expires:
                    resp.set_cookie(key, value, max_age=expires)
                else:
                    resp.set_cookie(key, value)
                flash(f"Cookie '{key}' added successfully!", "success")
            else:
                flash("Please provide both key and value!", "error")

        elif action == "delete_one":
            key = request.form.get("key")
            if key:
                resp.delete_cookie(key)
                flash(f"Cookie '{key}' deleted successfully!", "success")
            else:
                flash("Please provide a cookie key to delete!", "error")

        elif action == "delete_all":
            for key in request.cookies.keys():
                resp.delete_cookie(key)
            flash("All cookies deleted successfully!", "success")

        return resp

    cookies = request.cookies.items()
    return render_template("auth/profile.html", username=username, cookies=cookies, theme=theme)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/set_theme/<theme>")
def set_theme(theme):
    if theme not in ["light", "dark"]:
        flash("Invalid theme selected!", "error")
        return redirect(url_for("auth.profile"))

    resp = make_response(redirect(url_for("auth.profile")))
    resp.set_cookie("theme", theme, max_age=60 * 60 * 24 * 30)
    flash(f"Theme changed to {theme} mode!", "info")
    return resp


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("auth.login"))
