from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
import crud # crud.py đã được sửa để không dùng passlib (hoặc dùng passlib tùy theo lựa chọn cuối cùng của bạn)
from database import SessionLocal, engine
from typing import List, Optional
import os
import shutil
import uuid

# models.Base.metadata.create_all(bind=engine) # Comment lại nếu dùng Alembic hoặc chỉ chạy 1 lần

app = FastAPI(title="E-Learning API", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIRECTORY = os.path.join(STATIC_DIR, "uploads")
VIDEO_DIRECTORY = os.path.join(UPLOAD_DIRECTORY, "videos") # Hoặc một tên chung hơn như "files"
os.makedirs(VIDEO_DIRECTORY, exist_ok=True) # Đảm bảo thư mục tồn tại
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Trong production, nên giới hạn lại
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === USER ENDPOINTS ===
@app.post("/users/", response_model=schemas.UserInfo, tags=["Users"])
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_by_email = crud.get_user_by_email(db, email=user.Email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email đã được đăng ký.")
    db_user_by_username = crud.get_user_login(db, username=user.UserName)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại.")
    # Giả sử crud.create_user đang lưu plain text password (theo yêu cầu tạm thời của bạn)
    return crud.create_user(db, user=user)

@app.put("/users/{user_id}", response_model=schemas.UserInfo, tags=["Users"])
def update_user_endpoint(user_id: int, user_update_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user_check = crud.get_user_basic(db, user_id=user_id)
    if not db_user_check:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại.")
    if user_update_data.Email:
        existing_user_by_email = crud.get_user_by_email(db, email=user_update_data.Email)
        if existing_user_by_email and existing_user_by_email.UserID != user_id:
            raise HTTPException(status_code=400, detail="Email này đã được sử dụng bởi người dùng khác.")
    if user_update_data.UserName:
        existing_user_by_username = crud.get_user_login(db, username=user_update_data.UserName)
        if existing_user_by_username and existing_user_by_username.UserID != user_id:
             raise HTTPException(status_code=400, detail="Tên đăng nhập này đã được sử dụng bởi người dùng khác.")
    updated_user = crud.update_user(db, user_id=user_id, user_update=user_update_data)
    return updated_user

@app.delete("/users/{user_id}", tags=["Users"])
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại.")
    return {"detail": "Người dùng đã được xóa thành công."}

@app.get("/users/{user_id}", response_model=schemas.UserInfo, tags=["Users"])
def get_user_basic_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_basic(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại.")
    return db_user

@app.post("/users/login", response_model=schemas.UserInfo, tags=["Users"])
def login_endpoint(user_login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_login(db, username=user_login_data.UserName)
    # ĐANG SO SÁNH PLAIN TEXT (THEO YÊU CẦU TẠM THỜI)
    if not db_user or db_user.Password != user_login_data.Password:
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng.")
    return db_user

# === COURSE ENDPOINTS ===
@app.get("/courses/all", response_model=List[schemas.CourseInfo], tags=["Courses"])
def get_all_courses_endpoint(
    skip: int = 0, limit: int = 100,
    sort_by: Optional[str] = Query(None, description="Cột để sắp xếp (vd: CourseName, Price)"),
    sort_order: str = Query("asc", description="Thứ tự sắp xếp ('asc' hoặc 'desc')"),
    filter_name: Optional[str] = Query(None, description="Lọc theo tên khóa học"),
    is_public: Optional[bool] = Query(None, description="Lọc theo trạng thái công khai (true/false)"),
    db: Session = Depends(get_db)
):
    if sort_order.lower() not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="sort_order phải là 'asc' hoặc 'desc'.")
    valid_sort_columns = [column.name for column in models.Course.__table__.columns]
    if sort_by and sort_by not in valid_sort_columns:
        sort_by = None 
    courses = crud.get_all_courses(
        db, skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order,
        filter_name=filter_name, is_public=is_public
    )
    return courses

@app.post("/courses/", response_model=schemas.CourseInfo, tags=["Courses"])
def create_course_endpoint(course_data: schemas.CourseCreate, db: Session = Depends(get_db)):
    creator = crud.get_user_basic(db, user_id=course_data.UserID)
    if not creator:
        raise HTTPException(status_code=404, detail=f"Người dùng (người tạo) với ID {course_data.UserID} không tồn tại.")
    return crud.create_course(db, course=course_data)

@app.put("/courses/{course_id}", response_model=schemas.CourseInfo, tags=["Courses"])
def update_course_endpoint(course_id: int, course_update_data: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course_check = crud.get_course_basic(db, course_id=course_id)
    if not db_course_check:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    # Thêm kiểm tra quyền ở đây (ví dụ: current_user.UserID == db_course_check.UserID)
    updated_course = crud.update_course(db, course_id=course_id, course_update=course_update_data)
    if not updated_course: # Nên có trong crud.update_course, nhưng check lại cho chắc
         raise HTTPException(status_code=404, detail="Không tìm thấy khóa học để cập nhật.")
    return updated_course

@app.delete("/courses/{course_id}", tags=["Courses"])
def delete_course_endpoint(course_id: int, db: Session = Depends(get_db)):
    db_course_check = crud.get_course_basic(db, course_id=course_id)
    if not db_course_check:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    # Thêm kiểm tra quyền
    deleted_course_obj = crud.delete_course(db, course_id=course_id)
    if not deleted_course_obj:
        raise HTTPException(status_code=400, detail="Không thể xóa khóa học. Khóa học có thể đã có người đăng ký hoặc chứa chương/phần học.")
    return {"detail": "Khóa học đã được xóa thành công."}

@app.get("/courses/{course_id}", response_model=schemas.CourseInfo, tags=["Courses"])
def get_course_basic_endpoint(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_basic(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    return db_course

@app.get("/courses/{course_id}/detail", response_model=schemas.CourseDetail, tags=["Courses"])
def get_course_detail_endpoint(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_detail(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    return db_course

@app.get("/courses/{course_id}/creator", response_model=schemas.UserInfo, tags=["Courses"])
def get_course_creator_info_endpoint(course_id: int, db: Session = Depends(get_db)):
    course_check = crud.get_course_basic(db, course_id=course_id)
    if not course_check:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    db_user = crud.get_course_creator_info(db, course_id=course_id)
    if not db_user: # Điều này không nên xảy ra nếu Course.UserID là NOT NULL
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin người tạo cho khóa học này.")
    return db_user

@app.get("/users/{user_id}/created-courses", response_model=List[schemas.CourseInfo], tags=["Users", "Courses"])
def get_user_created_courses_endpoint(user_id: int, db: Session = Depends(get_db)):
    user_check = crud.get_user_basic(db, user_id=user_id)
    if not user_check:
        raise HTTPException(status_code=404, detail=f"Người dùng với ID {user_id} không tồn tại.")
    return crud.get_courses_created_by_user(db, user_id=user_id)


# === CHAPTER ENDPOINTS ===
@app.post("/chapters/", response_model=schemas.ChapterInfo, tags=["Chapters"])
def create_chapter_endpoint(chapter_data: schemas.ChapterCreate, db: Session = Depends(get_db)):
    course_check = crud.get_course_basic(db, course_id=chapter_data.CourseID)
    if not course_check:
        raise HTTPException(status_code=404, detail=f"Khóa học với ID {chapter_data.CourseID} không tồn tại.")
    # Thêm kiểm tra quyền: người dùng hiện tại có phải chủ khóa học course_check.UserID không?
    return crud.create_chapter(db, chapter=chapter_data)

@app.put("/chapters/{chapter_id}", response_model=schemas.ChapterInfo, tags=["Chapters"])
def update_chapter_endpoint(chapter_id: int, chapter_update_data: schemas.ChapterUpdate, db: Session = Depends(get_db)):
    db_chapter_check = crud.get_chapter_by_id(db, chapter_id=chapter_id)
    if not db_chapter_check:
        raise HTTPException(status_code=404, detail="Chương không tồn tại.")
    # Thêm kiểm tra quyền
    updated_chapter = crud.update_chapter(db, chapter_id=chapter_id, chapter_update=chapter_update_data)
    if not updated_chapter: # Nên được xử lý bởi check ở trên
         raise HTTPException(status_code=404, detail="Không tìm thấy chương để cập nhật.")
    return updated_chapter

@app.delete("/chapters/{chapter_id}", tags=["Chapters"])
def delete_chapter_endpoint(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter_check = crud.get_chapter_by_id(db, chapter_id=chapter_id)
    if not db_chapter_check:
        raise HTTPException(status_code=404, detail="Chương không tồn tại.")
    # Thêm kiểm tra quyền
    deleted_chapter_obj = crud.delete_chapter(db, chapter_id=chapter_id)
    if not deleted_chapter_obj:
        raise HTTPException(status_code=400, detail="Không thể xóa chương. Chương có thể đang chứa các phần học.")
    return {"detail": "Chương đã được xóa thành công."}

@app.get("/courses/{course_id}/chapters", response_model=List[schemas.ChapterInfo], tags=["Chapters"])
def get_chapters_by_course_endpoint(course_id: int, db: Session = Depends(get_db)):
    course_check = crud.get_course_basic(db, course_id=course_id)
    if not course_check:
        raise HTTPException(status_code=404, detail=f"Khóa học với ID {course_id} không tồn tại.")
    return crud.get_chapters_by_course(db, course_id=course_id)

# === PART ENDPOINTS ===
@app.post("/parts/", response_model=schemas.PartInfo, tags=["Parts"])
def create_part_endpoint(part_data: schemas.PartCreate, db: Session = Depends(get_db)):
    chapter_check = crud.get_chapter_by_id(db, chapter_id=part_data.ChapterID)
    if not chapter_check:
        raise HTTPException(status_code=404, detail=f"Chương với ID {part_data.ChapterID} không tồn tại.")
    # Thêm kiểm tra quyền
    return crud.create_part(db, part=part_data)

@app.put("/parts/{part_id}", response_model=schemas.PartInfo, tags=["Parts"])
def update_part_endpoint(part_id: int, part_update_data: schemas.PartUpdate, db: Session = Depends(get_db)):
    db_part_check = crud.get_part_by_id(db, part_id=part_id)
    if not db_part_check:
        raise HTTPException(status_code=404, detail="Phần học không tồn tại.")
    # Thêm kiểm tra quyền
    updated_part = crud.update_part(db, part_id=part_id, part_update=part_update_data)
    if not updated_part:
        raise HTTPException(status_code=404, detail="Không tìm thấy phần học để cập nhật.")
    return updated_part

@app.delete("/parts/{part_id}", tags=["Parts"])
def delete_part_endpoint(part_id: int, db: Session = Depends(get_db)):
    db_part_check = crud.get_part_by_id(db, part_id=part_id)
    if not db_part_check:
        raise HTTPException(status_code=404, detail="Phần học không tồn tại.")
    # Thêm kiểm tra quyền
    deleted_part_obj = crud.delete_part(db, part_id=part_id)
    if not deleted_part_obj: # crud.delete_part trả về part đã xóa hoặc None nếu không tìm thấy
        raise HTTPException(status_code=404, detail="Phần học không tìm thấy để xóa (có thể đã bị xóa).")
    return {"detail": "Phần học đã được xóa thành công."}

@app.get("/chapters/{chapter_id}/parts", response_model=List[schemas.PartInfo], tags=["Parts"])
def get_parts_by_chapter_endpoint(chapter_id: int, db: Session = Depends(get_db)):
    chapter_check = crud.get_chapter_by_id(db, chapter_id=chapter_id)
    if not chapter_check:
        raise HTTPException(status_code=404, detail=f"Chương với ID {chapter_id} không tồn tại.")
    return crud.get_parts_by_chapter(db, chapter_id=chapter_id)

# === REGISTERED COURSE ENDPOINTS ===
@app.post("/registered-courses/", response_model=schemas.RegisteredCourseInfo, tags=["Registered Courses"])
def create_registered_course_endpoint(reg_data: schemas.RegisteredCourseCreate, db: Session = Depends(get_db)):
    user_check = crud.get_user_basic(db, user_id=reg_data.UserID)
    if not user_check:
        raise HTTPException(status_code=404, detail=f"Người dùng với ID {reg_data.UserID} không tồn tại.")
    course_check = crud.get_course_basic(db, course_id=reg_data.CourseID)
    if not course_check:
        raise HTTPException(status_code=404, detail=f"Khóa học với ID {reg_data.CourseID} không tồn tại.")
    existing_reg = crud.get_registration_by_user_and_course(db, user_id=reg_data.UserID, course_id=reg_data.CourseID)
    if existing_reg:
        raise HTTPException(status_code=400, detail="Bạn đã đăng ký khóa học này rồi.")
    return crud.create_registered_course(db, reg=reg_data)

@app.get("/users/{user_id}/registered-courses", response_model=List[schemas.RegisteredCourseInfo], tags=["Registered Courses"])
def get_registered_courses_by_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user_check = crud.get_user_basic(db, user_id=user_id)
    if not user_check:
        raise HTTPException(status_code=404, detail=f"Người dùng với ID {user_id} không tồn tại.")
    return crud.get_registered_courses_by_user(db, user_id=user_id)

# === FILE UPLOAD ENDPOINT ===
@app.post("/uploadvideo/", response_model=schemas.FileUploadResponse, tags=["File Uploads"])
async def upload_video_file_endpoint(file: UploadFile = File(...)):
    allowed_extensions = ('.mp4', '.mov', '.webm', '.ogg', '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.gif')
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
         raise HTTPException(status_code=400, detail=f"Phần mở rộng file không hợp lệ. Chấp nhận: {', '.join(allowed_extensions)}")

    MAX_FILE_SIZE = 200 * 1024 * 1024 # 200 MB
    file_content_length = 0
    async for chunk in file.chunks(): # Cách đọc file an toàn hơn
        file_content_length += len(chunk)
        if file_content_length > MAX_FILE_SIZE:
            await file.close() # Đóng file trước khi raise
            raise HTTPException(status_code=413, detail=f"Kích thước file quá lớn. Tối đa {MAX_FILE_SIZE // (1024*1024)}MB.")
    
    await file.seek(0) # Đưa con trỏ về đầu file để đọc lại khi lưu

    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    # Đảm bảo VIDEO_DIRECTORY được định nghĩa đúng ở đầu file
    file_path = os.path.join(VIDEO_DIRECTORY, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer) # file.file là đối tượng file thực sự
    except Exception as e:
        print(f"Error saving file: {e}") # Nên dùng logging
        raise HTTPException(status_code=500, detail="Không thể lưu file lên server.")
    finally:
        await file.close() # Luôn đóng file

    file_url = f"/static/uploads/videos/{unique_filename}" # Đường dẫn tương đối
    return schemas.FileUploadResponse(filename=unique_filename, file_url=file_url)


if __name__ == "__main__":
    import uvicorn
    try:
        # Chỉ chạy create_all khi khởi động server nếu đây là môi trường dev/test
        # hoặc khi bạn chắc chắn về schema.
        # Trong production, Alembic được khuyến nghị.
        models.Base.metadata.create_all(bind=engine)
        print("Database tables created/checked successfully.")
    except Exception as e:
        print(f"Error creating/checking database tables: {e}")

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)