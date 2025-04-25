from fastapi import FastAPI, UploadFile, File
from pdf_parser import extract_text_from_pdf
from quiz_generator import generate_quiz
from s3_uploader import upload_pdf_to_s3
import os
import shutil


app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save locally
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Upload to S3
    # upload_pdf_to_s3(open(temp_path, "rb"), file.filename)

    # Extract text
    text = extract_text_from_pdf(temp_path)

    # Generate quiz
    quiz = generate_quiz(text)

    # Clean up
    os.remove(temp_path)

    return {"quiz": quiz}
