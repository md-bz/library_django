from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from typing import Dict

import db


@require_http_methods(["GET", "POST"])
def login(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "Users/login.html")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")

    user = db.get_user(username)
    if user and user.get("password") == password:
        request.session["username"] = user["username"]
        request.session["role"] = user.get("role", "user")
        return redirect("dashboard")

    return render(request, "Users/login.html", {"error": "Invalid username or password"})



@require_http_methods(["GET", "POST"])
def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "Users/signup.html")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    role = request.POST.get("role") or "user"

    if not username or not password:
        return render(request, "Users/signup.html", {"error": "Username and password are required"})

    try:
        db.add_user({"username": username, "password": password, "role": role})
    except ValueError as exc:
        return render(request, "Users/signup.html", {"error": str(exc)})

    return redirect("login")



@require_http_methods(["GET"])
def dashboard(request: HttpRequest) -> HttpResponse:
    username = request.session.get("username")
    role = request.session.get("role")
    if not username:
        return redirect("login")

    # List of books for everyone
    books = db.get_books()
    users = db.get_users() if role == "admin" else []

    context = {
        "username": username,
        "role": role,
        "notifications": [],
        "books": books,
        "users": users,
    }
    return render(request, "Users/dashboard.html", context)


@require_http_methods(["GET", "POST"])
def user_update(request: HttpRequest, username: str) -> HttpResponse:
    current_username = request.session.get("username")
    role = request.session.get("role")
    if not current_username:
        return redirect("login")
    if role != "admin":
        return redirect("dashboard")

    user = db.get_user(username)
    if not user:
        return redirect("dashboard")

    if request.method == "GET":
        return render(request, "Users/user_update.html", {"user": user})

    new_password = request.POST.get("password")
    new_role = request.POST.get("role")
    payload: Dict[str, str] = {"username": username}
    if new_password is not None and new_password != "":
        payload["password"] = new_password
    if new_role:
        payload["role"] = new_role
    try:
        db.update_user(payload)  # type: ignore[arg-type]
        return redirect("dashboard")
    except ValueError as exc:
        return render(request, "Users/user_update.html", {"user": user, "error": str(exc)})


@require_http_methods(["POST"])
def user_delete(request: HttpRequest, username: str) -> HttpResponse:
    current_username = request.session.get("username")
    role = request.session.get("role")
    if not current_username:
        return redirect("login")
    if role != "admin":
        return redirect("dashboard")

    try:
        db.remove_user(username)
    except ValueError:
        pass
    return redirect("dashboard")
