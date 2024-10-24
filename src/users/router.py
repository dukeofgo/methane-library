from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from . import crud, schemas, service
from .database import get_db

router = APIRouter(
    prefix = "/users",
)

@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already existed
    db_user = crud.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user, db=db)

@router.get("/retrieve/{email}", response_model=schemas.User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(email=email, db=db)
    if not db_user: 
        raise HTTPException(status_code=404, detail="Target user does not exist")
    return db_user

@router.patch("/update/{user_id}", response_model=schemas.User)
def update_user(user: schemas.UserUpdate, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        HTTPException(status_code=400, detail="Target user does not exist")
    updated_db_user = crud.update_user(user_id=user_id, user=user, db=db)
    return updated_db_user

@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        HTTPException(status_code=400, detail="Target user does not exist")
    return crud.delete_user(user_id=user_id, db=db)

@router.get("/users/me/", response_model=schemas.User)
async def get_users_me(current_user: Annotated[schemas.User, Security(service.get_current_user, scopes=["own"])]):
    return current_user