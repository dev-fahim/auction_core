import datetime
import typing

from ninja import Schema

from core.api.schemas import BaseSchema, VerifiedBySchema, UserSchema, PaginatedObjectListSchema


class CategorySchema(BaseSchema):
    name: str


class ProductSchema(VerifiedBySchema, BaseSchema):
    user: UserSchema
    category: CategorySchema = None

    name: str
    description: str = None

    min_bid_price: int
    bid_starts: datetime.datetime
    bid_expires: datetime.datetime


class CreateProductSchema(Schema):
    category: str = None

    name: str
    description: str = None

    min_bid_price: int = 0
    bid_starts: datetime.datetime
    bid_expires: datetime.datetime


class UpdateProductSchema(Schema):
    category: str = None

    name: str
    description: str = None

    min_bid_price: int = 0
    bid_starts: datetime.datetime
    bid_expires: datetime.datetime


class ProductListSchema(PaginatedObjectListSchema):
    data: typing.List[ProductSchema]
