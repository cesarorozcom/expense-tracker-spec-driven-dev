# Research: Personal Finance Bookkeeping

## Decision 1: Use Django for the application framework

- Decision: Build the app with Django 5 using server-rendered templates and Django forms.
- Rationale: Django gives a mature, maintainable structure for forms, validation, admin support, and database-backed workflows without needing a separate frontend application.
- Alternatives considered: Flask with custom wiring, FastAPI with a separate frontend, and Next.js. Flask and FastAPI would require more assembly for form-heavy UI flows; Next.js adds a second deployment concern and more moving parts than needed for this bookkeeping workflow.

## Decision 2: Use PostgreSQL for transaction storage

- Decision: Store transactions, photo metadata, and running balance snapshots in PostgreSQL.
- Rationale: The ledger is relational, transaction ordering matters, and PostgreSQL provides reliable constraints, indexing, and Heroku support.
- Alternatives considered: SQLite, MySQL, and document storage. SQLite is less suitable for Heroku production usage; document storage makes balance queries and reconciliation harder.

## Decision 3: Store invoice photos outside Heroku dynos

- Decision: Upload invoice photos to S3-compatible object storage and save only metadata in PostgreSQL.
- Rationale: Heroku filesystems are ephemeral, so photo persistence must use external storage. Object storage also scales cleanly for multiple photos per transaction.
- Alternatives considered: Local disk storage, database BLOBs, and Heroku filesystem storage. Local disk and Heroku filesystem storage are not durable; database BLOBs complicate backups and increase database size.

## Decision 4: Keep the frontend server-rendered with HTMX enhancement

- Decision: Use Django templates with a small amount of HTMX for in-place updates where helpful.
- Rationale: This keeps the application easy to deploy and maintain while still feeling responsive for create/edit flows.
- Alternatives considered: A separate React SPA, mobile-first native clients, and pure full-page reloads. A SPA would increase maintenance overhead; pure reloads are simpler but less ergonomic for attachments and balance refreshes.

## Decision 5: Use pytest-based automated testing

- Decision: Standardize on pytest, pytest-django, and factory_boy.
- Rationale: These tools support fast, readable tests for model logic, form validation, balance recalculation, and request/response behavior.
- Alternatives considered: Django's built-in test runner only, unittest, and end-to-end-only validation. The built-in runner is functional but less expressive; end-to-end-only testing would be too slow and brittle for core bookkeeping logic.

## Decision 6: Deploy on Heroku with gunicorn and WhiteNoise

- Decision: Package the app for Heroku with gunicorn as the app server and WhiteNoise for static assets.
- Rationale: Heroku is a straightforward fit for a Django app, and these components minimize deployment complexity while keeping maintenance predictable.
- Alternatives considered: Docker-only deployment, managed Kubernetes, and self-hosted VPS deployment. Those options add operational overhead without improving this feature's core value.

## Decision 7: Use Django i18n with Spanish as the default language

- Decision: Enable Django's locale framework and expose a language selector that switches the active locale, with `es` as the default language.
- Rationale: The requirement only needs application-level language selection, and Django's built-in i18n support keeps the solution simple, testable, and consistent with the existing server-rendered UI.
- Alternatives considered: Detecting the browser locale automatically, storing the preference in a user profile table, and using locale-specific subdomains. Automatic detection is less explicit for users, profile storage adds unnecessary data-model complexity for a single-user app, and subdomains add deployment overhead.
