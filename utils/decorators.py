from functools import wraps

import jwt
from flask import request

from utils.errors import APIError
from utils.jwt_utils import decode_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            raise APIError("Missing or malformed Authorization header", status_code=401)

        token = auth_header.split(" ", 1)[1]

        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise APIError("Token has expired", status_code=401)
        except jwt.InvalidTokenError:
            raise APIError("Invalid token", status_code=401)

        request.current_user = {"id": payload["user_id"], "role": payload["role"]}
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.current_user.get("role") != "admin":
            raise APIError("Admin privileges required", status_code=403)
        return f(*args, **kwargs)

    return decorated
