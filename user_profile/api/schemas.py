import typing

from core.api.schemas import UserSchema, VerifiedBySchema, BaseSchema, PaginatedObjectListSchema
from user_profile.enums import UserTypeEnum


class ProfileSchema(VerifiedBySchema, BaseSchema):
    user: UserSchema
    user_type: UserTypeEnum


class ProfileListSchema(PaginatedObjectListSchema):
    data: typing.List[ProfileSchema]
