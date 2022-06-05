from django.contrib import admin

# Register your models here.
from core.admin import BaseVerifiedAdmin, BaseAdmin
from user_profile.models import Profile, Credit, CreditTransaction


@admin.register(Profile)
class ProfileAdmin(BaseVerifiedAdmin):
    pass


@admin.register(Credit)
class CreditAdmin(BaseAdmin):
    pass


@admin.register(CreditTransaction)
class CreditTransactionAdmin(BaseAdmin):
    pass
