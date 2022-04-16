# ===================================================={ all imports }============================================================

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import pandas as pd

from .. import schemas, crud
from ..database import get_db
from ..login import get_current_active_user
from ..models import Exercise, User, Attempt, Course
from ..constants import general_exception, templates

# ==================================================={ global objects }==========================================================

router = APIRouter()  # API router object

# ============================================{ create new course post route }====================================================


@router.post("/", response_model=schemas.Course)
async def add_new_course(
    course: schemas.CourseBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user_id = current_user.id
    try:
        return crud.create_course(db, course, user_id)
    except Exception as e:
        print(e)
        raise general_exception
