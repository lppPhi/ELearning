from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column('UserID', Integer, primary_key=True, index=True)
    full_name = Column('FullName', String, index=True)
    email = Column('Email', String, unique=True, index=True)
    password = Column('Password', String)

    courses = relationship("Course", back_populates="user")
    registered_courses = relationship("RegisteredCourse", back_populates="user")