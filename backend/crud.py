from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime
from passlib.context import CryptContext
from typing import Optional, List # <<--- THÊM Optional VÀ List (nếu chưa có)

# --- Cấu hình Hashing Password ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === USER CRUD FUNCTIONS ===

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate) -> models.User: # Không thay đổi vì luôn trả về models.User
    hashed_password = get_password_hash(user.Password)
    db_user = models.User(
        UserName=user.UserName,
        Email=user.Email,
        Password=hashed_password,
        Phone=user.Phone,
        Image=user.Image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# SỬA Ở ĐÂY
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if db_user:
        # Giả sử bạn đang dùng Pydantic v2 cho .model_dump()
        # Nếu dùng Pydantic v1, đổi thành .dict(exclude_unset=True)
        update_data = user_update.model_dump(exclude_unset=True)

        if "Password" in update_data and update_data["Password"]:
            hashed_password = get_password_hash(update_data["Password"])
            update_data["Password"] = hashed_password
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
    return db_user

# SỬA Ở ĐÂY
def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None

# SỬA Ở ĐÂY
def get_user_basic(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.UserID == user_id).first()

# SỬA Ở ĐÂY
def get_user_login(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.UserName == username).first()

# SỬA Ở ĐÂY
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.Email == email).first()


# === COURSE CRUD FUNCTIONS ===

def create_course(db: Session, course: schemas.CourseCreate) -> models.Course: # Không thay đổi
    # Giả sử Pydantic v2
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# SỬA Ở ĐÂY
def update_course(db: Session, course_id: int, course_update: schemas.CourseUpdate) -> Optional[models.Course]:
    db_course = db.query(models.Course).filter(models.Course.CourseID == course_id).first()
    if db_course:
        # Giả sử Pydantic v2
        update_data = course_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_course, key, value)
        db.commit()
        db.refresh(db_course)
    return db_course

# SỬA Ở ĐÂY
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

# SỬA Ở ĐÂY
def get_course_basic(db: Session, course_id: int) -> Optional[models.Course]:
    return db.query(models.Course).filter(models.Course.CourseID == course_id).first()

# SỬA Ở ĐÂY
def get_course_detail(db: Session, course_id: int) -> Optional[models.Course]:
    return db.query(models.Course).filter(models.Course.CourseID == course_id).first()

# SỬA Ở ĐÂY
def get_course_creator_info(db: Session, course_id: int) -> Optional[models.User]:
    course = db.query(models.Course).filter(models.Course.CourseID == course_id).first()
    if course:
        return db.query(models.User).filter(models.User.UserID == course.UserID).first()
    return None

def get_all_courses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = None, # Tên cột để sắp xếp (ví dụ: "CourseName", "Price")
    sort_order: str = "asc",       # "asc" hoặc "desc"
    filter_name: Optional[str] = None, # Lọc theo tên khóa học (tìm kiếm)
    is_public: Optional[bool] = None   # Lọc theo trạng thái công khai
) -> List[models.Course]:
    """
    Lấy danh sách tất cả các khóa học với các tùy chọn phân trang, sắp xếp và lọc.
    """
    query = db.query(models.Course)

    # Áp dụng bộ lọc (Filtering)
    if filter_name:
        query = query.filter(models.Course.CourseName.ilike(f"%{filter_name}%")) # Tìm kiếm không phân biệt hoa thường

    if is_public is not None: # Cho phép lọc theo is_public = True hoặc is_public = False
        query = query.filter(models.Course.IsPublic == is_public)

    # Áp dụng sắp xếp (Sorting)
    if sort_by:
        column_to_sort = getattr(models.Course, sort_by, None)
        if column_to_sort: # Kiểm tra xem cột có tồn tại trong model không
            if sort_order.lower() == "desc":
                query = query.order_by(desc(column_to_sort))
            else:
                query = query.order_by(column_to_sort)
        else:
            # Mặc định hoặc nếu sort_by không hợp lệ, sắp xếp theo CourseID
            query = query.order_by(models.Course.CourseID)
    else:
        # Mặc định luôn cần ORDER BY cho MSSQL khi có OFFSET/LIMIT
        query = query.order_by(models.Course.CourseID)

    # Tùy chọn: Chỉ load các cột cần thiết nếu bạn biết chắc chắn danh sách hiển thị
    # Đây là một ví dụ, bạn cần điều chỉnh các cột cho phù hợp với schemas.CourseInfo
    # query = query.options(
    #     load_only(
    #         models.Course.CourseID,
    #         models.Course.CourseName,
    #         models.Course.Decription,
    #         models.Course.Image,
    #         models.Course.Price,
    #         models.Course.IsPublic,
    #         models.Course.UserID, # Cần cho việc tạo CourseInfo nếu bạn dùng UserID trong đó
    #         models.Course.NumberOfRegistrations
    #     )
    # )
    # Lưu ý: Nếu dùng load_only, khi truy cập các cột không được load, SQLAlchemy sẽ tự động thực hiện query bổ sung.
    # Điều này có thể hữu ích để giảm tải ban đầu, nhưng nếu bạn luôn cần tất cả các cột trong CourseInfo,
    # thì việc không dùng load_only có thể đơn giản hơn.

    # Áp dụng phân trang (Pagination)
    courses = query.offset(skip).limit(limit).all()
    
    return courses


