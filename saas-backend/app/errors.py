from flask import jsonify

def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Resource not found"}), 404

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"success": False, "error": "Forbidden"}), 403

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "error": "Internal server error"}), 500
