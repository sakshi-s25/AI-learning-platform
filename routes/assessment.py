from flask import Blueprint, request, jsonify

from database.database import get_connection


assessment_bp = Blueprint("assessment", __name__)


questions = [

    {
        "id": 1,
        "question": "What does HTML stand for?",
        "options": [
            "Hyper Text Markup Language",
            "High Text Machine Language",
            "Hyper Tool Multi Language",
            "Home Text Markup Language"
        ],
        "answer": "Hyper Text Markup Language"
    },

    {
        "id": 2,
        "question": "Which language is commonly used for AI?",
        "options": [
            "Python",
            "HTML",
            "CSS",
            "SQL"
        ],
        "answer": "Python"
    },

    {
        "id": 3,
        "question": "What is CSS used for?",
        "options": [
            "Styling web pages",
            "Creating database",
            "Machine Learning",
            "Backend server"
        ],
        "answer": "Styling web pages"
    }

]


@assessment_bp.route("/quiz", methods=["GET"])
def get_quiz():

    quiz_questions = []


    for question in questions:

        quiz_questions.append({

            "id": question["id"],
            "question": question["question"],
            "options": question["options"]

        })


    return jsonify({
        "success": True,
        "questions": quiz_questions
    })


@assessment_bp.route("/submit", methods=["POST"])
def submit_quiz():

    data = request.get_json()

    user_id = data.get("user_id")
    answers = data.get("answers", {})


    score = 0


    for question in questions:

        question_id = str(question["id"])

        user_answer = answers.get(question_id)


        if user_answer == question["answer"]:

            score += 1


    total_questions = len(questions)


    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute("""

        INSERT INTO assessment_results
        (user_id, score, total_questions)

        VALUES (?, ?, ?)

    """, (

        user_id,
        score,
        total_questions

    ))


    connection.commit()
    connection.close()


    return jsonify({

        "success": True,
        "score": score,
        "total_questions": total_questions,

        "message": "Assessment submitted successfully"

    })