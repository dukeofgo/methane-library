from sqlalchemy import select
from sqlalchemy.orm import Session

from ..auth import service
from . import models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.execute(select(models.User).where(models.User.id == user_id)).first()

def get_user_by_email(db: Session, email: str):
    return db.execute(select(models.User).where(models.User.email == email)).first()

def create_user(user: schemas.UserCreate, db: Session):
    #hash password with passlib
    user_hashed_password = service.hash_password(user.password)
    #instantiate User model
    db_user = models.User(email=user.email, name=user.name, age=user.age, hashed_password=user_hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def update_user(db: Session, user: schemas.UserUpdate, user_id: int):
    #query user with user id
    query_user = get_user_by_id(user_id=user_id, db=db)
    #turn user (pydantic model) into python dict
    #allow partial update with exclude_unset=True
    update_data = user.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(query_user, key, value)

    db.commit()
    db.refresh(query_user)

    return query_user

def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(user_id=user_id, db=db)

    db.delete(db_user)
    db.commit()

    return {"message": "User deleted successfully"}