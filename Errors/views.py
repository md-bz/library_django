from django.shortcuts import render

def not_found(request):
    return render(request, "Errors/404.html")

def unauthorized(request):
    return render(request, "Errors/403.html")
