from flask import Blueprint, request, jsonify

from models.user_model import create_user, get_user_by_email


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:

        return jsonify({
            "success": False,
            "message": "Name, email and password are required"
        }), 400


    existing_user = get_user_by_email(email)

    if existing_user:

        return jsonify({
            "success": False,
            "message": "User already exists"
        }), 400


    result = create_user(name, email, password)


    if result["success"]:

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "user_id": result["user_id"]
        }), 201

    else:

        return jsonify({
            "success": False,
            "message": "Registration failed"
        }), 500


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")


    if not email or not password:

        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400


    user = get_user_by_email(email)


    if not user:

        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404


    if user["password"] != password:

        return jsonify({
            "success": False,
            "message": "Incorrect password"
        }), 401


    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    })