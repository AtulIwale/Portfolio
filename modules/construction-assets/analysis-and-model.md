# Analysis and ML — Construction Assets — Fixed & Movable

Data version AEC-DEMO-2026.1; 5,000 primary rows; 5,000 details and 5,000 capture events. Reporting date 2025-03-01.

## Descriptive results

Monthly depreciation: 73,740,000.00. Median 14,625.00; 90th percentile 27,375.00. All statuses are included: these record totals are not recognized revenue or posted-ledger balances. Monetary examples use INR.

| Status | Records | Value |
|---|---:|---:|
| Available | 1,626 | 24,368,625.00 |
| Deployed | 1,625 | 24,807,750.00 |
| Retired | 120 | 0.00 |
| Under maintenance | 1,629 | 24,563,625.00 |

## Model

Target: Unplanned breakdown in the following month. Creation-time inputs: age_months, utilization_rate, days_since_service, prior_breakdowns. Decision tree: maximum depth 4; minimum leaf 60 training rows.

| Metric | Value |
|---|---:|
| trainRows | 2500 |
| testRows | 1410 |
| excludedRows | 1090 |
| trainCutoff | 2024-06-01 |
| testStart | 2024-08-01 |
| labelCutoff | 2024-08-01 |
| auc | 0.6397 |
| accuracy | 0.6915 |
| precision | 0.4483 |
| recall | 0.0915 |
| brier | 0.1994 |
| baselineBrier | 0.2113 |
| baselineAccuracy | 0.6979 |
| testEventRate | 0.3021 |
| confusionMatrix | [[936, 48], [387, 39]] |

Temporal holdout on synthetic data only. January–May training; June–July excluded; August–October test. Training labels must be known before August. Repeated entities may occur in both periods: this tests future records for known populations, not unseen suppliers or employees. Scores are uncalibrated tree frequencies, not established real-world probabilities. Model features are captured at record creation; outcomes, status, payment and completion fields are excluded. No automated approvals or personnel decisions.

Lower Brier score is better. Compare against the constant-probability baseline; retain weak results. Accuracy uses a 0.50 threshold and is compared to the majority-class baseline.

## Reproduction

`npm run data` generates the same seeded records and applies the versioned exported tree. `npm run train` retrains the experiments after installing requirements.txt.

Validation checks unique IDs, supporting-record joins, arithmetic controls, linked HR/payroll records and Python/JavaScript model parity. The app provides filters, source evidence, CSV export, what-if scoring and a deterministic three-intent evidence assistant. It does not call an LLM or authorize business decisions.
