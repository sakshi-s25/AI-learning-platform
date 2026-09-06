from flask import Blueprint, request, jsonify

from models.user_model import get_user_by_id
from services.recommendation import get_recommendation


learning_bp = Blueprint("learning", __name__)


@learning_bp.route("/recommendation/<int:user_id>", methods=["GET"])
def recommendation(user_id):

    user = get_user_by_id(user_id)


    if not user:

        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404


    if not user["skills"] or not user["learning_goal"]:

        return jsonify({
            "success": False,
            "message": "Please complete your profile first"
        }), 400


    result = get_recommendation(
        user["skills"],
        user["learning_goal"]
    )


    return jsonify(result)


@learning_bp.route("/recommend", methods=["POST"])
def direct_recommendation():

    data = request.get_json()


    skills = data.get("skills", "")
    learning_goal = data.get("learning_goal", "")


    if not skills or not learning_goal:

        return jsonify({
            "success": False,
            "message": "Skills and learning goal are required"
        }), 400


    result = get_recommendation(
        skills,
        learning_goal
    )


    return jsonify(result)