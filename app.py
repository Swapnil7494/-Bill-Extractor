from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import List
import os
import uuid
import shutil

from extractor.gemini_extractor import extract_from_file
from utils.csv_writer import append_to_csv


app = FastAPI()


# -------------------------------
# CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace * with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# DIRECTORIES
# -------------------------------
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
CSV_FILE = "all_bills.csv"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -------------------------------
# ALLOWED FILE TYPES
# -------------------------------
ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".pdf", ".heic"]


# -------------------------------
# VALIDATION
# -------------------------------
def is_valid_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


# -------------------------------
# SAVE UPLOADED FILE
# -------------------------------
def save_upload(file: UploadFile):
    clean_name = os.path.basename(file.filename)

    unique_filename = f"{uuid.uuid4()}_{clean_name}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path, clean_name


# -------------------------------
# PROCESS SINGLE FILE
# -------------------------------
def process_file(file_path: str, filename: str):
    try:
        result = extract_from_file(file_path)

        if "error" in result:
            return {
                "file": filename,
                "status": "failed",
                "error": result
            }

        append_to_csv(result, file_name=filename)

        return {
            "file": filename,
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "file": filename,
            "status": "failed",
            "error": str(e)
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# -------------------------------
# UPLOAD + EXTRACT API
# -------------------------------
@app.post("/extract-bill")
async def extract_bill(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        filename = os.path.basename(file.filename)

        if not is_valid_file(filename):
            results.append({
                "file": filename,
                "status": "failed",
                "error": "Unsupported file type"
            })
            continue

        file_path, clean_name = save_upload(file)
        result = process_file(file_path, clean_name)
        results.append(result)

    return {
        "status": "completed",
        "total_files": len(results),
        "results": results,
        "download_url": "/download-csv"
    }


# -------------------------------
# DOWNLOAD CSV API
# -------------------------------
@app.get("/download-csv")
def download_csv():
    file_path = os.path.join(OUTPUT_DIR, CSV_FILE)

    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404,
            content={
                "status": "failed",
                "error": "CSV not found. Please upload and extract bills first."
            }
        )

    return FileResponse(
        path=file_path,
        filename=CSV_FILE,
        media_type="text/csv"
    )


# -------------------------------
# ROOT API
# -------------------------------
@app.get("/")
def root():
    return {
        "message": "API Running 🚀",
        "upload_endpoint": "/extract-bill",
        "download_endpoint": "/download-csv"
    }
