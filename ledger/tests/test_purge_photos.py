import pytest
import io
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
import os
from django.core.management import call_command

from ledger.models import Account, Transaction

@pytest.mark.django_db
def test_purge_photos_command(tmp_path, monkeypatch):
    account = Account.objects.create(name='Checking')
    # create fake photo file
    file_path = tmp_path / 'old_photo.jpg'
    file_path.write_bytes(b'test')

    tx = Transaction.objects.create(
        account=account,
        occurred_at=timezone.now(),
        amount=Decimal('10.00'),
        description='Old receipt',
        photo=str(file_path),
        photo_uploaded_at=timezone.now() - timezone.timedelta(days=400),
    )

    # monkeypatch os.path.exists and os.remove to avoid actual fs ops
    monkeypatch.setattr('os.path.exists', lambda p: True)
    removed = []
    def fake_remove(p):
        removed.append(p)
    monkeypatch.setattr('os.remove', fake_remove)

    call_command('purge_photos')
    tx.refresh_from_db()
    assert tx.photo is None or tx.photo == ''
