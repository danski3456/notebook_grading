#===================================================={ all imports }============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..import schemas, crud
from ..constants import general_exception, unauthorized_exception
from ..database import get_db
from ..login import get_current_active_user
from ..security import create_access_token
from ..models import User

#==================================================={ global objects }==========================================================

router = APIRouter()   # API router object

#=================================================={ Task post route }==========================================================

@router.post("/", response_model=schemas.Task)
async def add_new_task(task: schemas.TaskBase,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)
                       ):
    
    exercise_name = task.exercise_name
    course_name = task.course_name
    exercise = crud.get_exercise(db, exercise_name, course_name)
    #print(exercise)
    if exercise is None:
        raise general_exception
    if exercise.course.owner_id != current_user.id:
        raise unauthorized_exception
    try:
        return crud.create_task(db, task)
    except Exception as e:
        #print(e)
        raise general_exception
#======================================================{ Code ends }===========================================================
