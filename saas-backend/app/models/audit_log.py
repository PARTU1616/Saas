from app.extensions import db
from datetime import datetime

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, nullable=False)
    org_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
