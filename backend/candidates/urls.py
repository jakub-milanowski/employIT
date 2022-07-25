from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginUser, name="login"),
    path('csrf', views.getCsrfToken, name="get CSRF Token"),
    path('register', views.registerUser, name="register")
]