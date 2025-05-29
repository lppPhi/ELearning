from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import SessionLocal, engine
from typing import List, Optional
import os
import shutil
import uuid

app = FastAPI(title="E-Learning API", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_BASE_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOAD_BASE_DIR, exist_ok=True)
COURSE_IMAGES_DIR = os.path.join(UPLOAD_BASE_DIR, "course_images")
os.makedirs(COURSE_IMAGES_DIR, exist_ok=True)
AVATARS_DIR = os.path.join(UPLOAD_BASE_DIR, "avatars") # Thêm thư mục cho avatar
os.makedirs(AVATARS_DIR, exist_ok=True)
GENERAL_FILES_DIR = os.path.join(UPLOAD_BASE_DIR, "general_files") # Cho các file chung
os.makedirs(GENERAL_FILES_DIR, exist_ok=True)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
@app.post("/uploadavatar/")
async def upload_avatar(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()  # Ép phần mở rộng về chữ thường
    filename = f"{uuid.uuid4().hex}.{ext}"      # Tạo tên file duy nhất
    file_path = os.path.join(STATIC_DIR, "uploads", "avatars", filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "file_name": filename,
        "file_url": f"/static/uploads/avatars/{filename}"
    }

@app.post("/uploadcourseimage/", response_model=schemas.FileUploadResponse, tags=["File Uploads", "Courses"])
async def upload_course_image_endpoint(file: UploadFile = File(...)):
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp') # Chỉ cho phép các định dạng ảnh phổ biến
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
         raise HTTPException(status_code=400, detail=f"Định dạng file ảnh không hợp lệ. Chấp nhận: {', '.join(allowed_extensions)}")

    MAX_IMAGE_SIZE = 10 * 1024 * 1024 # Giới hạn 10MB cho ảnh bìa
    
    # Kiểm tra kích thước file an toàn
    temp_file_path = os.path.join(COURSE_IMAGES_DIR, f"temp_{uuid.uuid4().hex}")
    file_content_length = 0
    with open(temp_file_path, "wb") as temp_buffer:
        async for chunk in file.chunks():
            file_content_length += len(chunk)
            if file_content_length > MAX_IMAGE_SIZE:
                await file.close()
                os.remove(temp_file_path)
                raise HTTPException(status_code=413, detail=f"Kích thước ảnh quá lớn. Tối đa {MAX_IMAGE_SIZE // (1024*1024)}MB.")
            temp_buffer.write(chunk)
    
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    final_file_path = os.path.join(COURSE_IMAGES_DIR, unique_filename)
    try:
        shutil.move(temp_file_path, final_file_path)
    except Exception as e:
        if os.path.exists(temp_file_path): os.remove(temp_file_path)
        print(f"Lỗi di chuyển file ảnh khóa học: {e}")
        raise HTTPException(status_code=500, detail="Không thể hoàn tất lưu file ảnh khóa học.")
    finally:
        await file.close()

    # Trả về đường dẫn tương đối mà frontend có thể lưu vào DB hoặc sử dụng để hiển thị
    # Đường dẫn này sẽ được ghép với API_BASE_URL ở frontend nếu cần URL đầy đủ
    relative_file_url = f"/static/uploads/course_images/{unique_filename}"
        
    return schemas.FileUploadResponse(filename=unique_filename, file_url=relative_file_url)

# ... (Các endpoint USER, COURSE, CHAPTER, PART, REGISTERED COURSE giữ nguyên như phiên bản đầy đủ trước đó) ...
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
    if not db_user or db_user.Password != user_login_data.Password: 
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng.")
    return db_user

@app.get("/courses/all", response_model=List[schemas.CourseInfo], tags=["Courses"])
def get_all_courses_endpoint(
    skip: int = 0, limit: int = 100,
    sort_by: Optional[str] = Query(None), sort_order: str = Query("asc"),
    filter_name: Optional[str] = Query(None), is_public: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    if sort_order.lower() not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="sort_order phải là 'asc' hoặc 'desc'.")
    valid_sort_columns = [column.name for column in models.Course.__table__.columns]
    if sort_by and sort_by not in valid_sort_columns: sort_by = None 
    return crud.get_all_courses(db, skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filter_name=filter_name, is_public=is_public)

@app.post("/courses/", response_model=schemas.CourseInfo, tags=["Courses"])
def create_course_endpoint(course_data: schemas.CourseCreate, db: Session = Depends(get_db)):
    creator = crud.get_user_basic(db, user_id=course_data.UserID)
    if not creator: raise HTTPException(status_code=404, detail=f"Người dùng (tạo) ID {course_data.UserID} không tồn tại.")
    return crud.create_course(db, course=course_data)

@app.put("/courses/{course_id}", response_model=schemas.CourseInfo, tags=["Courses"])
def update_course_endpoint(course_id: int, course_update_data: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course_check = crud.get_course_basic(db, course_id=course_id)
    if not db_course_check: raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    updated_course = crud.update_course(db, course_id=course_id, course_update=course_update_data)
    return updated_course

@app.delete("/courses/{course_id}", tags=["Courses"])
def delete_course_endpoint(course_id: int, db: Session = Depends(get_db)):
    db_course_check = crud.get_course_basic(db, course_id=course_id)
    if not db_course_check: raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    deleted_course_obj = crud.delete_course(db, course_id=course_id)
    if not deleted_course_obj: raise HTTPException(status_code=400, detail="Không thể xóa khóa học.")
    return {"detail": "Khóa học đã được xóa thành công."}

@app.get("/courses/{course_id}", response_model=schemas.CourseInfo, tags=["Courses"])
def get_course_basic_endpoint(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_basic(db, course_id=course_id)
    if not db_course: raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    return db_course

@app.get("/courses/{course_id}/detail", response_model=schemas.CourseDetail, tags=["Courses"])
def get_course_detail_endpoint(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_detail(db, course_id=course_id)
    if not db_course: raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    return db_course

@app.get("/courses/{course_id}/creator", response_model=schemas.UserInfo, tags=["Courses"])
def get_course_creator_info_endpoint(course_id: int, db: Session = Depends(get_db)):
    course_check = crud.get_course_basic(db, course_id=course_id)
    if not course_check: raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")
    db_user = crud.get_course_creator_info(db, course_id=course_id)
    if not db_user: raise HTTPException(status_code=404, detail="Không tìm thấy người tạo khóa học.")
    return db_user

@app.get("/users/{user_id}/created-courses", response_model=List[schemas.CourseInfo], tags=["Users", "Courses"])
def get_user_created_courses_endpoint(user_id: int, db: Session = Depends(get_db)):
    user_check = crud.get_user_basic(db, user_id=user_id)
    if not user_check: raise HTTPException(status_code=404, detail=f"Người dùng ID {user_id} không tồn tại.")
    return crud.get_courses_created_by_user(db, user_id=user_id)

@app.post("/chapters/", response_model=schemas.ChapterInfo, tags=["Chapters"])
def create_chapter_endpoint(chapter_data: schemas.ChapterCreate, db: Session = Depends(get_db)):
    course_check = crud.get_course_basic(db, course_id=chapter_data.CourseID)
    if not course_check: raise HTTPException(status_code=404, detail=f"Khóa học ID {chapter_data.CourseID} không tồn tại.")
    return crud.create_chapter(db, chapter=chapter_data)

@app.put("/chapters/{chapter_id}", response_model=schemas.ChapterInfo, tags=["Chapters"])
def update_chapter_endpoint(chapter_id: int, chapter_update_data: schemas.ChapterUpdate, db: Session = Depends(get_db)):
    db_chapter_check = crud.get_chapter_by_id(db, chapter_id=chapter_id)
    if not db_chapter_check: raise HTTPException(status_code=404, detail="Chương không tồn tại.")
    return crud.update_chapter(db, chapter_id=chapter_id, chapter_update=chapter_update_data)

@app.delete("/chapters/{chapter_id}", tags=["Chapters"])
def delete_chapter_endpoint(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter_check = crud.get_chapter_by_id(db, chapter_id=chapter_id)
    if not db_chapter_check: raise HTTPException(status_code=404, detail="Chương không tồn tại.")
    deleted_chapter_obj = crud.delete_chapter(db, chapter_id=chapter_id)
    if not deleted_chapter_obj: raise HTTPException(status_code=400, detail="Không thể xóa chương.")
    return {"detail": "Chương đã được xóa thành công."}

@app.get("/courses/{course_id}/chapters", response_model=List[schemas.ChapterInfo], tags=["Chapters"])
def get_chapters_by_course_endpoint(course_id: int, db: Session = Depends(get_db)):
    course_check = crud.get_course_basic(db, course_id=course_id)
    if not course_check: raise HTTPException(status_code=404, detail=f"Khóa học ID {course_id} không tồn tại.")
    return crud.get_chapters_by_course(db, course_id=course_id)

@app.post("/parts/", response_model=schemas.PartInfo, tags=["Parts"])
def create_part_endpoint(part_data: schemas.PartCreate, db: Session = Depends(get_db)):
    chapter_check = crud.get_chapter_by_id(db, chapter_id=part_data.ChapterID)
    if not chapter_check: raise HTTPException(status_code=404, detail=f"Chương ID {part_data.ChapterID} không tồn tại.")
    return crud.create_part(db, part=part_data)

@app.put("/parts/{part_id}", response_model=schemas.PartInfo, tags=["Parts"])
def update_part_endpoint(part_id: int, part_update_data: schemas.PartUpdate, db: Session = Depends(get_db)):
    db_part_check = crud.get_part_by_id(db, part_id=part_id)
    if not db_part_check: raise HTTPException(status_code=404, detail="Phần học không tồn tại.")
    return crud.update_part(db, part_id=part_id, part_update=part_update_data)

@app.delete("/parts/{part_id}", tags=["Parts"])
def delete_part_endpoint(part_id: int, db: Session = Depends(get_db)):
    db_part_check = crud.get_part_by_id(db, part_id=part_id)
    if not db_part_check: raise HTTPException(status_code=404, detail="Phần học không tồn tại.")
    deleted_part_obj = crud.delete_part(db, part_id=part_id)
    if not deleted_part_obj: raise HTTPException(status_code=404, detail="Không tìm thấy phần học để xóa.")
    return {"detail": "Phần học đã được xóa thành công."}

@app.get("/chapters/{chapter_id}/parts", response_model=List[schemas.PartInfo], tags=["Parts"])
def get_parts_by_chapter_endpoint(chapter_id: int, db: Session = Depends(get_db)):
    chapter_check = crud.get_chapter_by_id(db, chapter_id=chapter_id)
    if not chapter_check: raise HTTPException(status_code=404, detail=f"Chương ID {chapter_id} không tồn tại.")
    return crud.get_parts_by_chapter(db, chapter_id=chapter_id)

@app.post("/registered-courses/", response_model=schemas.RegisteredCourseInfo, tags=["Registered Courses"])
def create_registered_course_endpoint(reg_data: schemas.RegisteredCourseCreate, db: Session = Depends(get_db)):
    user_check = crud.get_user_basic(db, user_id=reg_data.UserID)
    if not user_check: raise HTTPException(status_code=404, detail=f"Người dùng ID {reg_data.UserID} không tồn tại.")
    course_check = crud.get_course_basic(db, course_id=reg_data.CourseID)
    if not course_check: raise HTTPException(status_code=404, detail=f"Khóa học ID {reg_data.CourseID} không tồn tại.")
    existing_reg = crud.get_registration_by_user_and_course(db, user_id=reg_data.UserID, course_id=reg_data.CourseID)
    if existing_reg: raise HTTPException(status_code=400, detail="Bạn đã đăng ký khóa học này rồi.")
    return crud.create_registered_course(db, reg=reg_data)

@app.get("/users/{user_id}/registered-courses", response_model=List[schemas.RegisteredCourseInfo], tags=["Registered Courses"])
def get_registered_courses_by_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user_check = crud.get_user_basic(db, user_id=user_id)
    if not user_check: raise HTTPException(status_code=404, detail=f"Người dùng ID {user_id} không tồn tại.")
    return crud.get_registered_courses_by_user(db, user_id=user_id)

# === FILE UPLOAD ENDPOINT ===
# Sử dụng endpoint chung này cho các loại upload khác nhau
@app.post("/uploadfile/", response_model=schemas.FileUploadResponse, tags=["File Uploads"])
async def upload_general_file_endpoint(
    file: UploadFile = File(...), 
    sub_folder: Optional[str] = Query(None, description="Thư mục con trong static/uploads (ví dụ: avatars, course_images)")
):
    # Xác định thư mục đích dựa trên sub_folder
    if sub_folder:
        allowed_sub_folders = ["avatars", "course_images", "course_documents", "part_documents", "chapter_documents", "videos", "general"]
        if sub_folder not in allowed_sub_folders:
            raise HTTPException(status_code=400, detail=f"Thư mục con '{sub_folder}' không hợp lệ.")
        target_dir = os.path.join(UPLOAD_BASE_DIR, sub_folder)
    else:
        target_dir = os.path.join(UPLOAD_BASE_DIR, "general") # Thư mục mặc định
    
    os.makedirs(target_dir, exist_ok=True) # Đảm bảo thư mục đích tồn tại

    # Kiểm tra loại file dựa trên phần mở rộng
    allowed_extensions = ('.mp4', '.mov', '.webm', '.ogg', '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.gif', '.txt', '.webp')
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
         raise HTTPException(status_code=400, detail=f"Định dạng file không hợp lệ. Cho phép: {', '.join(allowed_extensions)}")

    # Kiểm tra kích thước file
    MAX_FILE_SIZE = 200 * 1024 * 1024 # 200 MB
    
    # Lưu file tạm để kiểm tra kích thước trước, sau đó di chuyển
    temp_file_id = uuid.uuid4().hex
    temp_file_path = os.path.join(target_dir, f"temp_{temp_file_id}{file_ext}")
    
    file_content_length = 0
    try:
        with open(temp_file_path, "wb") as temp_buffer:
            # SỬA Ở ĐÂY: Dùng await file.read(chunk_size) trong vòng lặp
            chunk_size = 4096 # 4KB
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                file_content_length += len(chunk)
                if file_content_length > MAX_FILE_SIZE:
                    # Không cần await file.close() ở đây vì nó sẽ được đóng trong finally
                    raise HTTPException(status_code=413, detail=f"Kích thước file quá lớn. Tối đa {MAX_FILE_SIZE // (1024*1024)}MB.")
                temp_buffer.write(chunk)
    except HTTPException as http_exc: # Bắt lại HTTPException để xóa file tạm
        if os.path.exists(temp_file_path): os.remove(temp_file_path)
        await file.close() # Đảm bảo đóng file gốc
        raise http_exc
    except Exception as e: # Các lỗi khác khi ghi file tạm
        if os.path.exists(temp_file_path): os.remove(temp_file_path)
        print(f"Lỗi khi ghi file tạm: {e}")
        await file.close() # Đảm bảo đóng file gốc
        raise HTTPException(status_code=500, detail="Lỗi khi xử lý file upload.")
    
    # Nếu kích thước ổn, đổi tên file tạm thành file chính thức
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    final_file_path = os.path.join(target_dir, unique_filename)
    try:
        shutil.move(temp_file_path, final_file_path)
    except Exception as e:
        if os.path.exists(temp_file_path): os.remove(temp_file_path) 
        print(f"Lỗi di chuyển file tạm: {e}")
        # await file.close() # File gốc đã được đóng ở finally hoặc exception trên
        raise HTTPException(status_code=500, detail="Không thể hoàn tất lưu file.")
    # Không cần finally cho file.close() ở đây nữa vì đã xử lý
    
    await file.close() # Đóng file gốc sau khi đã xử lý xong

    # Tạo URL tương đối chính xác
    relative_path_parts = ["uploads"]
    if sub_folder:
        relative_path_parts.append(sub_folder)
    relative_path_parts.append(unique_filename)
    
    file_url = f"/static/{'/'.join(relative_path_parts)}"
        
    return schemas.FileUploadResponse(filename=unique_filename, file_url=file_url)


# Thay thế endpoint /uploadcourseimage/ bằng cách gọi /uploadfile/?sub_folder=course_images từ frontend
# Bạn không cần endpoint /uploadcourseimage/ riêng nữa nếu đã có /uploadfile/ chung.
# Nếu vẫn muốn giữ /uploadcourseimage/ riêng, bạn có thể định nghĩa nó và gọi logic tương tự như /uploadfile/
# nhưng với target_dir cố định là COURSE_IMAGES_DIR


if __name__ == "__main__":
    import uvicorn
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Database tables created/checked successfully.")
    except Exception as e:
        print(f"Error creating/checking database tables: {e}")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)