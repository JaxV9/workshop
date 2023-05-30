from django import forms
from .models import User, Category, State, Product, Comment


#_________________________Create product form

class ProductForm(forms.ModelForm):
    title = forms.CharField(
        max_length=64,
        required=True,
        label='Titre',
        widget=forms.TextInput(attrs={'class': 'title_product_form'})
    )

    description = forms.CharField(
        required=True,
        label='Description',
        widget=forms.Textarea(attrs={'class': 'description_product_form'})
    )

    image = forms.URLField(
        required=True,
        label='Image',
        widget=forms.URLInput(attrs={'class': 'image_product_form'})
    )

    exchange = forms.BooleanField(
        required=False,
        label='Echange',
        widget=forms.CheckboxInput(attrs={'class': 'exchange_product_form'})
    )

    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        required=True,
        label='Etat'
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label='Catégorie'
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label='Prix',
        widget=forms.NumberInput(attrs={'class': 'price_product_form'})
    )

    localisation = forms.CharField(
        max_length=64,
        required=True,
        label='Localisation',
        widget=forms.TextInput(attrs={'class': 'localisation_product_form'})
    )

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "image",
            "exchange",
            "state",
            "category",
            "price",
            "localisation"
        ]

#_________________________Search form

class SearchForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    product = forms.CharField(max_length=64, required=False)
    localisation = forms.CharField(max_length=64, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'category_field'})
        self.fields['product'].widget.attrs.update({'class': 'product_field'})
        self.fields['localisation'].widget.attrs.update({'class': 'localisation_field'})
