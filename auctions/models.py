from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class AuctionListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    current_bid = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)
    image = models.ImageField(upload_to='media', blank=True)
    category = models.CharField(max_length=255)
    date_listed = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    
    def __str__(self):
        return f"title: {self.title} description: {self.description}"


class Watchlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listings = models.ManyToManyField(AuctionListing, through='WatchlistItem')

    def __str__(self):
        return f"{self.user.username}'s watchlist ({self.listings} items)"


class WatchlistItem(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['listing', 'watchlist']


class User(AbstractUser):
    pass



class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented on {self.listing}"
    

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_bid = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} bid {self.bid_amount} on {self.listing}"
