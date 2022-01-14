from typing import Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    name: str

class Course(CourseBase):
    name: str
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    courses: list[Course] = []

    class Config:
        orm_mode = True

# class UserInDB(User):
#     hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
