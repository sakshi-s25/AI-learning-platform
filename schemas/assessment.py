import uuid
from typing import List

from pydantic import BaseModel


class AssessmentQuestionOut(BaseModel):
    """What the frontend sees before answering — no correct_option_index."""

    id: uuid.UUID
    competency_id: uuid.UUID
    question_text: str
    options: List[str]

    class Config:
        from_attributes = True


class AnswerIn(BaseModel):
    question_id: uuid.UUID
    selected_option: int


class AssessmentSubmission(BaseModel):
    answers: List[AnswerIn]


class CompetencyResultOut(BaseModel):
    competency_name: str
    current_score: float
    required_level: float
    gap_value: float
    priority: str


class AssessmentResultOut(BaseModel):
    results: List[CompetencyResultOut]
