from django import forms
from .models import Listing, Category, Wishlist, Bid

#_____________________________________LISTING FORM

class ListingForm(forms.ModelForm):
    title = forms.CharField(
        max_length=64,
        required=True,
        label='Titre',
        widget=forms.TextInput(attrs={'class': 'title_listing_form'})
    )

    description = forms.CharField(
        required=True,
        label='Description',
        widget=forms.Textarea(attrs={'class': 'description_listing_form'})
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label='Prix',
        widget=forms.NumberInput(attrs={'class': 'price_listing_form'})
    )

    image = forms.URLField(
        required=True,
        label='Image',
        widget=forms.URLInput(attrs={'class': 'image_listing_form'})
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=True, 
        label='Catégorie'
    )

    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "price",
            "image",
            "category"
        ]

#_____________________________________WISHLIST FORM

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = [
        ]

#_____________________________________BID FORM

class BidForm(forms.ModelForm):
    bid = forms.DecimalField(
        max_digits=10,
        label='Prix',
        widget=forms.NumberInput(attrs={'id': 'my_bid', 'name': 'bid', 'value': 'bid',})
    )

    class Meta:
        model = Bid
        fields = [
            "bid"
        ]

#_____________________________________Statut FORM

class StatutForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
        ]

#_____________________________________Comment FORM

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,
        label='',
        widget=forms.Textarea(attrs={'class': 'comment_form', 'name': 'comment', 'value': 'comment',})
    )

    class Meta:
        model = Listing
        fields = [
        ]