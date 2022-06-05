from django.contrib import admin

# Register your models here.
from core.admin import BaseVerifiedAdmin, BaseCreatedAdmin
from product.models import Category, Product


@admin.register(Category)
class CategoryAdmin(BaseCreatedAdmin):
    pass


@admin.register(Product)
class ProductAdmin(BaseVerifiedAdmin):
    pass
