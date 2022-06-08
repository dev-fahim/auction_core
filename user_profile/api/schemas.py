import typing

from ninja import Schema

from core.api.schemas import UserSchema, VerifiedBySchema, BaseSchema, PaginatedObjectListSchema
from user_profile.enums import UserTypeEnum


class UserProfileStatus(Schema):
    can_create_product: bool = False
    can_attend_auction: bool = False
    can_login: bool = False


class ProfileSchema(UserProfileStatus, VerifiedBySchema, BaseSchema):
    user: UserSchema
    user_type: UserTypeEnum


class SignUpSchema(Schema):
    email: str
    first_name: str
    last_name: str
    password: str
    is_buyer: bool = True


class ProfileUpdateSchema(Schema):
    email: str
    first_name: str
    last_name: str


class CheckEmailSchema(Schema):
    email: str


class SignInSchema(Schema):
    email: str
    password: str


class UserTokenSchema(Schema):
    accessToken: str
    profile: ProfileSchema


class VerifyUserProfile(Schema):
    guid: str
    is_verified: bool = False


class ProfileListSchema(PaginatedObjectListSchema):
    data: typing.List[ProfileSchema]
