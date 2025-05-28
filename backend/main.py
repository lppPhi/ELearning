from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import SessionLocal, engine
from typing import List
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Thêm cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc chỉ định ['http://127.0.0.1:5500']
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# USERS
@app.post("/users/", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.put("/users/{user_id}", response_model=schemas.UserInfo)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}

@app.get("/users/{user_id}", response_model=schemas.UserInfo)
def get_user_basic(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_basic(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/login", response_model=schemas.UserInfo)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_login(db, user.UserName)
    if not db_user or db_user.Password != user.Password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user

# COURSES
@app.get("/courses/all", response_model=List[schemas.CourseInfo])
def get_all_courses(db: Session = Depends(get_db)):
    return crud.get_all_courses(db)

@app.post("/courses/", response_model=schemas.CourseInfo)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)

@app.put("/courses/{course_id}", response_model=schemas.CourseInfo)
def update_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = crud.update_course(db, course_id, course)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.delete_course(db, course_id)
    if not db_course:
        raise HTTPException(status_code=400, detail="Cannot delete course (maybe registered)")
    return {"ok": True}

@app.get("/courses/{course_id}", response_model=schemas.CourseInfo)
def get_course_basic(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_basic(db, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@app.get("/courses/{course_id}/detail", response_model=schemas.CourseDetail)
def get_course_detail(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_detail(db, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@app.get("/courses/{course_id}/creator", response_model=schemas.UserInfo)
def get_course_creator_info(course_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_course_creator_info(db, course_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# CHAPTERS
@app.post("/chapters/", response_model=schemas.ChapterInfo)
def create_chapter(chapter: schemas.ChapterCreate, db: Session = Depends(get_db)):
    return crud.create_chapter(db, chapter)

@app.put("/chapters/{chapter_id}", response_model=schemas.ChapterInfo)
def update_chapter(chapter_id: int, chapter: schemas.ChapterUpdate, db: Session = Depends(get_db)):
    db_chapter = crud.update_chapter(db, chapter_id, chapter)
    if not db_chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return db_chapter

@app.delete("/chapters/{chapter_id}")
def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter = crud.delete_chapter(db, chapter_id)
    if not db_chapter:
        raise HTTPException(status_code=400, detail="Cannot delete chapter (maybe has parts)")
    return {"ok": True}

@app.get("/courses/{course_id}/chapters", response_model=List[schemas.ChapterInfo])
def get_chapters_by_course(course_id: int, db: Session = Depends(get_db)):
    return crud.get_chapters_by_course(db, course_id)

# PARTS
@app.post("/parts/", response_model=schemas.PartInfo)
def create_part(part: schemas.PartCreate, db: Session = Depends(get_db)):
    return crud.create_part(db, part)

@app.put("/parts/{part_id}", response_model=schemas.PartInfo)
def update_part(part_id: int, part: schemas.PartUpdate, db: Session = Depends(get_db)):
    db_part = crud.update_part(db, part_id, part)
    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")
    return db_part

@app.delete("/parts/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db)):
    db_part = crud.delete_part(db, part_id)
    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")
    return {"ok": True}

@app.get("/chapters/{chapter_id}/parts", response_model=List[schemas.PartInfo])
def get_parts_by_chapter(chapter_id: int, db: Session = Depends(get_db)):
    return crud.get_parts_by_chapter(db, chapter_id)

# REGISTERED COURSES
@app.post("/registered-courses/", response_model=schemas.RegisteredCourseInfo)
def create_registered_course(reg: schemas.RegisteredCourseCreate, db: Session = Depends(get_db)):
    return crud.create_registered_course(db, reg)

@app.get("/users/{user_id}/registered-courses", response_model=List[schemas.RegisteredCourseInfo])
def get_registered_courses_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_registered_courses_by_user(db, user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
