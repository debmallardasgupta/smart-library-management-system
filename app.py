from flask import Flask
import os

from routes.health import health_bp
from routes.user import user_bp
from errors import register_error_handlers
from config import DevelopmentConfig, ProductionConfig
from extensions import db

def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # initialize db
    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp, url_prefix="/users")

    register_error_handlers(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
