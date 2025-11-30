from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
csrf = CSRFProtect()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name="development"):
    from config import DevelopmentConfig, TestingConfig, ProductionConfig

    config_classes = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    app = Flask(__name__)
    app.config.from_object(config_classes.get(config_name, DevelopmentConfig))

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)

    from app.posts import models
    from app.products import models
    from app.users import models

    from app.views import main_bp
    from app.users.views import users_bp
    from app.products.views import products_bp
    from app.auth.views import auth_bp
    from app.contact.views import contact_bp
    from app.posts.views import post_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(contact_bp, url_prefix="/contact")
    app.register_blueprint(post_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app

from app.users.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))