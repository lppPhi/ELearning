from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Course(Base):
    __tablename__ = 'courses'

    course_id = Column('CourseID', Integer, primary_key=True, index=True)
    course_name = Column('CourseName', String, index=True)
    description = Column('Description', Text)
    detail_course = Column('DetailCourse', Text)
    is_free = Column('IsFree', Boolean, default=False)
    is_public = Column('IsPublic', Boolean, default=True)
    number_of_registrations = Column('NumberOfRegistrations', Integer, default=0)
    evaluate = Column('Evaluate', Float, default=0.0)
    user_id = Column('UserID', Integer, ForeignKey('users.UserID'))
    # image_url = Column('ImageUrl', String, nullable=True)

    user = relationship("User", back_populates="courses")
    chapters = relationship("Chapter", back_populates="course")
    registrations = relationship("RegisteredCourse", back_populates="course")
    categories = relationship("Category", back_populates="course")