"""
URL configuration for Library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index,name="index"),
    path("api/",include("Api.urls")),
    path("errors/",include("Errors.urls")),
    path("books/",views.index,name="books"),
    path("books/add/",views.add_book,name="add_book"),
    path("books/<int:id>/update",views.update_book,name="update_book"),
    path("books/<int:id>/remove",views.remove_book,name="remove_book"),
    path("books/<int:id>/borrow",views.borrow_book,name="borrow_book"),
    path("books/waiting-approval",views.waiting_approval,name="waiting_approval"),
    path("books/active-borrowings",views.active_borrowings,name="active_borrowings"),
    path("books/<int:id>/return-book",views.return_book,name="return_book"),     
    path("books/<int:id>/",views.book_by_id,name="book_by_id"),
    path("books/<slug:slug>/",views.book,name="book"),
    path("users/",include("Users.urls")),
    path("<path:path>/",views.not_found),
]
