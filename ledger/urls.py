from django.urls import path, include
from . import views
from . import import_export_views
from . import preload

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/create/', views.create_account, name='create_account'),
    path('accounts/<uuid:account_id>/', views.account_detail, name='account_detail'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('transactions/create/<uuid:account_id>/', views.create_transaction, name='create_transaction_for_account'),
    path('transactions/<uuid:transaction_id>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transactions/<uuid:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    path('transactions/<uuid:transaction_id>/photo/', views.view_transaction_photo, name='view_transaction_photo'),
    # Import/Export
    path('import/', import_export_views.import_transactions, name='import_transactions'),
    path('export/', import_export_views.export_transactions, name='export_transactions'),
    # Reports
    path('reports/ledger/', import_export_views.ledger_report, name='ledger_report'),
    path('reports/summary/', import_export_views.summary_report, name='summary_report'),
    # Preload accounts
    path('preload-accounts/', preload.preload_accounts, name='preload_accounts'),
    # Authentication (login/logout/password reset)
    path('auth/', include('django.contrib.auth.urls')),
]
