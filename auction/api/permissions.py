from django.contrib.auth.models import User

from core.api.errors import NotPermittedError
from user_profile.enums import UserTypeEnum


def check_user_buyer(user: User):
    if user.profile.user_type != UserTypeEnum.BUYER:
        raise NotPermittedError("user_not_buyer")


def check_profile_limited(user: User):
    if (user.is_active and
            user.profile.can_login and
            user.profile.is_verified and
            user.profile.can_attend_auction) is False:
        raise NotPermittedError("user_buyer_profile_limited")
