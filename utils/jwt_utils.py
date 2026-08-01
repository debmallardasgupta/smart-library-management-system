import datetime

import jwt
from flask import current_app


def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    """Returns the payload dict, or raises jwt exceptions on invalid/expired tokens."""
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
