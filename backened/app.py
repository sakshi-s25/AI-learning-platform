from flask import Flask, jsonify
from database.database import create_tables
from routes.auth import auth_bp
from routes.user import user_bp
from routes.learning import learning_bp
from routes.assessment import assessment_bp
from routes.upload import upload_bp

app = Flask(__name__)

create_tables()

@app.route("/")
def home():

    return jsonify({

        "success": True,
        "message": "Backened Running",
        "features": [
            "Competency Gap Analysis",
            "Personalized Learning Recommendations",
            "iGOT Karmayogi Course Recommendations"
            "Assessment"
            "Learning Material Upload"
            "AI Based MCQ Generation"
        ]
    })

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(learning_bp, url_prefix="/learning")
app.register_blueprint(assessment_bp, url_prefix="/assessment")
app.register_blueprint(upload_bp, url_prefix="/upload")

if __name__ == "__main__":
    app.run(debug=True)