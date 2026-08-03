from flask import Flask, jsonify

from config import Config
from extensions import db
from routes import auth_bp, book_bp, loan_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(book_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(loan_bp)

    @app.route("/")
    def index():
        return jsonify({
            "message": "Smart Library Management System API",
            "status": "running",
        })

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
