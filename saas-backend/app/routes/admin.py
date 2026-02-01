from flask import Blueprint, jsonify
from app.utils.permissions import role_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@role_required("ADMIN")
def admin_dashboard():
    return jsonify({"message": "Admin access granted"})
