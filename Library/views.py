from django.shortcuts import render
from .db import get_books,get_book,get_book_by_id

def index(request):
    return render(request, "Library/index.html",{"books":get_books()})

def book(request,slug):
    book = get_book(slug)
    if book:
        return render(request, "Library/book.html",{"book":book})
    else:
        return render(request, "Library/404.html")

def book_by_id(request,id):
    book = get_book_by_id(id)
    if book:
        return render(request, "Library/book.html",{"book":book})
    else:
        return render(request, "Library/404.html")  