import uuid
from sqlalchemy import Column, String, Integer, DateTime, func, UUID
from .base import Base

class Batch(Base):
    __tablename__ = "batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    total_docs = Column(Integer)
    processed = Column(Integer, default=0)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
