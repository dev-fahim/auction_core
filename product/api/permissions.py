from django.contrib.auth.models import User

from core.api.errors import NotPermittedError
from core.models import VerificationStatusTypes
from product.models import Product


def has_seller_permission(user: User):
    profile = user.profile

    return profile.can_login and profile.can_operate_product


def check_seller_limited(user: User):
    if has_seller_permission(user):
        return None
    raise NotPermittedError("profile")


def check_product_is_locked(product: Product):
    if product.is_updatable:
        return None
    raise NotPermittedError("product_locked")


def check_product_is_unlocked(product: Product):
    if not product.is_updatable:
        return None
    raise NotPermittedError("product_unlocked")
