import datetime
import os
import random
import time
from functools import wraps

from django.utils import timezone
from mimesis import Person, Text, Hardware

try:
    from django import setup

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_core.settings')

    setup()

    from django.contrib.auth.models import User
    from user_profile.models import Profile, Credit, CreditTransaction
    from product.models import Product, Category
    from auction.models import Auction, BidTransaction
    from user_profile.enums import UserTypeEnum
    from auction.queries import create_bid_transaction
    from core.api.errors import ApiError
    from user_profile.queries import transfer_in

    from django.db import DatabaseError
except ModuleNotFoundError:
    exit(1)


def profile_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)
        print("Process took", "%.2f" % (time.time() - start), ' seconds')
        return f

    return wrapper


def get_random_date(start_date: datetime, end_date: datetime):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    return start_date + timezone.timedelta(days=random_number_of_days)


@profile_func
def main():
    person = Person()
    text = Text()
    hardware = Hardware()
    total_records = 100

    try:
        super_user = User.objects.get(username='fahim')
    except User.DoesNotExist:
        super_user = User.objects.create_user(username='fahim', password='1234', is_superuser=True, is_active=True,
                                              is_staff=True)

    users = []

    categories = []
    for _ in range(int(total_records / 10)):
        category = Category.objects.create(
            name=text.word(),
            description=text.sentence(),
            created_by_id=super_user.id,
            is_active=True
        )
        categories.append(category)

    for _ in range(total_records):
        email = person.email()
        first_name = person.first_name()
        last_name = person.last_name()
        user_type = random.choice(list(UserTypeEnum)[-2:])

        user = User.objects.create_user(
            username=email,
            email=email,
            password='1234',
            last_name=last_name,
            first_name=first_name,
        )
        profile = Profile.objects.create(
            user_id=user.id, user_type=user_type, is_active=True, verified_by_id=super_user.id)

        print('PROFILE', profile.guid, profile.user.first_name, profile.user.last_name, profile.user.email)

        users.append(user)

        credit = Credit.objects.create(
            user_id=user.id,
            is_active=True,
            expiry=timezone.now() + timezone.timedelta(days=365)
        )

        if profile.user_type == UserTypeEnum.BUYER:
            for __ in range(int(total_records)):
                transfer_in(credit, random.randint(1000, 100000))

        if profile.user_type == UserTypeEnum.SELLER:
            for __ in range(int(total_records)):
                product_name = hardware.phone_model()
                product_description = text.sentence()

                product = Product.objects.create(
                    user_id=user.id,
                    name=product_name,
                    description=product_description,
                    category_id=random.choice(categories).id,
                    min_bid_price=random.randint(1000, 10000),
                    bid_starts=get_random_date(timezone.datetime(2022, 6, 1), timezone.datetime(2022, 8, 30)),
                    bid_expires=get_random_date(timezone.datetime(2022, 9, 1), timezone.datetime(2022, 11, 30)),
                    is_active=True,
                    verified_by_id=super_user.id,
                )
                print('PRODUCT', product.guid, product.name)

    products = Product.objects.all()
    for product in products:
        auction = Auction.objects.create(
            product_id=product.id,
            created_by_id=super_user.id,
            min_bid_price=int(product.min_bid_price / 2),
            bid_starts=product.bid_starts,
            bid_expires=product.bid_expires,
            min_required_credit=int(product.min_bid_price * 1.5),
            is_active=True
        )
        print('AUCTION', auction.guid, auction.product.name)
        amount = random.randint(auction.min_bid_price, auction.min_bid_price * 10)

        for ___ in range(int(total_records / 10)):
            try:
                create_bid_transaction(
                    random.choice(users),
                    auction.id,
                    amount)
            except (ApiError, DatabaseError) as e:
                print(e)


if __name__ == '__main__':
    main()
