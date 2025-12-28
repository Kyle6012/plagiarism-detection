from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
from app.services.storage import StorageService
from app.services.parsing import extract_text_from_file
from app.services.batch_processing import process_batch
from app.services.ai_detection import AIDetectionService
from pydantic import BaseModel

class AICheckRequest(BaseModel):
    text: str

from app.models.user import User
from app.api.auth import fastapi_users
from app.core.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid

router = APIRouter()
storage_service = StorageService()
ai_service = AIDetectionService()

@router.post("/ai-check")
async def check_ai_content(request: AICheckRequest, user: User = Depends(fastapi_users.current_user())):
    result = ai_service.detect(request.text)
    return {"status": "ok", "data": result}

@router.post("/documents/upload", status_code=202)
async def upload_documents(
    files: List[UploadFile] = File(...),
    analysis_type: str = "plagiarism",  # plagiarism, ai, or both
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user())
):
    for file in files:
        if file.size > 10 * 1024 * 1024:  # 10 MB limit
            raise HTTPException(status_code=413, detail=f"File size for {file.filename} exceeds 10MB limit.")

        allowed_mime_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
            "application/zip",
            "application/x-tar",
            "image/png",
            "image/jpeg"
        ]
        if file.content_type not in allowed_mime_types:
            raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}: {file.content_type}")
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
                    allowed_extensions=['.txt', '.pdf', '.docx', '.doc', '.md', '.png', '.jpg', '.jpeg']
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
        text_content = ""
        
        # Check if it's an image
        from app.services.ocr import OCRService
        
        if OCRService.is_image(filename):
            # Save temp file for OCR if not already saved
            if not temp_path:
                temp_path = os.path.join(tempfile.gettempdir(), filename)
                with open(temp_path, 'wb') as f:
                    f.write(content)
            
            text_content = OCRService.extract_text_from_image(temp_path)
        else:
            # Create a file-like object for text extraction
            from io import BytesIO
            file_obj = BytesIO(content)
            file_obj.name = filename
            text_content = await extract_text_from_file(file_obj)
            
            # Fallback to OCR for PDFs if text extraction yields little/no text (scanned PDF)
            if filename.lower().endswith('.pdf') and len(text_content.strip()) < 50:
                if not temp_path:
                    temp_path = os.path.join(tempfile.gettempdir(), filename)
                    with open(temp_path, 'wb') as f:
                        f.write(content)
                ocr_text = OCRService.extract_text_from_scanned_pdf(temp_path)
                if len(ocr_text.strip()) > len(text_content.strip()):
                    text_content = ocr_text

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
            except OSError as e:
                print(f"Error removing temporary file {temp_path}: {e}")

    await db.commit()

    process_batch.delay(str(batch_id))

    return {"status": "ok", "data": {"batch_id": str(batch_id)}}

@router.get("/batches/{batch_id}/export/csv")
async def export_batch_csv(
    batch_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user())
):
    batch = db.query(Batch).filter(Batch.id == batch_id, Batch.user_id == user.id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    documents = db.query(Document).filter(Document.batch_id == batch_id).all()
    
    from app.services.report import ReportService
    from fastapi.responses import Response
    
    csv_content = ReportService.generate_csv_report(documents)
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=report_{batch_id}.csv"}
    )

@router.get("/batches/{batch_id}/export/pdf")
async def export_batch_pdf(
    batch_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user())
):
    batch = db.query(Batch).filter(Batch.id == batch_id, Batch.user_id == user.id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    documents = db.query(Document).filter(Document.batch_id == batch_id).all()
    
    from app.services.report import ReportService
    from fastapi.responses import Response
    
    pdf_content = ReportService.generate_pdf_report(batch, documents)
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_{batch_id}.pdf"}
    )

@router.get("/admin/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user())
):
    # In a local tool, we allow any authenticated user to see stats
    # If strictly admin, check user.role == 'admin'
    
    total_users = db.query(User).count()
    total_batches = db.query(Batch).count()
    total_documents = db.query(Document).count()
    
    # Calculate storage usage (approximate)
    # In real app, query MinIO or check file sizes
    storage_usage_mb = total_documents * 0.5 # Assume 0.5MB per doc avg
    
    return {
        "status": "ok",
        "data": {
            "total_users": total_users,
            "total_batches": total_batches,
            "total_documents": total_documents,
            "storage_usage_mb": storage_usage_mb,
            "system_status": "Healthy",
            "version": "1.0.0"
        }
    }

@router.get("/batch/{batch_id}")
async def get_batch_status(batch_id: str, db: Session = Depends(get_db)):
    batch = await db.get(Batch, uuid.UUID(batch_id))
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {"status": "ok", "data": batch}

@router.get("/batch/{batch_id}/results")
async def get_batch_results(batch_id: str, db: Session = Depends(get_db)):
    # Join Comparison with Document to get filenames
    from sqlalchemy.orm import aliased
    DocA = aliased(Document)
    DocB = aliased(Document)
    
    results = await db.execute(
        select(
            DocA.filename.label("document_name"),
            Comparison.similarity,
            DocB.filename.label("similar_document_name")
        )
        .join(DocA, Comparison.doc_a == DocA.id)
        .join(DocB, Comparison.doc_b == DocB.id)
        .where(DocA.batch_id == uuid.UUID(batch_id))
    )
    
    return {"status": "ok", "data": [dict(r._mapping) for r in results.all()]}

@router.get("/document/{document_id}")
async def get_document(document_id: str, db: Session = Depends(get_db)):
    document = await db.get(Document, uuid.UUID(document_id))
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "ok", "data": document}
