from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    email: str
    name: str
    age: int

class User(UserBase):
    id: int
    is_active: bool
    is_borrower: bool
    is_member: bool
    borrowed_books: list
    registered_date: date   

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserCreate):
    pass
