from flask import Blueprint, request, jsonify
import os
from PyPDF2 import PdfReader
from services.mcq_generator import generate_mcqs

upload_bp = Blueprint(
    "upload",
    __name__

)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@upload_bp.route(
    "/material",
    methods=["POST"]
)

def upload_material():

    if "file" not in request.files:

        return jsonify({
            "success":False,
            "message": "No file uploaded"
            }), 400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    file_path = os.path.join(

        UPLOAD_FOLDER,
        file.filename
    )

    file.save(file_path)

    extracted_text = ""

    if file.filename.endswith(".txt"):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as text_file:

            extracted_text = text_file.read()

    elif file.filename.endswith(".pdf"):
        reader = PdfReader(file_path)

        for page in reader.pages:
            extracted_text += page.extract_text() or ""

    else:

        return jsonify({
            "success": False,
            "message":
            "Only PDF and TXT files supported"
        }), 400

    mcqs = generate_mcqs(extracted_text)

    return jsonify({
        "success": True,
        "message": "Learning material processed successfully",
        "generated_mcqs": mcqs
        
    })