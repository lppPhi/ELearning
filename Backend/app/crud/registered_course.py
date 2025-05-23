from sqlalchemy.orm import Session
from app.models.registered_course import RegisteredCourse
from app.schemas.registered_course import RegisteredCourseCreate, RegisteredCourseUpdate
from datetime import datetime

def create_registered_course(db: Session, registered_course: RegisteredCourseCreate):
    data = registered_course.dict()
    # Gán registration_date nếu chưa có
    if "registration_date" not in data or data["registration_date"] is None:
        data["registration_date"] = datetime.utcnow()
    db_registered_course = RegisteredCourse(**data)
    db.add(db_registered_course)
    db.commit()
    db.refresh(db_registered_course)
    return db_registered_course

def get_registered_course(db: Session, registered_course_id: int):
    return db.query(RegisteredCourse).filter(RegisteredCourse.register_id == registered_course_id).first()

def get_registered_courses(db: Session, skip: int = 0, limit: int = 100):
    # MSSQL requires an order_by when using offset/limit
    return db.query(RegisteredCourse).order_by(RegisteredCourse.register_id).offset(skip).limit(limit).all()

def update_registered_course(db: Session, registered_course_id: int, registered_course: RegisteredCourseUpdate):
    db_registered_course = db.query(RegisteredCourse).filter(RegisteredCourse.register_id == registered_course_id).first()
    if db_registered_course:
        for key, value in registered_course.dict(exclude_unset=True).items():
            setattr(db_registered_course, key, value)
        db.commit()
        db.refresh(db_registered_course)
    return db_registered_course

def delete_registered_course(db: Session, registered_course_id: int):
    db_registered_course = db.query(RegisteredCourse).filter(RegisteredCourse.register_id == registered_course_id).first()
    if db_registered_course:
        db.delete(db_registered_course)
        db.commit()
    return db_registered_course