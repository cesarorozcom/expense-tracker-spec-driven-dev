# Implementation Plan: Personal Finance Bookkeeping

**Branch**: `[001-personal-finance-bookkeeping]` | **Date**: 2026-05-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `spec.md`

## Summary

Build a Heroku-deployable personal bookkeeping web app that lets a single user record deposits and payments either through a manual form or by attaching invoice photos, then review the transaction history and running balance. The implementation favors a maintainable monolith: Django for server-rendered pages and forms, PostgreSQL for transactional data, S3-compatible storage for photo uploads, and HTMX for small progressive-enhancement interactions without a separate frontend build.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django 5, PostgreSQL, gunicorn, WhiteNoise, django-storages, boto3, HTMX

**Storage**: PostgreSQL for transactions and metadata; S3-compatible object storage for invoice photos

**Testing**: pytest, pytest-django, factory_boy

**Target Platform**: Heroku Dyno Basic with Heroku Postgres and S3-compatible object storage; mobile phone browsers as a primary client target

## Budget Constraints (monthly budget: 11 USD)

The feature must be deliverable and maintainable under a hard hosting budget of $11 per month. The target deployment is Heroku Dyno Basic, paired with the lowest-cost database and storage options that keep the monthly total at or below budget. Update the `quickstart.md` and deployment checklist accordingly.

Recommended deployment approach:

- Use Heroku Dyno Basic for the web process.
- Use the smallest viable Heroku Postgres plan or an equivalent low-cost managed PostgreSQL service.
- Use S3-compatible object storage only if the photo storage cost remains within budget; otherwise, reduce photo retention or move to a low-cost backup-oriented storage plan with documented trade-offs.

If the monthly total exceeds $11, choose one of the following fallback options (ordered by preference and cost-effectiveness):

- Option A — Minimal managed stack:
	- Keep Heroku Dyno Basic for the web process.
	- Use a small managed or self-hosted Postgres instance (or hosted Postgres shared plan) that fits the budget; if managed Postgres is unavailable within budget, use a local file-backed SQLite database with a documented backup strategy for production (backup to object storage).
	- For invoice photos, prefer an S3-compatible object store with a free or low-cost tier. If external object storage would exceed the budget, store photos on the dyno filesystem only with clear documentation of the ephemeral risk and an automated backup/retention job to offsite storage.

- Option B — Ultra-minimal single-host deployment (lowest-cost tradeoff):
	- Run Django + SQLite on a single low-cost VM and store photos on the same host; enable periodic offsite backups (compressed, encrypted) to a low-cost object storage bucket. This reduces monthly service costs but increases operational responsibility and risk due to single-host failure.

- Option C — Managed services with strict quotas (if available):
	- Use the smallest managed Postgres plan plus provider object storage if a provider offers a combined plan that fits under $11/month. This preserves durability at modest cost but depends on provider offerings.

Trade-offs and implementation notes:
- Durability: Option A/C preserve higher durability; Option B increases risk and requires solid backup automation.
- Scalability: All options limit scale; document expected limits (e.g., thousands of transactions, small photo retention) and include a migration path to managed DB/storage when budget allows.
- Performance: Adjust performance goals for the constrained environment (e.g., accept slightly higher p95 for large ledgers) and ensure tests reflect the chosen deployment profile.

Action required: select one option and update `quickstart.md` with concrete deployment commands and environment variable guidance for the chosen hosting approach.

**Project Type**: web app

**Performance Goals**: Save and render common transaction flows in under 300 ms p95 for normal ledger sizes; support ledger views for thousands of transactions without noticeable delay; accept image uploads up to the configured limit without blocking the request lifecycle longer than necessary

**Constraints**: Heroku uses an ephemeral filesystem, so invoice photos must live outside the dyno; configuration must be environment-driven; the first release is single-user and single-currency; the UI must remain simple enough to maintain without a separate frontend application; the interface must be responsive and touch-friendly on mobile phone screens

**Scale/Scope**: Single-user personal ledger with deposits, payments, running balances, and invoice photos; expected to handle thousands of transactions and multiple photos per transaction

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Code quality gate: pass. The plan uses a clear module boundary, testable components, and a small set of dependencies.
- Modularity gate: pass. Django apps will isolate transaction logic, balance calculation, and upload handling.
- Testing gate: pass. The plan includes unit, integration, and contract coverage for the critical flows.
- UX consistency gate: pass. A single server-rendered UI with shared templates and form validation keeps interaction patterns consistent.
- Mobile compatibility gate: pass. The responsive template approach and shared form components are designed to work on common mobile phone viewports.
- Deployability/performance gate: pass. Heroku deployment, Postgres, object storage, and gunicorn/WhiteNoise keep the release path simple and repeatable.

