from flask import jsonify

def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": "Invalid input provided"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": "Resource does not exist"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "error": "Internal Server Error"
        }), 500
