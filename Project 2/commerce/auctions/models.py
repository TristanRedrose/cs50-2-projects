from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class User(AbstractUser):
    pass

class Categories(models.Model):
    cat = models.CharField(max_length=32, unique=True, blank=False, default=None)

    class Meta:
        verbose_name= "Category"
        verbose_name_plural= "Categories"

    def __str__(self):
        return f"{self.cat}"

class Listings(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=100, blank=False, default=None)
    description = models.CharField(max_length=300, blank=False, default=None)
    ctg = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name= "category")
    picture = models.URLField(blank=True)
    bid = models.IntegerField(validators=[MinValueValidator(0)])
    time = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name= "Listing"
        verbose_name_plural= "Listings"

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer", editable=False)
    subject = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="subject", editable=False)
    comment = models.CharField(max_length=500, editable=False)

    def __str__(self):
        return f"Writer: {self.writer} // Subject: {self.subject.title} // Comment: {self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE, related_name="watcher")
    lists = models.ManyToManyField(Listings, related_name="watched")

    def __str__(self):
        return f"{self.user}'s watchlist"

class Bidding(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    bid = models.IntegerField(validators=[MinValueValidator(0)])
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name= "bids")

    def __str__(self):
        return f"{self.bidder}'s bid on {self.listing.title}"