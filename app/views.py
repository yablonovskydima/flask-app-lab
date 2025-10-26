from flask import Blueprint, render_template, request, redirect, url_for

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "username" in request.form and request.form["username"]:
            username = request.form["username"]
            return redirect(url_for("users.hi_user", name=username))
        elif "product" in request.form and request.form["product"]:
            product = request.form["product"]
            return redirect(url_for("products.show_product", product_name=product))
    return render_template("base.html")
