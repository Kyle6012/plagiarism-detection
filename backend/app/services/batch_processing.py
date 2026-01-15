from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.batch import Batch
from app.models.document import Document
from app.models.comparison import Comparison
from app.services.embedding import EmbeddingService
from app.services.ai_detection import AIDetectionService
# from app.services.comparison import ComparisonService # Deleted
import asyncio

celery = Celery(__name__)
celery.config_from_object("app.core.celery")

engine = create_async_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

embedding_service = EmbeddingService()
ai_service = AIDetectionService()

@celery.task
def process_batch(batch_id: str, provider: str = "local", ai_threshold: float = 0.5):
    """Process a batch of documents for plagiarism and/or AI detection"""
    asyncio.run(_process_batch_async(batch_id, provider, ai_threshold))

async def _process_batch_async(batch_id: str, provider: str, ai_threshold: float):
    async with SessionLocal() as session:
        # Get batch and documents
        batch = await session.get(Batch, batch_id)
        if not batch:
            print(f"Batch {batch_id} not found")
            return
        
        batch.status = "processing"
        await session.commit()
        
        # Get all documents in this batch
        from sqlalchemy import select
        result = await session.execute(
            select(Document).where(Document.batch_id == batch_id)
        )
        documents = result.scalars().all()
        
        analysis_type = batch.analysis_type or "plagiarism"  # default to plagiarism
        
        # Instantiate PlagiarismService
        from app.services.plagiarism import PlagiarismService
        plagiarism_service = PlagiarismService(session)

        # Process each document
        for doc in documents:
            try:
                doc.status = "processing"
                await session.commit()
                
                # AI Detection
                if analysis_type in ["ai", "both", "mixed"]:
                    if doc.text_content:
                        ai_result = ai_service.detect(doc.text_content, provider=provider, threshold=ai_threshold)
                        doc.ai_score = ai_result.get("score", 0.0)
                        doc.is_ai_generated = ai_result.get("is_ai", False)
                        doc.ai_confidence = ai_result.get("confidence", 0.0)
                        doc.ai_provider = ai_result.get("provider", "unknown")
                        
                        # Store detailed AI detection result in AIDetection table
                        from app.models.ai_detection import AIDetection
                        ai_detection_record = AIDetection(
                            document_id=doc.id,
                            model_version=ai_result.get("details", {}).get("model", "unknown"),
                            probability=ai_result.get("score", 0.0),
                            meta_data={
                                "provider": ai_result.get("provider", "unknown"),
                                "confidence": ai_result.get("confidence", 0.0),
                                "label": ai_result.get("label", "unknown"),
                                "details": ai_result.get("details", {})
                            }
                        )
                        session.add(ai_detection_record)
                
                # Plagiarism Detection (semantic similarity)
                if analysis_type in ["plagiarism", "both", "mixed"]:
                    if doc.text_content and embedding_service.model:
                        # Generate embedding (average) for legacy compatibility/search
                        embedding = embedding_service.generate_text_embedding(doc.text_content)
                        doc.embedding = embedding
                        
                        # Find similar documents in batch using new PlagiarismService
                        similar_results = await plagiarism_service.find_similar_in_batch(doc, batch_id)
                        
                        # Store comparisons
                        for res in similar_results:
                            comparison = Comparison(
                                doc_a=doc.id,
                                doc_b=res["document_id"],
                                similarity=res["similarity"],
                                matches=res.get("matches", [])  # Store detailed matches in JSONB field
                            )
                            session.add(comparison)
                
                doc.status = "completed"
                await session.commit()
            except Exception as e:
                print(f"Error processing document {doc.id}: {e}")
                doc.status = "failed"
                await session.commit()
        
        # Update batch status
        batch.status = "completed"
        batch.processed_docs = len([d for d in documents if d.status == "completed"])
        await session.commit()
