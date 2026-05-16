# Feature Specification: Personal Finance Bookkeeping

**Feature Branch**: `[001-personal-finance-bookkeeping]`

**Created**: 2026-05-15

**Status**: Draft

**Input**: User description: "Build an application that can help me register financial transaction to organize my personal finance. I want to register each transaction by taking a invoice photo, or enter manually using a form. This product looks like a personal bookkeeping to track deposits, payments, and balances."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record Transactions Manually (Priority: P1)

As a family managing personal finances, I want to enter a transaction manually so I can quickly record deposits and payments even when I do not have a receipt photo.

**Why this priority**: Manual entry is the most direct and reliable way to capture every transaction, so it establishes the core bookkeeping workflow.

**Independent Test**: A user can create a deposit or payment with the form, save it, and see it appear in the transaction list with the correct balance impact.

**Acceptance Scenarios**:

1. **Given** an empty ledger, **When** the user enters a valid payment in the form and saves it, **Then** the transaction is stored and the running balance changes accordingly.
2. **Given** a transaction form with required fields completed, **When** the user changes the transaction type from payment to deposit and saves, **Then** the entry is saved with the new type and updated amount effect.

---

### User Story 2 - Capture Invoice Photos (Priority: P2)

As a family managing personal finances, I want to attach an invoice photo to a transaction so I can keep a visual record of the source document, extract the relevant information and create a permanent record.

**Why this priority**: Photo capture supports real-world bookkeeping by preserving supporting evidence for each transaction. This is a key feature that differentiates the product from a simple ledger and adds value for users who want to keep detailed records.

**Independent Test**: A user can create a transaction, attach a photo, save it, and later reopen the entry with the same photo attached. The photo should be viewable and associated with the correct transaction in the ledger.

**Acceptance Scenarios**:

1. **Given** a new transaction entry, **When** the user adds an invoice photo and saves, **Then** the photo remains associated with that transaction. The user can view the photo when they review the transaction details later.
2. **Given** a saved transaction with an attached photo, **When** the user views the transaction later, **Then** the photo is available for review. The data should be preserved even if the transaction is edited or the photo is replaced with a new one.

---

### User Story 3 - Review Balances and History (Priority: P3)

As a family managing personal finances, I want to review my transaction history and running balance so I can understand how deposits and payments affect our finances. The key outcome is to let users understand where does their money come from and where does it go, and to confirm that their records are accurate and up to date.

**Why this priority**: Balance visibility is the main outcome of bookkeeping and helps users confirm the accuracy of their records.

**Independent Test**: A user can open the ledger view and verify that recent entries and the current balance reflect the saved transactions.

**Acceptance Scenarios**:

1. **Given** multiple saved transactions, **When** the user opens the ledger view, **Then** the entries appear in chronological order with the running balance shown.
2. **Given** a transaction is edited or removed, **When** the ledger is refreshed, **Then** the balance history updates to reflect the change.

---

### Edge Cases

- What happens when a transaction is entered without a required amount or date?
- How does the system handle a blurry, unreadable, or missing photo attachment?
- What happens when two entries use the same amount and date and may appear duplicated?
- How does the system recalculate the running balance after an edit or deletion?
- What happens if a user switches between deposit and payment for an existing entry?
- What happens if the information in the photo does not match the manually entered data?

## Requirements *(mandatory)*

### Core Business Logic

- A `deposit` increases the running balance.
- A `payment` decreases the running balance.
- The running balance is recalculated in transaction order whenever a transaction is created, edited, or deleted.
- Invoice photos are optional supporting evidence and do not change the balance.
- A transaction is valid only when required fields are present and the amount is greater than zero.

### Functional Requirements

- **FR-001**: The system MUST allow users to create a transaction manually with at least a transaction type, amount, date, and optional note.
- **FR-002**: The system MUST allow users to categorize each transaction.
- **FR-003**: The system MUST allow users to classify each transaction as a deposit or a payment.
- **FR-004**: The system MUST allow users to attach one or more invoice photos to a transaction.
- **FR-005**: The system MUST preserve each saved transaction with its associated photo attachments for later review.
- **FR-006**: The system MUST create a transaction ledger from a given photo or manual entry and update the running balance accordingly.
- **FR-007**: The system MUST display a running balance that updates after each saved transaction.
- **FR-008**: The system MUST recalculate the running balance when a transaction is edited or deleted.
- **FR-009**: The system MUST show a transaction history that includes date, type, amount, and balance impact.
- **FR-010**: The system MUST validate required inputs before saving a transaction and prevent incomplete entries from being stored.
- **FR-011**: The system MUST let users review saved transaction details after creation.
- **FR-012**: The system MUST support updating or removing previously saved transactions.
- **FR-013**: The system MUST provide a responsive interface that remains usable on mobile phone browsers.
- **FR-014**: The system MUST allow to record periodical transactions for example monthly subscriptions, or monthly bills.

### Key Entities *(include if feature involves data)*

- **Transaction**: A recorded financial event with type, amount, date, note, and balance impact.
- **Invoice Photo**: A visual attachment linked to a transaction for reference and verification.
- **Ledger**: The ordered set of transactions used to present the running balance and history.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 90% of test users can record a valid transaction using the manual form in under 2 minutes without assistance.
- **SC-002**: At least 90% of test users can attach an invoice photo to a transaction and save it successfully on the first attempt.
- **SC-003**: 100% of saved transactions appear in the ledger with the correct type, amount, and date after saving.
- **SC-004**: The running balance matches the expected total for 100% of validated test scenarios after create, edit, and delete actions.
- **SC-005**: At least 85% of test users can identify the current balance and find a recent transaction within 10 seconds.
- **SC-006**: At least 90% of test users can complete a transaction on a mobile phone browser without layout or interaction issues that block submission.


## Assumptions

- The product is a single-user personal bookkeeping experience rather than a shared household or business ledger.
- Invoice photos are stored as supporting evidence for transactions; automatic data extraction from photos is not required for the first version.
- The ledger uses one currency at a time.
- Users can correct or delete entries if they make a mistake.
- The first version focuses on recording, reviewing, and balancing transactions rather than budgeting, taxation, or bank synchronization.
- The first version must support common mobile phone viewport sizes with touch-friendly controls.
- The system will allow to create periodical transactions that can be automatically recorded at specified intervals, but the initial implementation will focus on manual entry and photo capture for one-time transactions.
- The system will extract data from invoice photos to pre-fill transaction details, but users can edit the extracted information before saving the transaction.
