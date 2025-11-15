import uuid
from sqlalchemy import Column, Integer, String, DateTime, func, UUID
from .base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_type = Column(String, nullable=False)  # 'process_text_upload', 'process_image_upload'
    status = Column(String, nullable=False, default="pending")  # 'pending', 'processing', 'completed', 'failed'
    progress = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
