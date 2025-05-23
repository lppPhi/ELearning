from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RegisteredCourseBase(BaseModel):
    user_id: int
    course_id: int

class RegisteredCourseCreate(RegisteredCourseBase):
    pass

class RegisteredCourseUpdate(BaseModel):
    user_id: Optional[int] = None
    course_id: Optional[int] = None

class RegisteredCourse(RegisteredCourseBase):
    register_id: int
    registration_date: datetime

    class Config:
        orm_mode = True