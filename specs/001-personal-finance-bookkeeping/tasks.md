---
description: "Implementation tasks for Personal Finance Bookkeeping feature"
---

# Tasks: Personal Finance Bookkeeping

**Input**: Design documents from `specs/001-personal-finance-bookkeeping/`

**Prerequisites**: plan.md (tech stack), spec.md (user stories P1-P4), data-model.md (entities), contracts/web-interface.md (endpoints), quickstart.md (setup)

**Technology Stack**: Python 3.12, Django 5.2, PostgreSQL, Bootstrap 5.3, HTMX, django-storages, boto3, pytest, gunicorn, WhiteNoise

**Project Structure**: Django monolith with `expense_tracker/` config and `ledger/` app; templates in `templates/`; internationalization in `locale/`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [TaskID] [P?] [Story?] Description with exact filepath`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, US4)
- **Filepath**: Exact relative path from repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and Heroku deployment structure

- [ ] T001 Create Procfile and runtime.txt for Heroku deployment with gunicorn and Python 3.12
- [ ] T002 Verify requirements.txt includes Django 5.2, postgresql, boto3, django-storages, WhiteNoise, and pytest dependencies
- [ ] T003 [P] Create locale directory structure at `locale/es/LC_MESSAGES/` and `locale/en/LC_MESSAGES/` for i18n catalogs
- [ ] T004 [P] Create S3 configuration and storage backend in `expense_tracker/storage_backends.py` for S3-compatible object storage with boto3
- [ ] T005 Initialize Django project settings in `expense_tracker/settings.py` with SECRET_KEY, DEBUG, ALLOWED_HOSTS, and database configuration
- [ ] T006 Configure MIDDLEWARE in `expense_tracker/settings.py` to include LocaleMiddleware, SessionMiddleware, and CSRFMiddleware
- [ ] T007 [P] Create base.html template in `templates/base.html` with Bootstrap 5.3, language selector form, and main navigation
- [ ] T008 [P] Create base CSS file in `templates/static/css/style.css` for responsive mobile-first styling with accessibility (WCAG 2.1 AA)
- [ ] T009 Create manage.py command scaffold in `ledger/management/commands/` with timezone-aware helpers for recurring tasks
- [ ] T010 Create pytest.ini configuration with django_db markers and test discovery settings

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T011 [P] Create Transaction model in `ledger/models.py` with fields: transaction_type, amount, transaction_date, note, running_balance_after, created_at, updated_at, and validation for amount > 0
- [ ] T012 [P] Create InvoicePhoto model in `ledger/models.py` with fields: transaction_id (FK), file (S3), original_filename, content_type, file_size_bytes, uploaded_at
- [ ] T013 [P] Create database migrations in `ledger/migrations/` for Transaction and InvoicePhoto models with PostgreSQL support
- [ ] T014 Create TransactionForm class in `ledger/forms.py` with fields: transaction_type, amount, transaction_date, note; include DateField with timezone awareness and amount validation
- [ ] T015 [P] Create balance recalculation service in `ledger/services.py` with function `recalculate_ledger_balance()` that updates running_balance_after for all transactions in date order
- [ ] T016 [P] Create photo upload validation service in `ledger/services.py` with `validate_invoice_photo()` function checking file size (max 10 MiB), MIME types (jpeg, png, webp)
- [ ] T017 [P] Create S3 upload service in `ledger/services.py` with `upload_photo_to_s3()` and `generate_signed_url()` functions for secure photo storage
- [ ] T018 Create timezone helper utilities in `ledger/utils.py` with functions for UTC conversion and localized timestamp display
- [ ] T019 Initialize URL routing in `ledger/urls.py` with route imports from views (to be implemented in user stories)
- [ ] T020 Configure i18n in `expense_tracker/settings.py` with LANGUAGE_CODE='es', supported languages ['es', 'en'], LOCALE_PATHS pointing to `locale/`
- [ ] T021 Create base test fixtures in `ledger/tests/conftest.py` with factory_boy factories for Transaction and InvoicePhoto models
- [ ] T022 [P] Create authentication middleware in `ledger/middleware.py` to ensure single-user access (login required for all ledger views)
- [ ] T023 Create admin.py registration in `ledger/admin.py` for Transaction and InvoicePhoto models with read-only access

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Manual Transaction Entry (Priority: P1) 🎯 MVP

**Goal**: Users can manually create deposits or payments with required fields (type, amount, date) and see them appear in the transaction list with correct balance impact.

**Independent Test**: A user can create a payment or deposit via form, save it, and verify it appears in the transaction list with the correct type, amount, date, and running balance.

### Tests for User Story 1 (TDD - write FAIL tests first) ⚠️

- [ ] T024 [P] [US1] Unit test for Transaction model validation in `ledger/tests/test_models.py`: verify amount must be positive, transaction_type is required, transaction_date is required
- [ ] T025 [P] [US1] Unit test for balance recalculation in `ledger/tests/test_models.py`: create two transactions (deposit then payment) and verify running_balance_after is correct for each
- [ ] T026 [P] [US1] Form validation test in `ledger/tests/test_forms.py`: verify TransactionForm rejects empty amount, invalid date, missing type; accepts valid inputs
- [ ] T027 [US1] Integration test for transaction creation flow in `ledger/tests/test_views.py`: POST /transactions with valid data, verify redirect to ledger, verify transaction persists in database with correct balance
- [ ] T028 [US1] Integration test for form display in `ledger/tests/test_views.py`: GET /transactions/new returns 200, form contains all required fields, CSRF token present

### Implementation for User Story 1

- [ ] T029 [P] [US1] Create transaction creation view `create_transaction` in `ledger/views.py` handling GET (render form) and POST (save transaction, recalculate balance, redirect)
- [ ] T030 [P] [US1] Create transaction list view `transaction_list` in `ledger/views.py` displaying all transactions ordered by date with running balances; render in `templates/ledger/index.html`
- [ ] T031 [P] [US1] Create HTML form template `templates/ledger/create_transaction.html` with fields: transaction_type (radio/select), amount (decimal input), transaction_date (date input), note (textarea); include validation error display and CSRF token
- [ ] T032 [US1] Add URL route in `ledger/urls.py` for GET/POST `/transactions/` mapping to `create_transaction` view
- [ ] T033 [US1] Add URL route in `ledger/urls.py` for GET `/transactions/new` mapping to transaction form display
- [ ] T034 [US1] Add URL route in `ledger/urls.py` for GET `/` (home) mapping to `transaction_list` view with running balance summary
- [ ] T035 [US1] Implement transaction_list template `templates/ledger/index.html` displaying current balance (last running_balance_after), transaction table with date/type/amount/balance columns, link to create form
- [ ] T036 [US1] Add form class enhancement in `ledger/forms.py`: TransactionForm `__init__` to set LANGUAGE_CODE context for date formatting, `clean_amount()` to reject amounts <= 0, `clean()` to validate date not in future
- [ ] T037 [US1] Add middleware hook in `ledger/middleware.py` to ensure all transaction views require authentication (login_required decorator or middleware check)
- [ ] T038 [US1] Create signal or model save handler to call `recalculate_ledger_balance()` after Transaction creation/update/delete in `ledger/models.py`

**Checkpoint**: User Story 1 is fully functional and testable independently. Users can create, view, and see balances update correctly.

---

## Phase 4: User Story 2 - Photo Attachment & Review (Priority: P2)

**Goal**: Users can attach invoice photos to transactions (during creation or later), view photos in transaction details, and have photos persist across edits/refreshes.

**Independent Test**: A user can create a transaction with an attached photo, verify the photo appears in the saved transaction details, refresh the page, and confirm the photo is still there. The user can also add a photo to an existing transaction.

### Tests for User Story 2 (TDD - write FAIL tests first) ⚠️

- [ ] T039 [P] [US2] Unit test for InvoicePhoto model in `ledger/tests/test_models.py`: verify FK to Transaction, file_size_bytes and content_type are optional, uploaded_at is auto-set
- [ ] T040 [P] [US2] Unit test for photo validation service in `ledger/tests/test_services.py`: verify `validate_invoice_photo()` rejects files > 10 MiB, rejects non-image MIME types, accepts valid jpeg/png/webp
- [ ] T041 [P] [US2] Unit test for S3 upload service in `ledger/tests/test_services.py`: mock boto3, verify `upload_photo_to_s3()` uploads file with correct key, returns URL; verify `generate_signed_url()` returns time-limited URL
- [ ] T042 [US2] Integration test for photo upload in transaction creation in `ledger/tests/test_views.py`: POST /transactions with valid photo, verify InvoicePhoto created, linked to transaction, file stored in S3
- [ ] T043 [US2] Integration test for photo display in transaction detail in `ledger/tests/test_views.py`: GET /transactions/<id> with attached photo, verify photo appears in HTML, signed URL is valid and time-limited
- [ ] T044 [US2] Integration test for add-photo-to-existing-transaction in `ledger/tests/test_views.py`: POST /transactions/<id>/photos with photo, verify new InvoicePhoto linked, previous data unchanged

### Implementation for User Story 2

- [ ] T045 [P] [US2] Create InvoicePhotoForm in `ledger/forms.py` with MultipleFileField, validate file size and type in `clean_invoice_photos()`
- [ ] T046 [P] [US2] Enhance TransactionForm in `ledger/forms.py` to include InvoicePhotoForm for multi-file upload during creation
- [ ] T047 [US2] Create transaction detail view `transaction_detail` in `ledger/views.py` displaying transaction data and all associated InvoicePhoto records with signed URLs
- [ ] T048 [US2] Create add-photos-to-transaction view `add_transaction_photos` in `ledger/views.py` handling POST to /transactions/<id>/photos; validate and save photos, link to transaction, regenerate balance if needed
- [ ] T049 [US2] Add URL route in `ledger/urls.py` for GET `/transactions/<id>/` mapping to `transaction_detail` view
- [ ] T050 [US2] Add URL route in `ledger/urls.py` for POST `/transactions/<id>/photos` mapping to `add_transaction_photos` view
- [ ] T051 [P] [US2] Create transaction detail template `templates/ledger/transaction_detail.html` displaying transaction data, all attached photos with signed download links, and form to add more photos
- [ ] T052 [P] [US2] Create photo upload partial template `templates/ledger/_photo_upload_form.html` with file input, validation hints, preview-on-select using lightweight JavaScript or HTMX
- [ ] T053 [US2] Add signal handler in `ledger/models.py` to delete photos from S3 when InvoicePhoto is deleted (cascade delete handler)
- [ ] T054 [US2] Create view photo endpoint GET `/photos/<photo_id>` in `ledger/views.py` that generates and redirects to signed S3 URL with time-limited access (15 minutes)
- [ ] T055 [US2] Add URL route in `ledger/urls.py` for GET `/photos/<photo_id>/` mapping to signed URL redirect view
- [ ] T056 [US2] Add photo metadata display in transaction detail template showing original filename, file size, upload date, with edit/remove buttons (to be implemented in US3)

**Checkpoint**: User Story 2 is fully functional. Users can attach photos to transactions and retrieve them with secure signed URLs. Photos persist across edits and refreshes.

---

## Phase 5: User Story 3 - Ledger Review & Balance Tracking (Priority: P3)

**Goal**: Users can review transaction history with running balances, identify recent entries, confirm accuracy, and understand financial flow. Users can edit or delete transactions with balance recalculation.

**Independent Test**: A user can view the ledger with multiple transactions, verify the balance matches the sum of deposits minus payments, edit a transaction and see balance recalculate, delete a transaction and see balance update correctly.

### Tests for User Story 3 (TDD - write FAIL tests first) ⚠️

- [ ] T057 [P] [US3] Unit test for balance recalculation after edit in `ledger/tests/test_models.py`: edit a middle transaction amount, verify balance_after recalculated for that transaction and all subsequent ones
- [ ] T058 [P] [US3] Unit test for balance recalculation after delete in `ledger/tests/test_models.py`: delete a transaction, verify balance_after recalculated for all subsequent transactions, verify no gaps in sequence
- [ ] T059 [US3] Integration test for edit transaction in `ledger/tests/test_views.py`: GET /transactions/<id>/edit returns form with pre-filled data, POST /transactions/<id> updates transaction and recalculates balance
- [ ] T060 [US3] Integration test for delete transaction in `ledger/tests/test_views.py`: POST /transactions/<id>/delete removes transaction, recalculates balance for remaining transactions, redirects to ledger
- [ ] T061 [US3] Integration test for ledger report view in `ledger/tests/test_views.py`: GET /report displays transaction history sorted by date, shows running balance, summary stats (total deposits, total payments, final balance)

### Implementation for User Story 3

- [ ] T062 [P] [US3] Create transaction edit view `edit_transaction` in `ledger/views.py` handling GET (render form with pre-filled data) and POST (update transaction, recalculate balance, redirect)
- [ ] T063 [P] [US3] Create transaction delete view `delete_transaction` in `ledger/views.py` handling POST (delete transaction, recalculate balance, redirect to ledger with success message)
- [ ] T064 [US3] Create ledger report view `ledger_report` in `ledger/views.py` querying all transactions ordered by date, calculating summary stats (total deposits, total payments, final balance, transaction count), rendering report template
- [ ] T065 [US3] Add URL route in `ledger/urls.py` for GET `/transactions/<id>/edit` mapping to `edit_transaction` view (GET only for form display)
- [ ] T066 [US3] Add URL route in `ledger/urls.py` for POST `/transactions/<id>/edit` or enhanced POST `/transactions/<id>` for edit submission
- [ ] T067 [US3] Add URL route in `ledger/urls.py` for POST `/transactions/<id>/delete` mapping to `delete_transaction` view
- [ ] T068 [US3] Add URL route in `ledger/urls.py` for GET `/report/` mapping to `ledger_report` view
- [ ] T069 [P] [US3] Create edit transaction template `templates/ledger/edit_transaction.html` with form pre-filled with existing data, including photos section showing current attachments with remove options
- [ ] T070 [P] [US3] Create delete confirmation template `templates/ledger/delete_transaction.html` with warning message, transaction summary, and delete/cancel buttons
- [ ] T071 [P] [US3] Create ledger report template `templates/ledger/ledger_report.html` displaying transaction history table with date/type/amount/balance columns, summary panel with stats, export-to-CSV link (placeholder for future)
- [ ] T072 [US3] Enhance transaction list template `templates/ledger/index.html` with edit/view/delete action buttons for each transaction, link to full ledger report view
- [ ] T073 [US3] Add transaction validation in edit view to prevent editing transactions with future dates, ensure amount stays > 0
- [ ] T074 [US3] Add confirmation message/flash to ledger view after successful edit or delete showing which transaction was modified and new balance
- [ ] T075 [US3] Create summary card partial template `templates/ledger/_balance_summary.html` displaying current balance (largest number), total deposits, total payments, transaction count for reuse in index and report
- [ ] T076 [US3] Add logging in `ledger/models.py` signal handlers to log transaction creation/update/delete events for audit trail

**Checkpoint**: User Story 3 is fully functional. Users can review, edit, and delete transactions with accurate balance recalculation. The ledger report provides complete financial overview.

---

## Phase 6: User Story 4 - Recurring Transactions & Localization (Priority: P4)

**Goal**: Users can define recurring transactions (daily, weekly, monthly) that generate instances automatically. When editing a generated instance, users choose to update only that occurrence or the recurring rule affecting all future instances.

**Independent Test**: A user can create a recurring monthly transaction rule, verify it generates instances on schedule, edit a generated instance (choosing "update rule"), and verify all future instances update. Then edit another instance choosing "update only this", verify only that instance changes.

### Tests for User Story 4 (TDD - write FAIL tests first) ⚠️

- [ ] T077 [P] [US4] Unit test for RecurringProfile model in `ledger/tests/test_models.py`: verify fields (rule_type, amount, account, start_date, rrule, timezone), timezone-aware calculations, next_run_date() method
- [ ] T078 [P] [US4] Unit test for recurring task runner in `ledger/tests/test_recurring.py`: generate monthly recurring transactions, verify Transaction instances created with correct dates, amounts, and types, verify no duplicates on re-run
- [ ] T079 [P] [US4] Unit test for edit-single-vs-edit-rule logic in `ledger/tests/test_services.py`: verify `apply_transaction_edit()` with update_mode='this_only' updates single transaction; update_mode='all_future' updates rule and regenerates future instances
- [ ] T080 [US4] Integration test for create recurring profile in `ledger/tests/test_views.py`: POST /recurring/profiles with rule_type, amount, start_date; verify RecurringProfile created, redirect to recurring list
- [ ] T081 [US4] Integration test for recurring task scheduler in `ledger/tests/test_views.py`: call recurring task runner, verify Transaction instances created for current period, verify user can see them in ledger as normal transactions
- [ ] T082 [US4] Integration test for edit recurring instance with choice in `ledger/tests/test_views.py`: edit a generated recurring instance with update_mode='all_future', verify rule updated, verify all future instances regenerated with new amount

### Implementation for User Story 4

- [ ] T083 [P] [US4] Create RecurringProfile model in `ledger/models.py` with fields: rule_type (daily/weekly/monthly), amount, account, start_date, rrule (RFC-5545 string), timezone, is_active, created_at, updated_at; add next_run_date() method
- [ ] T084 [P] [US4] Create database migration in `ledger/migrations/` for RecurringProfile model with PostgreSQL date/timezone support
- [ ] T085 [P] [US4] Create recurring task scheduler in `ledger/management/commands/run_recurring.py` that finds active RecurringProfile rules, calculates next run dates in their timezone, generates Transaction instances in bulk, logs results
- [ ] T086 [US4] Create recurring transaction service in `ledger/services.py` with functions: `generate_recurring_instances(profile, date_range)`, `apply_transaction_edit(transaction_id, updated_fields, update_mode)` handling 'this_only' vs 'all_future'
- [ ] T087 [US4] Create RecurringProfileForm in `ledger/forms.py` with fields: rule_type (select: daily/weekly/monthly), amount (decimal), start_date (date), optional rrule (textarea for advanced), timezone (select), is_active (checkbox); validate amount > 0
- [ ] T088 [US4] Create recurring profile creation view `create_recurring_profile` in `ledger/views.py` handling GET (show form) and POST (create profile, redirect to recurring list or confirmation page)
- [ ] T089 [US4] Create recurring profiles list view `recurring_profiles` in `ledger/views.py` displaying all active/inactive profiles with next_run_date, action buttons (edit, deactivate, run now)
- [ ] T090 [US4] Create edit recurring profile view `edit_recurring_profile` in `ledger/views.py` allowing users to change rule parameters; save changes, regenerate future instances (warn user)
- [ ] T091 [US4] Create "run recurring now" action handler in `ledger/views.py` triggering immediate generation of due recurring instances for a profile (for testing/manual trigger)
- [ ] T092 [US4] Create recurring profile edit form override to show "Choose update mode" dialog when editing a generated recurring transaction instance: "Update only this transaction" vs "Update recurring rule (affects all future)"
- [ ] T093 [US4] Add URL routes in `ledger/urls.py`: GET/POST `/recurring/profiles` (list/create), GET/POST `/recurring/profiles/<id>/edit`, POST `/recurring/profiles/<id>/run-now`
- [ ] T094 [P] [US4] Create recurring profiles list template `templates/ledger/recurring_profiles.html` with table showing: rule_type, amount, next_run_date, is_active status, action buttons (edit, run-now, deactivate/activate)
- [ ] T095 [P] [US4] Create recurring profile form template `templates/ledger/create_recurring_profile.html` with fields: rule_type (select), amount (decimal), start_date (date), timezone (select), advanced rrule (textarea with help text), is_active checkbox
- [ ] T096 [P] [US4] Create edit-mode-choice partial template `templates/ledger/_recurring_edit_mode_choice.html` with radio buttons: "Update only this transaction" vs "Update recurring rule" with explanation text, form submit
- [ ] T097 [US4] Add URL route in `ledger/urls.py` for POST `/recurring/edit-instance/<transaction_id>` handling both update modes with modal/form submission
- [ ] T098 [US4] Create Celery task or scheduled job definition for recurring transaction runner: `ledger/tasks.py` or Heroku Scheduler config in `Procfile.dev`
- [ ] T099 [US4] Add signal handler in `ledger/models.py` to handle cascade behavior: when RecurringProfile is deleted, optionally delete generated future instances (user confirmation required)

**Checkpoint**: User Story 4 is fully functional. Users can define, manage, and run recurring transactions with choice-based edit semantics.

---

## Phase 7: Internationalization (i18n) & Polish

**Purpose**: Full localization support, language selector, and UI polish across all stories

- [ ] T100 [P] Create Spanish message catalog in `locale/es/LC_MESSAGES/django.po` with translations for all user-facing strings: form labels, error messages, page titles, button text from all views and templates
- [ ] T101 [P] Create English message catalog in `locale/en/LC_MESSAGES/django.po` with English translations for all messages (EN is secondary language, ES is default)
- [ ] T102 [P] Compile message catalogs: run `python manage.py compilemessages` in `locale/` to generate `.mo` files for both `es` and `en`
- [ ] T103 Wrap all user-facing strings in templates with `{% trans %}` or `{% blocktrans %}` tags; wrap strings in Python code with `_()` or `gettext_lazy()`
- [ ] T104 Create language selector form partial template `templates/ledger/_language_selector.html` with POST form to `/i18n/setlang/` with radio buttons for 'es' and 'en', include CSRF token
- [ ] T105 Create i18n endpoint view `set_language` in `ledger/views.py` handling POST `/i18n/setlang/` to set language in session and redirect to referer (or home if referer unavailable)
- [ ] T106 Add URL route in `ledger/urls.py` for POST `/i18n/setlang/` mapping to `set_language` view
- [ ] T107 Include language selector in base.html footer or header with current language highlighted, ensure it appears on all pages
- [ ] T108 Test i18n: verify Spanish strings display by default, verify language selector works and persists across navigation, verify English strings display after selecting EN
- [ ] T109 [P] Add validation error messages to forms with i18n: ensure validation errors appear in the active language, test with both ES and EN
- [ ] T110 [P] Add accessibility enhancements: add aria-labels to form inputs, add role="alert" to error messages, ensure focus management on form errors, verify keyboard tab order is logical
- [ ] T111 [P] Add mobile-responsive testing: verify all templates render correctly on iPhone 12 (390px) and iPad (768px) viewports, check button click areas are >= 44px, verify form inputs are not covered by keyboard on mobile
- [ ] T112 Create comprehensive unit test suite in `ledger/tests/test_models.py` covering all model validations, balance calculations, and edge cases
- [ ] T113 Create comprehensive form test suite in `ledger/tests/test_forms.py` covering all form validations, error messages, with English and Spanish locales
- [ ] T114 Create contract test suite in `ledger/tests/test_contracts.py` verifying all endpoints match contract specs: correct status codes, expected response fields, error responses
- [ ] T115 [P] Create pytest configuration for parallel test execution with `pytest-xdist` plugin; verify all tests pass in isolation and in parallel
- [ ] T116 Update README.md with: project overview, setup instructions (venv, pip, migrate, runserver), environment variables, Heroku deployment steps, test suite commands, troubleshooting section
- [ ] T117 Update quickstart.md with verified local setup commands, Heroku deployment checklist, and budget deployment options (Option A/B/C) with trade-offs
- [ ] T118 Create deployment checklist in `specs/001-personal-finance-bookkeeping/checklists/deployment.md`: confirm all env vars set, test migrations on Heroku, verify photos upload to S3, test language selector in production
- [ ] T119 [P] Add performance monitoring: log request latency for transaction list, photo upload, and report generation; verify p95 latency <= 300ms for ledger rendering with 1000+ transactions
- [ ] T120 Create security checklist in `specs/001-personal-finance-bookkeeping/checklists/security.md`: CSRF protection verified, SQL injection prevention, XSS prevention in templates, S3 signed URLs time-limited, password requirements for single user

---

## Phase 8: Cross-Cutting Concerns & Final Validation

**Purpose**: Improvements affecting multiple user stories, final QA, deployment preparation

- [ ] T121 [P] Add audit logging in `ledger/models.py`: log all create/update/delete events for Transaction and InvoicePhoto with timestamp, action, old/new values
- [ ] T122 [P] Create error handling views in `expense_tracker/views.py`: custom 404, 500 error pages with friendly messaging, include language selector so errors display in active language
- [ ] T123 [P] Add request/response logging middleware in `expense_tracker/settings.py`: log request method/path/status for debugging
- [ ] T124 Add database query optimization: add indexes on `transaction_date` and `created_at` in Transaction model, verify no N+1 queries in ledger view (use `select_related`/`prefetch_related` for photos)
- [ ] T125 [P] Create production checklist in `docs/DEPLOYMENT.md`: environment variables, health check endpoint, database backup strategy, S3 bucket retention policy, uptime monitoring recommendations
- [ ] T126 [P] Add static file optimization: verify WhiteNoise serves CSS/JS with correct cache headers, minify CSS, ensure Bootstrap CDN URLs are correct for offline-fallback
- [ ] T127 Create end-to-end test scenario in `ledger/tests/test_e2e.py`: user creates transaction -> adds photo -> edits transaction -> creates recurring profile -> reviews ledger report; verify all data persists
- [ ] T128 Run full test suite and generate coverage report: target >= 80% coverage on models.py, services.py, forms.py, views.py; document any exclusions
- [ ] T129 Create local environment setup validation script in `.specify/scripts/bash/validate-local.sh`: check Python version, Django version, run migrations, create test user, run pytest, confirm all checks pass
- [ ] T130 [P] Manual QA checklist: test create/edit/delete on desktop (Chrome, Safari), mobile (iPhone Safari), tablet (iPad Chrome); verify form submission, photo upload, language switching, balance recalculation work correctly
- [ ] T131 [P] Create user documentation in `docs/USER_GUIDE.md`: how to add a transaction, how to attach a photo, how to edit/delete, how to review ledger, how to set language, FAQ for common issues
- [ ] T132 Run Heroku Scheduler test for recurring task: deploy to Heroku, configure scheduler to run `run_recurring` command every 10 minutes, verify Transaction instances are generated, verify balance is correct
- [ ] T133 Create backup and recovery documentation in `docs/BACKUP.md`: database backup strategy, photo retention policy, restore procedures, disaster recovery plan
- [ ] T134 Add analytics placeholder comments: identify key user journeys to measure (transaction creation, photo upload success rate, report views) for future instrumentation
- [ ] T135 Verify final deployment: confirm app runs on Heroku Dyno Basic, confirm total monthly cost <= $11, confirm Spanish is default language, confirm all features work end-to-end on production, document cost breakdown

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup (Phase 1)**: No dependencies - can start immediately
2. **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
3. **User Story 1 (Phase 3)**: Depends on Foundational completion - No dependencies on other stories
4. **User Story 2 (Phase 4)**: Depends on Foundational completion - Can integrate with US1 but independently testable
5. **User Story 3 (Phase 5)**: Depends on Foundational completion - May integrate with US1/US2 but independently testable
6. **User Story 4 (Phase 6)**: Depends on Foundational completion - Independently testable but can leverage US1-US3 components
7. **i18n & Polish (Phase 7)**: Depends on at least Phase 3 (US1) being functional
8. **Cross-Cutting & Final Validation (Phase 8)**: Depends on all feature phases being complete

### Parallel Opportunities Within Phases

#### Phase 1 Setup - Parallel Tasks
```
T001 (Procfile/runtime.txt)
T003 (locale directories) [P]
T004 (S3 storage backend) [P]
T007 (base.html) [P]
T008 (CSS styling) [P]

