from django.contrib import admin

# Register your models here.
from core.admin import BaseAdmin, BaseCreatedAdmin
from auction.models import Auction, BidTransaction


@admin.register(Auction)
class AuctionAdmin(BaseCreatedAdmin):
    pass


@admin.register(BidTransaction)
class BidTransactionAdmin(BaseAdmin):
    pass
