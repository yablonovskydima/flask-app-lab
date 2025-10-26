from flask import Blueprint, render_template, request, redirect, url_for

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "username" in request.form and request.form["username"]:
            username = request.form["username"]
            age = request.form.get("age", None)
            role = request.form.get("role", "User")
            return redirect(url_for("users.hi_user", name=username, age=age, role=role))
        elif "product" in request.form and request.form["product"]:
            product = request.form["product"]
            price = request.form.get("price", 0)
            return redirect(url_for("products.show_product", product_name=product, price=price))
    return render_template("base.html")