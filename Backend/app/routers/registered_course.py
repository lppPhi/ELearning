from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.models.user import User
from app.models.course import Course

router = APIRouter()

@router.post("/", response_model=schemas.RegisteredCourse)
def register_course(
    registered_course: schemas.RegisteredCourseCreate, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == registered_course.user_id).first()
    course = db.query(Course).filter(Course.course_id == registered_course.course_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="UserID does not exist")
    if not course:
        raise HTTPException(status_code=400, detail="CourseID does not exist")
    return crud.registered_course.create_registered_course(db=db, registered_course=registered_course)

@router.get("/{registered_course_id}", response_model=schemas.RegisteredCourse)
def get_registered_course(
    registered_course_id: int, db: Session = Depends(get_db)
):
    db_registered_course = crud.registered_course.get_registered_course(db=db, registered_course_id=registered_course_id)
    if db_registered_course is None:
        raise HTTPException(status_code=404, detail="Registered course not found")
    return db_registered_course

@router.get("/", response_model=list[schemas.RegisteredCourse])
def get_registered_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.registered_course.get_registered_courses(db=db, skip=skip, limit=limit)

@router.delete("/{registered_course_id}", response_model=schemas.RegisteredCourse)
def delete_registered_course(
    registered_course_id: int, db: Session = Depends(get_db)
):
    db_registered_course = crud.registered_course.delete_registered_course(db=db, registered_course_id=registered_course_id)
    if db_registered_course is None:
        raise HTTPException(status_code=404, detail="Registered course not found")
    return db_registered_course