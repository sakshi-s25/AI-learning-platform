from flask import Blueprint, request, jsonify

from models.user_model import get_user_by_id, update_user_profile


user_bp = Blueprint("user", __name__)


@user_bp.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):

    user = get_user_by_id(user_id)


    if not user:

        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404


    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "skills": user["skills"],
            "learning_goal": user["learning_goal"],
            "study_time": user["study_time"]
        }
    })


@user_bp.route("/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):

    data = request.get_json()

    skills = data.get("skills", "")
    learning_goal = data.get("learning_goal", "")
    study_time = data.get("study_time", 0)


    user = get_user_by_id(user_id)


    if not user:

        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404


    update_user_profile(
        user_id,
        skills,
        learning_goal,
        study_time
    )


    return jsonify({
        "success": True,
        "message": "Profile updated successfully"
    })