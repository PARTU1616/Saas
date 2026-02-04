from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.models.role import Role
from app.extensions import db
from app.utils.permissions import role_required, tenant_required
from app.utils.decorators import admin_required 
from app.utils.tenant import get_current_org_id
from app.utils.audit import log_action
from app.extensions import limiter
from app.utils.security import generate_password_hash, check_password_hash


users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["POST"])
@tenant_required
@admin_required
def create_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role_name = data.get("role", "USER")

    if not all([email, password, role_name]):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"error": "Invalid role"}), 400

    org_id = get_current_org_id()

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        org_id=org_id,
        role_id=role.id
    )

    db.session.add(user)
    db.session.commit()

    log_action("CREATE_USER", target=f"user:{user.id}")

    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": role.name,
            "is_active": user.is_active
        }
    }), 201


@users_bp.route("/", methods=["GET"])
@tenant_required
@role_required("ADMIN")
@limiter.limit("20 per minute")
def list_users():
    org_id = get_current_org_id()

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    pagination = User.query.filter_by(org_id=org_id)\
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "data": [
            {
                "id": u.id,
                "email": u.email,
                "role": u.role.name,
                "is_active": u.is_active
            }
            for u in pagination.items
        ],
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages
        }
    })


@users_bp.route("/<int:user_id>/role", methods=["PUT"])
@tenant_required
@role_required("ADMIN")
def change_role(user_id):
    data = request.get_json()
    new_role = data.get("role")

    if new_role not in ["ADMIN", "USER"]:
        return jsonify({"error": "Invalid role"}), 400

    org_id = get_current_org_id()
    user = User.query.filter_by(id=user_id, org_id=org_id).first_or_404()

    # 🔐 SECURITY HARDENING
    if user.id == int(get_jwt_identity()):
        return jsonify({"error": "Cannot change your own role"}), 400

    role = Role.query.filter_by(name=new_role).first()
    user.role = role
    db.session.commit()

    log_action("CHANGE_ROLE", target=f"user:{user.id}")

    return jsonify({"message": "Role updated"})

@users_bp.route("/<int:user_id>/status", methods=["PUT"])
@tenant_required
@role_required("ADMIN")
def change_status(user_id):
    data = request.get_json()
    is_active = data.get("is_active")

    org_id = get_current_org_id()
    user = User.query.filter_by(id=user_id, org_id=org_id).first_or_404()

    admin_role = Role.query.filter_by(name="ADMIN").first()

    # 🔐 SECURITY HARDENING
    if user.role_id == admin_role.id and is_active is False:
        admin_count = User.query.filter_by(
            org_id=org_id,
            role_id=admin_role.id,
            is_active=True
        ).count()

        if admin_count == 1:
            return jsonify(
                {"error": "At least one active admin is required"},
                400
            )

    user.is_active = bool(is_active)
    db.session.commit()

    log_action("CHANGE_STATUS", target=f"user:{user.id}")

    return jsonify({"message": "User status updated"})
