import os
import tempfile

from flask import Flask, jsonify, request,send_from_directory
from flask_cors import CORS

from parsing import file_to_text
from matching import cosine_match
from skill_extractor import extract_skills

from datetime import datetime
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "resumes"
    )
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

JD_FOLDER = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "JD"
    )
)
PDF_FOLDER = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "JD_PDF"
    )
)

JD_FILES = {
    "Frontend Developer": "frontend.txt",
    "Backend Developer": "backend.txt",
    "Full Stack Developer": "full_stack.txt",
    "Business Analyst": "business.txt",
    "Machine Learning Engineer": "ML.txt"
}
JD_PDFS = {
    "frontend": "frontend.pdf",
    "backend": "backend.pdf",
    "fullstack": "full_stack.pdf",
    "business": "business.pdf",
    "ml": "ML.pdf"
}
os.makedirs(
    JD_FOLDER,
    exist_ok=True
)

@app.post("/api/upload")
def upload_resume():

    if "file" not in request.files:
        return jsonify({
            "error":"No file uploaded"
        }),400

    upload = request.files["file"]

    if upload.filename == "":
        return jsonify({
            "error":"No file selected"
        }),400

    ext = os.path.splitext(upload.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({
            "error":f"Unsupported file type: {ext}"
        }),400

    filename = secure_filename(upload.filename)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    name, extension = os.path.splitext(filename)

    unique_filename = f"{name}_{timestamp}{extension}"

    save_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )
    print("Saving location:", save_path)
    upload.save(save_path)

    print("File saved:", save_path)
    print("File size:", os.path.getsize(save_path), "bytes")




    resume_text = file_to_text(save_path)
    skills = extract_skills(resume_text)



  
    results = {}

    for role, filename in JD_FILES.items():

        jd_path = os.path.join(
                JD_FOLDER,
                filename
        )

        with open(jd_path, "r", encoding="utf-8") as file:
            jd_text = file.read()

        score = cosine_match(
            resume_text,
            jd_text
        )

        results[role] = score

    print(results)

    return jsonify({

        "message": "Upload successful",

        "filename": unique_filename,

        "matches": results,
        "skills":skills,
        "path": save_path

    })


@app.post("/api/parse")
def parse_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    upload = request.files["file"]

    if upload.filename == "":
        return jsonify({"error": "No file selected"}), 400

    ext = os.path.splitext(upload.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": f"Unsupported file type: {ext}"}), 400

    fd, temp_path = tempfile.mkstemp(suffix=ext)
    os.close(fd)

    try:
        upload.save(temp_path)
        text = file_to_text(temp_path)
    except Exception as exc:
        return jsonify({"error": f"Failed to parse file: {exc}"}), 500


    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return jsonify({
        "filename": upload.filename,
        "text": text
    })  

@app.get("/api/jd/<role>")
def view_job_description(role):

    filename = JD_PDFS.get(role)

    if not filename:
        return jsonify({
            "error": "Job Description not found"
        }), 404
    print("PDF Folder:", PDF_FOLDER)
    print("Filename:", filename)
    print("Full Path:", os.path.join(PDF_FOLDER, filename))

    return send_from_directory(
        PDF_FOLDER,
        filename
    )
if __name__ == "__main__":
    app.run(debug=True, port=9000)


