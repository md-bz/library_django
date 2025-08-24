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
from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/",views.dashboard,name="dashboard"),
    path("login/",views.login,name="login"),
    path("signup/",views.signup,name="signup"),
    path("user_update/<int:user_id>",views.user_update,name="user_update"),
    path("user_delete/<int:user_id>",views.user_delete,name="user_delete"),
    path("update_me",views.update_me,name="update_me"),
    path("send_notification/<int:user_id>",views.send_notification,name="send_notification"),
    path("clear_notifications/<int:user_id>",views.clear_notifications,name="clear_notifications"),
]
