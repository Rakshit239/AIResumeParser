import os

import fitz
from docx import Document


def pdf_to_text(file_path):

    pdf = fitz.open(file_path)

    text = ""

    
    for page in pdf:
        text += page.get_text()

  
    pdf.close()

    return text


def docx_to_text(file_path):
    doc = Document(file_path)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text


def txt_to_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


EXTENSION_HANDLERS = {
    ".pdf": pdf_to_text,
    ".docx": docx_to_text,
    ".txt": txt_to_text,
}


def file_to_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    handler = EXTENSION_HANDLERS.get(ext)

    if handler is None:
        raise ValueError(f"Unsupported file type: {ext}")

    return handler(file_path)
