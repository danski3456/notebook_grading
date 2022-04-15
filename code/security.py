#===================================================={ all imports }============================================================

from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

#==================================================={ global objects }==========================================================

ALGORITHM = "HS256"
# SECRET = os.getenv("SECRET")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#==============================================={ verify_password function }====================================================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#=============================================={ get_password_hash function }===================================================

def get_password_hash(password):
    return pwd_context.hash(password)

#================================================{ decode_token function }======================================================

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      
#============================================={ create_access_token function }==================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=120)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#==================================================={ code ends here }==========================================================
