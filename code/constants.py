#===================================================={ all imports }============================================================

from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates

#====================================================={ all objects }===========================================================

general_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong",
        headers={"WWW-Authenticate": "Bearer"},
    )

unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

templates = Jinja2Templates(directory="./code/templates")

#====================================================={ Code ends here }========================================================

