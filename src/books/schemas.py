from pydantic import BaseModel
from datetime import date

class BookBase(BaseModel):
    title: str
    author: str
    edition: str | None 
    publisher: str
    publish_date: str | None  
    publish_place: str | None
    number_of_pages: int | None 
    description: str | None 
    language: str | None 
    isbn: str
    lccn: str | None 
    subtitle: str | None 
    subjects: str | None 

class Book(BookBase):
    id: int
    added_date: date
    borrowed_date: date | None 
    returned_date: date | None 
    is_borrowed: bool | None = None

    class Config:
        orm_mode = True

class BookCreate(BookBase):
    pass

class BookUpdate(BookCreate):
    pass