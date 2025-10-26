from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    from app.views import main_bp
    from app.users.views import users_bp
    from app.products.views import products_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")

    return app
