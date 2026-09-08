
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class LearningMaterial(Base):
    __tablename__ = "learning_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id"), nullable=False)
    filename = Column(String, nullable=False)
    status = Column(String, default="processing")  # processing | ready | failed
    created_at = Column(DateTime, default=datetime.utcnow)

    competency = relationship("Competency")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    material_id = Column(UUID(as_uuid=True), ForeignKey("learning_materials.id"), nullable=False)
    chunk_text = Column(String, nullable=False)
    chunk_index = Column(Integer, nullable=False)
