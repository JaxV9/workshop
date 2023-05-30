from django.contrib import admin

from .models import User, Listing, Bid, Comments, Category, Wishlist

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price", "image", "category", "user", "date")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid", "user", "listing")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "user", "listing")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_id", "user_id")

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Wishlist, WishlistAdmin)


