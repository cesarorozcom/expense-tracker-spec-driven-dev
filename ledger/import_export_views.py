import csv
from io import StringIO
from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .import_export import CSVImportForm, ReportFilterForm


@require_http_methods(["GET", "POST"])
def import_transactions(request):
    """Import transactions from CSV."""
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            transactions = form.parse_csv()
            
            # Validate and create transactions
            created_count = 0
            error_count = 0
            errors = []
            
            for tx_data in transactions:
                if 'error' in tx_data:
                    error_count += 1
                    errors.append(f"Row {tx_data['row']}: {tx_data['error']}")
                    continue
                
                try:
                    # Get or create account
                    account, _ = Account.objects.get_or_create(
                        name=tx_data['account_name']
                    )
                    
                    # Parse date
                    try:
                        occurred_at = datetime.strptime(tx_data['date_str'], '%Y-%m-%d %H:%M')
                        occurred_at = timezone.make_aware(occurred_at)
                    except ValueError:
                        try:
                            occurred_at = datetime.strptime(tx_data['date_str'], '%Y-%m-%d')
                            occurred_at = timezone.make_aware(occurred_at.replace(hour=0, minute=0))
                        except ValueError:
                            errors.append(f"Row {tx_data['row']}: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM")
                            error_count += 1
                            continue
                    
                    # Parse amount
                    try:
                        amount = Decimal(tx_data['amount_str'])
                    except:
                        errors.append(f"Row {tx_data['row']}: Invalid amount")
                        error_count += 1
                        continue
                    
                    # Create transaction
                    Transaction.objects.create(
                        account=account,
                        occurred_at=occurred_at,
                        amount=amount,
                        description=tx_data['description']
                    )
                    created_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f"Row {tx_data['row']}: {str(e)}")
            
            return render(request, 'ledger/import_result.html', {
                'created_count': created_count,
                'error_count': error_count,
                'errors': errors[:10],  # Show first 10 errors
                'total_errors': len(errors),
            })
    else:
        form = CSVImportForm()
    
    return render(request, 'ledger/import_transactions.html', {'form': form})


def export_transactions(request):
    """Export transactions to CSV."""
    form = ReportFilterForm(request.GET)
    
    # Get transactions
    transactions = Transaction.objects.all().order_by('-occurred_at')
    
    if form.is_valid():
        if form.cleaned_data.get('account'):
            transactions = transactions.filter(account=form.cleaned_data['account'])
        
        if form.cleaned_data.get('start_date'):
            transactions = transactions.filter(
                occurred_at__date__gte=form.cleaned_data['start_date']
            )
        
        if form.cleaned_data.get('end_date'):
            transactions = transactions.filter(
                occurred_at__date__lte=form.cleaned_data['end_date']
            )
        
        if form.cleaned_data.get('min_amount'):
            transactions = transactions.filter(
                amount__gte=form.cleaned_data['min_amount']
            )
        
        if form.cleaned_data.get('max_amount'):
            transactions = transactions.filter(
                amount__lte=form.cleaned_data['max_amount']
            )
    
    # Create CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Account', 'Date', 'Amount', 'Description', 'Status'])
    
    for tx in transactions:
        writer.writerow([
            tx.account.name,
            tx.occurred_at.strftime('%Y-%m-%d %H:%M'),
            tx.amount,
            tx.description,
            tx.photo_status if tx.has_photo() else 'No photo',
        ])
    
    return response


def ledger_report(request):
    """View ledger report with filters."""
    form = ReportFilterForm(request.GET)
    
    # Get transactions
    transactions = Transaction.objects.select_related('account').order_by('-occurred_at')
    
    if form.is_valid():
        if form.cleaned_data.get('account'):
            transactions = transactions.filter(account=form.cleaned_data['account'])
        
        if form.cleaned_data.get('start_date'):
            transactions = transactions.filter(
                occurred_at__date__gte=form.cleaned_data['start_date']
            )
        
        if form.cleaned_data.get('end_date'):
            transactions = transactions.filter(
                occurred_at__date__lte=form.cleaned_data['end_date']
            )
        
        if form.cleaned_data.get('min_amount'):
            transactions = transactions.filter(
                amount__gte=form.cleaned_data['min_amount']
            )
        
        if form.cleaned_data.get('max_amount'):
            transactions = transactions.filter(
                amount__lte=form.cleaned_data['max_amount']
            )
    
    # Paginate and calculate running balance per page to avoid loading all rows
    from django.core.paginator import Paginator
    paginator = Paginator(transactions, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    running_balance = Decimal('0.00')
    ledger_data = []
    for tx in page_obj.object_list:
        running_balance += tx.amount
        ledger_data.append({
            'transaction': tx,
            'balance': running_balance,
        })

    return render(request, 'ledger/ledger_report.html', {
        'form': form,
        'ledger_data': ledger_data,
        'page_obj': page_obj,
    })


def summary_report(request):
    """View summary statistics."""
    form = ReportFilterForm(request.GET)
    
    # Get accounts
    accounts = Account.objects.all()
    
    account_summary = []
    total_balance = Decimal('0.00')
    total_transactions = 0
    
    for account in accounts:
        txs = account.transactions.all()
        
        if form.is_valid():
            if form.cleaned_data.get('start_date'):
                txs = txs.filter(occurred_at__date__gte=form.cleaned_data['start_date'])
            
            if form.cleaned_data.get('end_date'):
                txs = txs.filter(occurred_at__date__lte=form.cleaned_data['end_date'])
            
            if form.cleaned_data.get('min_amount'):
                txs = txs.filter(amount__gte=form.cleaned_data['min_amount'])
            
            if form.cleaned_data.get('max_amount'):
                txs = txs.filter(amount__lte=form.cleaned_data['max_amount'])
        
        balance = txs.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        count = txs.count()
        photos = txs.filter(photo__isnull=False).count()
        
        account_summary.append({
            'account': account,
            'balance': balance,
            'transaction_count': count,
            'photo_count': photos,
        })
        
        total_balance += balance
        total_transactions += count
    
    return render(request, 'ledger/summary_report.html', {
        'form': form,
        'account_summary': account_summary,
        'total_balance': total_balance,
        'total_transactions': total_transactions,
    })
