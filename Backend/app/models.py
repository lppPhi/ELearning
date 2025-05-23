from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RegisteredCourse(Base):
    __tablename__ = 'RegisteredCourses'  # Đúng tên bảng

    RegisterID = Column(Integer, primary_key=True, autoincrement=True)
    CourseID = Column(Integer, nullable=False)
    UserID = Column(Integer, nullable=False)
    RegistrationDate = Column(DateTime, nullable=False)