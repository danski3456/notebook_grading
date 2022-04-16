#===================================================={ all imports }============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..constants import general_exception
from ..database import get_db

#==================================================={ global objects }==========================================================

router = APIRouter()   # API router object

#================================================{ attempt post route }==========================================================

@router.post("/", response_model=schemas.Attempt)
async def add_new_task(
    attempt: schemas.AttemptBase,
    task_attempts: list[schemas.TaskAttemptBase],
    db: Session = Depends(get_db)
    ):
    
    try:
        return crud.create_attempt(db, attempt, task_attempts)
    except Exception as e:
        print(e)
        raise general_exception
    
#======================================================{ Code ends }===========================================================
