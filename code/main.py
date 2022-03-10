import os
from typing import Optional
from datetime import datetime, timedelta

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from sqlalchemy import func, and_

from jose import JWTError

from code import crud, models, schemas
from code.models import User
import code.schemas as schemas
import code.http as http
from code.database import SessionLocal, engine, get_db
from code.security import verify_password, create_access_token
from code.login import authenticate_user, get_current_active_user
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="code/templates")

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

@app.get("/users/")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('new_user.html', context={'request': request, 'result': result})


@app.post("/users/", response_model=schemas.User)
def create_user(
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...)
    ):
    user = schemas.UserCreate(username=username, password=password)
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
    exercise_name = task.exercise_name
    course_name = task.course_name
    exercise = crud.get_exercise(db, exercise_name, course_name)
    print(exercise)
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


#@app.get("/course/{course_name}/{username}")#, response_model=list[schemas.Attempt])
def form_post(
    username: str,
    course_name: str,
    request: Request,
    db: Session = Depends(get_db)
    ):


    subq = db.query(
        models.Attempt.exercise_name,
        models.Attempt.course_name,
        func.max(models.Attempt.date).label('maxdate')
    ).group_by(models.Attempt.exercise_name, models.Attempt.course_name).subquery('t2')

    query = db.query(models.Attempt).join(
        subq,
        and_(
            models.Attempt.exercise_name == subq.c.exercise_name,
            models.Attempt.course_name == subq.c.course_name,
            models.Attempt.date == subq.c.maxdate
        )
    ).all()
    # return query

    response = []
    for attempt in query:
        for task in attempt.task_attempts:
            row = {
                "course": attempt.course_name,
                "exercise": attempt.exercise_name,
                "task": task.name,
                "is_correct": task.is_correct,
            }
            response.append(row)
    return templates.TemplateResponse(
        'course_student.html', 
        context={
            'request': request,
            'items': query,
            # 'student': username,
        })

    return response


@app.get("/course/{course_name}")#, response_model=list[schemas.Attempt])
def course_stats(
    course_name: str,
    request: Request,
    db: Session = Depends(get_db)
    ):



    # course = db.query(models.Course).filter(models.Course.name == course_name).first()

    subq = db.query(
        models.Attempt.username,
        models.Attempt.exercise_name,
        models.Attempt.course_name,
        func.max(models.Attempt.date).label('maxdate')
    ).group_by(
        models.Attempt.exercise_name,
        models.Attempt.course_name,
        models.Attempt.username
    ).subquery('t2')

    query = db.query(models.Attempt).join(
        subq,
        and_(
            models.Attempt.exercise_name == subq.c.exercise_name,
            models.Attempt.course_name == subq.c.course_name,
            models.Attempt.date == subq.c.maxdate,
            models.Attempt.username == subq.c.username,
        )
    ).all()


    response = []
    for attempt in query:
        row = {}
        row["Username"] = attempt.username
        row["Exercise"] = attempt.exercise_name
        row["# Correct"] = attempt.total_correct
        row["# Total"] = attempt.total_enabled
        row["Last Attempt Date"] = attempt.date
        response.append(row)
        # for task in attempt.task_attempts:
        #     row = {
        #         "course": attempt.course_name,
        #         "exercise": attempt.exercise_name,
        #         "task": task.name,
        #         "is_correct": task.is_correct,
        #     }
        #     response.append(row)

    return templates.TemplateResponse(
        'course_stats.html', 
        context={
            'request': request,
            'items': response,
            # 'student': username,
        })

@app.get("/course/{course_name}/summary")#, response_model=list[schemas.Attempt])
def course_stats(
    course_name: str,
    request: Request,
    db: Session = Depends(get_db)
    ):



    course = db.query(models.Course).filter(models.Course.name == course_name).first()

    subq = db.query(
        models.Attempt.username,
        models.Attempt.exercise_name,
        models.Attempt.course_name,
        func.max(models.Attempt.date).label('maxdate')
    ).group_by(
        models.Attempt.exercise_name,
        models.Attempt.course_name,
        models.Attempt.username
    ).subquery('t2')

    query = db.query(models.Attempt).join(
        subq,
        and_(
            models.Attempt.exercise_name == subq.c.exercise_name,
            models.Attempt.course_name == subq.c.course_name,
            models.Attempt.date == subq.c.maxdate,
            models.Attempt.username == subq.c.username,
        )
    ).all()



    response = []
    for attempt in query:
        row = {}
        # students[attempt.username] += attempt.total_correct
        row["Username"] = attempt.username
        row["Exercise"] = f"{attempt.exercise_name} (/{attempt.total_enabled})"
        row["# Correct"] = attempt.total_correct
        row["# Total"] = attempt.total_enabled
        row["Last Attempt Date"] = attempt.date
        response.append(row)
    # response = {"students": students, "total": course.total_points}

    df = pd.DataFrame(response)
    df = pd.pivot(df, index="Username", columns="Exercise", values="# Correct")
    df = df.fillna(0).astype(int)
    df["Obtained Points"] = df.sum(axis=1)
    df["Maximum Available Points"] = course.total_points
    df["Final Grade"] = (df["Obtained Points"] / df["Maximum Available Points"]).apply(lambda x: f"{x * 100:.0f} %")
    

    return templates.TemplateResponse(
        'course_summary.html', 
        context={
            'request': request,
            'items': df.to_html(),
            # 'student': username,
        })
