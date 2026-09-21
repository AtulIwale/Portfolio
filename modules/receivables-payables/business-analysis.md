# Business analysis — Accounts Receivable & Accounts Payable

## AS-IS discovery scenario

Invoices arrive by email; matching and approvals use spreadsheets. Separate receipt/payment trackers obscure unpaid balances.

Hypothetical scenario, not a claim about an actual company.

## TO-BE workflow

Invoice → Match / certify → Approve → Post → Allocate settlement → Age balance → Reconcile

Process owner: Finance controller.

| Requirement | Data concepts | Rule | Acceptance test |
|---|---|---|---|
| Invoice identity | invoice_no, entity_id, invoice_type | Detect supplier/customer invoice duplicates using entity plus invoice number. | A duplicate document must be rejected before posting. |
| Source matching | source_id, match_variance | AP matches accepted order/receipt or certified work; standalone invoices have their own authority. | A price/quantity mismatch remains on hold. |
| Accounting period | record_date, ledger_period | Post only to an open demonstration period with defined control accounts. | Closed-period posting is blocked. |
| Settlement allocation | gross_amount, settled_amount, outstanding | Do not allocate more than the invoice balance; keep AR/AP totals separate. | Test partial settlement and over-allocation. |
| Aging | due_date, as_of_date | Age outstanding balances using the fixed reporting date. | Verify not-due, due-today and 1/30/60/90-day boundaries. |

## Deliverables

- Invoice/matching and settlement requirements
- AR/AP control-account reconciliation
- Period and aging acceptance tests

Sample AP invoices link to completed orders; AR invoices link to contracts or sales. The ledger is a sample, not full source-system totals.
