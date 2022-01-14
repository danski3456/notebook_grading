from typing import Optional

from pydantic import BaseModel

class TaskBase(BaseModel):
    task_name: str
    task_answer: str
    exercise_id: int

class Task(TaskBase):
    id: int
    
    class Config:
        orm_mode = True


class ExerciseBase(BaseModel):
    name: str
    course_name: str

class Exercise(ExerciseBase):
    id: int
    tasks: list[Task] = []
    
    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    name: str

class Course(CourseBase):
    owner_id: int
    exercises: list[Exercise] = []

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
