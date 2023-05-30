from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ListingForm, WishlistForm, BidForm, StatutForm, CommentForm

from .models import User, Listing, Wishlist, Bid, Comments, Category


# _________________________________________________________________________PAGE D'ACCUEIL


def index(request):  # Affiche la page d'accueil avec la liste des annonces
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()  # Envoie les annonces au template
    })


# _________________________________________________________________________PAGE DE CREATION D'UNE ANNONCE


@login_required(login_url='/login')
def create_listing(request):  # Affiche la page de création d'une annonce

    if request.method == "POST":  # Si le formulaire est envoyé
        form = ListingForm(request.POST)  # Crée un objet ListingForm avec les données du formulaire
        if form.is_valid():  # Si le formulaire est valide
            listing = form.save(commit=False)  # Crée un objet Listing mais ne l'enregistre pas encore dans la base de données
            listing.user = request.user  # Définit l'utilisateur de l'objet Listing comme l'utilisateur actuel
            listing.save()  # Enregistre l'objet Listing dans la base de données

        return redirect(index)  # Redirige vers la page d'accueil (index)

    else:
        form = ListingForm()  # Crée un objet ListingForm vide

    return render(request, "auctions/create_listing.html",
                  {  # Affiche la page de création d'une annonce avec le formulaire
                      "form": form  # Envoie le formulaire au template create_listing.html
                  })


# _________________________________________________________________________PAGE DE PRODUIT (ANNONCE)

@login_required(login_url='/login')
def listing(request, listing_id):  # Affiche la page de l'annonce
    listing = get_object_or_404(Listing, pk=listing_id)  # Récupère l'annonce à partir de son id
    form = WishlistForm(request.POST)  # Création du formulaire pour ajouter l'annonce à la wishlist de l'utilisateur connecté
    bidForm = BidForm(request.POST)  # Création du formulaire pour ajouter une enchère à l'annonce
    bid = Bid.objects.filter(listing=listing_id).last()
    statutForm = StatutForm(request.POST)
    commentForm = CommentForm(request.POST)
    comments = Comments.objects.filter(listing=listing_id)

    if "wishlist" in request.POST :
        if form.is_valid():  # Si le formulaire est envoyé et valide
            wishlist = form.save(commit=False) # Création d'un objet wishlist mais ne l'enregistre pas encore dans la base de données
            wishlist.user = request.user  
            wishlist.listing = listing
            wishlist.save()  # Enregistrement de l'objet wishlist dans la base de données (ajout de l'annonce à la wishlist de l'utilisateur connecté)
            return redirect('listing', listing_id=listing_id)

    if "bid" in request.POST :
        if bidForm.is_valid():
            bid = bidForm.save(commit=False)
            bid.user = request.user
            bid.listing = listing
            bid.save()
            return redirect('listing', listing_id=listing_id)


    if "change_status" in request.POST:
        if statutForm.is_valid():
            listing.statut = False
            listing.save()
            bid.win = True
            bid.save()
            return redirect('listing', listing_id=listing_id)

    if 'comment' in request.POST:
        if commentForm.is_valid():
            comment = Comments()
            comment.user = request.user
            comment.listing = listing
            comment.comment = request.POST['comment']
            comment.save()
            return redirect('listing', listing_id=listing_id) # Redirige vers la page de l'annonce pour afficher la liste des commentaires

    return render(request, "auctions/listing.html", {
        # Affichage de la page de l'annonce avec les données de l'annonce et du formulaire pour ajouter l'annonce à la wishlist
        "listing": listing,  # Envoie les données de l'annonce au template listing.html
        "bid": bid, # Envoie les données de l'enchère au template listing.html
        "form": form,  # Envoie le formulaire au template listing.html pour l'afficher
        "bidForm": bidForm,  # Envoie le formulaire au template listing.html pour l'afficher
        "statutForm": statutForm, # Envoie le formulaire au template listing.html pour l'afficher
        "commentForm": commentForm, # Envoie le formulaire au template listing.html pour l'afficher
        "message": "Wishlist already exists.",
        "comments": comments
    })

# _________________________________________________________________________PAGE DE CATEGORIES


@login_required(login_url='/login')
def categories(request):  # Affiche la page des catégories
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()  # Envoie les catégories au template
    })


# _________________________________________________________________________PAGE DE CATEGORIE

