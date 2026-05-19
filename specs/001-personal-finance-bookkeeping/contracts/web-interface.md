# Web Interface Contract: Personal Finance Bookkeeping

This feature uses server-rendered HTML forms and pages rather than a public JSON API.

## Pages and Routes

### GET `/`

- Purpose: Show the ledger overview with the current running balance and recent transactions.
- Response: HTML page with balance summary and transaction list.

### GET `/transactions/new`

- Purpose: Show the manual transaction form.
- Response: HTML page with empty form fields and validation hints.

### POST `/transactions`

- Purpose: Create a new transaction.
- Form fields:
  - `transaction_type`: `deposit` or `payment`
  - `amount`: positive decimal
  - `transaction_date`: required date
  - `note`: optional text
  - `invoice_photos[]`: zero or more image uploads
- Success response: Redirect to the ledger or transaction detail page.
- Validation failure: Re-render the form with inline errors and preserve entered values.

### GET `/transactions/<id>`

- Purpose: Show a saved transaction and any attached invoice photos.
- Response: HTML detail page.

### POST `/transactions/<id>`

- Purpose: Update an existing transaction.
- Form fields: same as create, with any edit-specific attachment controls.
- Success response: Redirect to the updated transaction or ledger.
- Validation failure: Re-render the edit form with errors.

### POST `/transactions/<id>/delete`

- Purpose: Remove a saved transaction.
- Success response: Redirect to the ledger with the balance recalculated.

### POST `/transactions/<id>/photos`

- Purpose: Attach additional invoice photos to an existing transaction.
- Form fields:
  - `invoice_photos[]`: image uploads
- Success response: Redirect to the transaction detail page.

### POST `/i18n/setlang/`

- Purpose: Switch the active application language for the current browser session.
- Form fields:
  - `language`: supported locale code, currently `es` or `en`
- Success response: Redirect back to the current page or the configured next URL with the selected locale active.
- Validation failure: Reject unsupported language codes and keep the existing locale active.

## Validation Rules

- `amount` must be greater than zero.
- `transaction_type` must be one of the supported ledger types.
- `transaction_date` is required.
- Photo uploads must be images and must respect the configured size limit.
- The UI must show validation feedback without losing user-entered form data.
- The default UI language must be Spanish unless the user explicitly selects another supported locale.
- The language switcher must only expose supported application locales.

## UX Expectations

- Deposit and payment actions must look consistent across create and edit forms.
- The ledger must always show the latest balance after a successful save.
- Upload errors must be visible and actionable.
