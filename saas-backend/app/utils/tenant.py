from flask_jwt_extended import get_jwt

def get_current_org_id():
    claims = get_jwt()
    return claims.get("org_id")
