from flask import Blueprint, render_template, request

products_bp = Blueprint(
    "products", __name__,
    template_folder="templates"
)

@products_bp.route("/<product_name>")
def show_product(product_name):
    price = request.args.get("price", 0)
    return render_template("products/info.html", product_name=product_name, product_price=price)
