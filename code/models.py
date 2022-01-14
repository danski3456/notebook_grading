from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
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
    owner_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    owner = relationship("User", back_populates="courses")

# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
