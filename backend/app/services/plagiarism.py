from typing import List, Dict, Any
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Document
from app.services.embedding import EmbeddingService

class PlagiarismService:
    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session
        self.embedding_service = EmbeddingService()

    def calculate_similarity(self, embedding_a, embedding_b) -> float:
        """Calculate cosine similarity between two embeddings"""
        if embedding_a is None or embedding_b is None:
            return 0.0
        
        # Ensure numpy arrays
        vec_a = np.array(embedding_a)
        vec_b = np.array(embedding_b)
        
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

    async def compare_documents(self, doc_a_text: str, doc_b_text: str) -> Dict[str, Any]:
        """
        Compare two documents using chunk-based analysis.
        Returns overall similarity and specific matching passages.
        """
        chunks_a, embeddings_a = self.embedding_service.encode_chunks(doc_a_text)
        chunks_b, embeddings_b = self.embedding_service.encode_chunks(doc_b_text)
        
        if not embeddings_a or not embeddings_b:
            return {"score": 0.0, "matches": []}

        matches = []
        total_similarity = 0.0
        
        # Compare every chunk in A against every chunk in B
        # This is O(N*M), fine for reasonable document sizes
        # For production with large docs, use FAISS or pgvector for chunk search
        
        for i, emb_a in enumerate(embeddings_a):
            best_match_score = 0.0
            best_match_idx = -1
            
            for j, emb_b in enumerate(embeddings_b):
                score = self.calculate_similarity(emb_a, emb_b)
                if score > best_match_score:
                    best_match_score = score
                    best_match_idx = j
            
            # Threshold for a "match"
            if best_match_score > 0.75:
                matches.append({
                    "source_chunk": chunks_a[i],
                    "target_chunk": chunks_b[best_match_idx],
                    "score": round(best_match_score, 4),
                    "source_index": i,
                    "target_index": best_match_idx
                })
                total_similarity += best_match_score

        # Normalize overall score
        # Simple approach: (sum of matched chunk scores) / (total chunks in A)
        # This represents "how much of A is found in B"
        overall_score = total_similarity / len(chunks_a) if chunks_a else 0.0

        return {
            "score": round(overall_score, 4),
            "matches": matches,
            "details": {
                "chunks_a": len(chunks_a),
                "chunks_b": len(chunks_b)
            }
        }

    async def find_similar_in_batch(self, document: Document, batch_id: str) -> List[Dict[str, Any]]:
        """Find similar documents within the same batch"""
        if not self.db_session:
            raise ValueError("Database session required for batch search")

        # Get all other docs in batch
        # In production, use pgvector similarity search on chunks
        # Here we iterate for detailed comparison
        query = select(Document).where(
            Document.batch_id == batch_id,
            Document.id != document.id
        )
        result = await self.db_session.execute(query)
        other_docs = result.scalars().all()
        
        results = []
        for other_doc in other_docs:
            comparison = await self.compare_documents(document.text_content, other_doc.text_content)
            if comparison["score"] > 0.1: # Filter low similarity
                results.append({
                    "document_id": str(other_doc.id),
                    "filename": other_doc.filename,
                    "similarity": comparison["score"],
                    "matches": comparison["matches"]
                })
        
        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results
