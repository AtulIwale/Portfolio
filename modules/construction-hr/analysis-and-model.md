# Analysis and ML — Construction HR

Data version AEC-DEMO-2026.1; 5,000 primary rows; 5,000 details and 5,000 capture events. Reporting date 2025-03-01.

## Descriptive results

Worked days: 115,011.00. Median 23.00; 90th percentile 25.00. All statuses are included: these record totals are not recognized revenue or posted-ledger balances. Monetary examples use INR.

| Status | Records | Value |
|---|---:|---:|
| Approved | 1,281 | 29,412.00 |
| Draft | 1,193 | 27,453.00 |
| Returned | 1,257 | 28,937.00 |
| Submitted | 1,269 | 29,209.00 |

## Model

Target: Attendance record needs clerical correction at review. Creation-time inputs: manual_entry, missing_punches, overtime_hours, shift_changes. Decision tree: maximum depth 4; minimum leaf 60 training rows.

| Metric | Value |
|---|---:|
| trainRows | 2500 |
| testRows | 1500 |
| excludedRows | 1000 |
| trainCutoff | 2024-06-01 |
| testStart | 2024-08-01 |
| labelCutoff | 2024-08-01 |
| auc | 0.7007 |
| accuracy | 0.6667 |
| precision | 0.6261 |
| recall | 0.3752 |
| brier | 0.2105 |
| baselineBrier | 0.2387 |
| baselineAccuracy | 0.6073 |
| testEventRate | 0.3927 |
| confusionMatrix | [[779, 132], [368, 221]] |

Temporal holdout on synthetic data only. January–May training; June–July excluded; August–October test. Training labels must be known before August. Repeated entities may occur in both periods: this tests future records for known populations, not unseen suppliers or employees. Scores are uncalibrated tree frequencies, not established real-world probabilities. Model features are captured at record creation; outcomes, status, payment and completion fields are excluded. No automated approvals or personnel decisions.

Lower Brier score is better. Compare against the constant-probability baseline; retain weak results. Accuracy uses a 0.50 threshold and is compared to the majority-class baseline.

## Reproduction

`npm run data` generates the same seeded records and applies the versioned exported tree. `npm run train` retrains the experiments after installing requirements.txt.

Validation checks unique IDs, supporting-record joins, arithmetic controls, linked HR/payroll records and Python/JavaScript model parity. The app provides filters, source evidence, CSV export, what-if scoring and a deterministic three-intent evidence assistant. It does not call an LLM or authorize business decisions.
