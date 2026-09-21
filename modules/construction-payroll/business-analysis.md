# Business Analysis — Construction Payroll

**Work:** Defined pay calculations, deductions, reconciliation and release controls.

**Current-process scenario:** Payroll teams rekey approved timesheets into salary spreadsheets, then reconcile allowances, deductions and project postings manually.

**Proposed flow:** Approved attendance → Pay elements → Gross calculation → Deductions → Reconciliation → Payroll approval → Payment and posting.

| Control | Rule | Acceptance check |
| --- | --- | --- |
| Attendance eligibility | Hold payroll when the linked attendance is not approved. | A returned timesheet creates a held, unpaid payroll line. |
| Pay calculation | Calculate gross from explicit approved components; use configured rates. | Verify paid leave, unpaid absence and authorized overtime. |
| Deductions | Demo deductions are configurable assumptions, not statutory advice. Net pay cannot be negative. | High deductions are capped or referred for review. |
| Reconciliation | Reconcile gross less deductions to net and payment allocations to paid records. | An unpaid approved run must not count as cash disbursed. |
| Approval segregation | Payroll preparer, reviewer and payment authority are separate roles. | A maker cannot release their own payroll batch. |

**Deliverables:** Salary elements and attendance mapping; Payroll reconciliation and release controls; Parallel-run and payment UAT.

**Owner / handoff:** Payroll lead. The same HR attendance rows drive pay. HR changes require regeneration, recalculation and a new dataset version.

Hypothetical discovery and proposed configuration; [dataset fields and assumptions](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-payroll.xlsx)
