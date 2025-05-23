from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    course_name: str
    description: Optional[str] = None
    detail_course: Optional[str] = None
    is_free: Optional[bool] = None
    is_public: Optional[bool] = None
    number_of_registrations: Optional[int] = None
    evaluate: Optional[float] = None
    user_id: Optional[int] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    description: Optional[str] = None
    detail_course: Optional[str] = None
    is_free: Optional[bool] = None
    is_public: Optional[bool] = None
    number_of_registrations: Optional[int] = None
    evaluate: Optional[float] = None
    user_id: Optional[int] = None

class Course(CourseBase):
    course_id: int

    class Config:
        orm_mode = True