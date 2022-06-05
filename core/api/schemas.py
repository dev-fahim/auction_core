import datetime
import typing

from ninja import Schema


class BaseSchema(Schema):
    guid: str
    created: datetime.datetime
    updated: datetime.datetime
    is_active: bool


class UserSchema(Schema):
    username: str
    first_name: str = None
    last_name: str = None
    email: str = None
    date_joined: datetime.datetime


class VerifiedBySchema(Schema):
    is_verified: bool
    verified_by: UserSchema = None
    verification_timestamp: datetime.datetime = None


class CreatedBySchema(Schema):
    created_by: UserSchema = None


class PaginatedObjectListSchema(Schema):
    count: int
    next_page: int = None
    previous_page: int = None
    total_pages: int


class PaginationBuilderSchema(Schema):
    count: int
    next_page: int = None
    previous_page: int = None
    total_pages: int
    data: typing.List[typing.Any]
