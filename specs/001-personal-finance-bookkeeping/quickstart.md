# Quickstart: Personal Finance Bookkeeping

## Prerequisites

- Python 3.12
- PostgreSQL
- Heroku CLI
- An S3-compatible object storage bucket for invoice photos

## Local Setup

1. Create and activate a virtual environment.
2. Install the project dependencies.
3. Configure environment variables for the database, storage, and Django settings.
4. Run database migrations.
5. Start the development server.
6. Run the test suite before making changes.

Example commands:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=src.config.settings
export DATABASE_URL=postgres://localhost/personal_finance
export SECRET_KEY=change-me
export DEBUG=1
python manage.py migrate
python manage.py runserver
pytest
```

## Required Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Django secret key
- `DEBUG`: enable or disable local debug mode
- `ALLOWED_HOSTS`: comma-separated host list
- `AWS_ACCESS_KEY_ID`: storage access key for invoice photos
- `AWS_SECRET_ACCESS_KEY`: storage secret key for invoice photos
- `AWS_STORAGE_BUCKET_NAME`: object storage bucket name
- `AWS_S3_REGION_NAME`: storage region
- `HEROKU_POSTGRESQL_*`: provided by Heroku Postgres in production

## Heroku Deployment

1. Create a Heroku app.
2. Set the web dyno type to Basic.
3. Add the smallest Heroku Postgres plan that fits the budget, or configure the chosen low-cost PostgreSQL provider.
4. Set the configuration variables for Django and object storage.
5. Push the repository to Heroku.
6. Run migrations on Heroku.
7. Open the deployed app and verify that transactions and photo uploads work end to end.

Example commands:

```bash
heroku create
heroku ps:type basic
heroku addons:create heroku-postgresql:essential-0
heroku config:set SECRET_KEY=change-me DEBUG=0 AWS_STORAGE_BUCKET_NAME=your-bucket
git push heroku main
heroku run python manage.py migrate
heroku open
```

## Verification Checklist

- Manual transaction creation saves correctly.
- Invoice photo upload persists after refresh.
- Running balance updates after edit and delete actions.
- Static assets load correctly in production.
- The app remains usable on a mobile phone viewport with no clipped controls or blocked form submission.
