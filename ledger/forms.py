from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Account, Transaction


def validate_photo_file(file):
    """Validate photo file type and size."""
    # Check file type
    allowed_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
    if file.content_type not in allowed_types:
        raise ValidationError(_('Only JPEG, PNG, GIF, and WebP images are allowed.'))
    
    # Check file size (max 10MB)
    if file.size > 10 * 1024 * 1024:
        raise ValidationError(_('Photo size must be under 10MB.'))


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name']
        labels = {
            'name': _('Account name'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Account name (e.g., Checking)')}),
        }


class TransactionForm(forms.ModelForm):
    photo = forms.ImageField(
        required=False,
        validators=[validate_photo_file],
        label=_('Photo'),
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        help_text=_('Upload a receipt photo (JPEG, PNG, GIF, or WebP). Max 10MB.')
    )

    class Meta:
        model = Transaction
        fields = ['account', 
                  'occurred_at', 
                  'transaction_type', 
                  'amount', 
                  'description', 
                  'photo', 
                  'is_recurring']
        labels = {
            'account': _('Account'),
            'occurred_at': _('Date and time'),
            'transaction_type': _('Transaction type'),
            'amount': _('Amount'),
            'description': _('Description'),
            'is_recurring': _('Recurring'),
        }
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'occurred_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': _('Description')}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
