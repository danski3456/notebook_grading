#===================================================={ all imports }============================================================

from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from ..constants import general_exception, templates
from .. import crud, schemas
from ..database import get_db
from ..login import get_current_active_user
from ..models import User


#==================================================={ global objects }==========================================================

router = APIRouter()   # API router object

#========================================={ User get route return html page }===================================================

@router.get("/")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('new_user.html', context={'request': request, 'result': result})

#==========================================={ create new user in database }=====================================================

@router.post("/", response_model=schemas.User)
def create_user(db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
    
    user = schemas.UserCreate(username=username, password=password)
    db_user = crud.get_user_by_email(db, username=user.username)
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        return crud.create_user(db=db, user=user)
    except Exception as e:
        raise general_exception

#======================================{ get the current active user route }===================================================

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

#======================================={ delete current active user route }===================================================

@router.delete("/")
async def delete_current_active_user(current_user: User = Depends(get_current_active_user), db:Session = Depends(get_db)):
    if(crud.delete_user(db, current_user.id)):
        return {"detail": f"User with id {current_user.id} is deleted"}
    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User is not deleted")

#======================================================{ Code ends }===========================================================
