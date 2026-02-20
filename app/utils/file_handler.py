import os
from fastapi import UploadFile, HTTPException
from app.core.config import UPLOAD_FOLDER, MAX_FILE_SIZE, ALLOWED_TYPES

def save_file(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")

    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(path, "wb") as f:
        f.write(content)

    return path
