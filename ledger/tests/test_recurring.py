import pytest
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from ledger.models import Account, RecurringProfile, Transaction


@pytest.mark.django_db
def test_recurring_profile_due_and_generation(monkeypatch, tmp_path, capsys):
    account = Account.objects.create(name='Checking')
    now = timezone.now()
    profile = RecurringProfile.objects.create(
        account=account,
        amount=Decimal('10.00'),
        description='Subscription',
        frequency='daily',
        interval=1,
        next_occurrence=now - timedelta(days=1),
    )

    # Run management command
    from django.core.management import call_command
    call_command('run_recurring')

    # Transaction should be created
    assert Transaction.objects.filter(description='Subscription').exists()
    tx = Transaction.objects.filter(description='Subscription').first()
    assert tx.amount == Decimal('10.00')

    # Profile next_occurrence should be advanced
    profile.refresh_from_db()
    assert profile.next_occurrence > now


@pytest.mark.django_db
def test_recurring_profile_not_due():
    account = Account.objects.create(name='Savings')
    now = timezone.now()
    profile = RecurringProfile.objects.create(
        account=account,
        amount=Decimal('5.00'),
        frequency='weekly',
        interval=1,
        next_occurrence=now + timedelta(days=7),
    )

    from django.core.management import call_command
    call_command('run_recurring')

    assert not Transaction.objects.filter(account=account).exists()
