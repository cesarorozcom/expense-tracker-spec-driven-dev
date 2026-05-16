import pytest
import io
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from decimal import Decimal

from ledger.models import Account, Transaction


@pytest.mark.django_db
def test_index_view_no_accounts():
    """Test index view with no accounts."""
    client = Client()
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert b'No accounts yet' in response.content


@pytest.mark.django_db
def test_index_view_with_accounts():
    """Test index view with accounts."""
    account = Account.objects.create(name="Checking")
    client = Client()
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert b'Checking' in response.content


@pytest.mark.django_db
def test_create_account():
    """Test creating an account."""
    client = Client()
    response = client.post(reverse('create_account'), {'name': 'Savings'})
    assert response.status_code == 302  # Redirect after creation
    assert Account.objects.filter(name='Savings').exists()


@pytest.mark.django_db
def test_account_detail_with_transactions():
    """Test account detail view with transactions."""
    account = Account.objects.create(name="Checking")
    transaction = Transaction.objects.create(
        account=account,
        occurred_at=timezone.now(),
        amount=Decimal('50.00'),
        description="Grocery Store"
    )
    
    client = Client()
    response = client.get(reverse('account_detail', kwargs={'account_id': account.id}))
    assert response.status_code == 200
    assert b'Checking' in response.content
    assert b'Grocery Store' in response.content
    assert b'$50.00' in response.content


@pytest.mark.django_db
def test_create_transaction():
    """Test creating a transaction."""
    account = Account.objects.create(name="Checking")
    client = Client()
    
    response = client.post(
        reverse('create_transaction'),
        {
            'account': account.id,
            'occurred_at': '2026-05-16T10:00',
            'amount': '25.50',
            'description': 'Coffee',
            'is_recurring': False,
        }
    )
    
    assert response.status_code == 302  # Redirect after creation
    assert Transaction.objects.filter(description='Coffee').exists()
    tx = Transaction.objects.get(description='Coffee')
    assert tx.amount == Decimal('25.50')


@pytest.mark.django_db
def test_edit_transaction():
    """Test editing a transaction."""
    account = Account.objects.create(name="Checking")
    transaction = Transaction.objects.create(
        account=account,
        occurred_at=timezone.now(),
        amount=Decimal('10.00'),
        description="Coffee"
    )
    
    client = Client()
    response = client.post(
        reverse('edit_transaction', kwargs={'transaction_id': transaction.id}),
        {
            'account': account.id,
            'occurred_at': transaction.occurred_at.isoformat(),
            'amount': '15.00',
            'description': 'Coffee (updated)',
            'is_recurring': False,
        }
    )
    
    assert response.status_code == 302  # Redirect after edit
    transaction.refresh_from_db()
    assert transaction.amount == Decimal('15.00')
    assert transaction.description == 'Coffee (updated)'


@pytest.mark.django_db
def test_delete_transaction():
    """Test deleting a transaction."""
    account = Account.objects.create(name="Checking")
    transaction = Transaction.objects.create(
        account=account,
        occurred_at=timezone.now(),
        amount=Decimal('10.00'),
        description="Coffee"
    )
    
    client = Client()
    response = client.post(
        reverse('delete_transaction', kwargs={'transaction_id': transaction.id})
    )
    
    assert response.status_code == 302  # Redirect after delete
    assert not Transaction.objects.filter(id=transaction.id).exists()


def create_test_image():
    """Create a test image file."""
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(
        "test_photo.jpg",
        file.getvalue(),
        content_type="image/jpeg"
    )


@pytest.mark.django_db
def test_create_transaction_with_photo():
    """Test creating a transaction with a photo."""
    account = Account.objects.create(name="Checking")
    client = Client()
    
    photo = create_test_image()
    
    response = client.post(
        reverse('create_transaction'),
        {
            'account': account.id,
            'occurred_at': '2026-05-16T10:00',
            'amount': '25.50',
            'description': 'Coffee with receipt',
            'photo': photo,
            'is_recurring': False,
        }
    )
    
    assert response.status_code == 302  # Redirect after creation
    tx = Transaction.objects.get(description='Coffee with receipt')
    assert tx.photo is not None
    assert tx.photo_status == 'unverified'
    assert tx.photo_uploaded_at is not None


@pytest.mark.django_db
def test_transaction_photo_methods():
    """Test transaction photo helper methods."""
    account = Account.objects.create(name="Checking")
    transaction = Transaction.objects.create(
        account=account,
        occurred_at=timezone.now(),
        amount=Decimal('10.00'),
        description="Coffee"
    )
    
    # No photo initially
    assert not transaction.has_photo()
    
    # Add a photo
    photo = create_test_image()
    transaction.photo = photo
    transaction.save()
    
    assert transaction.has_photo()
    
    # Mark as verified
    transaction.mark_photo_verified()
    transaction.refresh_from_db()
    assert transaction.photo_status == 'verified'
    assert transaction.photo_uploaded_at is not None
    
    # Mark as failed
    transaction.mark_photo_failed()
    transaction.refresh_from_db()
    assert transaction.photo_status == 'failed'


@pytest.mark.django_db
def test_photo_file_size_validation():
    """Test that oversized photos are rejected."""
    from ledger.forms import TransactionForm
    from django.core.exceptions import ValidationError
    
    account = Account.objects.create(name="Checking")
    
    # Create a mock file that's too large
    oversized_file = SimpleUploadedFile(
        "large_photo.jpg",
        b"x" * (11 * 1024 * 1024),  # 11MB
        content_type="image/jpeg"
    )
    
    form = TransactionForm(
        data={
            'account': account.id,
            'occurred_at': '2026-05-16T10:00',
            'amount': '25.50',
            'description': 'Test',
        },
        files={'photo': oversized_file}
    )
    
    # Form should be invalid due to file size
    assert not form.is_valid()
    assert 'photo' in form.errors


@pytest.mark.django_db
def test_view_transaction_photo():
    """Test viewing transaction photo."""
    account = Account.objects.create(name="Checking")
    
    photo = create_test_image()
    transaction = Transaction.objects.create(
        account=account,
        occurred_at=timezone.now(),
        amount=Decimal('10.00'),
        description="Coffee",
        photo=photo,
        photo_status='verified'
    )
    
    client = Client()
    response = client.get(reverse('view_transaction_photo', kwargs={'transaction_id': transaction.id}))
    assert response.status_code == 200
    assert b'Transaction Photo' in response.content
    assert b'verified' in response.content or b'Verified' in response.content

