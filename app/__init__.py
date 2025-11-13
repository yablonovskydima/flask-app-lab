from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name="development"):
    from config import DevelopmentConfig, TestingConfig, ProductionConfig

    config_classes = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    app = Flask(__name__)
    app.config.from_object(config_classes.get(config_name, DevelopmentConfig))

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.posts import models

    from app.views import main_bp
    from app.users.views import users_bp
    from app.products.views import products_bp
    from app.auth.views import auth_bp
    from app.contact.views import contact_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(contact_bp, url_prefix="/contact")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app
