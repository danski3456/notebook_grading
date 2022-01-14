from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Datetime
from sqlalchemy.orm import relationship

from code.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    courses = relationship("Course", back_populates="owner")
    # items = relationship("Item", back_populates="owner")

class Course(Base):
    __tablename__ = "courses"
    
    name = Column(String, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="courses")
    exercises = relationship("Exercise", back_populates="course")

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    course_name = Column(String, ForeignKey("courses.name"))
    course = relationship("Course", back_populates="exercises")
    tasks = relationship("Task", back_populates="exercise")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    task_answer = Column(String)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    exercise = relationship("Exercise", back_populates="tasks")

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
     = Column(String)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    exercise = relationship("Exercise", back_populates="tasks")