Can all run in parallel - independent file creation
```

#### Phase 2 Foundational - Parallel Tasks
```
T011 (Transaction model) [P]
T012 (InvoicePhoto model) [P]
T014 (TransactionForm) [P]
T015 (balance recalculation service) [P]
T016 (photo validation service) [P]
T017 (S3 upload service) [P]
T021 (test fixtures/factories) [P]
T022 (authentication middleware) [P]

Models can run in parallel with each other
Services can run in parallel with each other
Form and fixtures can run in parallel
Middleware can run in parallel
All depend on: T005, T006, T020 (settings config)
```

#### Phase 3 US1 - Parallel Tasks
```
T024-T026 (model/form tests) [P]
T029 (create view) [P]
T030 (list view) [P]
T031 (form template) [P]
T035 (list template) [P]
T036 (form enhancements) [P]

Can write all tests in parallel (failing)
Can implement all views/templates in parallel
All depend on: Phase 2 completion
```

#### Phase 4 US2 - Parallel Tasks
```
T039-T041 (InvoicePhoto tests) [P]
T045 (PhotoForm) [P]
T047 (detail view) [P]
T051 (detail template) [P]
T052 (photo upload partial) [P]

Tests and implementation can proceed in parallel
All depend on: Phase 2 + Phase 3 (US1) completion
```

#### Phase 7 i18n - Parallel Tasks
```
T100 (Spanish catalog) [P]
T101 (English catalog) [P]
T109 (form i18n) [P]
T110 (accessibility) [P]
T111 (mobile testing) [P]
T115 (parallel test config) [P]

