from django.db.models import TextChoices


class UserTypeEnum(TextChoices):
    ATTN = 'ATTN'
    ADMIN = 'ADMIN'
    BUYER = 'BUYER'
    SELLER = 'SELLER'


class CreditTransactionTypeChoices(TextChoices):
    IN = 'IN'
    OUT = 'OUT'
