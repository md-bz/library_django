import json
from typing import Optional, List, Dict, Any

FILENAME = "db.json"

def read_books_from_file() -> List[Dict[str, Any]]:
    with open(FILENAME, "r") as file:
        return json.load(file)

def write_books_to_file(books: List[Dict[str, Any]]) -> None:
    with open(FILENAME, "w") as file:
        json.dump(books, file, indent=4)

def get_book(slug: str) -> Optional[Dict[str, Any]]:
    books = read_books_from_file()
    return next((book for book in books if book["slug"] == slug), None)

def get_books() -> List[Dict[str, Any]]:
    return read_books_from_file()

def get_book_by_id(book_id: int) -> Optional[Dict[str, Any]]:
    books = read_books_from_file()
    return next((book for book in books if book["id"] == book_id), None)

def remove_book(book_id: int) -> None:
    books = read_books_from_file()
    books = [book for book in books if book["id"] != book_id]
    write_books_to_file(books)

def add_book(book: Dict[str, Any]) -> None:
    books = read_books_from_file()
    # assign next available ID
    new_id = max([b["id"] for b in books], default=0) + 1
    book["id"] = new_id
    books.append(book)
    write_books_to_file(books)

def update_book(book: Dict[str, Any]) -> None:
    books = read_books_from_file()
    for idx, b in enumerate(books):
        if b["id"] == book["id"]:
            books[idx] = book
            break
    write_books_to_file(books)
