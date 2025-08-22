import json
from typing import Optional, List, Dict, Any
import os

FILENAME = "db.json"
USERS_FILENAME = "users.json"

def read_books_from_file() -> List[Dict[str, Any]]:
    if not os.path.exists(FILENAME):
        return []  
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

def search_books(query: str) -> List[Dict[str, Any]]:
    books = read_books_from_file()
    return [book for book in books if query.lower() in book["title"].lower()]

# -----------------------------
# Users CRUD (stored in users.json)
# Schema: {"username": str, "password": str, "role": "admin"|"user", "notifications": List[str]}
# -----------------------------

def read_users_from_file() -> List[Dict[str, Any]]:
    if not os.path.exists(USERS_FILENAME):
        return []
    with open(USERS_FILENAME, "r") as file:
        return json.load(file)


def write_users_to_file(users: List[Dict[str, Any]]) -> None:
    with open(USERS_FILENAME, "w") as file:
        json.dump(users, file, indent=4)


def get_user(username: str) -> Optional[Dict[str, Any]]:
    users = read_users_from_file()
    return next((user for user in users if user.get("username") == username), None)


def get_users() -> List[Dict[str, Any]]:
    return read_users_from_file()


def add_user(user: Dict[str, Any]) -> None:
    users = read_users_from_file()

    required_fields = {"username", "password", "role"}
    missing_fields = [field for field in required_fields if field not in user]
    if missing_fields:
        raise ValueError(f"Missing user fields: {', '.join(missing_fields)}")

    if any(u.get("username") == user["username"] for u in users):
        raise ValueError("Username already exists")

    if user["role"] not in ("admin", "user"):
        raise ValueError("Invalid role; must be 'admin' or 'user'")

    users.append({
        "username": user["username"],
        "password": user["password"],
        "role": user["role"],
        "notifications": [],
    })
    write_users_to_file(users)


def update_user(user: Dict[str, Any]) -> None:
    users = read_users_from_file()

    updated = False
    for idx, existing in enumerate(users):
        if existing.get("username") == user.get("username"):
            merged = {**existing, **user}
            if merged.get("role") not in ("admin", "user"):
                raise ValueError("Invalid role; must be 'admin' or 'user'")
            users[idx] = merged
            updated = True
            break

    if not updated:
        raise ValueError("User not found")

    write_users_to_file(users)


def remove_user(username: str) -> None:
    users = read_users_from_file()
    new_users = [u for u in users if u.get("username") != username]
    if len(new_users) == len(users):
        raise ValueError("User not found")
    write_users_to_file(new_users)

