from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Categories, Listings, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def newlist(request):
    if request.method == "POST":
        owner = User.objects.get(pk=int(request.POST["owner"]))
        title = request.POST["title"]
        if title == "":
            return render(request, "auctions/newlist.html", {
                "message": "Title is required.",
                "categories": Categories.objects.all()
            })
        description = request.POST["description"]
        if description == "":
            return render(request, "auctions/newlist.html", {
                "message": "Description is required.",
                "categories": Categories.objects.all()
            })
        catg = Categories.objects.get(pk=int(request.POST["category"]))
        picture = request.POST["picture"]
        bid = request.POST["bid"]
        new = Listings(creator=owner, title=title, description=description, ctg=catg, picture=picture, bid=bid)
        new.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/newlist.html", {
            "categories": Categories.objects.all()
        })
    
def list_view(request, listid):
    check = False
    if request.user.is_authenticated:
        name= User.objects.get(username=request.user.username)
        watchlists = Watchlist.objects.all()
        listing = Listings.objects.get(pk=int(listid))
        for watchlist in watchlists:
            if watchlist.user == name:
                for watch in watchlist.lists.all():
                    if watch.title == listing.title:
                        check = True
    if request.method == "POST":
        writer = User.objects.get(pk=request.POST["name"])
        subject = Listings.objects.get(pk=listid)
        comment = request.POST["comment"]
        if comment == "":
            return render(request, "auctions/listing.html", {
            "listing": Listings.objects.get(pk=int(listid)),
            "comments": Comment.objects.all(),
            "check": check
            })
        new = Comment(writer=writer, subject=subject, comment=comment)
        new.save()
        return render(request, "auctions/listing.html", {
            "listing": Listings.objects.get(pk=int(listid)),
            "comments": Comment.objects.all(),
            "check": check
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": Listings.objects.get(pk=int(listid)),
            "comments": Comment.objects.all(),
            "check": check
        })

def category_view(request):
    return render(request, "auctions/category.html", {
         "categories": Categories.objects.all()
    })

def category_listview(request, catid):
    return render(request, "auctions/categoryview.html", {
         "ctg": Categories.objects.get(pk=catid),
         "listings": Listings.objects.all()
    })

def close_list(request, listid):
    if request.method == "POST":
        c_list = Listings.objects.get(pk=int(listid))
        value = request.POST["closer"]
        c_list.active = value
        c_list.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/close.html", {
            "listing": Listings.objects.get(pk=int(listid))
        })

def watch(request):
    check = True
    name = User.objects.get(username=request.user.username)
    try: 
        Watchlist.objects.get(user=name)
    except Watchlist.DoesNotExist:
        check = False
    if request.method == "POST":
        watcher = User.objects.get(pk=request.POST["name"])
        try:
            new = Watchlist.objects.get(user=watcher)
        except Watchlist.DoesNotExist:
            new = Watchlist(user=watcher)
            new.save()
        subject = Listings.objects.get(pk=request.POST["list-name"])
        new.lists.add(subject)
        return render(request, "auctions/watchlist.html", {
            "watchlists": Watchlist.objects.all(),  
            "check": True
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "watchlists": Watchlist.objects.all(),
            "check": check
        })
    





        



