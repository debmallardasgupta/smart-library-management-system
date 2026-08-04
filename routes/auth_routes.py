from flask import Blueprint, jsonify, request

from extensions import db
from models.user import User
from schemas import login_schema, register_schema
from utils.decorators import token_required
from utils.errors import APIError
from utils.jwt_utils import generate_token
from utils.validation import validate_payload

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = validate_payload(register_schema, request.get_json(silent=True))

    if User.query.filter_by(username=data["username"]).first():
        raise APIError("Username already taken", status_code=409)

    if User.query.filter_by(email=data["email"]).first():
        raise APIError("Email already registered", status_code=409)

    user = User(username=data["username"], email=data["email"], role=data["role"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = validate_payload(login_schema, request.get_json(silent=True))

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        raise APIError("Invalid username or password", status_code=401)

    token = generate_token(user.id, user.role)

    return jsonify({"token": token, "user": user.to_dict()}), 200


@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    user = User.query.get(request.current_user["id"])
    if not user:
        raise APIError("User not found", status_code=404)
    return jsonify(user.to_dict()), 200
