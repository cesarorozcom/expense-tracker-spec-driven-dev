# Tasks: Personal Finance Bookkeeping

**Input**: Design documents from `specs/001-personal-finance-bookkeeping/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/web-interface.md

**Tests**: Included because the plan and constitution require coverage for core logic, integration, and contract flows.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g. US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and baseline Django scaffolding

- [ ] T001 Create the Django project skeleton and app directories in `src/config/`, `src/ledger/`, and `src/transactions/`
- [ ] T002 Initialize Python dependencies for Django, Postgres, gunicorn, WhiteNoise, django-storages, boto3, pytest, pytest-django, and factory_boy in `requirements.txt`
- [ ] T003 Configure project runtime files for Heroku deployment in `Procfile` and `runtime.txt`
- [ ] T004 [P] Add repository-level linting and formatting configuration in `pyproject.toml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that must exist before any user story work begins

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

- [ ] T005 Create Django settings, URL routing, ASGI, and WSGI entrypoints in `src/config/settings.py`, `src/config/urls.py`, `src/config/asgi.py`, and `src/config/wsgi.py`
- [ ] T006 [P] Configure environment-driven database, secret key, allowed hosts, and debug settings in `src/config/settings.py`
- [ ] T007 [P] Configure static files and WhiteNoise support in `src/config/settings.py`
- [ ] T008 [P] Configure storage backends and signed-object URL settings for invoice photos in `src/config/settings.py`
- [ ] T009 Define the core ledger models and migrations for `Transaction` and `InvoicePhoto` in `src/transactions/models.py` and `src/transactions/migrations/`
- [ ] T010 Define the transaction validation and balance recalculation service in `src/transactions/services.py`
- [ ] T011 [P] Add the base authenticated layout and form error shell templates in `src/templates/base.html` and `src/templates/includes/`
- [ ] T012 Configure test support factories and shared test fixtures in `tests/conftest.py` and `tests/factories/`

---

## Phase 3: User Story 1 - Record Transactions Manually (Priority: P1) 🎯 MVP

**Goal**: A user can create a deposit or payment manually, save it, and see it in the ledger with the correct balance impact.

**Independent Test**: A user can submit the manual transaction form with valid data and see the new transaction appear in the ledger with the running balance updated.

### Tests for User Story 1

- [ ] T013 [P] [US1] Add contract tests for transaction creation and validation in `tests/contract/test_transactions_contract.py`
- [ ] T014 [P] [US1] Add integration tests for manual transaction creation and balance updates in `tests/integration/test_manual_transaction_flow.py`

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement the manual transaction form and field validation in `src/transactions/forms.py`
- [ ] T016 [US1] Implement create transaction view and POST handler in `src/transactions/views.py`
- [ ] T017 [US1] Add the transaction creation and success templates in `src/templates/transactions/new.html` and `src/templates/transactions/create_success.html`
- [ ] T018 [US1] Wire the manual entry route in `src/config/urls.py`
- [ ] T019 [US1] Persist transaction records and recompute running balances in `src/transactions/services.py`
- [ ] T020 [P] [US1] Add transaction list rendering with date, type, amount, and balance impact in `src/templates/ledger/index.html`

**Checkpoint**: User Story 1 should be fully functional and independently testable.

---

## Phase 4: User Story 2 - Capture Invoice Photos (Priority: P2)

**Goal**: A user can attach one or more invoice photos to a transaction, save them, and reopen the transaction with the photos preserved.

**Independent Test**: A user can upload a photo to a transaction, refresh the page, and still see the same photo attached to the saved entry.

### Tests for User Story 2

- [ ] T021 [P] [US2] Add contract tests for photo attachment upload and retrieval in `tests/contract/test_photo_contract.py`
- [ ] T022 [P] [US2] Add integration tests for attaching, replacing, and viewing photos in `tests/integration/test_photo_attachment_flow.py`

### Implementation for User Story 2

- [ ] T023 [P] [US2] Add photo attachment validation and upload form fields in `src/transactions/forms.py`
- [ ] T024 [US2] Implement invoice photo attachment and replacement handling in `src/transactions/views.py`
- [ ] T025 [US2] Implement photo storage adapter integration and signed URL generation in `src/transactions/storage.py`
- [ ] T026 [US2] Update transaction detail view to show attached photos in `src/templates/transactions/detail.html`
- [ ] T027 [US2] Add photo upload controls and error messages in `src/templates/transactions/detail.html` and `src/templates/transactions/edit.html`
- [ ] T028 [US2] Persist invoice photo metadata and cleanup behavior in `src/transactions/models.py` and `src/transactions/services.py`

**Checkpoint**: User Story 2 should be fully functional and independently testable.

---

## Phase 5: User Story 3 - Review Balances and History (Priority: P3)

**Goal**: A user can review the transaction history and current running balance to confirm their records are accurate and up to date.

**Independent Test**: A user can open the ledger view and verify the saved entries are shown in chronological order with the correct running balance.

### Tests for User Story 3

