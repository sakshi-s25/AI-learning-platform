
import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id"), nullable=False)
    question_text = Column(String, nullable=False)
    options = Column(JSONB, nullable=False)  # e.g. ["option A", "option B", "option C", "option D"]
    correct_option_index = Column(Integer, nullable=False)  # 0-3
    explanation = Column(String, nullable=True)
    difficulty = Column(String, default="Medium")
    is_ai_generated = Column(Boolean, default=False)
    source_reference = Column(String, nullable=True)  # filled in later, for AI-generated questions
