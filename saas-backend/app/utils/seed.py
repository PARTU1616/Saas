from app.extensions import db
from app.models.role import Role

def seed_roles():
    for name in ["ADMIN", "USER"]:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))
    db.session.commit()
