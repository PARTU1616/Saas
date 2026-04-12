from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.models.role import Role
from app.extensions import db
from app.utils.permissions import role_required, tenant_required
from app.utils.tenant import get_current_org_id
from app.utils.audit import log_action
from flask_jwt_extended import jwt_required, get_jwt
from app.models.organization import Organization

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@role_required("ADMIN")
def admin_dashboard():
    return jsonify({"message": "Admin access granted"})

@admin_bp.route("/users/<int:user_id>/role", methods=["PATCH"])
@tenant_required
@role_required("ADMIN")
def update_user_role(user_id):
    data = request.get_json()
    new_role = data.get("role")

    if new_role not in ["ADMIN", "USER"]:
        return jsonify({"error": "Invalid role"}), 400

    org_id = get_current_org_id()
    user = User.query.filter_by(id=user_id, org_id=org_id).first_or_404()

    # 🚫 Prevent self-demotion
    if user.id == int(get_jwt_identity()):
        return jsonify({"error": "Cannot change your own role"}), 400

    role = Role.query.filter_by(name=new_role).first()
    user.role = role
    db.session.commit()

    log_action("CHANGE_ROLE", target=f"user:{user.id}")

    return jsonify({
        "message": "Role updated",
        "user_id": user.id,
        "role": role.name
    })


@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
def admin_stats():
    claims = get_jwt()

    if claims.get("role") != "ADMIN":
        return jsonify({"error": "Admin access required"}), 403

    org_id = claims.get("org_id")

    return jsonify({
        "total_users": User.query.count(),
        "total_admins": User.query.join(Role).filter(Role.name == "ADMIN").count(),
        "total_organizations": Organization.query.count(),
        "users_in_org": User.query.filter_by(org_id=org_id).count()
    })
