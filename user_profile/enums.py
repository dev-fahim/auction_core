from django.db.models import TextChoices


class UserTypeEnum(TextChoices):
    ATTN = 'ATTN'
    ADMIN = 'ADMIN'
    BUYER = 'BUYER'
    SELLER = 'SELLER'
