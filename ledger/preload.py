from django.shortcuts import render
from django import forms
from .models import Account
from django.views.decorators.http import require_http_methods


class PreloadAccountsForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.txt,.csv'}),
        help_text='Upload newline-separated account names or a CSV with an account_name column.'
    )


@require_http_methods(["GET", "POST"])
def preload_accounts(request):
    if request.method == 'POST':
        form = PreloadAccountsForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            content = f.read().decode('utf-8')
            lines = []
            # Try parsing as CSV with account_name header
            import csv
            try:
                reader = csv.DictReader(content.splitlines())
                if reader.fieldnames and 'account_name' in [h.strip() for h in reader.fieldnames]:
                    for row in reader:
                        name = (row.get('account_name') or '').strip()
                        if name:
                            lines.append(name)
                else:
                    raise ValueError('no account_name header')
            except Exception:
                # Fallback: treat as newline-separated names
                lines = [l.strip() for l in content.splitlines() if l.strip()]

            created = []
            skipped = []
            for name in lines:
                account, created_flag = Account.objects.get_or_create(name=name)
                if created_flag:
                    created.append(name)
                else:
                    skipped.append(name)

            return render(request, 'ledger/preload_result.html', {
                'created': created,
                'skipped': skipped,
                'total': len(lines),
            })
    else:
        form = PreloadAccountsForm()

    return render(request, 'ledger/preload_accounts.html', {'form': form})
