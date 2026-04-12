from app.extensions import db
from app.models.role import Role
from sqlalchemy import inspect

def bootstrap_app():
    # Check if tables exist before seeding
    inspector = inspect(db.engine)
    if not inspector.has_table("role"):
        print("Tables not ready yet — skipping bootstrap")
        return

    roles = ["ADMIN", "USER"]
    for name in roles:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))
    db.session.commit()
    print("Bootstrap complete")