login_required(login_url='/login')
def category(request, category_id):  # Affiche la page de la catégorie
    category = get_object_or_404(Category, pk=category_id)  # Récupère la catégorie à partir de son id
    return render(request, "auctions/category.html", {
        # Affichage de la page de la catégorie avec les données de la catégorie
        "category": category,  # Envoie les données de la catégorie au template category.html
        "listings": Listing.objects.filter(category=category_id)  # Envoie les annonces de la catégorie au template category.html
    })




# _________________________________________________________________________PAGE DE WISHLIST


@login_required(login_url='/login')
def listing_register(request):  # Affiche la page de la wishlist de l'utilisateur connecté

    return render(request, "auctions/listing_register.html",
                  {  # Affichage de la page de la wishlist de l'utilisateur connecté avec les données de la wishlist
                      "wishlist": Wishlist.objects.filter(user=request.user)
                      # Envoie les données de la wishlist au template listing_register.html (wishlist de l'utilisateur connecté)
                  })


# _________________________________________________________________________PAGE DE SUPPRESSION D'UNE ANNONCE DE LA WISHLIST

@login_required(login_url='/login')
def delete_wishlist(request, pk):  # Supprime l'annonce de la wishlist de l'utilisateur connecté (pk = id de l'annonce)
    wishlist = get_object_or_404(Wishlist, pk=pk)  # Récupère l'annonce à partir de son id (pk)
    wishlist.delete()  # Supprime l'annonce de la wishlist de l'utilisateur connecté (supprime l'objet wishlist de la base de données)
    return redirect(
        'listing_register')  # Redirige vers la page listing_register (wishlist) pour afficher la wishlist sans l'annonce supprimée


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
    
    

# Page des annonces actives : l'itinéraire par défaut de votre application Web doit permettre aux utilisateurs d'afficher toutes les annonces d'enchères
# actuellement actives. OK

# Pour chaque annonce active, cette page doit afficher (au minimum) le titre, la description, le prix actuel et la photo (s'il en existe une pour l'annonce).
# OK

# Page de la liste : cliquer sur une liste devrait amener les utilisateurs à une page spécifique à cette liste. Sur cette page, les utilisateurs doivent
# pouvoir afficher tous les détails de l'annonce, y compris le prix actuel de l'annonce. OK

# Si l'utilisateur est connecté, l'utilisateur doit pouvoir ajouter l'élément à sa "liste de surveillance". Si l'élément est déjà sur la liste de
# surveillance, l'utilisateur devrait pouvoir le supprimer. OK

# Si l'utilisateur est connecté, il devrait pouvoir enchérir sur l'objet. L'enchère doit être au moins aussi importante que l'enchère de départ et doit être
# supérieure à toutes les autres enchères qui ont été placées (le cas échéant). OK
#
# Si l'enchère ne répond pas à ces critères, l'utilisateur doit recevoir une erreur. OK

# Si l'utilisateur est connecté et est celui qui a créé l'annonce, l'utilisateur doit avoir la possibilité de "clôturer" l'enchère à partir de
# cette page, ce qui fait du meilleur enchérisseur le gagnant de l'enchère et rend l'annonce inactive. OK

# Si un utilisateur est connecté sur une page de liste fermée et que l'utilisateur a remporté cette enchère, la page doit le dire. OK

# Les utilisateurs connectés doivent pouvoir ajouter des commentaires à la page de la liste. La page de liste doit afficher tous les commentaires qui
# ont été faits sur la liste. OK

# Liste de surveillance : les utilisateurs connectés doivent pouvoir visiter une page de liste de surveillance, qui doit afficher toutes les annonces qu'un utilisateur a
# ajoutées à sa liste de surveillance. En cliquant sur l'une de ces listes, l'utilisateur devrait être redirigé vers la page de cette liste. OK

# Catégories : les utilisateurs doivent pouvoir visiter une page qui affiche une liste de toutes les catégories d'annonces. Cliquer sur le nom de n'importe quelle catégorie
# devrait amener l'utilisateur à une page qui affiche toutes les listes actives dans cette catégorie.   OK

# Interface d'administration de Django : via l'interface d'administration de Django, un administrateur de site doit pouvoir afficher, ajouter, modifier et supprimer toutes
# les annonces, commentaires et enchères effectués sur le site. OK
