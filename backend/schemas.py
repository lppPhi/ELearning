from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    UserName: str
    Email: str
    Phone: Optional[str] = None
    Image: Optional[str] = None

class UserCreate(UserBase):
    Password: str

class UserUpdate(UserBase):
    Password: Optional[str] = None

class UserLogin(BaseModel):
    UserName: str
    Password: str

class UserInfo(UserBase):
    UserID: int
    class Config:
        orm_mode = True

# Course schemas
class CourseBase(BaseModel):
    CourseName: str
    Decription: Optional[str] = None
    IsPublic: Optional[bool] = True
    Price: Optional[float] = 0
    Image: Optional[str] = None

class CourseCreate(CourseBase):
    UserID: int
    DetailCourse: Optional[str] = None

class CourseUpdate(CourseBase):
    DetailCourse: Optional[str] = None

class CourseInfo(CourseBase):
    CourseID: int
    class Config:
        orm_mode = True

class CourseDetail(CourseInfo):
    DetailCourse: Optional[str] = None

# Chapter schemas
class ChapterBase(BaseModel):
    ChapterName: str
    Document: Optional[str] = None

class ChapterCreate(ChapterBase):
    CourseID: int

class ChapterUpdate(ChapterBase):
    pass

class ChapterInfo(ChapterBase):
    ChapterID: int
    class Config:
        orm_mode = True

# Part schemas
class PartBase(BaseModel):
    PartName: str
    Document: Optional[str] = None

class PartCreate(PartBase):
    ChapterID: int

class PartUpdate(PartBase):
    pass

class PartInfo(PartBase):
    PartID: int
    class Config:
        orm_mode = True

# RegisteredCourse schemas
class RegisteredCourseCreate(BaseModel):
    CourseID: int
    UserID: int

class RegisteredCourseInfo(BaseModel):
    RegisterID: int
    CourseID: int
    UserID: int
    RegistrationDate: datetime
    class Config:
        orm_mode = True
