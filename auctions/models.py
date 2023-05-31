from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    image = models.URLField(max_length=1000, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
    
class State(models.Model):
    state = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.state}"


class Product(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    image = models.URLField(max_length=200, blank=True)
    exchange = models.BooleanField(null=True, default=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    localisation = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.user}"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments",  null=True)

    def __str__(self):
        return f"{self.content} {self.user} {self.product}"

class Exchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchanges")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="exchanges")
    exchange = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="exchanges2")
    confirmation = models.BooleanField(null=True, default=False)
    delete = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f"{self.user} {self.product} {self.exchange}"
    
class Gift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gifts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gifts")
    confirmation = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f"{self.user} {self.product}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="watchlists")

    def __str__(self):
        return f"{self.user} {self.product}"