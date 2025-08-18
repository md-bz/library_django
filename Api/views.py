from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import db
from helpers import slugify


@csrf_exempt
@require_http_methods(["GET","POST"])
def books(request):
    if request.method == "GET":
        search_query = request.GET.get("search")
        if search_query:
            return JsonResponse({"books": db.search_books(search_query)})
        return JsonResponse({"books": db.get_books()})
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not all(k in data for k in ("title", "author", "year")):
        return JsonResponse({"error": "Missing fields"}, status=400)

    book = {
        "title": data["title"],
        "author": data["author"],
        "year": data["year"],
        "slug": slugify(data["title"])
    }
    db.add_book(book)
    return JsonResponse({"message": "Book added", "book": book}, status=201)


def update_book(request, id, book):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    updated_book = {
        "id": id,
        "title": data.get("title", book["title"]),
        "author": data.get("author", book["author"]),
        "year": data.get("year", book["year"]),
        "slug": slugify(data.get("title", book["title"]))
    }
    db.update_book(updated_book)
    return JsonResponse({"message": "Book updated", "book": updated_book})


def remove_book(id, book):
    db.remove_book(id)
    return JsonResponse({"message": "Book removed"},status=204)


@csrf_exempt
@require_http_methods(["GET","PATCH","DELETE"])
def book_by_id(request, id):
    book = db.get_book_by_id(id)
    if not book:
        return JsonResponse({"error": "Book not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(book)
    elif request.method == "PATCH":
        return update_book(request, id, book)
    return remove_book(id, book)


@csrf_exempt
@require_http_methods(["GET","PATCH","DELETE"])
def book_by_slug(request, slug):
    book = db.get_book(slug)
    if not book:
        return JsonResponse({"error": "Book not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(book)
    elif request.method == "PATCH":
        return update_book(request, book["id"], book)
    return remove_book(book["id"], book)
