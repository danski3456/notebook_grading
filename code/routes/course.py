#===================================================={ all imports }============================================================

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import pandas as pd

from .. import schemas, crud
from ..database import get_db
from ..login import get_current_active_user
from ..models import Exercise, User, Attempt, Course
from ..constants import general_exception, templates

#==================================================={ global objects }==========================================================

router = APIRouter()   # API router object

#============================================{ create new course post route }====================================================

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

#================================================={ get course by name }========================================================

@router.get("/{course_name}")#, response_model=list[schemas.Attempt])
def course_stats(course_name: str, request: Request, db: Session = Depends(get_db)):
    
    # course = db.query(models.Course).filter(models.Course.name == course_name).first()

    subq = db.query(
        Attempt.username,
        Attempt.exercise_name,
        Attempt.course_name,
        func.max(Attempt.date).label('maxdate')
    ).group_by(
        Attempt.exercise_name,
        Attempt.course_name,
        Attempt.username
    ).subquery('t2')

    query = db.query(Attempt).join(
        subq,
        and_(
            Attempt.exercise_name == subq.c.exercise_name,
            Attempt.course_name == subq.c.course_name,
            Attempt.date == subq.c.maxdate,
            Attempt.username == subq.c.username,
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
    
#=============================================={ get course summary route }======================================================

@router.get("/{course_name}/summary")#, response_model=list[schemas.Attempt])
def course_stats(course_name: str, request: Request, db: Session = Depends(get_db)):

    course = db.query(Course).filter(Course.name == course_name).first()

    subq = db.query(
        Attempt.username,
        Attempt.exercise_name,
        Attempt.course_name,
        func.max(Attempt.date).label('maxdate')
    ).group_by(
        Attempt.exercise_name,
        Attempt.course_name,
        Attempt.username
    ).subquery('t2')

    query = db.query(Attempt).join(
        subq,
        and_(
            Attempt.exercise_name == subq.c.exercise_name,
            Attempt.course_name == subq.c.course_name,
            Attempt.date == subq.c.maxdate,
            Attempt.username == subq.c.username,
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

#============================================={ delete the course route }=========================================================

@router.delete("/{course_name}")
async def delete_course(course_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return crud.delete_course(db, course_name, current_user.id)

#============================================{ get course by usersname route }====================================================

#@app.get("/{course_name}/{username}")#, response_model=list[schemas.Attempt])
def form_post(username: str, course_name: str, request: Request, db: Session = Depends(get_db)):

    subq = db.query(
        Attempt.exercise_name,
        Attempt.course_name,
        func.max(Attempt.date).label('maxdate')
    ).group_by(Attempt.exercise_name, Attempt.course_name).subquery('t2')

    query = db.query(Attempt).join(
        subq,
        and_(
            Attempt.exercise_name == subq.c.exercise_name,
            Attempt.course_name == subq.c.course_name,
            Attempt.date == subq.c.maxdate
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

#======================================================{ Code ends }=============================================================
