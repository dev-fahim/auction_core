from ninja import Router

from core.api.auth import JWTAuth
from auction.api.permissions import check_user_buyer, check_profile_limited
from auction.queries import auction_object, auction_queryset, bid_transaction_queryset, create_bid_transaction
from auction.api.schemas import \
    AuctionSchema, \
    AuctionListSchema, \
    BidTransactionSchema, \
    BidTransactionListSchema, \
    PlaceBidTransactionSchema
from core.api.schemas import ErrorSchema
from core.helpers import func_debugger
from core.utils.builders import page_builder

router = Router(auth=[JWTAuth()])


@router.get('/all', response=AuctionListSchema)
@func_debugger
def get_all_auction_list(request, page_number: int = 1, is_running: bool = False):
    return page_builder(auction_queryset(request.user, is_running), 10, page_number)


@router.get('/get/{guid}', response={200: AuctionSchema, 422: ErrorSchema})
@func_debugger
def get_auction_object(request, guid: str):
    return auction_object(request.user, guid)


@router.get('/bid-transactions/all/{auction_guid}', response=BidTransactionListSchema)
@func_debugger
def get_all_bid_transactions(request, auction_guid: str, page_number: int = 1):
    auction = auction_object(request.user, auction_guid)
    return page_builder(bid_transaction_queryset(auction.id), 10, page_number)


@router.post('/place-bid-transaction', response={200: BidTransactionSchema, 422: ErrorSchema})
@func_debugger
def place_bid_transaction(request, data: PlaceBidTransactionSchema):
    check_user_buyer(request.user)
    check_profile_limited(request.user)

    auction = auction_object(request.user, data.auction_guid)
    bid_transaction = create_bid_transaction(request.user, auction.id, data.amount)
    return bid_transaction
