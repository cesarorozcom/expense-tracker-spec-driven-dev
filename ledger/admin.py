from django.contrib import admin
from .models import Account, Transaction
from .models import RecurringProfile

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('occurred_at', 'account', 'amount', 'is_recurring')
    list_filter = ('is_recurring', 'account')


@admin.register(RecurringProfile)
class RecurringProfileAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'frequency', 'interval', 'next_occurrence', 'active')
    list_filter = ('frequency', 'active')
