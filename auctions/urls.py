from django.urls import path
from django.contrib.auth import views as auth_views

path('/login/', auth_views.LoginView.as_view()),
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
<<<<<<< HEAD
    path("create_product", views.create_product, name="create_product")
=======
    path("create_product", views.create_product, name="create_product"),
    path("products", views.products, name="products"),
>>>>>>> cbb0497711fef9a6eac348058d36420169ed6969
]
