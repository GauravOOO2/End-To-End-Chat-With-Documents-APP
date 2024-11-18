from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.document import Document
from app.services.parsing import parse_document
import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

router = APIRouter()

# Load AWS credentials from environment variables
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Set up S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

UPLOAD_FOLDER = "./uploaded_files"  # Temporary folder to store files

def upload_to_s3(file: UploadFile):
    try:
        # Generate a unique file name
        s3_file_name = f"{file.filename}"

        # Upload the file to S3
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, s3_file_name)

        # Construct file URL (this assumes the S3 bucket is publicly accessible, adjust if needed)
        file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_file_name}"
        return file_url
    except NoCredentialsError:
        raise Exception("AWS credentials not found!")
    except Exception as e:
        raise Exception(f"Error uploading file to S3: {str(e)}")

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save the file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Upload the file to S3
    try:
        file_url = upload_to_s3(file)
    except Exception as e:
        return {"error": f"File upload to S3 failed: {str(e)}"}

    # Parse the document
    try:
        parsed_data = parse_document(file_path)
    except Exception as e:
        return {"error": f"Document parsing failed: {str(e)}"}

    # Save parsed data in the database
    new_document = Document(
        file_name=file.filename,
        file_url=file_url,  # Save the S3 URL
        parsed_content=parsed_data["parsed_content"],
        metadata_content=parsed_data["metadata"],  # Use metadata_content here
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    # Clean up the temporary file
    os.remove(file_path)

    return {"message": "Document uploaded, parsed, and stored successfully!", "data": new_document}
