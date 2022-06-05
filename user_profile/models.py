from django.db import models

# Create your models here.
from core.models import BaseModel, VerificationModel
from user_profile.enums import UserTypeEnum


class Profile(VerificationModel, BaseModel):
    # TODO: add a picture (ImageField) field

    verification_related_name = 'profiles_verified'

    USER_TYPE_CHOICES = (
        (UserTypeEnum.USER_TYPE_ATTN, UserTypeEnum.USER_TYPE_ATTN),
        (UserTypeEnum.USER_TYPE_ADMIN, UserTypeEnum.USER_TYPE_ADMIN),
        (UserTypeEnum.USER_TYPE_BUYER, UserTypeEnum.USER_TYPE_BUYER),
        (UserTypeEnum.USER_TYPE_SELLER, UserTypeEnum.USER_TYPE_SELLER),
    )

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, related_name='profile')
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)


class Credit(BaseModel):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, related_name='credit')
    balance = models.PositiveIntegerField(default=0)
    expiry = models.DateTimeField(null=True, blank=True)


class CreditTransaction(BaseModel):
    TYPE_IN = 'IN'
    TYPE_OUT = 'OUT'
    TYPE_CHOICES = (
        (TYPE_IN, TYPE_IN),
        (TYPE_OUT, TYPE_OUT),
    )

    credit = models.ForeignKey('user_profile.Credit', on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
