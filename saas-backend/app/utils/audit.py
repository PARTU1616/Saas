from app.extensions import db
from app.models.audit_log import AuditLog
from flask_jwt_extended import get_jwt_identity, get_jwt

def log_action(action, target=None):
    claims = get_jwt()
    log = AuditLog(
        actor_id=int(get_jwt_identity()),
        org_id=claims["org_id"],
        action=action,
        target=target
    )
    db.session.add(log)
    db.session.commit()
