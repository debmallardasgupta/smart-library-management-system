from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route("/")
def health():
    return {"status": "ok"}

# Dynamic URL parameter
@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id <= 0:
        abort(400)

    return jsonify({
        "user_id": user_id,
        "name": f"User{user_id}"
    })

# Error handler
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad Request",
        "message": "Invalid input provided"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found"
    }), 404

if __name__ == "__main__":
    app.run(debug=True)