import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, ForeignKeyConstraint
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

    @hybrid_property
    def total_points(self):
        return sum(ex.total_points for ex in self.exercises)

class Exercise(Base):
    __tablename__ = "exercises"
    
    #id = Column(Integer, primary_key=True, index=True)
    name = Column(String, primary_key=True)
    course_name = Column(String, ForeignKey("courses.name"), primary_key=True)
    course = relationship("Course", back_populates="exercises")
    tasks = relationship("Task", back_populates="exercise")

    attempts = relationship("Attempt", back_populates="exercise")
    @hybrid_property
    def total_points(self):
        return sum(1 if not t.disabled else 0 for t in self.tasks)

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        ForeignKeyConstraint(["exercise_name", "course_name"], ["exercises.name", "exercises.course_name"]),
    )
    #id = Column(Integer, primary_key=True, index=True)
    name = Column(String, primary_key=True)
    exercise_name = Column(String, primary_key=True)
    course_name = Column(String, primary_key=True)
    answer = Column(String)
    disabled = Column(Boolean, default=False)
    exercise = relationship("Exercise", back_populates="tasks")

    task_attempts = relationship("TaskAttempt", back_populates="task")

class Attempt(Base):
    __tablename__ = "attempts"
    __table_args__ = (
        ForeignKeyConstraint(["exercise_name", "course_name"], ["exercises.name", "exercises.course_name"]),
    )

    id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String)
    course_name = Column(String)
    username = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    exercise = relationship("Exercise", back_populates="attempts")

    task_attempts = relationship("TaskAttempt", back_populates="attempt")

    @hybrid_property
    def total_correct(self):
        return sum(ta.is_correct for ta in self.task_attempts if not ta.task.disabled)

    @hybrid_property
    def total_enabled(self):
        return sum(1 for ta in self.task_attempts if not ta.task.disabled)


class TaskAttempt(Base):
    __tablename__ = "task_attempts"
    __table_args__ = (
        ForeignKeyConstraint(
            ["name", "exercise_name", "course_name"],
            ["tasks.name", "tasks.exercise_name", "tasks.course_name"]
        ),
    )
    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String)
    name = Column(String, nullable=False)
    exercise_name = Column(String, nullable=False)
    course_name = Column(String, nullable=False)
    task = relationship("Task", back_populates="task_attempts") 

    attempt_id = Column(Integer, ForeignKey("attempts.id"))
    attempt = relationship("Attempt", back_populates="task_attempts")

    @hybrid_property
    def is_correct(self):
        return self.answer == self.task.answer 
