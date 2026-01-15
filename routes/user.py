from flask import Blueprint, jsonify, abort

user_bp = Blueprint("user", __name__)

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id <= 0:
        abort(400)

    return jsonify({
        "id": user_id,
        "name": f"User{user_id}"
    })
