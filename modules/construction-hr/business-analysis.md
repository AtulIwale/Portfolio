# Business analysis — Construction HR

## AS-IS discovery scenario

Site attendance is consolidated from paper muster rolls, shift messages and emailed leave records before HR approval.

Hypothetical scenario, not a claim about an actual company.

## TO-BE workflow

Employee master → Deployment → Shift allocation → Attendance → Leave → Timesheet review → Approved payroll handoff

Process owner: HR operations lead.

| Requirement | Data concepts | Rule | Acceptance test |
|---|---|---|---|
| Employee identity | employee_id, payroll_group | Use fictional IDs and one active employment record; do not store personal bank or government identifiers in the demo. | Reject duplicate employee-month attendance. |
| Shift and leave | scheduled_days, worked_days, paid_leave_days | Worked, leave and absence days must reconcile to scheduled days. | Overlapping leave and worked days are rejected. |
| Timesheet ownership | project_id, approver | Supervisor checks the site record; HR verifies exceptions. | The preparer cannot approve their own timesheet. |
| Overtime authorization | overtime_hours, overtime_approved | Payable overtime must be authorized before payroll cut-off. | Unapproved overtime stays out of payroll gross. |
| Handoff lock | attendance_id, status | Only approved attendance feeds payroll; other records remain held. | A returned timesheet cannot produce a paid payroll record. |

## Deliverables

- Employee-to-payroll data dictionary
- Shift, absence and approval workflow
- Attendance reconciliation and handoff UAT

Employee and attendance IDs join Payroll directly; review scores concern data quality, not worker performance.
