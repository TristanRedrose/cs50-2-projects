from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions  import ValidationError

from .models import User, Categories, Listings, Comment, Watchlist, Bidding

def get_listings():

    # Get highest bid for every listing
    listings_qset = Listings.objects.all()
    for listing in listings_qset:
        highest_bids = listing.bids.all().order_by("-bid")
        if highest_bids.exists():
            listing.highest_bid = highest_bids[0].bid
        else:
            listing.highest_bid = None
    return listings_qset

def index(request):

    activelists = []

    listings = get_listings()
    for listing in listings:
        if listing.active == True:
            activelists.append(listing)

    return render(request, "auctions/index.html", {
        "listings": activelists
    })

def closed_view(request):

    closedlists = []

    listings = get_listings()
    for listing in listings:
        if listing.active == False:
            closedlists.append(listing)

    return render(request, "auctions/closed_view.html", {
        "listings": closedlists
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

        # Return error message if user left title field empty
        title = title.strip()
        if title == "":
            return render(request, "auctions/newlist.html", {
                "message": "Title is required.",
                "categories": Categories.objects.all()
            })
        description = request.POST["description"]

        # Return error message if user left description field empty
        description = description.strip()
        if description == "":
            return render(request, "auctions/newlist.html", {
                "message": "Description is required.",
                "categories": Categories.objects.all()
            })
        catg = Categories.objects.get(pk=int(request.POST["category"]))
        picture = request.POST["picture"]
        bid = request.POST["bid"]

        # Create a new listing and return to index page
        new = Listings(creator=owner, title=title, description=description, ctg=catg, picture=picture, bid=bid)
        new.save()
        return HttpResponseRedirect(reverse("index"))
    else:

        # Show newlist form page
        return render(request, "auctions/newlist.html", {
            "categories": Categories.objects.all()
        })
    
def list_view(request, listid):

    check = False
    listing = Listings.objects.get(pk=int(listid))

    # Check if the listing is currently on the users watchlist
    if request.user.is_authenticated:
        name = User.objects.get(username=request.user.username)
        watchlists = Watchlist.objects.all()
        for watchlist in watchlists:
            if watchlist.user == name:
                for watch in watchlist.lists.all():
                    if watch.title == listing.title:
                        check = True
    
    # Check if bids on the listing exist and choose the highest bid
    x = 0
    bids = Bidding.objects.filter(listing=listing)
    for bidding in bids:
        if x < bidding.bid:
            x = bidding.bid
    try:
        bid = Bidding.objects.get(bid=x,listing=listing)
        bid_check = bid.bid + 1
    except Bidding.DoesNotExist:
        bid = None
        bid_check = None

    # Add comment to listing page
    if request.method == "POST":
        writer = User.objects.get(pk=request.POST["name"])
        subject = Listings.objects.get(pk=listid)
        comment = request.POST["comment"]
        
        # Save the comment and reload the page
        new = Comment(writer=writer, subject=subject, comment=comment)
        new.save()
        return render(request, "auctions/listing.html", {
            "listing": Listings.objects.get(pk=int(listid)),
            "comments": Comment.objects.all(),
            "bid": bid,
            "bid_check": bid_check,
            "check": check
        })
    else:
        
        # Show listing page
        return render(request, "auctions/listing.html", {
            "listing": Listings.objects.get(pk=int(listid)),
            "comments": Comment.objects.all(),
            "bid_check": bid_check,
            "bid": bid,
            "check": check
        })

def category_view(request):

    # Render a page where the user picks a category
    return render(request, "auctions/category.html", {
         "categories": Categories.objects.all()
    })

def category_listview(request, catid):

    # Show all listings that fit the selected category
    cat = Categories.objects.get(pk=catid)
    category = cat.cat
    
    categorylists = []

    listings = get_listings()
    for listing in listings:
        if listing.ctg == cat and listing.active == True:
            categorylists.append(listing)
    
    return render(request, "auctions/categoryview.html", {
         "listings": categorylists
    })

def close_list(request, listid):
    if request.method == "POST":

        # If confirmed set active status to false
        c_list = Listings.objects.get(pk=int(listid))
        value = request.POST["closer"]
        c_list.active = value
        c_list.save()
        return HttpResponseRedirect(reverse("index"))
    else:

        # Ask for confirmation
        return render(request, "auctions/close.html", {
            "listing": Listings.objects.get(pk=int(listid))
        })

def watch(request):

    if request.method == "POST":

        # See if user already has a watchlist to add to, if not create new and add item
        watcher = User.objects.get(pk=request.POST["name"])
        try:
            new = Watchlist.objects.get(user=watcher)
        except Watchlist.DoesNotExist:
            new = Watchlist(user=watcher)
            new.save()
        subject = Listings.objects.get(pk=request.POST["list-name"])
        new.lists.add(subject)

        # Show items in watchlist
        return render(request, "auctions/watchlist.html", {
            "watchlists": Watchlist.objects.get(user=watcher),
            "listings": get_listings(),
            "check": True
        })
    else:

        # Check if user has any items on his watchlist
        check = True
        name = User.objects.get(username=request.user.username)
        try: 
            new = Watchlist.objects.get(user=name)
        except Watchlist.DoesNotExist:
            new = None
            check = False
        
        # Show users watchlist
        return render(request, "auctions/watchlist.html", {
            "watchlists": new,
            "listings": get_listings(),
            "check": check
        })
    
def watchdel(request):

    if request.method == "POST":

        # Find and remove item from users watchlist
        watchlists = Watchlist.objects.all()
        name = User.objects.get(pk=request.POST["name"])
        subject = Listings.objects.get(pk=request.POST["list-name"])
        old = Watchlist.objects.get(user=name)
        old.lists.remove(subject)

        # Check if the user has no items in watchlist and if so, remove user from watchlist
        i = 0
        for watchlist in watchlists:
            if watchlist.user == name:
                for watch in watchlist.lists.all():
                        i = i + 1
        if i == 0:
            old.delete()
            old = None
            # Return empty watchlist
            return render(request, "auctions/watchlist.html", {  
                "watchlists": old,
                "listings": get_listings(),
                "check": False
            })
        # Show remaining items in watchlist
        return render(request, "auctions/watchlist.html", {  
            "watchlists": Watchlist.objects.get(user=name),
            "listings": get_listings(),
            "check": True
    })

def addbid(request):
    name = User.objects.get(pk=request.POST["name"])
    item = Listings.objects.get(pk=request.POST["item"])
    bid = request.POST["bid"]

    # Check is the bid greater than previous bids, or if no bids exist, equal or greater to the starting price
    bids = Bidding.objects.filter (listing=item)
    if int(bid) < int(item.bid):
        raise ValidationError("Bid must be greater or equal than the starting price")
    for x in bids:
        if int(bid) <= int(x.bid):
            raise ValidationError("Bid must be greater than the previous bid")
    
    # Create new bid if the user currently hasn't bid on the item, or update existing bid
    old = Bidding.objects.filter(listing=item, bidder=name)
    if not old:
        new = Bidding(bidder=name, bid=bid, listing=item)
        new.save()
    else: 
        old.update(bid=bid)

    # Reload page 
    return redirect(f"listing/{item.id}")
