# Business Analysis — Construction HR

**Work:** Mapped attendance, leave, overtime approvals and payroll handoffs.

**Current-process scenario:** Site attendance is consolidated from paper muster rolls, shift messages and emailed leave records before HR approval.

**Proposed flow:** Employee master → Deployment → Shift allocation → Attendance → Leave → Timesheet review → Approved payroll handoff.

| Control | Rule | Acceptance check |
| --- | --- | --- |
| Employee identity | Use fictional IDs and one active employment record; do not store personal bank or government identifiers in the demo. | Reject duplicate employee-month attendance. |
| Shift and leave | Worked, leave and absence days must reconcile to scheduled days. | Overlapping leave and worked days are rejected. |
| Timesheet ownership | Supervisor checks the site record; HR verifies exceptions. | The preparer cannot approve their own timesheet. |
| Overtime authorization | Payable overtime must be authorized before payroll cut-off. | Unapproved overtime stays out of payroll gross. |
| Handoff lock | Only approved attendance feeds payroll; other records remain held. | A returned timesheet cannot produce a paid payroll record. |

**Deliverables:** Employee-to-payroll data dictionary; Shift, absence and approval workflow; Attendance reconciliation and handoff UAT.

**Owner / handoff:** HR operations lead. Employee and attendance IDs join Payroll directly; review scores concern data quality, not worker performance.

Hypothetical discovery and proposed configuration; [dataset fields and assumptions](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-hr.xlsx)
