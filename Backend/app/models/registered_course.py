from sqlalchemy import Column, Integer, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class RegisteredCourse(Base):
    __tablename__ = 'RegisteredCourses'

    register_id = Column('RegisterID', Integer, primary_key=True, autoincrement=True)
    course_id = Column('CourseID', Integer, ForeignKey('courses.CourseID'), nullable=False)
    user_id = Column('UserID', Integer, ForeignKey('users.UserID'), nullable=False)
    registration_date = Column('RegistrationDate', DateTime, nullable=False)

    # Thiết lập quan hệ ORM
    user = relationship("User", back_populates="registered_courses")
    course = relationship("Course", back_populates="registrations")