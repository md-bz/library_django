from django.shortcuts import render,redirect
import db
from helpers import slugify

def index(request):
    return render(request, "Library/index.html",{"books":db.get_books().values()})

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

def add_book(request):
    if request.method == "POST":
        book = request.POST.copy()
        if "title" not in book or "author" not in book or "year" not in book:
            return render(request, "Library/missing_fields.html")
        db.add_book({"title": book["title"], "author": book["author"], "year": book["year"],"slug":slugify(book["title"])})

        return redirect("index")
    else:
        return render(request, "Library/add_book.html")

def update_book(request,id):
    if request.method == "POST":
        book = request.POST.copy()
        if "title" not in book or "author" not in book or "year" not in book:
            return render(request, "Library/missing_fields.html")
        db.update_book({"id":id, "title": book["title"], "author": book["author"], "year": book["year"],"slug":slugify(book["title"])})
        return redirect("index")
    else:
        return render(request, "Library/update_book.html",{"book":db.get_book_by_id(id),"id":id})

def remove_book(request,id):
    db.remove_book(id)
    return redirect("index")

