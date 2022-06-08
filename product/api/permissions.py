from django.contrib.auth.models import User

from core.api.errors import NotPermittedError


def has_seller_permission(user: User):
    profile = user.profile

    return profile.can_login and profile.can_operate_product


def check_seller_limited(user: User):
    if has_seller_permission(user):
        return None
    raise NotPermittedError("profile")
