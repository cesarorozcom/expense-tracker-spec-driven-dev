# Analysis Report: Personal Finance Bookkeeping

**Feature**: Personal Finance Bookkeeping (`001-personal-finance-bookkeeping`)
**Created**: 2026-05-16
**Scope**: Specification quality analysis and detection passes against spec, plan, data model, contracts, and research artifacts.

## Summary Findings

- Overall, the specification is comprehensive for a v1 single-user bookkeeping web app focusing on manual entry and photo attachments.
- Core functional requirements and data model are well-aligned: `Transaction`, `InvoicePhoto`, and `Ledger` are defined with clear fields and validation rules.
- The plan provides a concrete, implementable stack (Django, Postgres, S3-compatible storage) and deployment guidance.

## Key Gaps and Ambiguities (High Priority)

- OCR / data-extraction: The spec contains contradictory assumptions. `Assumptions` and `FR-006` reference both "automatic extraction" and "not required for first version". Clarify whether OCR is in-scope for v1. [Gap, Spec §Assumptions, FR-006]
- Recurring transactions: `FR-014` requires periodical transactions, but the spec lacks details for scheduling semantics, timezone handling, edit/delete behavior for generated instances, and UI for managing recurring rules. [Coverage, Spec §FR-014]
- Photo failure modes: The user scenarios mention blurry/unreadable photos and missing attachments but the spec lacks explicit handling/UX guidance (e.g., reject vs accept with warning, retry guidance). [Edge Case, Spec §Edge Cases]
- Duplicate detection policy: No requirement specifies whether duplicates should be detected, merged, or left to user choice. [Edge Case, Spec §Edge Cases]
- Traceability: No explicit ID mapping from requirements to test cases beyond FR-/SC- IDs. A formal traceability matrix or sample test vectors for running-balance verification is missing. [Traceability, Spec §Success Criteria]

## Non-Functional Notes (Medium Priority)

- Accessibility: `FR-013` mandates responsive interface but does not quantify keyboard navigation, screen reader labels, or contrast requirements. Add WCAG AA targets or minimum keyboard/focus behaviors. [Non-Functional, Spec §FR-013]
- Performance: The plan includes p95 goals, but the spec lacks acceptance-level metrics and where they apply (ledger list rendering, upload latency). Link performance goals to SC entries. [Non-Functional, Spec §Performance Goals]
- Privacy & retention: Photo storage expectations (retention period, encryption-at-rest, access control policies) are not specified. Add minimal data-protection constraints. [Non-Functional, Spec §Assumptions]
- Security: Single-user assumption reduces auth complexity, but the plan should still define local auth/session expectations and handling for API endpoints and object storage URLs (signed URLs vs public objects). [Security, Spec §Assumptions]

## Consistency Checks

- `Core Business Logic` and `Data Model` consistently define `deposit` and `payment` effects, and the ledger recalculation rule appears in multiple places; ensure a single authoritative source of truth (e.g., `Core Business Logic` + `Data Model` combined). [Consistency]
- `FR-006` (create ledger from photo) versus assumption "automatic data extraction not required" needs resolution to avoid conflicting developer expectations. [Conflict]

## Recommended Remediations (Actionable)

1. Decide OCR scope for v1 and update `Assumptions` and `FR-006` to match. If OCR is deferred, change FR-006 to explicitly mention "photo storage and optional manual entry; OCR out-of-scope for v1".
2. Expand `FR-014` with sub-requirements: schedule format, timezone normalization, recurrence edit semantics, and UI management endpoints. Add acceptance scenarios for recurring payments creation and cancellation.
3. Add explicit photo failure-mode requirements: detection, user messaging, and retry guidance; include file-size and type limits in `FR-004` or `Contracts` with concrete values.
4. Add at least three sample ledger test vectors showing transactions and expected running balances to validate SC-004 measurably.
5. Define minimal data-protection controls for invoice photos (encryption-at-rest, signed access URLs, retention policy) and link to privacy section.
6. Add accessibility acceptance criteria (WCAG AA checkpoints relevant to forms and lists) to FR-013 and SC entries.

## Low Priority Suggestions

- Define duplicate-detection policy or explicitly state it is out of scope.
- Add performance measurement points in the spec mapping to the plan's p95 goals (which pages/actions and under what dataset sizes).
- Include short implementation notes in the plan about signed URLs for photo uploads vs server-proxied uploads and their security implications.

## Checklist Status

- Existing requirements checklist updated with CHK001–CHK012 to cover the primary gaps discovered.
- Recommend author addresses CHK001, CHK002, CHK006, CHK008, CHK009, CHK010, and CHK011 as highest-priority edits.

## Next Steps

- Author decision: OCR in-scope or deferred (this will unblock several items).
- Add `tasks.md` if you want full task-traceable analysis (generation scripts expect it). The absence of `tasks.md` previously blocked automated steps; consider creating one using the plan's `Project Structure` as a guide.
- After updates, re-run this analysis to confirm remediation and produce an acceptance-focused checklist for QA.

---

*Generated by speckit.analyze on 2026-05-16*
