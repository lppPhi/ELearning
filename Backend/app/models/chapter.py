from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Chapter(Base):
    __tablename__ = 'chapters'

    chapter_id = Column('ChapterID', Integer, primary_key=True, index=True)
    course_id = Column('CourseID', Integer, ForeignKey('courses.CourseID'))
    chapter_name = Column('ChapterName', String, index=True)
    document = Column('Document', Text)

    course = relationship("Course", back_populates="chapters")
    parts = relationship("Part", back_populates="chapter")