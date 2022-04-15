#===================================================={ all imports }============================================================

import datetime
from pydantic import BaseModel
from typing import Optional

#==================================================={ Task schemas }============================================================

class TaskAttemptBase(BaseModel):
    answer: str
    name: str

class TaskAttempt(TaskAttemptBase):
    id: int
    attempt_id: int
    is_correct: bool

    class Config:
        orm_mode = True        

class AttemptBase(BaseModel):
    username: str
    exercise_name: str
    course_name: str


class Attempt(AttemptBase):
    id: int
    date: datetime.datetime
    total_correct: int
    total_enabled: int

    task_attempts: list[TaskAttempt] = []

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    name: str
    answer: str
    exercise_name: str
    course_name: str
    disabled: Optional[bool] = False

class Task(TaskBase):
    
    class Config:
        orm_mode = True

#================================================={ Exercise schemas }==========================================================

class ExerciseBase(BaseModel):
    name: str
    course_name: str

class Exercise(ExerciseBase):
    tasks: list[Task] = []
    
    class Config:
        orm_mode = True

#=================================================={ Course schemas }===========================================================

class CourseBase(BaseModel):
    name: str

class Course(CourseBase):
    owner_id: int
    exercises: list[Exercise] = []

    class Config:
        orm_mode = True

#==================================================={ User schemas }============================================================

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

#=================================================={ Token schemas }===========================================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

#=================================================={ Code ends here }==========================================================