- [ ] T029 [P] [US3] Add contract tests for the ledger overview and transaction detail pages in `tests/contract/test_ledger_contract.py`
- [ ] T030 [P] [US3] Add integration tests for ledger ordering, edit/delete recalculation, and detail review in `tests/integration/test_ledger_review_flow.py`

### Implementation for User Story 3

- [ ] T031 [P] [US3] Implement the ledger overview query and ordering logic in `src/ledger/services.py`
- [ ] T032 [US3] Implement the ledger overview and transaction detail views in `src/ledger/views.py`
- [ ] T033 [US3] Add the ledger overview and transaction detail templates in `src/templates/ledger/index.html` and `src/templates/transactions/detail.html`
- [ ] T034 [US3] Wire the ledger routes in `src/config/urls.py`
- [ ] T035 [US3] Implement transaction edit and delete flows with balance recalculation in `src/transactions/views.py` and `src/transactions/services.py`
- [ ] T036 [P] [US3] Add responsive mobile layout and balance summary styling in `src/static/css/app.css`

**Checkpoint**: User Stories 1, 2, and 3 should now be independently functional.

---

## Phase 6: User Story 4 - Manage Recurring Transactions (Priority: P4)

**Goal**: A user can define recurring transactions, generate future instances, and edit or stop the schedule without losing historical records.

**Independent Test**: A user can create a recurring rule, generate a transaction instance, and verify that future instances follow the saved recurrence settings.

### Tests for User Story 4

- [ ] T037 [P] [US4] Add contract tests for recurring-rule creation and generation in `tests/contract/test_recurring_contract.py`
- [ ] T038 [P] [US4] Add integration tests for recurring transaction generation and edit semantics in `tests/integration/test_recurring_transactions_flow.py`

### Implementation for User Story 4

- [ ] T039 [P] [US4] Add the recurring rule model and migrations in `src/transactions/models.py` and `src/transactions/migrations/`
- [ ] T040 [US4] Implement recurrence parsing, timezone handling, and next-run calculation in `src/transactions/recurrence.py`
- [ ] T041 [US4] Implement recurring rule create/update views in `src/transactions/views.py`
- [ ] T042 [US4] Add recurring rule forms and validation in `src/transactions/forms.py`
- [ ] T043 [US4] Add recurring rule templates and controls in `src/templates/transactions/recurring.html`
- [ ] T044 [US4] Implement scheduled generation support and explicit "Generate now" behavior in `src/transactions/services.py`

**Checkpoint**: Recurring transaction support should be independently functional without breaking existing stories.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T045 [P] Improve accessibility labels, focus states, and error summaries across templates in `src/templates/`
- [ ] T046 [P] Add performance checks and query optimizations for large ledgers in `src/ledger/services.py`
- [ ] T047 Tighten security-related settings and signed upload defaults in `src/config/settings.py`
- [ ] T048 [P] Update quickstart and deployment notes for Heroku Dyno Basic in `specs/001-personal-finance-bookkeeping/quickstart.md` and `specs/001-personal-finance-bookkeeping/plan.md`
- [ ] T049 [P] Add final documentation cleanup in `specs/001-personal-finance-bookkeeping/`
- [ ] T050 Validate the end-to-end quickstart steps and deployment path in `specs/001-personal-finance-bookkeeping/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational completion
- **Polish (Final Phase)**: Depends on the desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - no dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - may integrate with US1 but remains independently testable
- **User Story 3 (P3)**: Can start after Foundational - may integrate with US1/US2 but remains independently testable
- **User Story 4 (P4)**: Can start after Foundational - may integrate with earlier stories but remains independently testable

### Within Each User Story

- Tests are written first and should fail before implementation
- Forms/models before views/templates
- Services before endpoints or schedule-driven behavior
- Core implementation before integration polish
- Story complete before moving to the next priority

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel
- Foundational tasks marked [P] can run in parallel once setup is done
- Different user stories can be worked on in parallel after foundation is ready
- Test tasks marked [P] can run in parallel within a story
- Model and template work marked [P] can run in parallel when they touch different files

---

## Parallel Example: User Story 1

```bash
# Launch the User Story 1 tests together:
Task: "Add contract tests for transaction creation and validation in tests/contract/test_transactions_contract.py"
Task: "Add integration tests for manual transaction creation and balance updates in tests/integration/test_manual_transaction_flow.py"

# Launch the User Story 1 implementation files together:
Task: "Implement the manual transaction form and field validation in src/transactions/forms.py"
Task: "Implement transaction list rendering with date, type, amount, and balance impact in src/templates/ledger/index.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate the manual transaction flow independently
5. Demo or deploy if ready

### Incremental Delivery

1. Complete Setup + Foundational
2. Add User Story 1 and validate it
3. Add User Story 2 and validate it
4. Add User Story 3 and validate it
5. Add User Story 4 and validate recurring transactions separately
6. Finish with polish and cross-cutting improvements

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. After foundation is complete:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Each story is validated independently before integration

---

## Extension Hooks

**Optional Pre-Hook**: git
Command: `/speckit.git.commit`
Description: Auto-commit before task generation

Prompt: Commit outstanding changes before task generation?
To execute: `/speckit.git.commit`
