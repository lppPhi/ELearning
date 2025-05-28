from sqlalchemy.orm import Session
from sqlalchemy import desc
import models, schemas
from datetime import datetime
from typing import Optional, List

# --- Cấu hình Hashing Password (ĐÃ BỎ) ---
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === USER CRUD FUNCTIONS ===

# def verify_password(plain_password: str, hashed_password: str) -> bool: # Bỏ
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password: str) -> str: # Bỏ
#     return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    # Bỏ hashing, lưu mật khẩu plain text
    db_user = models.User(
        UserName=user.UserName,
        Email=user.Email,
        Password=user.Password, # LƯU PLAIN TEXT
        Phone=user.Phone,
        Image=user.Image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True) # Pydantic v2

        # Nếu có trường "Password" trong update_data và nó có giá trị,
        # thì nó sẽ được cập nhật trực tiếp (plain text) bởi vòng lặp bên dưới.
        # Không cần xử lý đặc biệt cho password ở đây nữa.
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user 
    return None

def get_user_basic(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.UserID == user_id).first()

def get_user_login(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.UserName == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.Email == email).first()


# === COURSE CRUD FUNCTIONS === (Giữ nguyên như phiên bản đầy đủ trước đó)
def create_course(db: Session, course: schemas.CourseCreate) -> models.Course:
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, course_id: int, course_update: schemas.CourseUpdate) -> Optional[models.Course]:
    db_course = db.query(models.Course).filter(models.Course.CourseID == course_id).first()
    if db_course:
        update_data = course_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_course, key, value)
        db.commit()
        db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int) -> Optional[models.Course]:
    registration_count = db.query(models.RegisteredCourse).filter(models.RegisteredCourse.CourseID == course_id).count()
    if registration_count > 0:
        return None 
    db_course = db.query(models.Course).filter(models.Course.CourseID == course_id).first()
    if db_course:
        chapters_to_delete = db.query(models.Chapter).filter(models.Chapter.CourseID == course_id).all()
        for chapter in chapters_to_delete:
            db.query(models.Part).filter(models.Part.ChapterID == chapter.ChapterID).delete(synchronize_session=False)
            db.delete(chapter) 
        db.delete(db_course)
        db.commit()
        return db_course 
    return None

def get_course_basic(db: Session, course_id: int) -> Optional[models.Course]:
    return db.query(models.Course).filter(models.Course.CourseID == course_id).first()

def get_course_detail(db: Session, course_id: int) -> Optional[models.Course]:
    return db.query(models.Course).filter(models.Course.CourseID == course_id).first()

def get_course_creator_info(db: Session, course_id: int) -> Optional[models.User]:
    course = db.query(models.Course).filter(models.Course.CourseID == course_id).first()
    if course and course.user: 
        return course.user
    elif course: 
         return db.query(models.User).filter(models.User.UserID == course.UserID).first()
    return None

def get_all_courses(
    db: Session, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None,
    sort_order: str = "asc", filter_name: Optional[str] = None, is_public: Optional[bool] = None
) -> List[models.Course]:
    query = db.query(models.Course)
    if filter_name: query = query.filter(models.Course.CourseName.ilike(f"%{filter_name}%"))
    if is_public is not None: query = query.filter(models.Course.IsPublic == is_public)
    if sort_by:
        column_to_sort = getattr(models.Course, sort_by, None)
        if column_to_sort:
            if sort_order.lower() == "desc": query = query.order_by(desc(column_to_sort))
            else: query = query.order_by(column_to_sort)
        else: query = query.order_by(models.Course.CourseID) 
    else: query = query.order_by(models.Course.CourseID) 
    return query.offset(skip).limit(limit).all()

def get_courses_created_by_user(db: Session, user_id: int) -> List[models.Course]:
    return db.query(models.Course).filter(models.Course.UserID == user_id).order_by(desc(models.Course.CourseID)).all()

# === CHAPTER CRUD FUNCTIONS === (Giữ nguyên)
def create_chapter(db: Session, chapter: schemas.ChapterCreate) -> models.Chapter: # ...
    db_chapter = models.Chapter(**chapter.model_dump())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

def update_chapter(db: Session, chapter_id: int, chapter_update: schemas.ChapterUpdate) -> Optional[models.Chapter]: # ...
    db_chapter = db.query(models.Chapter).filter(models.Chapter.ChapterID == chapter_id).first()
    if db_chapter:
        update_data = chapter_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_chapter, key, value)
        db.commit()
        db.refresh(db_chapter)
    return db_chapter

def delete_chapter(db: Session, chapter_id: int) -> Optional[models.Chapter]: # ...
    part_count = db.query(models.Part).filter(models.Part.ChapterID == chapter_id).count()
    if part_count > 0:
        return None
    db_chapter = db.query(models.Chapter).filter(models.Chapter.ChapterID == chapter_id).first()
    if db_chapter:
        db.delete(db_chapter)
        db.commit()
        return db_chapter
    return None

def get_chapters_by_course(db: Session, course_id: int) -> List[models.Chapter]: # ...
    return db.query(models.Chapter).filter(models.Chapter.CourseID == course_id).order_by(models.Chapter.ChapterID).all()

def get_chapter_by_id(db: Session, chapter_id: int) -> Optional[models.Chapter]: # ...
    return db.query(models.Chapter).filter(models.Chapter.ChapterID == chapter_id).first()

# === PART CRUD FUNCTIONS === (Giữ nguyên)
def create_part(db: Session, part: schemas.PartCreate) -> models.Part: # ...
    db_part = models.Part(**part.model_dump())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

def update_part(db: Session, part_id: int, part_update: schemas.PartUpdate) -> Optional[models.Part]: # ...
    db_part = db.query(models.Part).filter(models.Part.PartID == part_id).first()
    if db_part:
        update_data = part_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_part, key, value)
        db.commit()
        db.refresh(db_part)
    return db_part

def delete_part(db: Session, part_id: int) -> Optional[models.Part]: # ...
    db_part = db.query(models.Part).filter(models.Part.PartID == part_id).first()
    if db_part:
        db.delete(db_part)
        db.commit()
        return db_part
    return None

def get_parts_by_chapter(db: Session, chapter_id: int) -> List[models.Part]: # ...
    return db.query(models.Part).filter(models.Part.ChapterID == chapter_id).order_by(models.Part.PartID).all()

def get_part_by_id(db: Session, part_id: int) -> Optional[models.Part]: # ...
    return db.query(models.Part).filter(models.Part.PartID == part_id).first()

# === REGISTERED COURSE CRUD FUNCTIONS === (Giữ nguyên)
def create_registered_course(db: Session, reg: schemas.RegisteredCourseCreate) -> models.RegisteredCourse: # ...
    db_reg = models.RegisteredCourse(**reg.model_dump(), RegistrationDate=datetime.utcnow())
    db.add(db_reg)
    db.commit()
    db.refresh(db_reg)
    return db_reg

def get_registered_courses_by_user(db: Session, user_id: int) -> List[models.RegisteredCourse]: # ...
    return db.query(models.RegisteredCourse).filter(models.RegisteredCourse.UserID == user_id).all()

def get_registration_by_user_and_course(db: Session, user_id: int, course_id: int) -> Optional[models.RegisteredCourse]: # ...
    return db.query(models.RegisteredCourse).filter(
        models.RegisteredCourse.UserID == user_id,
        models.RegisteredCourse.CourseID == course_id
    ).first()