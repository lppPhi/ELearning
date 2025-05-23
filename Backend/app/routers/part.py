from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.models.chapter import Chapter  # Thêm dòng này

router = APIRouter()

@router.post("/", response_model=schemas.Part)
def create_part(part: schemas.PartCreate, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.chapter_id == part.chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=400, detail="ChapterID does not exist")
    return crud.part.create_part(db=db, part=part)

@router.get("/{part_id}", response_model=schemas.Part)
def read_part(part_id: int, db: Session = Depends(get_db)):
    db_part = crud.part.get_part(db=db, part_id=part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return db_part

@router.put("/{part_id}", response_model=schemas.Part)
def update_part(part_id: int, part: schemas.PartUpdate, db: Session = Depends(get_db)):
    db_part = crud.part.get_part(db=db, part_id=part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return crud.part.update_part(db=db, part_id=part_id, part=part)

@router.delete("/{part_id}", response_model=schemas.Part)
def delete_part(part_id: int, db: Session = Depends(get_db)):
    db_part = crud.part.get_part(db=db, part_id=part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return crud.part.delete_part(db=db, part_id=part_id)