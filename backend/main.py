from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import SessionLocal, engine
from typing import List
import os
import shutil
import uuid

# Tạo các bảng trong DB nếu chưa tồn tại (chỉ nên chạy một lần hoặc khi model thay đổi)
# models.Base.metadata.create_all(bind=engine) # Bạn có thể comment dòng này sau lần chạy đầu tiên

app = FastAPI(title="E-Learning API", version="1.0.0")

# --- Thư mục lưu trữ file uploads ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIRECTORY = os.path.join(STATIC_DIR, "uploads")
VIDEO_DIRECTORY = os.path.join(UPLOAD_DIRECTORY, "videos")

os.makedirs(VIDEO_DIRECTORY, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- Cấu hình CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependency để lấy DB session ---
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
    if user_update_data.UserName: # Giả sử cho phép cập nhật UserName
        existing_user_by_username = crud.get_user_login(db, username=user_update_data.UserName)
        if existing_user_by_username and existing_user_by_username.UserID != user_id:
             raise HTTPException(status_code=400, detail="Tên đăng nhập này đã được sử dụng bởi người dùng khác.")

    updated_user = crud.update_user(db, user_id=user_id, user_update=user_update_data)
    if not updated_user: # Trường hợp db_user không tìm thấy trong crud (dù đã check ở trên)
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại (lỗi không mong muốn).")
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

@app.post("/users/login", response_model=schemas.UserInfo, tags=["Users"]) # Hoặc response_model=schemas.Token nếu dùng OAuth2
def login_endpoint(user_login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_login(db, username=user_login_data.UserName)
    if not db_user or not crud.verify_password(user_login_data.Password, db_user.Password):
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng.")
    # Nếu dùng OAuth2, bạn sẽ tạo token ở đây và trả về schemas.Token
    return db_user

# === COURSE ENDPOINTS ===
@app.get("/courses/all", response_model=List[schemas.CourseInfo], tags=["Courses"])
def get_all_courses_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)): # Thêm skip, limit
    return crud.get_all_courses(db, skip=skip, limit=limit)

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
    # Thêm kiểm tra quyền ở đây nếu cần (ví dụ, current_user.UserID == db_course_check.UserID)
    updated_course = crud.update_course(db, course_id=course_id, course_update=course_update_data)
    if not updated_course: # Trường hợp không tìm thấy trong crud
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại (lỗi không mong muốn).")
    return updated_course

@app.delete("/courses/{course_id}", tags=["Courses"])
def delete_course_endpoint(course_id: int, db: Session = Depends(get_db)):
    db_course_check = crud.get_course_basic(db, course_id=course_id)
    if not db_course_check:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    # Thêm kiểm tra quyền
    deleted_course_obj = crud.delete_course(db, course_id=course_id)
    if not deleted_course_obj:
        raise HTTPException(status_code=400, detail="Không thể xóa khóa học. Khóa học có thể đã có người đăng ký hoặc có lỗi khác.")
    return {"detail": "Khóa học đã được xóa thành công."}

