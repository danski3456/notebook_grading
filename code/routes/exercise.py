#===================================================={ all imports }============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db
from ..login import get_current_active_user
from ..models import User
from ..constants import unauthorized_exception, general_exception

#==================================================={ global objects }==========================================================

router = APIRouter()   # API router object

#============================================{ Add new exercise post route }====================================================

@router.post("/", response_model=schemas.Exercise)
async def add_new_exercise(exercise: schemas.ExerciseBase, 
                           db: Session = Depends(get_db), 
                           current_user: User = Depends(get_current_active_user)
                           ):
    
    course_name = exercise.course_name
    user_courses = [c.name for c in current_user.courses]
    #print(user_courses, course_name)
    
    if course_name not in user_courses:
        raise unauthorized_exception
    try:
        return crud.create_exercise(db, exercise)
    except Exception as e:
        #print(e)
        raise general_exception
    
#======================================================{ Code ends }===========================================================
