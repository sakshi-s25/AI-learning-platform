import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=True)
    required_level = Column(Float, default=75.0)  # target score, 0-100


class UserCompetency(Base):

    __tablename__ = "user_competencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id"), nullable=False)
    current_score = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    competency = relationship("Competency")


class CompetencyGap(Base):

    __tablename__ = "competency_gaps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    competency_id = Column(UUID(as_uuid=True), ForeignKey("competencies.id"), nullable=False)
    gap_value = Column(Float, nullable=False)
    priority = Column(String, nullable=False)  # strong | moderate | gap | priority_gap
    computed_at = Column(DateTime, default=datetime.utcnow)

    competency = relationship("Competency")
