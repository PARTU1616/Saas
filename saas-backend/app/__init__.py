from flask import Flask
from app.config import Config
from app import models
from app.extensions import db, migrate, jwt, limiter
from app.utils.seed import seed_roles

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    from app.extensions import cors
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    
    with app.app_context():
        seed_roles()


    # 🔥 REGISTER BLUEPRINTS
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")
    
    from app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")
    
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    limiter.init_app(app)





    return app
