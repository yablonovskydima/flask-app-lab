from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    app.secret_key = os.getenv("SECRET_KEY", "fallback_key")

    from app.views import main_bp
    from app.users.views import users_bp
    from app.products.views import products_bp
    from app.auth.views import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")

    return app
