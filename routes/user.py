from models.user import (
    create_user,
    get_all_users,
    update_user,
    delete_user
)


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return {"error": "Invalid input"}, 400

    updated = update_user(user_id, data["name"], data["email"])
    if updated == 0:
        return {"error": "User not found"}, 404

    return {"message": "User updated successfully"}


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    deleted = delete_user(user_id)
    if deleted == 0:
        return {"error": "User not found"}, 404

    return {"message": "User deleted successfully"}
