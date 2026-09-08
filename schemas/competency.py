import uuid
from typing import Optional

from pydantic import BaseModel


class CompetencyOut(BaseModel):
    id: uuid.UUID
    name: str
    category: Optional[str]
    required_level: float

    class Config:
        from_attributes = True


class UserCompetencyOut(BaseModel):
    competency: CompetencyOut
    current_score: float

    class Config:
        from_attributes = True


class GapOut(BaseModel):
    competency: CompetencyOut
    gap_value: float
    priority: str

    class Config:
        from_attributes = True
