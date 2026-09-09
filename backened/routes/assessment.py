from flask import Blueprint,request, jsonify
from database.database import get_connection
assessment_bp=Blueprint(
    "assessment",
    __name__
)
questions=[
    {
        "id":1,
        "question":"What is the primarypurpose of official statistics?",
        "options": [
            "Entertainment","Evidence based decision making",
            "Gaming",
            "Social media"
        ],
        "answer":
        "Evidence based decision making"
    },
    {
        "id":2,
        "question":
        "Which skill is important for data analysis?",
        "options":[
            "Statistics",
            "Painting",
            "Singing"
            "Driving"
        ],
        "answer":
        "Statistics"
    },
    {
        "id":3,
        "question":
        "What helps ensure reliable statistical information?",
        "options":[
            "Data Quality",
            "Random Guessing",
            "Entertainment",
            "Advertising"
        ],
        "answer":
        "Data Quality"
    }
]

@assessment_bp.route(
    "/quiz",
    methods=["Get"]
)
def get_quiz(): 
    quiz_question=[]
    for question in questions:
        quiz_question.append({
            "id":question["id"],
            "question":question["question"],
            "options":question["options"]
        })
    
    return jsonify({
       "success":True,
       "question":quiz_questions
    })
@assessment_bp.route(
    "/submit",
    methods=["POST"]
)
def submit_quiz():
    data=request.get_json()
    user_id=data.get("user_id")
    answers=data.get("answers",{})
    score=0
    for question in questions:
        question_id=str(question["id"])
        if answers.get(question_id)==question["answer"]:
            score+=1
    total_questions=len(questions)  
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(""" INSERT INTO assessment_results (user_id,score,total_questions) VALUES(?,?,?)
         """,(
             user_id,score,total_questions))     
    connection.commit()
    connection.close()

    return jsonify({
        "success":"True",
        "score":score,
        "total_questions":total_questions,
        "message":
        "Assessment completed successfully"
    })

