from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.models.course import Course  # Thêm dòng này

router = APIRouter()

@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == category.course_id).first()
    if not course:
        raise HTTPException(status_code=400, detail="CourseID does not exist")
    return crud.category.create_category(db=db, category=category)

@router.get("/", response_model=list[schemas.Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = crud.category.get_categories(db=db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.category.get_category(db=db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    category_data = crud.category.get_category(db=db, category_id=category_id)
    if category_data is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.category.update_category(db=db, category_id=category_id, category=category)

@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.category.get_category(db=db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.category.delete_category(db=db, category_id=category_id)