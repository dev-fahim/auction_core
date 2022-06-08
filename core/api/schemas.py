import datetime
import enum
import typing

from ninja import Schema


class ErrorCodes(int, enum.Enum):
    GLOBAL_GET_ERROR = 1001
    GLOBAL_CREATE_ERROR = 1002
    GLOBAL_UPDATE_ERROR = 1003
    GLOBAL_DELETE_ERROR = 1004
    GLOBAL_OPERATION_ERROR = 1005
    GLOBAL_TRANSACTIONAL_ERROR = 1006
    GLOBAL_UNIQUE_ERROR = 1007
    GLOBAL_INTEGRITY_ERROR = 1008
    GLOBAL_CREDENTIAL_ERROR = 1009
    GLOBAL_NOT_PERMITTED_ERROR = 1010

    NOT_FOUND = 2001

    USER_UPDATE_ERROR = 3001

    USER_SIGN_UP_DATABASE_ERROR = 4001

    SIGN_IN_WRONG_CREDENTIALS = 5001


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


class ErrorSchema(Schema):
    error: str
    code: ErrorCodes


class SuccessSchema(Schema):
    success: str


class MsgSchema(Schema):
    msg: str
