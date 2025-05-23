from sqlalchemy.orm import Session
from app.models.part import Part
from app.schemas.part import PartCreate, PartUpdate

def create_part(db: Session, part: PartCreate):
    db_part = Part(**part.dict())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

def get_part(db: Session, part_id: int):
    return db.query(Part).filter(Part.part_id == part_id).first()

def get_parts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Part).offset(skip).limit(limit).all()

def update_part(db: Session, part_id: int, part: PartUpdate):
    db_part = db.query(Part).filter(Part.part_id == part_id).first()
    if db_part:
        for key, value in part.dict(exclude_unset=True).items():
            setattr(db_part, key, value)
        db.commit()
        db.refresh(db_part)
    return db_part

def delete_part(db: Session, part_id: int):
    db_part = db.query(Part).filter(Part.part_id == part_id).first()
    if db_part:
        db.delete(db_part)
        db.commit()
    return db_part