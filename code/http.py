from fastapi import HTTPException, status

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