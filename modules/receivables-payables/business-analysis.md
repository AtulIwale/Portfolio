# Business Analysis — Accounts Receivable & Accounts Payable

**Work:** Defined invoice matching, settlement allocation and aging controls.

**Current-process scenario:** Invoices arrive by email; matching and approvals use spreadsheets. Separate receipt/payment trackers obscure unpaid balances.

**Proposed flow:** Invoice → Match / certify → Approve → Post → Allocate settlement → Age balance → Reconcile.

| Control | Rule | Acceptance check |
| --- | --- | --- |
| Invoice identity | Detect supplier/customer invoice duplicates using entity plus invoice number. | A duplicate document must be rejected before posting. |
| Source matching | AP matches accepted order/receipt or certified work; standalone invoices have their own authority. | A price/quantity mismatch remains on hold. |
| Accounting period | Post only to an open demonstration period with defined control accounts. | Closed-period posting is blocked. |
| Settlement allocation | Do not allocate more than the invoice balance; keep AR/AP totals separate. | Test partial settlement and over-allocation. |
| Aging | Age outstanding balances using the fixed reporting date. | Verify not-due, due-today and 1/30/60/90-day boundaries. |

**Deliverables:** Invoice/matching and settlement requirements; AR/AP control-account reconciliation; Period and aging acceptance tests.

**Owner / handoff:** Finance controller. Sample AP invoices link to completed orders; AR invoices link to contracts or sales. The ledger is a sample, not full source-system totals.

Hypothetical discovery and proposed configuration; [dataset fields and assumptions](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/receivables-payables.xlsx)
