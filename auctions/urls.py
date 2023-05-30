from django.urls import path
from django.contrib.auth import views as auth_views

path('/login/', auth_views.LoginView.as_view()),
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_product", views.create_product, name="create_product")
]
