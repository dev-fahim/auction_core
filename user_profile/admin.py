# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Profile, Credit, CreditTransaction


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'guid',
        'created',
        'updated',
        'is_active',
        'verified_by',
        'verification_timestamp',
        'user',
        'user_type',
    )
    list_filter = (
        'created',
        'updated',
        'is_active',
        'verified_by',
        'verification_timestamp',
        'user',
    )


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'guid',
        'created',
        'updated',
        'is_active',
        'user',
        'balance',
        'expiry',
    )
    list_filter = ('created', 'updated', 'is_active', 'user', 'expiry')


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'guid',
        'created',
        'updated',
        'is_active',
        'credit',
        'amount',
        'type',
    )
    list_filter = ('created', 'updated', 'is_active', 'credit')
