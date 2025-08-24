from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from typing import Dict

import db
from .decorators import require_auth, require_admin


@require_http_methods(["GET", "POST"])
def login(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "Users/login.html")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")

    user = db.get_user_by_username(username)
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



@require_auth
@require_http_methods(["GET"])
def dashboard(request: HttpRequest) -> HttpResponse:
    username = request.session.get("username")
    role = request.session.get("role")

    # List of books for everyone
    books = db.get_books()
    users = db.get_users() if role == "admin" else []
    user = db.get_user_by_username(username)

    context = {
        "username": username,
        "role": role,
        "user":user,
        "notifications": user['notifications'],
        "books": books,
        "users": users,
    }
    return render(request, "Users/dashboard.html", context)


@require_admin
@require_http_methods(["GET", "POST"])
def user_update(request: HttpRequest, user_id: int) -> HttpResponse:
    user = db.get_user_by_id(user_id)
    if not user:
        return redirect("dashboard")

    if request.method == "GET":
        return render(request, "Users/user_update.html", {"user": user})

    new_password = request.POST.get("password")
    new_role = request.POST.get("role")
    payload: Dict[str, str] = {"id": user_id}
    if new_password is not None and new_password != "":
        payload["password"] = new_password
    if new_role:
        payload["role"] = new_role
    try:
        db.update_user(payload)
        return redirect("dashboard")
    except ValueError as exc:
        return render(request, "Users/user_update.html", {"user": user, "error": str(exc)})


@require_admin
@require_http_methods(["POST"])
def user_delete(request: HttpRequest, user_id: int) -> HttpResponse:
    try:
        db.remove_user(user_id)
    except ValueError:
        pass
    return redirect("dashboard")


@require_admin
@require_http_methods(["GET", "POST"])
def send_notification(request: HttpRequest, user_id: int) -> HttpResponse:
    if request.method == "GET":
        user = db.get_user_by_id(user_id)
        return render(request, "Users/send_notification.html", {"user": user})

    message = request.POST.get("notification_message", "").strip()

    if not message:
        user = db.get_user_by_id(user_id)
        return render(request, "Users/send_notification.html", {
            "user": user,
            "error": "Message is required" 
        })

    try:
        db.add_notification(user_id, message)
        return redirect("dashboard")
    except ValueError as exc:
        user = db.get_user_by_id(user_id)
        return render(request, "Users/send_notification.html", {
            "user": user,
            "error": str(exc)
        })

@require_auth
@require_http_methods(["POST"])
def clear_notifications(request: HttpRequest, user_id: int) -> HttpResponse:
    current_username = request.session.get("username")
    current_user = db.get_user_by_username(current_username)

    if not current_user or current_user["id"] != user_id:
        return redirect("dashboard")

    try:
        db.clear_user_notifications(user_id)
        return redirect("dashboard")
    except ValueError:
        return redirect("dashboard")