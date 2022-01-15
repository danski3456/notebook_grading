import os
from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError

from code import crud, models, schemas
from code.models import User
import code.schemas as schemas
import code.http as http
from code.database import SessionLocal, engine, get_db
from code.security import verify_password, create_access_token
from code.login import authenticate_user, get_current_active_user
app = FastAPI()


models.Base.metadata.create_all(bind=engine)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        return crud.create_user(db=db, user=user)
    except Exception as e:
        raise http.general_exception


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# @app.post("/course/", response_model=schemas.Course)
# def add_new_course(
#     course: schemas.CourseBase,
#     current_user: User = Depends(get_current_active_user())
#     ):
    
#     user_id = current_user.id
#     db = get_db()
#     return crud.create_course(db, course, user_id)

@app.post("/course/", response_model=schemas.Course)
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
        raise http.general_exception

@app.post("/exercise/", response_model=schemas.Exercise)
async def add_new_exercise(
    exercise: schemas.ExerciseBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    course_name = exercise.course_name
    user_courses = [c.name for c in current_user.courses]
    print(user_courses, course_name)
    if course_name not in user_courses:
        raise http.unauthorized_exception
    try:
        return crud.create_exercise(db, exercise)
    except Exception as e:
        print(e)
        raise http.general_exception



@app.post("/task/", response_model=schemas.Task)
async def add_new_task(
    task: schemas.TaskBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    exercise_id = task.exercise_id
    exercise = crud.get_exercise(db, exercise_id)
    if exercise is None:
        raise http.general_exception
    if exercise.course.owner_id != current_user.id:
        raise http.unauthorized_exception
    try:
        return crud.create_task(db, task)
    except Exception as e:
        print(e)
        raise http.general_exception

@app.post("/attempt/", response_model=schemas.Attempt)
async def add_new_task(
    attempt: schemas.AttemptBase,
    task_attempts: list[schemas.TaskAttemptBase],
    db: Session = Depends(get_db),
):
    try:
        return crud.create_attempt(db, attempt, task_attempts)
    except Exception as e:
        print(e)
        raise http.general_exception