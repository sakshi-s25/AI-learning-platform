from flask import Flask, jsonify

from database.database import create_tables
from routes.auth import auth_bp
from routes.user import user_bp
from routes.learning import learning_bp
from routes.assessment import assessment_bp


app = Flask(__name__)


create_tables()


@app.route("/")
def home():
    return jsonify({
        "message": "AI Enabled Learning Platform Backend is Running",
        "status": "success"
    })


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(learning_bp, url_prefix="/learning")
app.register_blueprint(assessment_bp, url_prefix="/assessment")


if __name__ == "__main__":
    app.run(debug=True)