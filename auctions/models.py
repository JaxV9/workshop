from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField(auto_now_add=True)
    statut = models.BooleanField(null=True, default=True)

    def __str__(self):
        return f"{self.title} {self.user}"



class Wishlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="wishlist",related_query_name="wishlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist", default=None)
    
    def __str__(self):
        return f"{self.listing}"

class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    win = models.BooleanField(null=True, default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bid} {self.user} {self.listing}"


class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.comment} {self.user} {self.listing}"