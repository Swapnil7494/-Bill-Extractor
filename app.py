from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional
import shutil
import os
import uuid

from extractor.gemini_extractor import extract_from_file
from utils.csv_writer import append_to_csv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = ["image/png", "image/jpeg", "application/pdf","image/heic", "image/jpg", "image/webp", "image/bmp", ]


# -------------------------------
# Helper: Save Uploaded File
# -------------------------------
def save_upload(file: UploadFile):
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


# -------------------------------
# Helper: Process One File
# -------------------------------
def process_file(file_path, filename=""):
    try:
        result = extract_from_file(file_path)

        if "error" in result:
            return {"file": filename, "status": "failed", "error": result}

        append_to_csv(result)

        return {"file": filename, "status": "success", "data": result}

    except Exception as e:
        return {"file": filename, "status": "failed", "error": str(e)}

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# -------------------------------
# MAIN UNIFIED ENDPOINT
# -------------------------------
@app.post("/extract-bill")
async def extract_bill(
    files: Optional[List[UploadFile]] = File(None),
    folder_path: Optional[str] = Form(None)
):

    results = []

    # -------------------------------
    # CASE 1: Multiple / Single Upload
    # -------------------------------
    if files:
        for file in files:

            if file.content_type not in ALLOWED_TYPES:
                results.append({
                    "file": file.filename,
                    "status": "failed",
                    "error": "Unsupported file type"
                })
                continue

            file_path = save_upload(file)
            result = process_file(file_path, file.filename)
            results.append(result)

    # -------------------------------
    # CASE 2: Folder Batch Processing
    # -------------------------------
    elif folder_path:
        if not os.path.exists(folder_path):
            return {"status": "failed", "error": "Folder not found"}

        SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".pdf", ".heic"]

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            ext = os.path.splitext(file)[1].lower()

            if ext not in SUPPORTED_EXTENSIONS:
                continue

            result = process_file(file_path, file)
            results.append(result)

    else:
        return {"status": "failed", "error": "No input provided"}

    return {
        "status": "completed",
        "total_files": len(results),
        "results": results,
        "csv_file": os.path.join("output", "all_bills.csv")
    }


# -------------------------------
# Download CSV
# -------------------------------
from fastapi.responses import FileResponse

@app.get("/download-csv")
def download_csv():
    file_path = os.path.join("output", "all_bills.csv")

    if not os.path.exists(file_path):
        return {"status": "failed", "error": "CSV not found"}

    return FileResponse(
        path=file_path,
        filename="all_bills.csv",
        media_type="text/csv"
    )


# -------------------------------
# Health Check
# -------------------------------
@app.get("/")
def root():
    return {"message": "Bill Extraction API is running 🚀"}