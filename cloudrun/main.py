from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, StrictInt, Field 

app = FastAPI()

# Sample book data:
books = [
    {"id": 1, "title": "Chronicles of Narnia", "author": "C S Lewis",  "published_year": 1950},
    {"id": 2, "title": "Howl's Moving Castle", "author": "Diana Wynne Jones", "published_year": 1986},
    {"id": 3, "title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams",  "published_year": 1979},
    {"id": 4, "title": "20000 Leagues Beneath the Sea",  "author": "Jules Verne", "published_year": 1870},
    {"id": 5, "title": "Edible Economics", "author": "Ha-Joon Chang",  "published_year": 2023},
    {"id": 6, "title": "Charmed Life",  "author": "Diana Wynne Jones", "published_year": 1977},
]

class BookRequest(BaseModel):
    title: str = Field(min_length=3, max_length=1000)
    author: str = Field(min_length=3, max_length=1000)
    published_year: StrictInt = Field(gt=1800, lt=2025)

#To read book data:
@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/books")
async def read_all():
    return books

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int = Path(gt=0)):
    book_result = next((book for book in books if book["id"] == book_id), None)

    if book_result is not None:
        return book_result
    
    raise HTTPException(status_code=404, detail="Book not found")

#To add book data:
@app.post("/books")
async def create_book(book_request: BookRequest):
    new_book_id = max(book["id"] for book in books) + 1
    new_book = {
        "id": new_book_id,
        "title": book_request.title,
        "author": book_request.author,
        "published_year": book_request.published_year
    }
    books.append(new_book)
    return {"message": "A new book is successfully created"}

#To update book data:
@app.put("/books/{book_id}")
async def update_book(book_id: int, book_request: BookRequest):
    book_result = next((book for book in books if book["id"] == book_id), None)
    if book_result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_result["title"] = book_request.title
    book_result["author"] = book_request.author
    book_result["published_year"] = book_request.published_year

    return {"message": "Book successfully updated"}

#To delete book data:
@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_result = next((book for book in books if book["id"] == book_id), None)

    if book_result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        books.remove(book_result)

    return {"message": "Book successfully deleted"}
