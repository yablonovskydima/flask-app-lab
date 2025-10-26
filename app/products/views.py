from flask import Blueprint, render_template

products_bp = Blueprint(
    "products", __name__,
    template_folder="templates"
)

@products_bp.route("/<product_name>")
def show_product(product_name):
    return render_template("products/info.html", product_name=product_name)
