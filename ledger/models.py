from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    PHOTO_STATUS_CHOICES = [
        ('unverified', _('Unverified')),
        ('verified', _('Verified')),
        ('failed', _('Failed')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    occurred_at = models.DateTimeField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', _('Deposit')),
        ('payment', _('Payment')),
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='payment')
    description = models.CharField(max_length=500, blank=True)
    photo = models.ImageField(upload_to='receipts/', null=True, blank=True)
    photo_status = models.CharField(max_length=20, choices=PHOTO_STATUS_CHOICES, default='unverified')
    photo_uploaded_at = models.DateTimeField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-occurred_at']

    def __str__(self):
        return f"{self.occurred_at.date()} {self.amount} {self.description}"

    def has_photo(self):
        return bool(self.photo)

    def mark_photo_verified(self):
        """Mark photo as verified."""
        if self.photo:
            self.photo_status = 'verified'
            self.photo_uploaded_at = timezone.now()
            self.save(update_fields=['photo_status', 'photo_uploaded_at'])

    def mark_photo_failed(self):
        """Mark photo as failed."""
        if self.photo:
            self.photo_status = 'failed'
            self.save(update_fields=['photo_status'])


class RecurringProfile(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recurrences')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=500, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    interval = models.PositiveIntegerField(default=1, help_text='Repeat every N frequency units')
    next_occurrence = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-next_occurrence']

    def __str__(self):
        return f"Recurring {self.amount} to {self.account.name} ({self.frequency} x{self.interval})"

    def is_due(self, at=None):
        from django.utils import timezone
        at = at or timezone.now()
        if not self.active:
            return False
        if self.end_date and self.next_occurrence and self.next_occurrence > self.end_date:
            return False
        return self.next_occurrence and self.next_occurrence <= at

    def advance_next(self):
        """Advance next_occurrence by interval according to frequency."""
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta
        if self.frequency == 'daily':
            self.next_occurrence = self.next_occurrence + timedelta(days=self.interval)
        elif self.frequency == 'weekly':
            self.next_occurrence = self.next_occurrence + timedelta(weeks=self.interval)
        elif self.frequency == 'monthly':
            self.next_occurrence = self.next_occurrence + relativedelta(months=self.interval)
        self.save(update_fields=['next_occurrence'])