All independent file/config modifications
All depend on: at least Phase 3 completion
```

#### Phase 8 Cross-Cutting - Parallel Tasks
```
T121 (audit logging) [P]
T122 (error pages) [P]
T123 (request logging) [P]
T126 (static optimization) [P]
T130 (manual QA) [P]
T131 (user docs) [P]

All independent implementations
All depend on: Phases 1-7 complete
```

### Team Parallelization Example

**If 3 developers available after Foundational phase:**
- Developer A: Complete Phase 3 (US1) → Phase 5 (US3)
- Developer B: Complete Phase 4 (US2) 
- Developer C: Complete Phase 6 (US4)
- All together: Phase 7 (i18n), Phase 8 (final validation)

**Sequential Example (single developer):**
1. Complete Phase 1 (Setup)
2. Complete Phase 2 (Foundational)
3. Complete Phase 3 (US1) → **STOP and VALIDATE** ✓
4. Complete Phase 4 (US2) → **STOP and VALIDATE** ✓
5. Complete Phase 5 (US3) → **STOP and VALIDATE** ✓
6. Complete Phase 6 (US4) → **STOP and VALIDATE** ✓
7. Complete Phase 7 (i18n)
8. Complete Phase 8 (final validation)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Goal**: Deliver minimum viable product in shortest time

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T023) - **CRITICAL GATE**
3. Complete Phase 3: User Story 1 (T024-T038)
4. **STOP and VALIDATE**: Verify Transaction creation, list, and balance work end-to-end
5. **DEPLOY**: Deploy to Heroku, confirm no errors
6. **Result**: MVP complete - users can manually record transactions

### Incremental Delivery (All User Stories)

1. **Iteration 1**: Setup + Foundational + US1 (Phases 1-3)
   - Deploy to Heroku as MVP
   - Validate with users
   - Get feedback

2. **Iteration 2**: Add Phase 4 (US2 - Photo Attachment)
   - Build on MVP
   - Add photo upload capability
   - Deploy incremental improvement

3. **Iteration 3**: Add Phase 5 (US3 - Ledger Review)
   - Build editing/deletion capability
   - Add balance verification UI
   - Deploy enhanced version

4. **Iteration 4**: Add Phase 6 (US4 - Recurring)
   - Add recurring transaction management
   - Deploy final feature set

5. **Final**: Phase 7-8 (i18n, Polish, Final Validation)
   - Add Spanish localization (required by FR-015)
   - Polish UI/UX
   - Performance optimization
   - Final QA and deployment

### Testing Strategy

**Unit Tests (TDD)**: Write test FIRST (should FAIL), then implement to make pass
- Models: validation, calculation logic
- Services: business logic isolation
- Forms: validation, error messages

**Integration Tests**: Test feature workflows end-to-end
- Create transaction flow (US1)
- Photo upload flow (US2)
- Edit/delete recalculation (US3)
- Recurring generation (US4)

**Contract Tests**: Verify API responses match specs
- Status codes (200, 302, 400, 404, 500)
- Response content/structure
- Form submission and validation

**E2E Tests**: Manual QA on desktop, tablet, mobile
- Form submission accessibility
- Photo upload end-to-end
- Language switching
- Balance calculation verification

---

## Success Criteria by Phase

### Phase 1 Success
- All Heroku config files present (Procfile, runtime.txt)
- All dependencies in requirements.txt
- Project structure matches plan.md
- Django app boots without errors

### Phase 2 Success
- All models migrate without errors
- All services tested in isolation
- Authentication middleware protects all ledger views
- Forms validate correctly in both languages

### Phase 3 Success ✓ **MVP GATE**
- User can create transaction manually
- Transaction appears in list with correct data
- Balance is calculated and displayed
- All tests pass
- Form preserves data on validation error
- Works on mobile viewport

### Phase 4 Success
- User can attach photo during transaction creation
- Photo persists and is viewable in transaction detail
- Photo can be replaced or removed
- Photos are stored in S3 with signed URLs
- All tests pass

### Phase 5 Success
- User can edit existing transaction
- User can delete transaction
- Balance recalculates correctly after edit/delete
- Ledger report shows accurate history and summary
- All tests pass

### Phase 6 Success
- User can create recurring profile
- Scheduled task generates Transaction instances correctly
- User can edit generated instance with choice (this-only vs all-future)
- Recurring profiles manage state correctly
- All tests pass

### Phase 7 Success
- Spanish is default language
- Language selector works on all pages
- All strings translated to EN/ES
- WCAG 2.1 AA compliance verified
- Mobile layout tested and responsive

### Phase 8 Success
- All tests pass (>80% coverage)
- Manual QA checklist completed
- Heroku deployment works
- Monthly cost confirmed <= $11
- Documentation complete
- Backup/recovery procedures documented

---

## Notes & Best Practices

1. **Each [P] task can run in parallel** - different files, no blocking dependencies
2. **Each [Story] task maps to specific user story** - enables traceability and independent delivery
3. **Tests FIRST** - write failing tests before implementing features (TDD)
4. **Commit after each task** - creates clear history and enables rollback
5. **Validate at checkpoints** - stop after each phase to confirm independent functionality
6. **File paths are exact** - copy/paste them into create commands
7. **Template format STRICT** - ensure all tasks follow `- [ ] [ID] [P?] [Story?] Description filepath`
8. **Stop at MVP (Phase 3)** - Phase 3 completion = deployable product; other phases add value incrementally
9. **Avoid: vague descriptions, untraceable dependencies, cross-story blocking**
10. **Database migrations REQUIRED** - run after model changes before testing

---

**TOTAL TASKS**: 135  
**MVP SCOPE** (Phases 1-3): 38 tasks  
**FULL SCOPE** (Phases 1-8): 135 tasks  
**ESTIMATED TIME** (single developer): 4-6 weeks MVP, 8-12 weeks full feature

**Next Step**: Start Phase 1 (Setup) - no dependencies, can begin immediately.