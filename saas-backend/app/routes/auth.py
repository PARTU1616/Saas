from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from app.extensions import db
from app.models.user import User
from app.models.organization import Organization
from app.models.role import Role
from app.utils.security import generate_password_hash, check_password_hash
from app.extensions import limiter
import uuid
from datetime import datetime, timedelta
import secrets
from app.utils.security import hash_token




auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Auth blueprint working"})

from app.models.role import Role
@auth_bp.route("/signup", methods=["POST"])
@limiter.limit("3 per minute")
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    org_name = data.get("org_name")

    if not all([email, password, org_name]):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    # Organization
    org = Organization.query.filter_by(name=org_name).first()
    if not org:
        org = Organization(name=org_name)
        db.session.add(org)
        db.session.commit()

    # Role decision
    user_count = User.query.filter_by(org_id=org.id).count()
    role_name = "ADMIN" if user_count == 0 else "USER"
    role = Role.query.filter_by(name=role_name).first()

    # Create user
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        org_id=org.id,
        role_id=role.id
    )

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "org_id": user.org_id,
            "role": role.name
        }
    )

    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": role.name,
        "org_id": user.org_id
    }), 201



@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()

    user = User.query.get_or_404(int(user_id))

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "org_id": user.org_id,
            "role": user.role.name
        }
    )

    return jsonify({"access_token": access_token})

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(email=email, is_active=True).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "org_id": user.org_id,
            "role": user.role.name
        }
    )

    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": user.role.name,
        "org_id": user.org_id
    })

@auth_bp.route("/forgot-password", methods=["POST"])
@limiter.limit("3 per minute")
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    user = User.query.filter_by(email=email, is_active=True).first()
    if not user:
        return jsonify({"message": "If account exists, reset link sent"}), 200
    
    token = secrets.token_urlsafe(32)
    hashed_token = hash_token(token)
    
    user.reset_token = hashed_token
    user.reset_token_expires_at = datetime.utcnow() + timedelta(minutes=15)

    db.session.commit()

    reset_link = f"http://localhost:9000/reset-password?token={token}"

    # TEMP: log instead of email
    print("RESET LINK:", reset_link)

    return jsonify({"message": "Password reset link sent"}), 200


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    new_password = data.get("password")
    incoming_token = data.get("token")
    if not incoming_token or not new_password:
        return jsonify({"error": "Invalid request"}), 400

    hashed_incoming = hash_token(incoming_token)

    user = User.query.filter_by(reset_token=hashed_incoming).first()

    if not user or user.reset_token_expires_at < datetime.utcnow():
        return jsonify({"error": "Invalid or expired token"}), 400

    user.password_hash = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires_at = None

    db.session.commit()

    return jsonify({"message": "Password reset successful"}), 200
