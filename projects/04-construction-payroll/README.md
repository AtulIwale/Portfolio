# Construction Payroll

## Problem
Construction payroll combines site hours, overtime, contracted rates and approvals. Errors discovered after release require payment corrections and create avoidable work for payroll teams and employees. This demo brings exceptions and their source records into a pre-release review worklist.

## Approach

### Business Analysis
- **Duplicate Hours:** flag every row when employee_id and pay_period occur more than once. A repeated combination is a review exception, not proof of duplicate payment.
- **Wrong Rate:** flag gross pay differing by more than ₹0.50 from regular hours × hourly rate + overtime hours × 1.5 × hourly rate. The name follows the requested rule; the evidence establishes a pay mismatch, not its root cause.
- **Missing Approval:** flag any approval_status other than Approved.
- **Overtime Miscalculation:** when overtime_hours > 0, flag gross pay at or below (regular hours + overtime hours) × hourly rate, allowing ₹0.50. No overtime premium is evident.

The workbook defines hours_worked as regular hours. ₹0.50 tolerance accommodates its whole-rupee rounding. Reviewers decide whether a flag needs correction before release.

### Project Management
Scope: one offline HTML file, all 2,400 timesheet records joined to 200 employees, four transparent checks, a ranked worklist, source-record comparisons and validation. Priorities were traceability, correct joins, rounding boundaries and clear reasons. Payroll posting, edits, approval automation and live ERP connections are outside this build.

### Data Analysis & Data Science
Join employees by employee_id and validation labels by row_id. Group all timesheet records by employee_id and pay_period, then calculate expected pay and straight-time pay for each record. Apply each rule independently; a record can trigger multiple rules.

Rank by rule count descending, absolute pay difference descending, gross pay descending, then row_id. This is a transparent review order, not a learned risk score or quantified saving. Search and error filters affect the worklist only; headline metrics cover the complete dataset.

### AI
This implementation is a deterministic rules engine, not a statistical or machine-learning model. It does not train or use answer-key labels to generate flags. A future ML version could prioritize unusual hours or rate patterns using independently reviewed outcomes, with held-out evaluation, explainable evidence and human review. Such a model is not included here.

## Data
Synthetic data patterned on real ERP structures, supplied in `data/04_Construction_Payroll.xlsx`:

| Sheet | Rows | Fields and purpose |
|---|---:|---|
| dim_employee | 200 | employee_id, name, role, site, hourly_rate (INR) |
| fact_timesheet | 2,400 | row_id, employee_id, pay_period, hours_worked, overtime_hours, approver_id, approval_status, gross_pay (INR) |
| answer_key | 2,400 | row_id, is_pay_error, error_type; one primary label per record |
| data_dictionary | 20 | Sheet, column, type and meaning |

The HTML embeds the workbook data as JSON and runs without network access. The Excel file is the source snapshot; changing Excel does not automatically refresh the embedded JSON.

### Approved dataset correction
The supplied workbook originally labeled 60 records Duplicate Hours even though none repeated an employee/pay-period combination. Forty pay-period cells were changed within existing employee records, producing 40 duplicate pairs. The original 60 labels now have supporting evidence, and 20 clean counterpart records were relabeled Duplicate Hours because both sides meet the rule. Two overtime-labeled records with zero overtime were assigned 2 overtime hours, leaving gross pay unchanged. Total rows, row IDs and all other cell values were preserved.

Corrected primary labels: 80 Duplicate Hours, 60 Wrong Rate, 60 Missing Approval, 60 Overtime Miscalculation and 2,140 No error.

## Validation
**Row-level precision: 100.0% (260/260). Recall: 100.0% (260/260).**

True positives: 260. False positives: 0. False negatives: 0. True negatives: 2,140.

**Perfect precision and recall is expected here because these are deterministic rule checks validated against synthetic labels built from the same rules. This is not a statistical model.** The approved corrections intentionally align the seeded examples and their labels with the rule definitions. The result demonstrates consistency on these synthetic cases; it is not an independent benchmark, evidence of generalization or a claim of perfect performance on real payroll. Independent real-world cases and policy validation would be needed for that assessment.

| Rule | Flagged rows | Primary labels | Matching primary labels | Exact-type precision | Exact-type recall |
|---|---:|---:|---:|---:|---:|
| Duplicate Hours | 80 | 80 | 80 | 100.0% | 100.0% |
| Wrong Rate | 120 | 60 | 60 | 50.0% | 100.0% |
| Missing Approval | 60 | 60 | 60 | 100.0% | 100.0% |
| Overtime Miscalculation | 60 | 60 | 60 | 100.0% | 100.0% |

Counts overlap: all 60 overtime cases also fail the expected-pay check. Their primary label is Overtime Miscalculation, so they lower Wrong Rate's exact-type precision to 50%, while remaining true pay-error detections. Every labeled error has its primary reason among the triggered rules. Exact-type recall uses the number of primary labels as its denominator; exact-type precision uses all rows flagged by that rule.

## How to run
Open index.html in any browser, or view it live at [Pages link](https://atuliwale.github.io/Portfolio/projects/04-construction-payroll/).
