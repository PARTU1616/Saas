from app.extensions import db
from app.models.role import Role

def bootstrap_app():

    # 2. Seed roles safely
    roles = ["ADMIN", "USER"]

    for name in roles:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))

    db.session.commit()