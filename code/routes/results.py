# ===================================================={ all imports }============================================================

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import pandas as pd

from .. import schemas, crud
from ..database import get_db
from ..login import get_current_active_user
from ..models import Exercise, User, Attempt, Course

from .. import models
from ..constants import general_exception, templates

from collections import defaultdict

# ==================================================={ global objects }==========================================================

router = APIRouter()  # API router object


def get_most_recent_attempts(db):
    subq = (
        db.query(
            Attempt.username,
            Attempt.exercise_name,
            Attempt.course_name,
            func.max(Attempt.date).label("maxdate"),
        )
        .group_by(Attempt.exercise_name, Attempt.course_name, Attempt.username)
        .subquery("t2")
    )

    query = db.query(Attempt).join(
        subq,
        and_(
            Attempt.exercise_name == subq.c.exercise_name,
            Attempt.course_name == subq.c.course_name,
            Attempt.date == subq.c.maxdate,
            Attempt.username == subq.c.username,
        ),
    )
    return query


@router.get("/{course_name}/{student_name}")  # , response_model=list[schemas.Attempt])
def course_stats(
    course_name: str, student_name: str, request: Request, db: Session = Depends(get_db)
):

    course = db.query(models.Course).filter(models.Course.name == course_name).one()

    recent_attempts = (
        get_most_recent_attempts(db)
        .filter(Attempt.course_name == course_name, Attempt.username == student_name)
        .all()
    )

    results = {}
    for ra in recent_attempts:
        results[ra.exercise_name] = {
            "correct": ra.total_correct,
            "total": ra.total_enabled,
        }

    # Add untried exercises
    for ex in course.exercises:
        if ex.name not in results:
            results[ex.name] = {"correct": 0, "total": ex.total_points}

    return results


@router.get("/{course_name}")  # , response_model=list[schemas.Attempt])
def course_stats(
    course_name: str,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):

    course = db.query(models.Course).filter(models.Course.name == course_name).one()

    assert course.owner_id == user.id

    recent_attempts = (
        get_most_recent_attempts(db).filter(Attempt.course_name == course_name).all()
    )

    results = defaultdict(dict)
    for ra in recent_attempts:
        student_name = ra.username

        results[student_name][ra.exercise_name] = {
            "correct": ra.total_correct,
            "total": ra.total_enabled,
        }

    # Add untried exercises
    for ex in course.exercises:
        for student in results.keys():
            if ex.name not in results[student]:
                results[student][ex.name] = {"correct": 0, "total": ex.total_points}

    return results
