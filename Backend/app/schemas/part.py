from pydantic import BaseModel
from typing import Optional

class PartBase(BaseModel):
    chapter_id: int
    part_name: str
    document: Optional[str] = None

class PartCreate(PartBase):
    pass

class PartUpdate(BaseModel):
    part_name: Optional[str] = None
    document: Optional[str] = None

class Part(PartBase):
    part_id: int

    class Config:
        orm_mode = True