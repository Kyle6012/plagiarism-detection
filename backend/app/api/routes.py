from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
from app.services.storage import StorageService
from app.services.batch_processing import process_batch
import uuid
from app.models.batch import Batch
from app.models.document import Document
from app.models.comparison import Comparison
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.db import get_db
from app.models.user import User
from app.api.auth import fastapi_users

router = APIRouter()
storage_service = StorageService()

@router.post("/documents/upload", status_code=202)
async def upload_documents(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user())
):
    batch_id = uuid.uuid4()

    batch = Batch(id=batch_id, user_id=user.id, total_docs=len(files), status="queued")
    db.add(batch)

    for file in files:
        content = await file.read()
        storage_path = f"{batch_id}/{file.filename}"
        storage_service.save(storage_path, content)

        document = Document(
            batch_id=batch_id,
            filename=file.filename,
            storage_path=storage_path,
            status="queued"
        )
        db.add(document)

    await db.commit()

    process_batch.delay(str(batch_id))

    return {"status": "ok", "data": {"batch_id": str(batch_id)}}

@router.get("/batch/{batch_id}")
async def get_batch_status(batch_id: str, db: Session = Depends(get_db)):
    batch = await db.get(Batch, uuid.UUID(batch_id))
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {"status": "ok", "data": batch}

@router.get("/batch/{batch_id}/results")
async def get_batch_results(batch_id: str, db: Session = Depends(get_db)):
    # This is a simplified query. A real implementation might involve more complex joins and filtering.
    comparisons = await db.execute(
        select(Comparison)
        .join(Document, Comparison.doc_a == Document.id)
        .where(Document.batch_id == uuid.UUID(batch_id))
    )
    return {"status": "ok", "data": comparisons.scalars().all()}

@router.get("/document/{document_id}")
async def get_document(document_id: str, db: Session = Depends(get_db)):
    document = await db.get(Document, uuid.UUID(document_id))
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "ok", "data": document}
