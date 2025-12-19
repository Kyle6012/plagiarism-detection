from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Document

class ComparisonService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_similar(self, embedding, top_k=5):
        try:
            # Use cosine distance for similarity
            # similarity = 1 - cosine_distance
            # Note: pgvector's cosine_distance operator returns 1 - cosine_similarity
            # So 1 - cosine_distance gives us the cosine similarity back
            results = await self.db_session.execute(
                select(Document, (1 - Document.embedding.cosine_distance(embedding)).label("similarity"))
                .order_by(Document.embedding.cosine_distance(embedding))
                .limit(top_k)
            )
            return results.all()
        except Exception as e:
            print(f"Error in find_similar: {e}")
            return []
