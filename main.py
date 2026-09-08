from fastapi import FastAPI
from database import engine
from sqlalchemy import text
from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from pypdf import PdfReader
app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "PS-101 Backend is running!"
    }

@app.get("/db-test")
def database_test():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "success",
            "message": "PostgreSQL connected successfully!"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/users")
def get_users():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM users ORDER BY id")
        )

        users = [dict(row._mapping) for row in result]

    return users

@app.get("/competencies")
def get_competencies():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM competencies ORDER BY id")
        )

        competencies = [dict(row._mapping) for row in result]

    return competencies



@app.get("/users/{user_id}/gaps")
def get_competency_gaps(user_id: int):

    query = text("""
        SELECT
            c.name AS competency,
            c.required_level,
            uc.current_level,
            (c.required_level - uc.current_level) AS gap,
            uc.assessment_score
        FROM user_competencies uc
        JOIN competencies c
            ON uc.competency_id = c.id
        WHERE uc.user_id = :user_id
        ORDER BY gap DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"user_id": user_id}
        )

        gaps = [dict(row._mapping) for row in result]

    return gaps

@app.get("/users/{user_id}/recommendations")
def get_recommendations(user_id: int):

    query = text("""
        SELECT
            c.name AS competency,
            (c.required_level - uc.current_level) AS gap,
            ic.title AS course,
            ic.difficulty,
            ic.duration_minutes,
            ic.course_url
        FROM user_competencies uc
        JOIN competencies c
            ON uc.competency_id = c.id
        JOIN igot_courses ic
            ON ic.competency_id = c.id
        WHERE uc.user_id = :user_id
          AND c.required_level > uc.current_level
        ORDER BY gap DESC, ic.duration_minutes ASC
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"user_id": user_id}
        )

        recommendations = [
            dict(row._mapping)
            for row in result
        ]

    return recommendations

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload-material")
async def upload_material(
    file: UploadFile = File(...)
):
    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    extracted_text = ""

    if file.filename.lower().endswith(".pdf"):
        reader = PdfReader(str(file_path))

        for page in reader.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

    else:
        extracted_text = "Only PDF extraction is enabled currently."

    return {
        "status": "success",
        "file_name": file.filename,
        "file_path": str(file_path),
        "text_length": len(extracted_text),
        "extracted_text": extracted_text[:2000]
    }



