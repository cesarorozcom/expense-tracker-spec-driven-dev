# Expense Tracker (scaffold)

Minimal Django 5 project scaffold for the expense tracker feature.

Setup (local):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py create_first_user --username admin --email admin@example.com --password 'change-me' --superuser
python manage.py runserver
```

Create first user (non-interactive):

```bash
python manage.py create_first_user --username admin --email admin@example.com --password 'change-me' --superuser
```

Create first regular user:

```bash
python manage.py create_first_user --username user1 --email user1@example.com --password 'change-me'
```
