import json
import os


def load_courses():

    current_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    file_path = os.path.join(
        current_directory,
        "data",
        "courses.json"
    )


    with open(file_path, "r") as file:

        data = json.load(file)

    return data["courses"]


def get_recommendation(user_skills, learning_goal):

    courses = load_courses()


    user_skills_list = [
        skill.strip().lower()
        for skill in user_skills.split(",")
    ]


    learning_goal = learning_goal.lower()


    selected_career = None


    for course in courses:

        if course["career"].lower() == learning_goal:

            selected_career = course

            break


    if not selected_career:

        return {
            "success": False,
            "message": "Career goal not found"
        }


    required_skills = selected_career["required_skills"]


    missing_skills = []


    for skill in required_skills:

        if skill.lower() not in user_skills_list:

            missing_skills.append(skill)


    return {
        "success": True,
        "career": selected_career["career"],
        "current_skills": user_skills_list,
        "required_skills": required_skills,
        "missing_skills": missing_skills,
        "recommended_courses": selected_career["courses"]
    }