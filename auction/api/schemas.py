import typing

from ninja import Field, Schema

from core.api.schemas import BaseSchema, CreatedBySchema, UserSchema, PaginatedObjectListSchema
from product.api.schemas import ProductSchema, ProductPriceSchema


class AuctionSchema(ProductPriceSchema, CreatedBySchema, BaseSchema):
    product: ProductSchema

    min_required_credit: int = Field(0, ge=0)


class AuctionListSchema(PaginatedObjectListSchema):
    data: typing.List[AuctionSchema]


class BidTransactionSchema(BaseSchema):
    auction: AuctionSchema = None
    user: UserSchema = None

    amount: int = Field(0, ge=0)
    has_won: bool = False


class BidTransactionListSchema(PaginatedObjectListSchema):
    data: typing.List[BidTransactionSchema]


class PlaceBidTransactionSchema(Schema):
    auction_guid: str
    amount: int = Field(0, gt=0)
