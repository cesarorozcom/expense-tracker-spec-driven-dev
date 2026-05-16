import pytest
import io
from django.test import Client
from django.urls import reverse
from ledger.models import Account


@pytest.mark.django_db
def test_preload_accounts_text_file():
    client = Client()
    content = b"Checking\nSavings\nCredit Card\n"
    f = io.BytesIO(content)
    f.name = 'accounts.txt'
    response = client.post(reverse('preload_accounts'), {'file': f})
    # Should return 200 and create accounts
    assert response.status_code == 200
    assert Account.objects.filter(name='Checking').exists()
    assert Account.objects.filter(name='Savings').exists()
    assert Account.objects.filter(name='Credit Card').exists()


@pytest.mark.django_db
def test_preload_accounts_csv_file():
    client = Client()
    content = b"account_name\nChecking\nSavings\n"
    f = io.BytesIO(content)
    f.name = 'accounts.csv'
    response = client.post(reverse('preload_accounts'), {'file': f})
    assert response.status_code == 200
    assert Account.objects.filter(name='Checking').exists()
    assert Account.objects.filter(name='Savings').exists()