# === CHAPTER CRUD FUNCTIONS ===

def create_chapter(db: Session, chapter: schemas.ChapterCreate) -> models.Chapter: # Không thay đổi
    # Giả sử Pydantic v2
    db_chapter = models.Chapter(**chapter.model_dump())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

# SỬA Ở ĐÂY
def update_chapter(db: Session, chapter_id: int, chapter_update: schemas.ChapterUpdate) -> Optional[models.Chapter]:
    db_chapter = db.query(models.Chapter).filter(models.Chapter.ChapterID == chapter_id).first()
    if db_chapter:
        # Giả sử Pydantic v2
        update_data = chapter_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_chapter, key, value)
        db.commit()
        db.refresh(db_chapter)
    return db_chapter

# SỬA Ở ĐÂY
def delete_chapter(db: Session, chapter_id: int) -> Optional[models.Chapter]:
    part_count = db.query(models.Part).filter(models.Part.ChapterID == chapter_id).count()
    if part_count > 0:
        return None

    db_chapter = db.query(models.Chapter).filter(models.Chapter.ChapterID == chapter_id).first()
    if db_chapter:
        db.delete(db_chapter)
        db.commit()
        return db_chapter
    return None

def get_chapters_by_course(db: Session, course_id: int) -> List[models.Chapter]: # List đã import
    return db.query(models.Chapter).filter(models.Chapter.CourseID == course_id).order_by(models.Chapter.ChapterID).all()

# SỬA Ở ĐÂY
def get_chapter_by_id(db: Session, chapter_id: int) -> Optional[models.Chapter]:
    return db.query(models.Chapter).filter(models.Chapter.ChapterID == chapter_id).first()


# === PART CRUD FUNCTIONS ===

def create_part(db: Session, part: schemas.PartCreate) -> models.Part: # Không thay đổi
    # Giả sử Pydantic v2
    db_part = models.Part(**part.model_dump())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

# SỬA Ở ĐÂY
def update_part(db: Session, part_id: int, part_update: schemas.PartUpdate) -> Optional[models.Part]:
    db_part = db.query(models.Part).filter(models.Part.PartID == part_id).first()
    if db_part:
        # Giả sử Pydantic v2
        update_data = part_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_part, key, value)
        db.commit()
        db.refresh(db_part)
    return db_part

# SỬA Ở ĐÂY
def delete_part(db: Session, part_id: int) -> Optional[models.Part]:
    db_part = db.query(models.Part).filter(models.Part.PartID == part_id).first()
    if db_part:
        db.delete(db_part)
        db.commit()
        return db_part
    return None

def get_parts_by_chapter(db: Session, chapter_id: int) -> List[models.Part]: # List đã import
    return db.query(models.Part).filter(models.Part.ChapterID == chapter_id).order_by(models.Part.PartID).all()

# SỬA Ở ĐÂY
def get_part_by_id(db: Session, part_id: int) -> Optional[models.Part]:
    return db.query(models.Part).filter(models.Part.PartID == part_id).first()


# === REGISTERED COURSE CRUD FUNCTIONS ===

def create_registered_course(db: Session, reg: schemas.RegisteredCourseCreate) -> models.RegisteredCourse: # Không thay đổi
    # Giả sử Pydantic v2
    db_reg = models.RegisteredCourse(**reg.model_dump(), RegistrationDate=datetime.utcnow())
    db.add(db_reg)
    db.commit()
    db.refresh(db_reg)
    return db_reg

def get_registered_courses_by_user(db: Session, user_id: int) -> List[models.RegisteredCourse]: # List đã import
    return db.query(models.RegisteredCourse).filter(models.RegisteredCourse.UserID == user_id).all()

# SỬA Ở ĐÂY
def get_registration_by_user_and_course(db: Session, user_id: int, course_id: int) -> Optional[models.RegisteredCourse]:
    return db.query(models.RegisteredCourse).filter(
        models.RegisteredCourse.UserID == user_id,
        models.RegisteredCourse.CourseID == course_id
    ).first()