## Project Structure

### Documentation (this feature)

```text
specs/001-personal-finance-bookkeeping/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── spec.md
```

### Source Code (repository root)

```text
Procfile
runtime.txt
requirements.txt
manage.py
src/
├── config/
├── ledger/
├── transactions/
├── templates/
└── static/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Use a single Django monolith with a `src/` layout and server-rendered templates. This keeps deployment simple on Heroku, avoids a second frontend build, and makes the bookkeeping workflow easier to maintain because the form handling, balance logic, and photo upload flow live in one deployable application.

## Complexity Tracking

No constitution violations require justification for this feature. The design intentionally stays within one deployable web application, one database, and one external object store for photos.

## Specification Updates and Clarifications (2026-05-16)

To resolve ambiguities discovered during analysis and to make the implementation plan actionable, the following clarifications and requirements are adopted for the initial implementation (v1):

- OCR / Data Extraction: OUT OF SCOPE for v1. The system MUST store invoice photos as supporting evidence and may offer manual pre-fill UI for users to enter parsed values; automatic OCR/extraction MAY be added in a later iteration and must be introduced via a separate RFC. Update: `FR-006` is interpreted as "photo storage and optional manual entry; OCR deferred".

- Recurring / Periodic Transactions: The system MUST support defining recurring transactions as first-class rules. Required sub-requirements:
	- Recurrence rules: support simple recurrence types (daily, weekly, monthly) and an optional RFC-5545-style `RRULE` string for advanced users.
	- Storage: persist a `RecurringRule` record separate from generated `Transaction` instances.
	- Generation semantics: recurring instances SHOULD be materialized only when a scheduled run occurs or when the user explicitly "Generate now"; the ledger view will show generated instances as normal `Transaction` records.
	- Edit semantics: editing a generated instance MUST offer the user a choice to update only that occurrence or update the underlying `RecurringRule` (affecting future generated instances). Deleting a rule MUST optionally delete generated future instances but MUST NOT automatically delete historical generated transactions without explicit user confirmation.
	- Timezones: recurrence rules MUST be defined with timezone-aware semantics; storage uses UTC timestamps and the rule stores the originating timezone for display and next-run calculations.

- Photo Failure Modes and Validation:
	- File types: accept `image/jpeg`, `image/png`, `image/webp`.
	- File size: server-enforced default limit 10 MiB per file (configurable via environment variable).
	- Upload UX: if an uploaded photo is corrupted/unreadable, the system SHOULD allow saving the transaction while flagging the photo as "unverified" and offer retry/remove options; the system MUST NOT silently discard user uploads.
	- Replace/remove: users MUST be able to replace or remove photos from a saved transaction; replacing a photo preserves other metadata and recalculation behavior.

- Photo Storage & Privacy:
	- Storage: invoice photos MUST be stored in S3-compatible object storage; only metadata is stored in Postgres.
	- Encryption: object storage MUST enforce encryption-at-rest; access to objects MUST be via short-lived signed URLs (pre-signed) for direct client download/upload flows.
	- Retention: retention policy MUST be configurable; default retention for v1: 2 years, with a configurable override via environment variables.

- Security & Access:
	- Single-user scope: v1 remains single-user, but the app MUST use Django's authentication to protect access to the ledger and attachments.
	- Signed uploads: prefer direct-to-S3 signed upload flows to avoid server-side buffering of large files; when proxy-upload is used, ensure request body limits and streaming.

- Accessibility (FR-013):
	- The UI MUST satisfy WCAG 2.1 AA for primary flows: form labels, error messages, keyboard navigation, focus management, and color contrast (4.5:1 for normal text).
	- Forms: every input MUST include an associated label; validation errors MUST be reachable by screen readers.

- Performance Targets (mapped to acceptance):
	- Ledger render: p95 latency <= 300 ms for a typical ledger page rendering up to 1000 transactions on reasonable infra.
	- Image upload end-to-end (direct-to-S3): p95 <= 2s on a broadband connection; server-proxied uploads excluded from this target and MUST be measured separately.

These clarifications will be reflected in updated specification documents and acceptance tests.
