import pytest
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["REDIS_URL"] = "memory://"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret"
os.environ["RATELIMIT_ENABLED"] = "0"

from app import create_app
from app.extensions import db as _db, limiter
from app.models.role import Role

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-jwt-secret",
        "SECRET_KEY": "test-secret",
    })
    return app

@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        _db.create_all()
        for name in ["ADMIN", "USER"]:
            if not Role.query.filter_by(name=name).first():
                _db.session.add(Role(name=name))
        _db.session.commit()
        yield _db
        _db.drop_all()

@pytest.fixture(scope="function")
def client(app, db):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def clean_db(db, app):
    yield db
    with app.app_context():
        from app.models.user import User
        from app.models.organization import Organization
        User.query.delete()
        Organization.query.delete()
        db.session.commit()
