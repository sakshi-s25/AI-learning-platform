from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.competency import Competency, UserCompetency
from app.models.user import User
from app.schemas.competency import CompetencyOut, UserCompetencyOut
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=List[CompetencyOut])
def list_competencies(db: Session = Depends(get_db)):
    return db.query(Competency).all()


@router.get("/me", response_model=List[UserCompetencyOut])
def my_competencies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(UserCompetency)
        .filter(UserCompetency.user_id == current_user.id)
        .all()
    )
