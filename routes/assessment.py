from collections import defaultdict
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.question import Question
from app.models.competency import Competency, UserCompetency, CompetencyGap
from app.models.user import User
from app.schemas.assessment import (
    AssessmentQuestionOut,
    AssessmentSubmission,
    AssessmentResultOut,
    CompetencyResultOut,
)
from app.auth.dependencies import get_current_user
from app.services.competency_engine import classify_gap

router = APIRouter()


@router.get("/initial", response_model=List[AssessmentQuestionOut])
def get_initial_assessment(db: Session = Depends(get_db)):
    """Returns every seeded question, without revealing the correct answer."""
    return db.query(Question).filter(Question.is_ai_generated.is_(False)).all()


@router.post("/submit", response_model=AssessmentResultOut)
def submit_assessment(
    payload: AssessmentSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    questions = db.query(Question).filter(Question.is_ai_generated.is_(False)).all()
    answers_by_question = {str(a.question_id): a.selected_option for a in payload.answers}

    by_competency = defaultdict(list)
    for q in questions:
        by_competency[str(q.competency_id)].append(q)

    results = []
    for competency_id, comp_questions in by_competency.items():
        total = len(comp_questions)
        correct = sum(
            1
            for q in comp_questions
            if answers_by_question.get(str(q.id)) == q.correct_option_index
        )
        score = round((correct / total) * 100, 1) if total else 0.0

        competency = db.query(Competency).filter(Competency.id == competency_id).first()
        gap_value, priority = classify_gap(score, competency.required_level)

        # Save or update the user's score for this competency
        user_competency = (
            db.query(UserCompetency)
            .filter(
                UserCompetency.user_id == current_user.id,
                UserCompetency.competency_id == competency_id,
            )
            .first()
        )
        if user_competency:
            user_competency.current_score = score
        else:
            db.add(
                UserCompetency(
                    user_id=current_user.id,
                    competency_id=competency_id,
                    current_score=score,
                )
            )

        # Save a gap snapshot so the admin dashboard can show history later
        db.add(
            CompetencyGap(
                user_id=current_user.id,
                competency_id=competency_id,
                gap_value=gap_value,
                priority=priority,
            )
        )

        results.append(
            CompetencyResultOut(
                competency_name=competency.name,
                current_score=score,
                required_level=competency.required_level,
                gap_value=gap_value,
                priority=priority,
            )
        )

    db.commit()

    # Largest gaps first, so the biggest priorities surface at the top
    results.sort(key=lambda r: r.gap_value, reverse=True)
    return AssessmentResultOut(results=results)
