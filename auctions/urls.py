from django.urls import path
from django.contrib.auth import views as auth_views

path('/login/', auth_views.LoginView.as_view()),
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing_register/", views.listing_register, name="listing_register"),
    path('delete_wishlist/<int:pk>', views.delete_wishlist, name='delete_wishlist'),
    path('categories', views.categories, name='categories'),
    path('category/<int:category_id>', views.category, name='category'),
]
