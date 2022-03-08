from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_views

from ProgettoArduAlessio import settings
from user_management import views

app_name = "user_management"

urlpatterns = [
    path("home/<int:pk>", views.user_detail, name="home"),

    path("register", views.UserCreateView.as_view(), name="register"),
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),

    path('check_username_unique', views.check_username_is_unique, name='check-username-unique'),
    path('check_email_unique', views.check_email_is_unique, name='check-email-unique'),
]