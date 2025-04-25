import boto3
import os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def upload_pdf_to_s3(file, filename):
    bucket = os.getenv("S3_BUCKET")
    key = f"uploads/{uuid4()}_{filename}"
    s3.upload_fileobj(file, bucket, key)
    return key
