from sqlalchemy.orm import Session
from app.models.chapter import Chapter
from app.schemas.chapter import ChapterCreate, ChapterUpdate

def get_chapter(db: Session, chapter_id: int):
    return db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()

def get_chapters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Chapter).offset(skip).limit(limit).all()

def create_chapter(db: Session, chapter: ChapterCreate):
    db_chapter = Chapter(**chapter.dict())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

def update_chapter(db: Session, chapter_id: int, chapter: ChapterUpdate):
    db_chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
    if db_chapter:
        for key, value in chapter.dict(exclude_unset=True).items():
            setattr(db_chapter, key, value)
        db.commit()
        db.refresh(db_chapter)
    return db_chapter

def delete_chapter(db: Session, chapter_id: int):
    db_chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
    if db_chapter:
        db.delete(db_chapter)
        db.commit()
    return db_chapter