@app.get("/courses/{course_id}", response_model=schemas.CourseInfo, tags=["Courses"])
def get_course_basic_endpoint(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_basic(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    return db_course

@app.get("/courses/{course_id}/detail", response_model=schemas.CourseDetail, tags=["Courses"])
def get_course_detail_endpoint(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_detail(db, course_id=course_id) # crud.get_course_detail hiện giống get_course_basic
    if not db_course:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    return db_course

@app.get("/courses/{course_id}/creator", response_model=schemas.UserInfo, tags=["Courses"])
def get_course_creator_info_endpoint(course_id: int, db: Session = Depends(get_db)):
    course_check = crud.get_course_basic(db, course_id=course_id)
    if not course_check:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    db_user = crud.get_course_creator_info(db, course_id=course_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin người tạo cho khóa học này.")
    return db_user

# === CHAPTER ENDPOINTS ===
@app.post("/chapters/", response_model=schemas.ChapterInfo, tags=["Chapters"])
def create_chapter_endpoint(chapter_data: schemas.ChapterCreate, db: Session = Depends(get_db)):
    course_check = crud.get_course_basic(db, course_id=chapter_data.CourseID)
    if not course_check:
        raise HTTPException(status_code=404, detail=f"Khóa học với ID {chapter_data.CourseID} không tồn tại.")
    # Thêm kiểm tra quyền (người dùng hiện tại có phải chủ khóa học không?)
    return crud.create_chapter(db, chapter=chapter_data)

@app.put("/chapters/{chapter_id}", response_model=schemas.ChapterInfo, tags=["Chapters"])
def update_chapter_endpoint(chapter_id: int, chapter_update_data: schemas.ChapterUpdate, db: Session = Depends(get_db)):
    db_chapter_check = crud.get_chapter_by_id(db, chapter_id=chapter_id)
    if not db_chapter_check:
        raise HTTPException(status_code=404, detail="Chương không tồn tại.")
    # Thêm kiểm tra quyền
    updated_chapter = crud.update_chapter(db, chapter_id=chapter_id, chapter_update=chapter_update_data)
    if not updated_chapter:
        raise HTTPException(status_code=404, detail="Chương không tồn tại (lỗi không mong muốn).")
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
        raise HTTPException(status_code=404, detail="Phần học không tồn tại (lỗi không mong muốn).")
    return updated_part

@app.delete("/parts/{part_id}", tags=["Parts"])
def delete_part_endpoint(part_id: int, db: Session = Depends(get_db)):
    db_part_check = crud.get_part_by_id(db, part_id=part_id)
    if not db_part_check:
        raise HTTPException(status_code=404, detail="Phần học không tồn tại.")
    # Thêm kiểm tra quyền
    deleted_part_obj = crud.delete_part(db, part_id=part_id)
    if not deleted_part_obj: # crud.delete_part trả về part đã xóa hoặc None nếu không tìm thấy
        raise HTTPException(status_code=404, detail="Phần học không tìm thấy để xóa.")
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
    allowed_video_types = ["video/mp4", "video/webm", "video/ogg", "video/quicktime", "application/pdf"] # Thêm PDF và các loại file tài liệu khác nếu muốn
    # Hoặc chấp nhận tất cả nếu bạn muốn linh hoạt hơn và kiểm tra ở frontend
    # if not file.content_type.startswith("video/") and not file.content_type == "application/pdf":
    #     raise HTTPException(status_code=400, detail=f"Loại file không hợp lệ. Chỉ chấp nhận video hoặc PDF.")
    
    # Kiểm tra phần mở rộng file để linh hoạt hơn với content_type
    allowed_extensions = ('.mp4', '.mov', '.webm', '.ogg', '.pdf', '.doc', '.docx', '.ppt', '.pptx')
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
         raise HTTPException(status_code=400, detail=f"Phần mở rộng file không hợp lệ. Chấp nhận: {', '.join(allowed_extensions)}")


    MAX_FILE_SIZE = 200 * 1024 * 1024 # 200 MB (Tăng lên nếu cần cho video)
    
    # Cách đọc file an toàn hơn để tránh đọc toàn bộ file lớn vào bộ nhớ cùng lúc
    file_content = b""
    chunk_size = 4096 # 4KB chunks
    size = 0
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        size += len(chunk)
        if size > MAX_FILE_SIZE:
            await file.close() # Đóng file trước khi raise exception
            raise HTTPException(status_code=413, detail=f"Kích thước file quá lớn. Tối đa {MAX_FILE_SIZE // (1024*1024)}MB.")
        file_content += chunk
    await file.seek(0) # Reset con trỏ file về đầu để shutil có thể đọc lại

    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(VIDEO_DIRECTORY, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer) # file.file là đối tượng file thực sự
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Không thể lưu file lên server.")
    finally:
        await file.close()

    file_url = f"/static/uploads/videos/{unique_filename}"
    return schemas.FileUploadResponse(filename=unique_filename, file_url=file_url)


if __name__ == "__main__":
    import uvicorn
    # Dòng models.Base.metadata.create_all(bind=engine) nên được chạy trước khi uvicorn.run
    # để đảm bảo bảng được tạo nếu chưa có.
    # Tuy nhiên, nếu bạn quản lý migration bằng Alembic, bạn sẽ không cần dòng này ở đây.
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Database tables created/checked successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)