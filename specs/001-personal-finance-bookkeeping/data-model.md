# Data Model: Personal Finance Bookkeeping

## Entity: Transaction

Represents one recorded financial event in the user's personal ledger.

### Fields

- `id`: unique identifier
- `transaction_type`: enum, either `deposit` or `payment`
- `amount`: decimal value greater than zero
- `transaction_date`: date the transaction occurred or was recorded
- `note`: optional free-text note
- `running_balance_after`: decimal snapshot of the balance immediately after this transaction is applied
- `created_at`: timestamp when the record was created
- `updated_at`: timestamp when the record was last updated

### Validation Rules

- `transaction_type` is required.
- `amount` is required and must be positive.
- `transaction_date` is required.
- `running_balance_after` is system-managed and recalculated whenever the ledger changes.
- Deleting or editing a transaction triggers a recalculation of subsequent balance snapshots.

### Relationships

- One `Transaction` can have zero or many `InvoicePhoto` records.
- A transaction belongs to the single-user ledger for the application.

## Entity: InvoicePhoto

Represents an uploaded image of a receipt or invoice attached to a transaction.

### Fields

- `id`: unique identifier
- `transaction_id`: foreign key to `Transaction`
- `file`: uploaded image asset stored in object storage
- `original_filename`: original uploaded filename for display and debugging
- `content_type`: optional MIME type metadata
- `file_size_bytes`: optional size metadata
- `uploaded_at`: timestamp when the file was stored

### Validation Rules

- `transaction_id` is required.
- Files must be valid image uploads.
- File size and type limits are enforced by form validation.
- When a transaction is deleted, its attached photos are removed or dereferenced according to the storage adapter's delete behavior.

### Relationships

- Each `InvoicePhoto` belongs to one `Transaction`.

## Derived Concept: Ledger

Represents the ordered view of all saved transactions and their running balance.

### Rules

- The ledger is derived from `Transaction` records; it is not treated as a separate persisted table in the first version.
- Ordering uses transaction date and stable secondary ordering so the running balance is deterministic.
- The ledger must always reflect the latest saved state after create, edit, or delete actions.

## State Transitions

- `Transaction` lifecycle: created -> updated -> deleted.
- `InvoicePhoto` lifecycle: uploaded -> attached to transaction -> deleted with transaction or removed independently if editing flow supports it later.
