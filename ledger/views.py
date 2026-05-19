from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from django.core.paginator import Paginator
from decimal import Decimal
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """List all accounts with running balance."""
    # Use aggregation to reduce DB queries
    accounts = Account.objects.annotate(
        transaction_count=Count('transactions'),
        balance=Sum('transactions__amount')
    )
    account_data = []
    for account in accounts:
        account_data.append({
            'account': account,
            'transaction_count': account.transaction_count or 0,
            'balance': account.balance or Decimal('0.00'),
        })
    
    return render(request, 'ledger/index.html', {
        'account_data': account_data,
    })


@login_required
def account_detail(request, account_id):
    """Show transactions for an account."""
    account = get_object_or_404(Account, id=account_id)
    transactions = account.transactions.all().order_by('-occurred_at')

    # Paginate transactions for performance
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate running balance for current page
    balance = Decimal('0.00')
    for tx in page_obj.object_list:
        balance += tx.amount

    return render(request, 'ledger/account_detail.html', {
        'account': account,
        'transactions': page_obj.object_list,
        'balance': balance,
        'page_obj': page_obj,
    })


@login_required
def create_account(request):
    """Create a new account."""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AccountForm()
    
    return render(request, 'ledger/create_account.html', {'form': form})


@login_required
def create_transaction(request, account_id=None):
    """Create a new transaction."""
    account = None
    if account_id:
        account = get_object_or_404(Account, id=account_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            if account and not form.cleaned_data.get('account'):
                transaction.account = account
            
            # Handle photo upload
            if form.cleaned_data.get('photo'):
                transaction.photo_status = 'unverified'
                transaction.photo_uploaded_at = timezone.now()
            # Ensure amount sign matches transaction_type: deposits are positive, payments negative
            try:
                amt = Decimal(form.cleaned_data.get('amount') or transaction.amount)
            except Exception:
                amt = Decimal('0.00')
            if form.cleaned_data.get('transaction_type') == 'deposit':
                transaction.amount = abs(amt)
            else:
                transaction.amount = -abs(amt)

            transaction.save()
            return redirect('account_detail', account_id=transaction.account.id)
    else:
        form = TransactionForm()
        if account:
            form.fields['account'].initial = account
    
    return render(request, 'ledger/create_transaction.html', {
        'form': form,
        'account': account,
    })


@login_required
def edit_transaction(request, transaction_id):
    """Edit an existing transaction."""
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)

            # Handle photo update
            if form.cleaned_data.get('photo') and form.files.get('photo'):
                transaction.photo_status = 'unverified'
                transaction.photo_uploaded_at = timezone.now()

            # Normalize amount sign to match transaction_type
            try:
                amt = Decimal(form.cleaned_data.get('amount') or transaction.amount)
            except Exception:
                amt = Decimal('0.00')
            if form.cleaned_data.get('transaction_type') == 'deposit':
                transaction.amount = abs(amt)
            else:
                transaction.amount = -abs(amt)

            transaction.save()
            return redirect('account_detail', account_id=transaction.account.id)
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'ledger/edit_transaction.html', {
        'form': form,
        'transaction': transaction,
    })


@login_required
def delete_transaction(request, transaction_id):
    """Delete a transaction."""
    transaction = get_object_or_404(Transaction, id=transaction_id)
    account_id = transaction.account.id
    
    if request.method == 'POST':
        transaction.delete()
        return redirect('account_detail', account_id=account_id)
    
    return render(request, 'ledger/delete_transaction.html', {
        'transaction': transaction,
    })


@login_required
def view_transaction_photo(request, transaction_id):
    """View transaction photo with signed URL (placeholder for S3 integration)."""
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if not transaction.photo:
        return redirect('account_detail', account_id=transaction.account.id)
    
    return render(request, 'ledger/view_photo.html', {
        'transaction': transaction,
        'photo_url': transaction.photo.url,
    })
