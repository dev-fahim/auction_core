from django.db import models

# Create your models here.
from core.models import BaseModel, CreatedByUserModel


class Auction(CreatedByUserModel, BaseModel):
    created_by_related_name = 'auctions_created'

    product = models.OneToOneField('product.Product', on_delete=models.CASCADE, related_name='auction')

    min_bid_price = models.PositiveIntegerField(default=0)
    bid_starts = models.DateTimeField()
    bid_expires = models.DateTimeField()

    min_required_credit = models.PositiveIntegerField(default=0)


class BidTransaction(BaseModel):
    auction = models.ForeignKey('auction.Auction', on_delete=models.CASCADE, null=True, related_name='bids')
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='bids')

    amount = models.PositiveIntegerField(default=0)
    has_won = models.BooleanField(default=False)
