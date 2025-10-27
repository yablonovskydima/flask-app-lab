from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response

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
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("auth.profile"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


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
    return render_template("auth/profile.html", username=username, cookies=cookies, theme=theme,)


@auth_bp.route("/set_theme/<theme>")
def set_theme(theme):
    if theme not in ["light", "dark"]:
        flash("Invalid theme selected!", "error")
        return redirect(url_for("auth.profile"))

    resp = make_response(redirect(url_for("auth.profile")))
    resp.set_cookie("theme", theme, max_age=60*60*24*30)
    flash(f"Theme changed to {theme} mode!", "info")
    return resp

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("auth.login"))
