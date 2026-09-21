# Analysis and ML — Procurement & Subcontracting

Data version AEC-DEMO-2026.1; 5,000 primary rows; 5,000 details and 5,000 capture events. Reporting date 2025-03-01.

## Descriptive results

Order value: 3,263,992,784.00. Median 504,982.00; 90th percentile 1,459,549.80. All statuses are included: these record totals are not recognized revenue or posted-ledger balances. Monetary examples use INR.

| Status | Records | Value |
|---|---:|---:|
| Approved | 243 | 156,989,521.00 |
| Cancelled | 233 | 154,972,362.00 |
| Completed | 3,497 | 2,284,665,998.00 |
| Draft | 234 | 146,415,381.00 |
| Part delivered | 271 | 178,219,886.00 |
| Pending approval | 276 | 188,069,589.00 |
| Rejected | 246 | 154,660,047.00 |

## Model

Target: Completion after the promised date. Creation-time inputs: lead_days, prior_delay_rate, approval_levels, urgency. Decision tree: maximum depth 4; minimum leaf 60 training rows.

| Metric | Value |
|---|---:|
| trainRows | 1915 |
| testRows | 1192 |
| excludedRows | 1893 |
| trainCutoff | 2024-06-01 |
| testStart | 2024-08-01 |
| labelCutoff | 2024-08-01 |
| auc | 0.6014 |
| accuracy | 0.5612 |
| precision | 0.542 |
| recall | 0.6345 |
| brier | 0.2425 |
| baselineBrier | 0.2499 |
| baselineAccuracy | 0.5134 |
| testEventRate | 0.4866 |
| confusionMatrix | [[301, 311], [212, 368]] |

Temporal holdout on synthetic data only. January–May training; June–July excluded; August–October test. Training labels must be known before August. Repeated entities may occur in both periods: this tests future records for known populations, not unseen suppliers or employees. Scores are uncalibrated tree frequencies, not established real-world probabilities. Model features are captured at record creation; outcomes, status, payment and completion fields are excluded. No automated approvals or personnel decisions.

Lower Brier score is better. Compare against the constant-probability baseline; retain weak results. Accuracy uses a 0.50 threshold and is compared to the majority-class baseline.

## Reproduction

`npm run data` generates the same seeded records and applies the versioned exported tree. `npm run train` retrains the experiments after installing requirements.txt.

Validation checks unique IDs, supporting-record joins, arithmetic controls, linked HR/payroll records and Python/JavaScript model parity. The app provides filters, source evidence, CSV export, what-if scoring and a deterministic three-intent evidence assistant. It does not call an LLM or authorize business decisions.
