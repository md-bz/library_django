from functools import wraps
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from typing import Callable


def require_auth(view_func: Callable) -> Callable:
    """Decorator to require user authentication via session username."""
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        username = request.session.get("username")
        if not username:
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


def require_admin(view_func: Callable) -> Callable:
    """Decorator to require admin role via session."""
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        username = request.session.get("username")
        role = request.session.get("role")
        
        if not username:
            return redirect("login")
        if role != "admin":
            return redirect("unauthorized")
        return view_func(request, *args, **kwargs)
    return wrapper
