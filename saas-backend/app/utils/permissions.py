from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims.get("role") not in roles:
                return jsonify({"error": "Forbidden"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


def tenant_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()

        if "org_id" not in claims:
            return jsonify({"error": "Tenant context missing"}), 403

        return fn(*args, **kwargs)
    return wrapper
