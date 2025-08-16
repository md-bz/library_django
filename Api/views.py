from django.http import JsonResponse
from db import get_books,get_book,get_book_by_id


def index(request):
    return JsonResponse({"books":get_books()})

def book(request,slug):
    book = get_book(slug)
    if book:
        return JsonResponse(book)
    else:
        return JsonResponse({"error":"Book not found"},status=404)

def book_by_id(request,id):
    book = get_book_by_id(id)
    if book:
        return JsonResponse(book)
    else:
        return JsonResponse({"error":"Book not found"},status=404)  
def not_found(request,path):
    return JsonResponse({"error":"Not found"},status=404)


