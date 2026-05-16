import pytest
from django.utils import timezone

from ledger.models import Account, Transaction


@pytest.mark.django_db
def test_create_account_and_transaction():
    acc = Account.objects.create(name="Checking")
    tx = Transaction.objects.create(
        account=acc,
        occurred_at=timezone.now(),
        amount=10.00,
        description="Coffee",
    )

    assert Account.objects.count() == 1
    assert Transaction.objects.filter(account=acc).count() == 1
