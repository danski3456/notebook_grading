from sqlalchemy.orm import Session

from code import models, schemas
from code.security import verify_password, get_password_hash

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_exercise(db: Session, exercise_name: str, course_name: str):
    out = db.query(models.Exercise).filter(
        models.Exercise.name == exercise_name,
        models.Exercise.course_name == course_name
    ).first()
    return out

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

def create_course(db:Session, course: schemas.CourseBase, user_id: int):
    db_item = models.Course(**course.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_exercise(db:Session, exercise: schemas.ExerciseBase):
    db_item = models.Exercise(**exercise.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_task(db:Session, task: schemas.TaskBase):
    db_item = models.Task(**task.dict())
    db_item = db.merge(db_item)
    db.commit()
    # db.refresh(db_item)
    return db_item


def create_attempt(
    db: Session,
    attempt: schemas.Attempt,
    task_attempts: list[schemas.TaskAttempt]
):
    db_attempt = models.Attempt(**attempt.dict())
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    attempt_id = db_attempt.id

    tas = [models.TaskAttempt(
        **ta.dict(),
        attempt_id=db_attempt.id,
        course_name=attempt.course_name,
        exercise_name=attempt.exercise_name,
        ) for ta in task_attempts]
    for ta in tas: db.add(ta)
    db.commit()
    
    return db_attempt 