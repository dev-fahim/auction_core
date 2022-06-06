# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Auction, BidTransaction


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'guid',
        'created',
        'updated',
        'is_active',
        'created_by',
        'product',
        'min_bid_price',
        'bid_starts',
        'bid_expires',
        'min_required_credit',
    )
    list_filter = (
        'created',
        'updated',
        'is_active',
        'created_by',
        'product',
        'bid_starts',
        'bid_expires',
    )


@admin.register(BidTransaction)
class BidTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'guid',
        'created',
        'updated',
        'is_active',
        'auction',
        'user',
        'amount',
        'has_won',
    )
    list_filter = (
        'created',
        'updated',
        'is_active',
        'auction',
        'user',
        'has_won',
    )
