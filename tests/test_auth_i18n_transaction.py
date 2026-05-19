import os
from decimal import Decimal
import pytest
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from ledger.models import Account, Transaction

@pytest.mark.django_db
def test_login_required_redirect(client):
    resp = client.get(reverse('index'))
    assert resp.status_code in (302, 301)
    assert settings.LOGIN_URL in resp['Location'] or '/auth/login/' in resp['Location']

@pytest.mark.django_db
def test_transaction_type_sign_behavior(client):
    # create and login user
    username = 'tester'
    password = 'pass1234'
    user = User.objects.create_user(username=username, password=password)
    assert client.login(username=username, password=password)

    # create account
    account = Account.objects.create(name='Test Account')

    # deposit should store positive amount
    resp = client.post(reverse('create_transaction'), {
        'account': str(account.id),
        'occurred_at': '2026-01-01T12:00',
        'transaction_type': 'deposit',
        'amount': '100.00',
        'description': 'Deposit test',
    })
    assert resp.status_code in (302, 303)
    tx = Transaction.objects.latest('created_at')
    assert tx.transaction_type == 'deposit'
    assert tx.amount == Decimal('100.00')

    # payment should store negative amount
    resp = client.post(reverse('create_transaction'), {
        'account': str(account.id),
        'occurred_at': '2026-01-02T12:00',
        'transaction_type': 'payment',
        'amount': '25.50',
        'description': 'Payment test',
    })
    assert resp.status_code in (302, 303)
    tx = Transaction.objects.latest('created_at')
    assert tx.transaction_type == 'payment'
    assert tx.amount == Decimal('-25.50')

@pytest.mark.django_db
def test_i18n_settings_and_po_present():
    # settings should include Spanish language
    assert any(code == 'es' for code, _ in settings.LANGUAGES)
    assert reverse('set_language') == '/i18n/setlang/'

    # basic check that a django.po file exists for es
    locale_po = os.path.join(settings.BASE_DIR, 'locale', 'es', 'LC_MESSAGES', 'django.po')
    assert os.path.exists(locale_po), f"Expected {locale_po} to exist"
    # and contains at least one translated msgid
    with open(locale_po, 'r', encoding='utf-8') as fh:
        content = fh.read()
    assert 'msgid "Sign In"' in content or 'msgid "Create Transaction"' in content


@pytest.mark.django_db
def test_navbar_changes_with_auth(client):
    # Anonymous user should see Sign In on the login page
    resp = client.get(reverse('login'))
    text = resp.content.decode('utf-8')
    assert 'Sign In' in text or 'Iniciar sesión' in text

    # After login, index should render and show Sign out link
    username = 'navtester'
    password = 'pass1234'
    user = User.objects.create_user(username=username, password=password)
    assert client.login(username=username, password=password)
    resp = client.get(reverse('index'))
    text = resp.content.decode('utf-8')
    assert 'Sign out' in text or 'Cerrar sesión' in text


@pytest.mark.django_db
def test_logout_via_post_redirects_to_login(client):
    username = 'logouttester'
    password = 'pass1234'
    User.objects.create_user(username=username, password=password)
    assert client.login(username=username, password=password)

    resp = client.post(reverse('logout'))

    assert resp.status_code in (302, 303)
    assert resp['Location'].endswith(reverse('login')) or '/auth/login/' in resp['Location']
    assert '_auth_user_id' not in client.session


@pytest.mark.django_db
def test_set_language_endpoint_sets_session_language(client):
    resp = client.post(reverse('set_language'), {
        'language': 'en',
        'next': reverse('login'),
    })

    assert resp.status_code in (302, 303)
    assert resp['Location'].endswith(reverse('login'))
    assert client.session.get(settings.LANGUAGE_COOKIE_NAME) == 'en'
