from django.db import models

# Create your models here.
from core.models import BaseModel, VerificationModel, CreatedByUserModel


class Category(CreatedByUserModel, BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(VerificationModel, BaseModel):
    # TODO: add a picture (ImageField) field

    verification_related_name = 'products_verified'

    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    category = models.ForeignKey('product.Category', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='products')

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    min_bid_price = models.PositiveIntegerField(default=0)
    bid_starts = models.DateTimeField()
    bid_expires = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def is_updatable(self):
        return self.is_verified is False
