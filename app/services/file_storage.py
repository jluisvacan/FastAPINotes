import os
import shutil
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException, status

router = APIRouter(prefix="/upload", tags=["uploads"])

MEDIA_DIR = "app/media"
ALLOW_MEDIA = ["image/png", "image/jpeg"]
MAX_MB = int(os.getenv("MAX_UPLOAD_MB", "3"))
CHUNKS = 1024 * 1024


def ensure_media() -> None:
    os.makedirs(MEDIA_DIR, exist_ok=True)



def save_image(file: UploadFile) -> dict:
    if file.content_type not in ALLOW_MEDIA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se permiten imagenes PNG o JPEG"
        )

    ensure_media()
    extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{extension}"

    file_path = os.path.join(MEDIA_DIR, filename)

    # class _ChunkCounter:
    #     def __init__(self, f):
    #         self._f = f
    #         self.calls = 0
    #         self.sizes = []
    #     def read(self, n=-1):
    #         data = self._f.read(n)
    #         if data:
    #             self.calls += 1
    #             self.sizes.append(len(data))
    #         return data
    #     def __getattr__(self, name):
    #         return getattr(self._f, name)
    #
    # reader = _ChunkCounter(file.file)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer, length=CHUNKS)

    size = os.path.getsize(file_path)
    if size > MAX_MB * CHUNKS:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"Too much data to upload (>{MAX_MB}) MB"
        )
    return {
        "filename": filename,
        "content_type": file.content_type,
        "url": f"media/{filename}",
        "size": size
        # "chunk_size_used": CHUNKS,
        # "chunk_calls": reader.calls,
        # "chunk_sizes_sample": reader.sizes[:5]
    }