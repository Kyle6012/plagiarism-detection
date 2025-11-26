from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
from app.services.storage import StorageService
from app.services.parsing import extract_text_from_file
from app.services.batch_processing import process_batch
from app.services.ai_detection import AIDetectionService
from pydantic import BaseModel

class AICheckRequest(BaseModel):
    text: str

router = APIRouter()
storage_service = StorageService()
ai_service = AIDetectionService()

@router.post("/ai-check")
async def check_ai_content(request: AICheckRequest, user: User = Depends(fastapi_users.current_user())):
    result = ai_service.detect(request.text)
    return {"status": "ok", "data": result}

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
    analysis_type: str = "plagiarism",  # plagiarism, ai, or both
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user())
):
    batch_id = uuid.uuid4()

    batch = Batch(
        id=batch_id, 
        user_id=user.id, 
        total_docs=0,  # Will update after processing
        status="queued",
        analysis_type=analysis_type
    )
    db.add(batch)
    
    from app.services.archive_extractor import ArchiveExtractor
    import tempfile
    import os
    from pathlib import Path
    
    all_files_to_process = []
    
    for uploaded_file in files:
        # Check if it's an archive
        if ArchiveExtractor.is_archive(uploaded_file.filename):
            # Save archive temporarily
            temp_archive_path = os.path.join(tempfile.gettempdir(), uploaded_file.filename)
            await uploaded_file.seek(0)
            content = await uploaded_file.read()
            with open(temp_archive_path, 'wb') as f:
                f.write(content)
            
            try:
                # Extract archive
                extracted_files = ArchiveExtractor.extract_and_filter(
                    temp_archive_path,
                    allowed_extensions=['.txt', '.pdf', '.docx', '.doc', '.md']
                )
                
                # Add extracted files to processing list
                for orig_name, extracted_path in extracted_files:
                    with open(extracted_path, 'rb') as ef:
                        file_content = ef.read()
                    all_files_to_process.append((orig_name, file_content, extracted_path))
                
                # Clean up temp archive
                os.remove(temp_archive_path)
            except Exception as e:
                print(f"Error extracting archive {uploaded_file.filename}: {e}")
                continue
        else:
            # Process as regular file
            await uploaded_file.seek(0)
            content = await uploaded_file.read()
            all_files_to_process.append((uploaded_file.filename, content, None))
    
    # Update batch total_docs
    batch.total_docs = len(all_files_to_process)

    # Process all files (from archives and direct uploads)
    for filename, content, temp_path in all_files_to_process:
        storage_path = f"{batch_id}/{filename}"
        storage_service.save(storage_path, content)

        # Extract text for processing
        # Create a file-like object for text extraction
        from io import BytesIO
        file_obj = BytesIO(content)
        file_obj.name = filename
        text_content = await extract_text_from_file(file_obj)

        document = Document(
            batch_id=batch_id,
            filename=filename,
            storage_path=storage_path,
            text_content=text_content,
            status="queued"
        )
        db.add(document)
        
        # Clean up temporary extracted file if exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

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
