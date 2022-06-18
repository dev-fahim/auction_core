from django.utils import timezone

from core.api.errors import OperationalError
from user_profile.enums import CreditTransactionTypeChoices
from user_profile.models import CreditTransaction, Credit


def transfer_in(credit: Credit, amount: int) -> CreditTransaction:
    """Make sure to run it in transaction.atomic()"""
    now = timezone.now()

    if credit.expiry >= now and credit.is_active:
        tr = CreditTransaction.objects.create(
            type=CreditTransactionTypeChoices.IN,
            amount=amount,
            credit_id=credit.id
        )
        credit.balance += amount
        credit.save()
        return tr


def transfer_out(credit: Credit, amount: int) -> CreditTransaction | None:
    """Make sure to run it in transaction.atomic()"""
    now = timezone.now()

    if credit.balance >= amount and credit.expiry >= now and credit.is_active:
        credit_transaction = CreditTransaction.objects.create(
            credit_id=credit.id,
            amount=amount,
            type=CreditTransactionTypeChoices.OUT,
            is_active=True
        )
        return credit_transaction
    else:
        raise OperationalError("credit_not_satisfied")
