from django import forms
from django.core.exceptions import ValidationError
from .models import User, Category, State, Product, Comment, Exchange, Gift


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
            "localisation"
        ]

#_________________________Search form

class SearchForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    product = forms.CharField(max_length=64, required=False)
    localisation = forms.CharField(max_length=64, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'category_field', 'placeholder': ''})
        self.fields['category'].label = ""
        self.fields['product'].widget.attrs.update({'class': 'product_field', 'placeholder': 'Que recherchez-vous ?'})
        self.fields['product'].label = ""
        self.fields['localisation'].widget.attrs.update({'class': 'localisation_field', 'placeholder': 'Saisissez une ville, une région'})
        self.fields['localisation'].label = ""

    def clean(self):
        cleaned_data = super().clean()
        if not any(cleaned_data.values()):
            raise ValidationError("Au moins un champ doit être rempli.")
        


#_________________________Exchange form

class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ['exchange']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  
        super(ExchangeForm, self).__init__(*args, **kwargs)
        if self.request is not None:
            self.fields['exchange'].queryset = Product.objects.filter(user=self.request.user)