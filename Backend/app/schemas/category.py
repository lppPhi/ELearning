from pydantic import BaseModel

class CategoryBase(BaseModel):
    course_id: int
    category_name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    category_name: str

class Category(CategoryBase):
    category_id: int

    class Config:
        orm_mode = True