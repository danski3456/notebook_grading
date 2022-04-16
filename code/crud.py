# ===================================================={ all imports }============================================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from . import models, schemas
from .security import verify_password, get_password_hash

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

# =============================================={ get_user_by_email function }====================================================


def get_user_by_email(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_course(db: Session, course_name: str):
    return db.query(models.Course).filter(models.Course.name == course_name).one()


# ================================================={ get_exercise function }======================================================


def get_exercise(db: Session, exercise_name: str, course_name: str):
    out = (
        db.query(models.Exercise)
        .filter(
            models.Exercise.name == exercise_name,
            models.Exercise.course_name == course_name,
        )
        .one()
    )
    return out


def get_task(db: Session, name: str, exercise_name: str, course_name: str):
    out = (
        db.query(models.Task)
        .filter(
            models.Task.name == name,
            models.Task.exercise_name == exercise_name,
            models.Task.course_name == course_name,
        )
        .one()
    )
    return out


def get_task(db: Session, name: str, exercise_name: str, course_name: str):
    out = (
        db.query(models.Task)
        .filter(
            models.Task.name == name,
            models.Task.exercise_name == exercise_name,
            models.Task.course_name == course_name,
        )
        .one()
    )
    return out


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

# =================================================={ create_user function }======================================================


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

# ==============================================={ create_course function }======================================================


def create_course(db: Session, course: schemas.CourseBase, user_id: int):
    db_item = models.Course(**course.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ==============================================={ create_exercise function }====================================================


def create_exercise(db: Session, exercise: schemas.ExerciseBase):
    db_item = models.Exercise(**exercise.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ================================================={ create_task function }======================================================


def create_task(db: Session, task: schemas.TaskBase):
    db_item = models.Task(**task.dict())
    db_item = db.merge(db_item)
    db.commit()
    # db.refresh(db_item)
    return db_item


# ==============================================={ create_attempt function }=====================================================


def create_attempt(
    db: Session, attempt: schemas.Attempt, task_attempts: list[schemas.TaskAttempt]
):
    db_attempt = models.Attempt(**attempt.dict())
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    attempt_id = db_attempt.id

    tas = [
        models.TaskAttempt(
            **ta.dict(),
            attempt_id=db_attempt.id,
            course_name=attempt.course_name,
            exercise_name=attempt.exercise_name,
        )
        for ta in task_attempts
    ]
    for ta in tas:
        db.add(ta)
    db.commit()

    return db_attempt


# ================================================={ delete_user function }======================================================


def delete_user(db: Session, user_id: int):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).one()
        db.delete(user)
        db.commit()
        return True
    except Exception as e:
        return False


# ================================================{ delete_course function }=====================================================
def delete_course(db: Session, course_name: str, user_id: int):
    # finding the course of current user by course name
    current_course = (
        db.query(models.Course)
        .filter(models.Course.name == course_name, models.Course.owner_id == user_id)
        .first()
    )

    # course not found returning error
    if not current_course:
        return HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Course with name {course_name} not found",
        )

    # if course exists deleting all the exercises
    db.query(models.Exercise).filter(models.Exercise.course == current_course).delete()

    # deleting the course
    db.delete(current_course)
    db.commit()

    return {"detail": f"Course with name {course_name} deleted successfully"}


# ====================================================={ Code ends here }========================================================
