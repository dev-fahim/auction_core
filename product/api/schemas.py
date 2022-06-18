import datetime
import typing

from django.utils import timezone
from ninja import Schema, Field

from core.api.schemas import BaseSchema, VerifiedBySchema, UserSchema, PaginatedObjectListSchema


class CategorySchema(BaseSchema):
    name: str


class ProductPriceSchema(Schema):
    min_bid_price: int = Field(0, ge=0)
    bid_starts: datetime.datetime = Field(None)
    bid_expires: datetime.datetime = Field(None)


class ProductSchema(ProductPriceSchema, VerifiedBySchema, BaseSchema):
    user: UserSchema
    category: CategorySchema = None

    name: str
    description: str = None

    is_updatable: bool = False


class CreateProductSchema(ProductPriceSchema, Schema):
    category: str = None

    name: str
    description: str = None


class UpdateProductSchema(Schema):
    category: str = None

    name: str
    description: str = None

    min_bid_price: int = Field(0, ge=0)
    bid_starts: datetime.datetime = Field(None)
    bid_expires: datetime.datetime = Field(None)


class ProductListSchema(PaginatedObjectListSchema):
    data: typing.List[ProductSchema]


class CategoryListSchema(Schema):
    data: typing.List[CategorySchema]
