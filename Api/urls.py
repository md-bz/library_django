from django.urls import path
from . import views

urlpatterns = [
    path("books/",views.index,name="api_index"),
    path("books/<int:id>/",views.book_by_id,name="api_book_by_id"),    
    path("books/<slug:slug>/",views.book,name="api_book"),
    path("<path:path>/",views.not_found, name="api_not_found"),
]
