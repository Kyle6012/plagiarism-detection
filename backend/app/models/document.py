import uuid
from sqlalchemy import Column, String, Text, DateTime, func, UUID
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from .base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    content_hash = Column(String, nullable=False, unique=True)
    mime_type = Column(String)
    text_content = Column(Text)
    embedding = Column(Vector(384))  # Assuming sentence-transformers/all-MiniLM-L6-v2 embedding dim
    storage_path = Column(String)
    uploaded_by = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
