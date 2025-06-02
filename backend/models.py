from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.mssql import NVARCHAR, NTEXT

class User(Base):
    __tablename__ = "Users"
    UserID = Column(Integer, primary_key=True, index=True)
    UserName = Column(String(100), nullable=False)
    Email = Column(String(100), nullable=False, unique=True)
    Phone = Column(String(20))
    Image = Column(String)
    Password = Column(String(255), nullable=False)
    courses = relationship("Course", back_populates="user")
    registered_courses = relationship("RegisteredCourse", back_populates="user")

class Course(Base):
    __tablename__ = "Courses"
    CourseID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    CourseName = Column(String(200), nullable=False)
    Decription = Column(String)
    DetailCourse = Column(String)
    IsPublic = Column(Boolean, default=True)
    Price = Column(DECIMAL(10,2), default=0)
    NumberOfRegistrations = Column(Integer, default=0)
    Image = Column(String)
    user = relationship("User", back_populates="courses")
    chapters = relationship("Chapter", back_populates="course")
    registered_courses = relationship("RegisteredCourse", back_populates="course")

class Chapter(Base):
    __tablename__ = "Chapters"
    ChapterID = Column(Integer, primary_key=True, index=True)
    CourseID = Column(Integer, ForeignKey("Courses.CourseID"), nullable=False)
    ChapterName = Column(String(200), nullable=False)
    Document = Column(String)
    course = relationship("Course", back_populates="chapters")
    parts = relationship("Part", back_populates="chapter")

class Part(Base):
    __tablename__ = "Parts"
    PartID = Column(Integer, primary_key=True, index=True)
    ChapterID = Column(Integer, ForeignKey("Chapters.ChapterID"), nullable=False)
    PartName = Column(String(200), nullable=False)
    Document = Column(String)
    chapter = relationship("Chapter", back_populates="parts")

class RegisteredCourse(Base):
    __tablename__ = "RegisteredCourses"
    RegisterID = Column(Integer, primary_key=True, index=True)
    CourseID = Column(Integer, ForeignKey("Courses.CourseID"), nullable=False)
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    RegistrationDate = Column(DateTime)
    course = relationship("Course", back_populates="registered_courses")
    user = relationship("User", back_populates="registered_courses")
