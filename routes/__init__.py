from .auth_routes import auth_bp
from .book_routes import book_bp
from .loan_routes import loan_bp

__all__ = ["book_bp", "auth_bp", "loan_bp"]
