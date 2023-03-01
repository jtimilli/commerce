from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import User, AuctionListing, Comment, Watchlist, Bid
from .forms import CommentForm


def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})


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


@login_required
def create_listing(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('starting_bid')
        image_url = request.POST.get('image') 
        category = request.POST.get('category')
        user = request.user

        # create a new instance of AuctionListing model
        listing = AuctionListing(title=title, description=description, starting_bid=starting_bid, image=image_url, category=category, user=user)

        # save the new listing to the database
        listing.save()

        # redirect the user to the homepage or the newly created listing
        return redirect('index')

    return render(request, 'auctions/create_listing.html')



def view_listing(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)

    if request.user.is_authenticated:
        watchlist, _ = Watchlist.objects.get_or_create(user=request.user)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.listing = listing
                comment.user = request.user
                comment.save()
                return redirect('listing', listing_id=listing_id)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
        watchlist = None
    
    try:
        bid = get_object_or_404(Bid, listing=listing)
        winner = bid.user
    except:
        winner = request.user

    return render(request, "auctions/listing.html", {"listing": listing, "form": comment_form, "watchlist": watchlist, "winner": winner })


@login_required
def add_watchlist(request, listing_id):
    item = get_object_or_404(AuctionListing, pk=listing_id)
    watchlist, _ = Watchlist.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if request.POST.get("add-watchlist"):
            if not watchlist.listings.filter(pk=listing_id).exists():
                watchlist.listings.add(item)
                watchlist.save()
        elif request.POST.get("remove-watchlist"):
            watchlist.listings.remove(item)
            watchlist.save()

    return redirect('listing', listing_id=listing_id)


@login_required
def go_watchlist(request):
    watchlist = get_object_or_404(Watchlist, user=request.user)
    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist})



@login_required
def update_bid(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    current_bid = listing.current_bid

    if request.method == "POST":
        if request.POST.get("new_bid") == '':
            return redirect('listing', listing_id=listing.id)
        
        new_bid = float(request.POST.get("new_bid"))
        user = request.user

        # check if there is an existing bid object for the current listing
        try:
            bid = Bid.objects.get(listing=listing)
        except Bid.DoesNotExist:
            bid = None

        if current_bid == 0 or (bid is None):
            # create a new bid object if there is no existing bid object
            bid = Bid.objects.create(listing=listing, user=user, bid_amount=new_bid)
            listing.current_bid = new_bid
        elif new_bid > current_bid:
            # update the existing bid object if the new bid is higher
            bid.bid_amount = new_bid
            bid.user = user
            listing.current_bid = new_bid

        # save the bid and listing objects
        bid.save()
        listing.save()

        return redirect('listing', listing_id=listing.id)


    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_bid": current_bid
    })


@login_required
def close_bid(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(AuctionListing, id=listing_id)
        listing.active = False
        listing.save()
        return redirect('listing', listing_id=listing.id)
    
def categories(request):
    if request.method == "POST":
        category = request.POST.get("category")
        try:
            listings = AuctionListing.objects.filter(category=category)
        except:
            listings = None
        
        return render(request, "auctions/categories.html", {"listings": listings})
    
    else:
        listings = None
        return render(request, "auctions/categories.html", {"listings": listings})
        




