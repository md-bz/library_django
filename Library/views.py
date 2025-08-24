from django.shortcuts import render,redirect
from Users.decorators import require_admin, require_auth
import db
from helpers import slugify
from datetime import datetime

def index(request):
    search_query = request.GET.get("search")
    available_only = request.GET.get("available_only") == "true"
    
    if search_query:
        if available_only:
            books = db.search_available_books(search_query)
        else:
            books = db.search_books(search_query)
    else:
        if available_only:
            books = db.get_available_books()
        else:
            books = db.get_books()
    
    return render(request, "Library/index.html", {
        "books": books,
        "search_query": search_query,
        "available_only": available_only
    })

def book(request,slug):
    book = db.get_book(slug)

    if book:
        return render(request, "Library/book.html",{"book":book})
    else:
        return render(request, "Library/404.html")

def book_by_id(request,id):
    book = db.get_book_by_id(id)
    if book:
        return render(request, "Library/book.html",{"book":book})
    else:
        return render(request, "Library/404.html")  
    
def not_found(request,path):
    return redirect("not_found")

@require_admin
def add_book(request):
    if request.method == "POST":
        book = request.POST.copy()
        if "title" not in book or "author" not in book or "year" not in book:
            return render(request, "Library/missing_fields.html")
        db.add_book({"title": book["title"], "author": book["author"], "year": book["year"],"slug":slugify(book["title"])})

        return redirect("index")
    else:
        return render(request, "Library/add_book.html")

@require_admin
def update_book(request,id):
    if request.method == "POST":
        book = request.POST.copy()
        if "title" not in book or "author" not in book or "year" not in book:
            return render(request, "Library/missing_fields.html")
        db.update_book({"id":id, "title": book["title"], "author": book["author"], "year": book["year"],"slug":slugify(book["title"])})
        return redirect("index")
    else:
        return render(request, "Library/update_book.html",{"book":db.get_book_by_id(id),"id":id})

@require_admin
def remove_book(request,id):
    db.remove_book(id)
    return redirect("index")


@require_auth
def borrow_book(request, id):

    book = db.get_book_by_id(id)
    if request.method == "GET":
        return render(request, "Library/borrow_book.html", {"book": book})
    
    borrowed_for = request.POST.get("borrowed_for")
    username = request.session.get("username")
    
    if not borrowed_for or not borrowed_for.isdigit() or int(borrowed_for) <= 0:
        return render(request, "Library/borrow_book.html", {
            "book": book,
            "error": "Please enter a valid number of days (greater than 0)"
        })
    
    try:
        user = db.get_user_by_username(username)
        if not user:
            return render(request, "Library/borrow_book.html", {
                "book": book,
                "error": "User not found"
            })
        
        db.add_borrowing({
            "book_id": id,
            "user_id": user["id"],
            "borrowed_for": int(borrowed_for)
        })
        return redirect("index")
    except ValueError as exc:
        return render(request, "Library/borrow_book.html", {
            "book": book,
            "error": str(exc)
        })


@require_admin
def waiting_approval(request):
    if request.method == "GET":
        waiting_requests = db.get_waiting_for_approve()

        requests = []
        for req in waiting_requests:
            book = db.get_book_by_id(req["book_id"])
            user = db.get_user_by_id(req["user_id"])
            requests.append({
                "request": req,
                "book": book,
                "user": user
            })

        return render(request, "Library/waiting_approval.html", {
            "requests": requests
        })

    try:
        borrowing_id = int(request.POST.get("borrowing_id"))
        action = request.POST.get("action")
        
        if action == "approve":
            db.approve_borrow(borrowing_id, True)
        elif action == "reject":
            db.approve_borrow(borrowing_id, False)
            
        return redirect("waiting_approval")
    except ValueError as exc:
        return redirect("waiting_approval")

@require_admin
def active_borrowings(request):
    borrowings = db.get_active_borrowings()
    for borrowing in borrowings:
        book = db.get_book_by_id(borrowing["book_id"])
        borrowing["book"] = book
        user = db.get_user_by_id(borrowing["user_id"])
        borrowing["user"] = user

    return render(request, "Library/active_borrowings.html",{"borrowings":borrowings})  

@require_admin
def return_book(request,id):
    borrowing = db.get_borrowing_by_id(id)
    book  = db.get_book_by_id(borrowing["book_id"])
    user  = db.get_user_by_id(borrowing["user_id"])

    borrowing["borrowed_till"] = datetime.fromtimestamp(borrowing["borrowed_till"]) if borrowing["borrowed_till"] else None
    borrowing["returned_at"] = datetime.fromtimestamp(borrowing["returned_at"]) if borrowing["returned_at"] else None

    
    if request.method == "GET":
        return render(request, "Library/return_book.html",{"book":book,"borrowing":borrowing,"user":user})
    try:
        db.return_book(id)
        return render(request, "Library/return_book.html",{"book":book,"borrowing":borrowing,"user":user,"success":"Book returned successfully"})
    except ValueError as exc:    
        return render(request, "Library/return_book.html",{"book":book,"borrowing":borrowing,"user":user,"error":str(exc)})
    