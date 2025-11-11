from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Document

class ComparisonService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_similar(self, embedding, top_k=5):
        results = await self.db_session.execute(
            select(Document).order_by(Document.embedding.l2_distance(embedding)).limit(top_k)
        )
        return results.scalars().all()
