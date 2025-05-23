from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.models.course import Course  # Thêm dòng này

router = APIRouter()

@router.post("/", response_model=schemas.Chapter)
def create_chapter(chapter: schemas.ChapterCreate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == chapter.course_id).first()
    if not course:
        raise HTTPException(status_code=400, detail="CourseID does not exist")
    return crud.chapter.create_chapter(db=db, chapter=chapter)

@router.get("/{chapter_id}", response_model=schemas.Chapter)
def read_chapter(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter = crud.chapter.get_chapter(db=db, chapter_id=chapter_id)
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return db_chapter

@router.put("/{chapter_id}", response_model=schemas.Chapter)
def update_chapter(chapter_id: int, chapter: schemas.ChapterUpdate, db: Session = Depends(get_db)):
    db_chapter = crud.chapter.get_chapter(db=db, chapter_id=chapter_id)
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return crud.chapter.update_chapter(db=db, chapter_id=chapter_id, chapter=chapter)

@router.delete("/{chapter_id}", response_model=schemas.Chapter)
def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter = crud.chapter.get_chapter(db=db, chapter_id=chapter_id)
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return crud.chapter.delete_chapter(db=db, chapter_id=chapter_id)