from fastapi import APIRouter, UploadFile, File
from typing import List
from app.services.storage import StorageService
from app.services.batch_processing import process_batch
from app.models import Batch
import uuid

router = APIRouter()
storage_service = StorageService()

@router.post("/documents/upload", status_code=202)
async def upload_documents(files: List[UploadFile] = File(...)):
    batch_id = uuid.uuid4()
    # In a real implementation, we would create a Batch object in the database here.
    # For now, we'll just create a placeholder.
    batch = {"id": batch_id, "status": "queued", "total_docs": len(files)}

    for file in files:
        content = await file.read()
        storage_path = storage_service.save(f"{batch_id}/{file.filename}", content)
        # In a real implementation, we would create a Document object in the database here.
        # document = {"batch_id": batch_id, "storage_path": storage_path, "status": "queued"}

    process_batch.delay(str(batch_id))

    return {"status": "ok", "data": {"batch_id": str(batch_id)}}
