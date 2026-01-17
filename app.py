from flask import Flask
from routes.health import health_bp
from routes.user import user_bp
from errors import register_error_handlers

def create_app():
    app = Flask(__name__)

    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp, url_prefix="/users")

    register_error_handlers(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
