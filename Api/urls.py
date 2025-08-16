from django.urls import path
from . import views

urlpatterns = [
    path("books/",views.index,name="index"),
    path("books/<int:id>/",views.book_by_id,name="book_by_id"),    
    path("books/<slug:slug>/",views.book,name="book"),
    path("<path:path>/",views.not_found),
]
