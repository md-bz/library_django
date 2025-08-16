import json
from typing import Optional, Dict, Any

FILENAME = "db.json"

def read_books_from_file() -> Dict[str, Any]:
    with open(FILENAME, "r") as file:
        return json.load(file)

def write_books_to_file(books: Dict[str, Any]) -> None:
    with open(FILENAME, "w") as file:
        json.dump(books, file, indent=4)

def get_book(slug: str) -> Optional[Dict[str, Any]]:
    books = read_books_from_file()
    return next((book for book in books.values() if book["slug"] == slug), None)

def get_books() -> Dict[str, Any]:
    return read_books_from_file()

def get_book_by_id(book_id: int) -> Optional[Dict[str, Any]]:
    books = read_books_from_file()
    return books.get(str(book_id))

def remove_book(book_id: int) -> None:
    books = read_books_from_file()
    if str(book_id) in books:
        del books[str(book_id)]
        write_books_to_file(books)

def add_book(book: Dict[str, Any]) -> None:
    books = read_books_from_file()
    id =len(books) + 1
    books[id] = book
    write_books_to_file(books)

def update_book(book: Dict[str, Any]) -> None:
    books = read_books_from_file()
    if str(book["id"]) in books:
        books[str(book["id"])] = book
        write_books_to_file(books)
