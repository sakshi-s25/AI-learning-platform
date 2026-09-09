from flask import Blueprint, request, jsonify
from models.user_model import (
    create_user,
    get_user_by_email

)
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

    result = create_user(
        name,
        email,
        password

    )

    return jsonify({
        "success": result["success"],
        "message": "Registration successful",
        "user_id": result.get("user_id")
    })