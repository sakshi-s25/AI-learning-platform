"""
Endpoint for viewing personalized recommendations — regenerates them from
the latest gaps every time it's called, so it's always up to date.
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.recommendation import RecommendationOut
from app.auth.dependencies import get_current_user
from app.services.recommendation_engine import generate_recommendations

router = APIRouter()


@router.get("/me", response_model=List[RecommendationOut])
def my_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recommendations = generate_recommendations(db, current_user.id)
    return [
        RecommendationOut(
            competency_name=rec.competency.name,
            course=rec.course,
            reason_text=rec.reason_text,
        )
        for rec in recommendations
    ]
