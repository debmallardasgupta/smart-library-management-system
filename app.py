from flask import Flask, jsonify, render_template

from config import Config
from extensions import db
from routes import auth_bp, book_bp, loan_bp
from utils.errors import APIError


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(book_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(loan_bp)

    @app.route("/")
    def dashboard():
        return render_template("index.html")

    @app.route("/api/health")
    def health():
        return jsonify({
            "message": "Smart Library Management System API",
            "status": "running",
        })

    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(err):
        return jsonify(err.to_dict()), err.status_code

    @app.errorhandler(404)
    def handle_not_found(err):
        return jsonify({"error": "The requested endpoint does not exist"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(err):
        return jsonify({"error": "This HTTP method is not allowed on this endpoint"}), 405

    @app.errorhandler(500)
    def handle_internal_error(err):
        app.logger.exception("Unhandled server error")
        return jsonify({"error": "Something went wrong on our end"}), 500


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
