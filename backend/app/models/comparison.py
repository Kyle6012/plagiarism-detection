import uuid
from sqlalchemy import Column, Float, DateTime, func, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from . import Base

class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_a = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    doc_b = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    similarity = Column(Float)
    details = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
