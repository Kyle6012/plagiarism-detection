from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.batch import Batch
from app.models.document import Document
from app.models.comparison import Comparison
from app.services.embedding import EmbeddingService
from app.services.ai_detection import AIDetectionService
from app.services.comparison import ComparisonService
import asyncio

celery = Celery(__name__)
celery.config_from_object("app.core.celery")

engine = create_async_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

embedding_service = EmbeddingService()
ai_service = AIDetectionService()

@celery.task
def process_batch(batch_id: str):
    """Process a batch of documents for plagiarism and/or AI detection"""
    asyncio.run(_process_batch_async(batch_id))

async def _process_batch_async(batch_id: str):
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
        
        # Process each document
        for doc in documents:
            try:
                doc.status = "processing"
                await session.commit()
                
                # AI Detection
                if analysis_type in ["ai", "both"]:
                    if doc.text_content:
                        ai_result = ai_service.detect(doc.text_content)
                        doc.ai_score = ai_result.get("score", 0.0)
                        doc.is_ai_generated = ai_result.get("is_ai", False)
                
                # Plagiarism Detection (semantic similarity)
                if analysis_type in ["plagiarism", "both"]:
                    if doc.text_content and embedding_service.enabled:
                        # Generate embedding
                        embedding = embedding_service.generate_text_embedding(doc.text_content)
                        doc.embedding = embedding
                        
                        # Find similar documents
                        comparison_service = ComparisonService(session)
                        similar_results = await comparison_service.find_similar(embedding, top_k=5)
                        
                        # Store comparisons
                        for similar_doc, similarity in similar_results:
                            if similar_doc.id != doc.id:  # Don't compare with self
                                comparison = Comparison(
                                    doc_a=doc.id,
                                    doc_b=similar_doc.id,
                                    similarity=similarity
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
