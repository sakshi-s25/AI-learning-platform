import json
import os

def load_courses():
    base_directory = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    file_path = os.path.join(
        base_directory,
        "data",
        "courses.json"
    )

    with open(file_path, "r") as file:
        data = json.load(file)

    return data["courses"]

def get_recommendation(

        user_skills,
        learning_goal
):

    courses = load_courses()
    user_skills_list = []

    for skill in user_skills.split(","):
        user_skills_list.append(
            skill.strip().lower()
        )

    selected_competency = None

    for course in courses:
        if course["competency"].lower() == learning_goal.lower():
            selected_competency = course
            break

    if not selected_competency:
        return {
            "success": False,
            "message": "Competency area not found"
        }

    required_skills = selected_competency["required_skills"]

    competency_gap = []

    for skills in required_skills:
        if skill.lower() not in user_skills_list:
            competency_gap.append(skill)

    return {

        "success": True,
        "competency": selected_competency["competency"],
        "current_competencies": user_skills_list,
        "required_competencies": required_skills,
        "competency_gap": competency_gap,
        "recommended_training": 
        selected_competency["recommended_training"],
        "recommended_platform": 
        selected_competency["platform"],
        
    }

    