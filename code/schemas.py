import datetime
from typing import Optional

from pydantic import BaseModel

class TaskAttemptBase(BaseModel):
    answer: str
    task_id: int
    attempt_id: int

class TaskAttempt(TaskAttemptBase):
    id: int

    class Config:
        orm_mode = True        

class AttemptBase(BaseModel):
    username: str
    answer: str
    exercise_id: int

class Attempt(AttemptBase):
    id: int
    date: datetime.datetime

    task_attempts: list[TaskAttempt] = []

    class Config:
        orm_mode = True

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
