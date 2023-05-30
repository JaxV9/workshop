from django.contrib import admin

from .models import User, Category, State, Product, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(State)
admin.site.register(Product)
admin.site.register(Comment)