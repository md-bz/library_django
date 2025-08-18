from django.urls import path
from . import views

urlpatterns = [
    path("books/",views.books,name="api_index"),
    path("books/<int:id>/",views.book_by_id,name="api_book_by_id"),    
    path("books/<slug:slug>/",views.book_by_slug,name="api_book"),
]
