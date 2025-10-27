from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint("auth", __name__, template_folder="templates")

#example data
VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("auth.profile"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth_bp.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        flash("Please login to view your profile", "warning")
        return redirect(url_for("auth.login"))
    return render_template("auth/profile.html", user=user)


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You logged out", "info")
    return redirect(url_for("auth.login"))
