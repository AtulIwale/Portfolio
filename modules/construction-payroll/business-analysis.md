# Business analysis — Construction Payroll

## AS-IS discovery scenario

Payroll teams rekey approved timesheets into salary spreadsheets, then reconcile allowances, deductions and project postings manually.

Hypothetical scenario, not a claim about an actual company.

## TO-BE workflow

Approved attendance → Pay elements → Gross calculation → Deductions → Reconciliation → Payroll approval → Payment and posting

Process owner: Payroll lead.

| Requirement | Data concepts | Rule | Acceptance test |
|---|---|---|---|
| Attendance eligibility | attendance_id, attendance_status | Hold payroll when the linked attendance is not approved. | A returned timesheet creates a held, unpaid payroll line. |
| Pay calculation | basic_pay, overtime_pay, allowance | Calculate gross from explicit approved components; use configured rates. | Verify paid leave, unpaid absence and authorized overtime. |
| Deductions | deductions, gross_pay | Demo deductions are configurable assumptions, not statutory advice. Net pay cannot be negative. | High deductions are capped or referred for review. |
| Reconciliation | net_pay, paid_amount, project_id | Reconcile gross less deductions to net and payment allocations to paid records. | An unpaid approved run must not count as cash disbursed. |
| Approval segregation | payroll_group, approver | Payroll preparer, reviewer and payment authority are separate roles. | A maker cannot release their own payroll batch. |

## Deliverables

- Salary elements and attendance mapping
- Payroll reconciliation and release controls
- Parallel-run and payment UAT

The same HR attendance rows drive pay. HR changes require regeneration, recalculation and a new dataset version.
