from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

# USERS

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def get_user_basic(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.UserID == user_id).first()

def get_user_login(db: Session, username: str):
    return db.query(models.User).filter(models.User.UserName == username).first()

# COURSES

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, course_id: int, course: schemas.CourseUpdate):
    db_course = db.query(models.Course).filter(models.Course.CourseID == course_id).first()
    if db_course:
        for key, value in course.dict(exclude_unset=True).items():
            setattr(db_course, key, value)
        db.commit()
        db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    # Only delete if not registered
    reg = db.query(models.RegisteredCourse).filter(models.RegisteredCourse.CourseID == course_id).first()
    if reg:
        return None
    db_course = db.query(models.Course).filter(models.Course.CourseID == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
    return db_course

def get_course_basic(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.CourseID == course_id).first()

def get_course_detail(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.CourseID == course_id).first()

def get_course_creator_info(db: Session, course_id: int):
    course = db.query(models.Course).filter(models.Course.CourseID == course_id).first()
    if course:
        return db.query(models.User).filter(models.User.UserID == course.UserID).first()
    return None

def get_all_courses(db: Session):
    return db.query(models.Course).all()

# CHAPTERS

def create_chapter(db: Session, chapter: schemas.ChapterCreate):
    db_chapter = models.Chapter(**chapter.dict())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

def update_chapter(db: Session, chapter_id: int, chapter: schemas.ChapterUpdate):
    db_chapter = db.query(models.Chapter).filter(models.Chapter.ChapterID == chapter_id).first()
    if db_chapter:
        for key, value in chapter.dict(exclude_unset=True).items():
            setattr(db_chapter, key, value)
        db.commit()
        db.refresh(db_chapter)
    return db_chapter

def delete_chapter(db: Session, chapter_id: int):
    part = db.query(models.Part).filter(models.Part.ChapterID == chapter_id).first()
    if part:
        return None
    db_chapter = db.query(models.Chapter).filter(models.Chapter.ChapterID == chapter_id).first()
    if db_chapter:
        db.delete(db_chapter)
        db.commit()
    return db_chapter

def get_chapters_by_course(db: Session, course_id: int):
    return db.query(models.Chapter).filter(models.Chapter.CourseID == course_id).all()

# PARTS

def create_part(db: Session, part: schemas.PartCreate):
    db_part = models.Part(**part.dict())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

def update_part(db: Session, part_id: int, part: schemas.PartUpdate):
    db_part = db.query(models.Part).filter(models.Part.PartID == part_id).first()
    if db_part:
        for key, value in part.dict(exclude_unset=True).items():
            setattr(db_part, key, value)
        db.commit()
        db.refresh(db_part)
    return db_part

def delete_part(db: Session, part_id: int):
    db_part = db.query(models.Part).filter(models.Part.PartID == part_id).first()
    if db_part:
        db.delete(db_part)
        db.commit()
    return db_part

def get_parts_by_chapter(db: Session, chapter_id: int):
    return db.query(models.Part).filter(models.Part.ChapterID == chapter_id).all()

# REGISTERED COURSES

def create_registered_course(db: Session, reg: schemas.RegisteredCourseCreate):
    db_reg = models.RegisteredCourse(**reg.dict(), RegistrationDate=datetime.now())
    db.add(db_reg)
    db.commit()
    db.refresh(db_reg)
    return db_reg

def get_registered_courses_by_user(db: Session, user_id: int):
    return db.query(models.RegisteredCourse).filter(models.RegisteredCourse.UserID == user_id).all()
