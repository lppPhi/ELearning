from pydantic import BaseModel
from typing import Optional

class ChapterBase(BaseModel):
    course_id: int
    chapter_name: str
    document: Optional[str] = None

class ChapterCreate(ChapterBase):
    pass

class ChapterUpdate(BaseModel):
    chapter_name: Optional[str] = None
    document: Optional[str] = None

class Chapter(ChapterBase):
    chapter_id: int

    class Config:
        orm_mode = True