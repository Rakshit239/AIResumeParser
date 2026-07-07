import os
import tempfile

from flask import Flask, jsonify, request
from flask_cors import CORS

from parsing import file_to_text

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


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

    # with tempfile.NamedTemporaryFile(suffix=ext, delete=True) as tmp:
    #     upload.save(tmp.name)
    #     try:
    #         text = file_to_text(tmp.name)
    #     except Exception as exc:
    #         return jsonify({"error": f"Failed to parse file: {exc}"}), 500

    # return jsonify({"filename": upload.filename, "text": text})

    tmp = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
    tmp.close()

    try:
        upload.save(tmp.name)
        text = file_to_text(tmp.name)
    except Exception as exc:
        return jsonify({"error": f"Failed to parse file: {exc}"}), 500
    finally:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)

    return jsonify({"filename": upload.filename, "text": text})

if __name__ == "__main__":
    app.run(debug=True, port=9000)
