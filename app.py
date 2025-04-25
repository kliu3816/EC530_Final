# app.py
from fastapi import FastAPI, UploadFile, File, Form
from pdf_parser import extract_text_from_pdf
from quiz_generator import generate_quiz
from s3_uploader import upload_pdf_to_s3
import os, shutil
import json

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(
    file: UploadFile = File(...),
    num_questions: int   = Form(5),          # default to 5
):
    # 1) store locally
    tmp = f"temp_{file.filename}"
    with open(tmp, "wb") as buf:
        shutil.copyfileobj(file.file, buf)

    # 2) optional: upload to S3
    #upload_pdf_to_s3(open(tmp, "rb"), file.filename)

    # 3) extract text
    text = extract_text_from_pdf(tmp)

    # 4) generate quiz with explanations
    quiz_list = generate_quiz(text, num_questions)

    # 5) cleanup
    os.remove(tmp)

    # 6) return as JSON string
    return {"quiz": json.dumps(quiz_list)}
