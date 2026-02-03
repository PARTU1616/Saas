from flask import Flask
from app.config import Config
from app import models
from app.extensions import db, migrate, jwt, limiter, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    limiter.init_app(app)

    # 🔥 SAFE BOOTSTRAP (FREE TIER FRIENDLY)
    with app.app_context():
        from app.utils.bootstrap import bootstrap_app
        bootstrap_app()

    # 🔥 REGISTER BLUEPRINTS
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app