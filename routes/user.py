from flask import Blueprint, request, jsonify
from models.user import create_user, get_all_users

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["POST"])
def add_user():
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return {"error": "Invalid input"}, 400

    create_user(data["name"], data["email"])
    return {"message": "User added"}, 201

@user_bp.route("/users", methods=["GET"])
def fetch_users():
    return jsonify(get_all_users())
