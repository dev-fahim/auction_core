# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'guid',
        'created',
        'updated',
        'is_active',
        'created_by',
        'name',
        'description',
    )
    list_filter = ('created', 'updated', 'is_active', 'created_by')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'guid',
        'created',
        'updated',
        'is_active',
        'verified_by',
        'verification_timestamp',
        'user',
        'category',
        'name',
        'description',
        'min_bid_price',
        'bid_starts',
        'bid_expires',
    )
    list_filter = (
        'created',
        'updated',
        'is_active',
        'verified_by',
        'verification_timestamp',
        'user',
        'category',
        'bid_starts',
        'bid_expires',
    )
    search_fields = ('name',)
