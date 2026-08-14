import os
import shutil
import uuid
from fastapi import File, UploadFile, HTTPException, status, APIRouter
from app.services.file_storage import save_image

router = APIRouter(prefix="/upload", tags=["uploads"])

MEDIA_DIR = "app/media"

#subida de archivo mediante bytes
@router.post("/bytes")
async def upload_bytes(file: bytes = File(...)):
    return {
        "filename": "archivo_subido",
        "size": len(file)
    }


#subida de archivo mediante uploadfile
@router.post("file")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }


#guardar el archivo subido
@router.post("/save")
async def save_file(file: UploadFile = File(...)):

    saved = save_image(file)

    return {
        "filename": saved["filename"],
        "content_type": file.content_type,
        "url": saved["url"]
        # "size": saved["size"],
        # "chunk_size_used": saved["chunk_size_used"],
        # "chunk_calls": saved["chunk_calls"],
        # "chunk_sizes_sample": saved["chunk_sizes_sample"]
    }