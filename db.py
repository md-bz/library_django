import json
import time
from typing import Optional, List, Dict, Any
import os

FILENAME = "db.json"
USERS_FILENAME = "users.json"
BORROWINGS_FILENAME = "borrowings.json"

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

def add_notification(username: str, notification: str) -> None:
    user = get_user(username)
    if not user:
        raise ValueError("User not found")
    user["notifications"].append(notification)
    update_user(user)

def clear_user_notifications(username: str) -> None:
    user = get_user(username)
    if not user:
        raise ValueError("User not found")
    user["notifications"] = []
    update_user(user)


# -----------------------------
# Borrowings CRUD (stored in borrowings.json)
# Schema: {"id": int, "book_id": int, "user_id": str, "borrowed_for": str, "borrowed_till": int|null, "approved": bool|null, "returned_at": int|null}
# -----------------------------

def read_borrowings_from_file() -> List[Dict[str, Any]]:
    if not os.path.exists(BORROWINGS_FILENAME):
        return []
    with open(BORROWINGS_FILENAME, "r") as file:
        return json.load(file)


def write_borrowings_to_file(borrowings: List[Dict[str, Any]]) -> None:
    with open(BORROWINGS_FILENAME, "w") as file:
        json.dump(borrowings, file, indent=4)


def get_borrowings() -> List[Dict[str, Any]]:
    return read_borrowings_from_file()


def get_borrowing_by_id(borrowing_id: int) -> Optional[Dict[str, Any]]:
    borrowings = read_borrowings_from_file()
    return next((borrowing for borrowing in borrowings if borrowing["id"] == borrowing_id), None)

def get_user_borrowings(username: str) -> List[Dict[str, Any]]:
    borrowings = read_borrowings_from_file()
    return [borrowing for borrowing in borrowings if borrowing["user_id"] == username]


def get_book_borrowings(book_id: int) -> List[Dict[str, Any]]:
    borrowings = read_borrowings_from_file()
    return [borrowing for borrowing in borrowings if borrowing["book_id"] == book_id]


def get_active_borrowings() -> List[Dict[str, Any]]:
    borrowings = read_borrowings_from_file()
    return [borrowing for borrowing in borrowings if borrowing.get("returned_at") is None and borrowing.get("approved") is True]


def get_waiting_for_approve() -> List[Dict[str, Any]]:
    borrowings = read_borrowings_from_file()
    return [borrowing for borrowing in borrowings if borrowing.get("approved") is None]


def get_available_books() -> List[Dict[str, Any]]:
    books = get_books()
    active_borrowings = get_active_borrowings()
    
    borrowed_book_ids = {borrowing["book_id"] for borrowing in active_borrowings}
    
    return [book for book in books if book["id"] not in borrowed_book_ids]



def add_borrowing(borrowing: Dict[str, Any]) -> None:
    borrowings = read_borrowings_from_file()
    
    required_fields = {"book_id", "user_id", "borrowed_for"}
    missing_fields = [field for field in required_fields if field not in borrowing]
    if missing_fields:
        raise ValueError(f"Missing borrowing fields: {', '.join(missing_fields)}")
    
    book = get_book_by_id(borrowing["book_id"])
    if not book:
        raise ValueError("Book not found")
    
    user = get_user(borrowing["user_id"])
    if not user:
        raise ValueError("User not found")
    
    active_borrowings = get_book_borrowings(borrowing["book_id"])
    if any(b.get("returned_at") is None for b in active_borrowings):
        raise ValueError("Book is already borrowed")

    # Check if user has any unreturned books
    user_active_borrowings = [b for b in get_user_borrowings(borrowing["user_id"]) if b.get("returned_at") is None]
    if user_active_borrowings:
        raise ValueError("User has unreturned books")

    # Check if user has more than 2 overdue books in their history
    user_borrowings = get_user_borrowings(borrowing["user_id"])
    overdue_count = sum(1 for b in user_borrowings if is_borrowing_overdue(b))
    if overdue_count >= 2:
        raise ValueError("User has too many overdue books in their history")

    
    new_id = max([b["id"] for b in borrowings], default=0) + 1
    
    borrowing_record = {
        "id": new_id,
        "book_id": borrowing["book_id"],
        "user_id": borrowing["user_id"],
        "borrowed_for": str(borrowing["borrowed_for"]),
        "borrowed_till": None,
        "approved": None,
        "returned_at": None
    }
    
    borrowings.append(borrowing_record)
    write_borrowings_to_file(borrowings)


def return_book(borrowing_id: int) -> None:
    borrowings = read_borrowings_from_file()
    
    for idx, borrowing in enumerate(borrowings):
        if borrowing["id"] == borrowing_id and borrowing.get("returned_at") is None and borrowing.get("approved") is True:
            borrowings[idx]["returned_at"] = int(time.time())
            write_borrowings_to_file(borrowings)
            return
    
    raise ValueError("Borrowing not found")


def approve_borrow(borrowing_id: int, approved: bool) -> None:
    borrowings = read_borrowings_from_file()
    
    for idx, borrowing in enumerate(borrowings):
        if borrowing["id"] == borrowing_id and borrowing.get("approved") is None:
            borrowings[idx]["approved"] = approved
            
            if approved:
                # Calculate borrowed_till from approval time
                current_timestamp = int(time.time())
                borrowed_for_days = int(borrowing["borrowed_for"])
                borrowed_till_timestamp = current_timestamp + (borrowed_for_days * 24 * 60 * 60)
                borrowings[idx]["borrowed_till"] = borrowed_till_timestamp
            
            write_borrowings_to_file(borrowings)
            return
    
    raise ValueError("Borrowing request not found")


def remove_borrowing(borrowing_id: int) -> None:
    borrowings = read_borrowings_from_file()
    new_borrowings = [b for b in borrowings if b["id"] != borrowing_id]
    if len(new_borrowings) == len(borrowings):
        raise ValueError("Borrowing not found")
    write_borrowings_to_file(new_borrowings)


def is_borrowing_overdue(borrowing: Dict[str, Any]) -> bool:
    if borrowing.get("returned_at") is not None or borrowing.get("approved") is not True:
        return False  # Book has been returned or not approved
    current_timestamp = int(time.time())
    return current_timestamp > borrowing["borrowed_till"]


def get_overdue_borrowings() -> List[Dict[str, Any]]:
    active_borrowings = get_active_borrowings()
    return [borrowing for borrowing in active_borrowings if is_borrowing_overdue(borrowing)]
