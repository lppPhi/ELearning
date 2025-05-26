from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.models import RegisteredCourse
from app.schemas.user import UserLogin
import logging

router = APIRouter()
logger = logging.getLogger("user_router")

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Received user data: {user.dict()}")
    try:
        created_user = crud.user.create_user(db=db, user=user)
        logger.info(f"User created: {created_user.user_id}")
        return created_user
    except ValueError as ve:
        logger.warning(str(ve))
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user.update_user(db=db, user_id=user_id, user=user)

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user.delete_user(db=db, user_id=user_id)

@router.post("/login")
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    user = crud.user.get_user_by_email(db, email=login_data.email)
    if not user or user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
    return {
        "user_id": user.user_id,
        "full_name": user.full_name,
        "email": user.email
    }