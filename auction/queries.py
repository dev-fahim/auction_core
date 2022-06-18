from django.contrib.auth.models import User
from django.db import DatabaseError, transaction
from django.db.models import QuerySet
from django.utils import timezone

from auction.models import Auction, BidTransaction
from core.api.errors import GetError, OperationalError, NotPermittedError
from user_profile.enums import UserTypeEnum, CreditTransactionTypeChoices
from user_profile.models import Credit, CreditTransaction
from user_profile.queries import transfer_out


def auction_queryset(user: User, is_running: bool = False) -> QuerySet[Auction]:
    now = timezone.now()

    auctions = Auction.objects.select_related('product', 'created_by').filter(is_active=True)
    if is_running:
        auctions = auctions.filter(bid_starts__gte=now, bid_expires__lte=now)
    if user.profile.user_type == UserTypeEnum.SELLER:
        auctions = auctions.filter(product__user_id=user.id)

    return auctions


def auction_object(user: User, guid: str) -> Auction:
    try:
        queryset = Auction.objects.select_related('product', 'created_by')

        if user.profile.user_type == UserTypeEnum.SELLER:
            auction = queryset.get(is_active=True, product__user_id=user.id, guid__exact=guid)
        else:
            auction = queryset.get(is_active=True, guid__exact=guid)
    except Auction.DoesNotExist:
        raise GetError("auction")

    return auction


def bid_transaction_queryset(auction_id: int, **extra_filters) -> QuerySet[BidTransaction]:
    return BidTransaction.objects.select_related('auction', 'user').filter(
        is_active=True,
        auction_id=auction_id,
        **extra_filters)


def highest_bid_transaction(auction_id: int) -> BidTransaction:
    return bid_transaction_queryset(auction_id, has_won=True).order_by('-amount').first()


def will_won_bid_transaction(auction_id: int, amount: int) -> bool:
    highest = highest_bid_transaction(auction_id)
    if highest is None:
        return True
    if amount > highest.amount:
        return True
    return False


def create_bid_transaction(user: User, auction_id: int, amount: int) -> BidTransaction:
    if user.profile.user_type == UserTypeEnum.SELLER:
        raise NotPermittedError("user")

    try:
        auction = Auction.objects.get(id=auction_id)
    except Auction.DoesNotExist:
        raise GetError("auction")

    if auction.min_bid_price >= amount:
        raise OperationalError("auction_bid_amount")

    try:
        with transaction.atomic():
            try:
                credit = Credit.objects.get(user_id=user.id)
            except Credit.DoesNotExist:
                raise GetError("credit_not_issued")

            credit_transaction = transfer_out(credit, amount)

            bid_transaction = BidTransaction.objects.create(
                user_id=user.id,
                auction_id=auction_id,
                amount=amount,
                has_won=will_won_bid_transaction(auction_id, amount),
                is_active=True
            )
            credit_transaction.auction_id = auction_id
            credit_transaction.bid_transaction_id = bid_transaction.id
            credit_transaction.is_active = True
            credit_transaction.save()
            credit.balance -= amount
            credit.save()

            return bid_transaction

    except DatabaseError:
        raise OperationalError("bid_transaction_and_credit")
