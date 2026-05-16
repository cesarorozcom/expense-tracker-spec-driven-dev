import csv
from io import StringIO
from django import forms
from django.core.exceptions import ValidationError
from .models import Account, Transaction


class CSVImportForm(forms.Form):
    """Form for importing transactions from CSV."""
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}),
        help_text='CSV format: account_name, date (YYYY-MM-DD HH:MM), amount, description'
    )
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='(Optional) Assign all rows to this account if not specified in CSV'
    )

    def clean_csv_file(self):
        """Validate CSV file format."""
        file = self.cleaned_data['csv_file']
        
        if not file.name.endswith('.csv'):
            raise ValidationError('File must be a CSV file.')
        
        try:
            content = file.read().decode('utf-8')
            csv.DictReader(StringIO(content))
        except Exception as e:
            raise ValidationError(f'Invalid CSV format: {str(e)}')
        
        return file

    def parse_csv(self):
        """Parse CSV and return list of transaction dicts."""
        file = self.cleaned_data['csv_file']
        content = file.read().decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        
        transactions = []
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
            try:
                account_name = row.get('account_name', '').strip()
                date_str = row.get('date', '').strip()
                amount_str = row.get('amount', '').strip()
                description = row.get('description', '').strip()
                
                if not account_name and not self.cleaned_data.get('account'):
                    raise ValueError('account_name required or select default account')
                
                if not date_str:
                    raise ValueError('date required')
                
                if not amount_str:
                    raise ValueError('amount required')
                
                transactions.append({
                    'row': row_num,
                    'account_name': account_name or (self.cleaned_data['account'].name if self.cleaned_data.get('account') else ''),
                    'date_str': date_str,
                    'amount_str': amount_str,
                    'description': description,
                })
            except ValueError as e:
                transactions.append({
                    'row': row_num,
                    'error': str(e),
                })
        
        return transactions


class ReportFilterForm(forms.Form):
    """Form for filtering transaction reports."""
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Account'
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Start Date'
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='End Date'
    )
    min_amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        label='Min Amount'
    )
    max_amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        label='Max Amount'
    )
