from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate

def create_course(db: Session, course: CourseCreate):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.course_id == course_id).first()

def get_courses(db: Session, skip: int = 0, limit: int = 10):
    # MSSQL requires an order_by when using offset/limit
    return db.query(Course).order_by(Course.course_id).offset(skip).limit(limit).all()

def update_course(db: Session, course_id: int, course: CourseUpdate):
    db_course = db.query(Course).filter(Course.course_id == course_id).first()
    if db_course:
        for key, value in course.dict(exclude_unset=True).items():
            setattr(db_course, key, value)
        db.commit()
        db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    db_course = db.query(Course).filter(Course.course_id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
    return db_course