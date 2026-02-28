from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.conf import settings

# Create your models here.
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField()
    image_url = models.URLField(blank=True)
    starting_bid = models.CharField()

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings"
    )

    def __str__(self):
        return f"{self.id}-{self.title} : {self.description} | Sold by {self.seller.username}, with a starting bid of {self.starting_bid}"

class Bid(models.Model):
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="bids"
    )

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids"
    )

    amount = models.FloatField()
    
    def __str__(self):
        return f"{self.id}-{self.bidder.username} has a bid of {self.amount} on {self.listing.id}-{self.listing.title}"

class Comments(models.Model):
    comment = models.CharField()
    date = models.DateField(auto_now_add=True)
    
    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments"
    )

    listing = models.ForeignKey (
        Listing,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return f"{self.id}-{self.commenter.username} commented : {self.comment} on {self.date}"