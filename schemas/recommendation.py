"""
API-facing shape for a recommendation the learner sees on their dashboard.
"""

import uuid
from typing import Optional

from pydantic import BaseModel


class CourseOut(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    resource_url: Optional[str]
    difficulty: str

    class Config:
        from_attributes = True


class RecommendationOut(BaseModel):
    competency_name: str
    course: CourseOut
    reason_text: str
