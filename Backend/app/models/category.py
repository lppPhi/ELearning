from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column('CategoryID', Integer, primary_key=True, index=True)
    course_id = Column('CourseID', Integer, ForeignKey('courses.CourseID'))
    category_name = Column('CategoryName', String, index=True)

    course = relationship("Course", back_populates="categories")