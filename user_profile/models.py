from django.db import models

# Create your models here.
from core.models import BaseModel, VerificationModel
from user_profile.enums import UserTypeEnum, CreditTransactionTypeChoices


class Profile(VerificationModel, BaseModel):
    # TODO: add a picture (ImageField) field

    verification_related_name = 'profiles_verified'

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, related_name='profile')
    user_type = models.CharField(max_length=100, choices=UserTypeEnum.choices)

    can_attend_auction: bool = models.BooleanField(default=False)

    @property
    def can_operate_product(self):
        if self.user.is_superuser:
            return True

        if self.user_type == UserTypeEnum.BUYER:
            return False

        return self.is_verified

    @property
    def can_login(self):
        if self.user.is_superuser:
            return True

        return self.is_active


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

    auction = models.ForeignKey('auction.Auction', on_delete=models.SET_NULL, null=True, blank=True)
    bid_transaction = models.OneToOneField('auction.BidTransaction', on_delete=models.SET_NULL, null=True, blank=True)

    credit = models.ForeignKey('user_profile.Credit', on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=10, choices=CreditTransactionTypeChoices.choices)
