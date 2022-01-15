import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

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

    attempts = relationship("Attempt", back_populates="exercise")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    task_answer = Column(String)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    exercise = relationship("Exercise", back_populates="tasks")

    task_attempts = relationship("TaskAttempt", back_populates="task")

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    exercise = relationship("Exercise", back_populates="attempts")

    task_attempts = relationship("TaskAttempt", back_populates="attempt")

    @hybrid_property
    def total_correct(self):
        return sum(ta.is_correct for ta in self.task_attempts)


class TaskAttempt(Base):
    __tablename__ = "task_attempts"
    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="task_attempts") 

    attempt_id = Column(Integer, ForeignKey("attempts.id"))
    attempt = relationship("Attempt", back_populates="task_attempts")

    @hybrid_property
    def is_correct(self):
        return self.answer == self.task.task_answer 
