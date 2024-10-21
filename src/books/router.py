from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. database import get_db
from . import schemas, crud
import httpx, json

router = APIRouter(
    prefix = "/books",

)

TIMEOUT = 15.0


@router.post("/create", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(book_id=book.id, db=db)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exist")  
    return crud.create_book(book=book, db=db)

@router.post("/create/{isbn}", response_model=schemas.BookCreate)
async def create_book_by_isbn(isbn: str, db: Session = Depends(get_db)):

    OPENLIB_URL = f"http://openlibrary.org/api/volumes/brief/isbn/{isbn}.json"
    
    #request data from external API
    async with httpx.AsyncClient() as client:
        try:
            book_response = await client.get(OPENLIB_URL, timeout=15.0)

        except httpx.ReadTimeout:
            raise HTTPException(status_code=400, detail= "Request Time Out") 
        except httpx.RequestError:
            raise HTTPException(status_code=400, detail= "Request Error")
        
    #retrieve json data from HTTP response object
    json_content = book_response.json()
    #convert json data to python dict
    dict_content = json.loads(json_content)

    OPENLIB_KEY = list(dict_content['records'].keys())

    #select certain book keys
    selected_keys = {
        'title': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('data', {}).get('title', None),
        'author': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('data', {}).get('authors', [{}])[0].get('name', None),
        'edition': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('details', {}).get('details', {}).get('edition_name', None),
        'publisher': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('data', {}).get('publishers', [{}])[0].get('name', None),
        'publish_date': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('publishDates', [None])[0],
        'publish_place': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('data', {}).get('publish_places', [{}])[0].get('name', None),
        'number_of_pages': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('data', {}).get('number_of_pages', None),
        'description': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('details', {}).get('details', {}).get('description', {}).get('value', None),
        'language': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('details', {}).get('details', {}).get('languages', [{}])[0].get('key', None),
        'isbn': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('isbns', [None])[0],
        'lccn': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('data', {}).get('identifiers', {}).get('lccn', None)[0],
        'subtitle': dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('data', {}).get('subtitle', None),
        'subjects':  dict_content.get('records', {}).get(f'{OPENLIB_KEY[0]}', {}).get('details', {}).get('details', {}).get('subjects', None)[0],
}     
    #convert python dict to pydantic object
    book = schemas.BookCreate(**selected_keys)

    return crud.create_book(book=book, db=db)

@router.get("/retrieve/{isbn_or_id}", response_model=schemas.Book)
def get_book_by_isbn_id(isbn_or_id: str, db: Session):
    db_book = crud.get_book_by_isbn_or_id(isbn_or_id=isbn_or_id, db=db)
    if not db_book:
        raise HTTPException(status_code=400, detail="Book not found")
    return db_book

@router.get("/retrieve/books", response_model=list[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_books = crud.get_books(skip=skip, limit=limit, db=db)
    return db_books

@router.patch("/update/{book_id}", response_model=schemas.BookUpdate)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(book_id=book_id, db=db)
    if not db_book:
        raise HTTPException(status_code=400, detail="Book not found")
    return crud.update_book(book_id=book_id, book=book, db=db)

@router.delete("/delete/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(book_id=book_id, db=db)
    if not db_book:
        HTTPException(status_code=400, detail="Target book does not exist")
    return crud.delete_book(book_id=book_id, db=db)