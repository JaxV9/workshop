from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from .models import User, Category, State, Product, Comment, Exchange, Gift
from .forms import ProductForm, SearchForm
from django.contrib import messages



# _________________________________________________________________________PAGE D'ACCUEIL


def index(request):  # Affiche la page d'accueil avec la liste des annonces
    
    search_form = SearchForm(request.GET or None) # Crée un formulaire de recherche
    
    return render(request, "auctions/index.html", {
        "products": Product.objects.all(),
        "form": search_form
    })


#________________________________________________________________________Page profil

def profil(request):

    return render(request, "auctions/profil.html")


#_________________________________________________________________________create_product

@login_required(login_url='/login')
def create_product(request):

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect(index)
        else:
            return render(request, "auctions/create_product.html", {
                "form": form
            })
    
    else:
        form = ProductForm()

    return render(request, "auctions/create_product.html",{
        "form": form
    })


#_________________________________________________________________________product result


def products(request):
    search = SearchForm(request.GET)
    products = []

    no_result = ""

    if search.is_valid():
        products = Product.objects.all()
        if search.cleaned_data["category"]:
            products = products.filter(category=search.cleaned_data["category"])
        if search.cleaned_data["product"]:
            products = products.filter(title__icontains=search.cleaned_data["product"])
        if search.cleaned_data["localisation"]:
            products = products.filter(localisation__icontains=search.cleaned_data["localisation"])


    if not products:
        no_result = "Aucun résultat"


    return render(request, "auctions/products.html", {
        "products": products,
        "search": search,
        "no_result": no_result
    })



#_________________________________________________________________________product details

@login_required
def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    products_user = Product.objects.filter(user=request.user, exchange=True)
    exchanges_products = Exchange.objects.filter(product=product)

    confirmationMessageUser = ""

    if request.method == 'POST':
        if 'products_user' in request.POST:
            selected_product_id = request.POST.get('products_user')
            selected_product = get_object_or_404(Product, pk=selected_product_id)

            exchange = Exchange()
            exchange.user = request.user
            exchange.product = product
            exchange.exchange = selected_product
            exchange.save()
        
            confirmationMessageUser = "Vous avez confirmé l'échange. Vous pouvez maintenant attendre la réponse de l'auteur de l'offre."

        elif 'confirmation' in request.POST: #formulaire pour confirmer l'échange

            exchange_id = request.POST.get('confirmation')
            exchange = get_object_or_404(Exchange, pk=exchange_id)
            exchange.confirmation = True
            exchange.save()
        
        elif 'refuse' in request.POST: #formulaire pour refuser l'échange

            exchange_id = request.POST.get('refuse')
            exchange = get_object_or_404(Exchange, pk=exchange_id)
            exchange.delete = True
            exchange.save()

        return render(request, "auctions/product_details.html", {
            "product": product,
            "products_user": products_user,
            "exchanges_products": exchanges_products,
            "confirmationMessageUser": confirmationMessageUser})

    else:
        return render(request, "auctions/product_details.html", {
            "product": product,
            "products_user": products_user,
            "exchanges_products": exchanges_products,
            "confirmationMessageUser": confirmationMessageUser
        })








# _________________________________________________________________________PAGE DE CONNEXION


def login_view(request):  # Affiche la page de connexion
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]  # Récupère le nom d'utilisateur saisi dans le formulaire
        password = request.POST["password"]  # Récupère le mot de passe saisi dans le formulaire
        user = authenticate(request, username=username,
                            password=password)  # Vérifie si l'utilisateur existe dans la base de données et si le mot de passe est correct (fonction authenticate de Django)

        # Check if authentication successful
        if user is not None:  # Si l'utilisateur existe et que le mot de passe est correct
            login(request, user)  # Connecte l'utilisateur (fonction login de Django)
            return HttpResponseRedirect(reverse("index"))  # Redirige vers la page d'accueil (index)
        else:
            return render(request, "auctions/login.html",
                          {  # Si l'utilisateur n'existe pas ou que le mot de passe est incorrect
                              "message": "Invalid username and/or password."  # Affiche un message d'erreur
                          })
    else:
        return render(request, "auctions/login.html")  # Affiche la page de connexion


# _________________________________________________________________________PAGE DE DECONNEXION

def logout_view(request):  # Déconnecte l'utilisateur
    logout(request)  # Fonction logout de Django
    return HttpResponseRedirect(reverse("index"))  # Redirige vers la page d'accueil (index)


# _________________________________________________________________________PAGE DE CREATION D'UN COMPTE UTILISATEUR

def register(request):
    if request.method == "POST":  # Si le formulaire est envoyé
        username = request.POST["username"]  # Récupère le nom d'utilisateur saisi dans le formulaire
        email = request.POST["email"]  # Récupère l'email saisi dans le formulaire

        # Ensure password matches confirmation
        password = request.POST["password"]  # Récupère le mot de passe saisi dans le formulaire
        confirmation = request.POST["confirmation"]  # Récupère la confirmation du mot de passe saisi dans le formulaire
        if password != confirmation:  # Si le mot de passe et la confirmation du mot de passe ne sont pas identiques
            return render(request, "auctions/register.html", {  # Affiche un message d'erreur
                "message": "Passwords must match."  # Affiche un message d'erreur
            })

        # Attempt to create new user
        try:  # Crée un nouvel utilisateur
            user = User.objects.create_user(username, email,
                                            password)  # Crée un nouvel utilisateur (fonction create_user de Django)
            user.save()  # Enregistre l'utilisateur dans la base de données
        except IntegrityError:  # Si le nom d'utilisateur existe déjà dans la base de données
            return render(request, "auctions/register.html", {  # Affiche un message d'erreur
                "message": "Username already taken."  # Affiche un message d'erreur
            })
        login(request, user)  # Connecte l'utilisateur (fonction login de Django)
        return HttpResponseRedirect(reverse("index"))  # Redirige vers la page d'accueil (index)
    else:
        return render(request, "auctions/register.html")  # Affiche la page d'inscription
    
    

