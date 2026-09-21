# Analysis and ML — Tendering & Contracts

Data version AEC-DEMO-2026.1; 5,000 primary rows; 17,602 details and 5,000 capture events. Reporting date 2025-03-01.

## Descriptive results

Package value: 21,333,880,000.00. Median 4,270,000.00; 90th percentile 7,251,000.00. All statuses are included: these record totals are not recognized revenue or posted-ledger balances. Monetary examples use INR.

| Status | Records | Value |
|---|---:|---:|
| Awarded | 733 | 3,049,100,000.00 |
| Cancelled | 718 | 3,163,560,000.00 |
| Contract active | 716 | 3,057,580,000.00 |
| Contract closed | 729 | 3,044,110,000.00 |
| Draft | 724 | 3,108,930,000.00 |
| In evaluation | 690 | 3,011,200,000.00 |
| Lost | 690 | 2,899,400,000.00 |

## Model

Target: Award delayed beyond planned evaluation days. Creation-time inputs: bid_count, scope_changes, approval_levels, planned_days. Decision tree: maximum depth 4; minimum leaf 60 training rows.

| Metric | Value |
|---|---:|
| trainRows | 1067 |
| testRows | 671 |
| excludedRows | 3262 |
| trainCutoff | 2024-06-01 |
| testStart | 2024-08-01 |
| labelCutoff | 2024-08-01 |
| auc | 0.6486 |
| accuracy | 0.6557 |
| precision | 0.5246 |
| recall | 0.27 |
| brier | 0.218 |
| baselineBrier | 0.2298 |
| baselineAccuracy | 0.6468 |
| testEventRate | 0.3532 |
| confusionMatrix | [[376, 58], [173, 64]] |

Temporal holdout on synthetic data only. January–May training; June–July excluded; August–October test. Training labels must be known before August. Repeated entities may occur in both periods: this tests future records for known populations, not unseen suppliers or employees. Scores are uncalibrated tree frequencies, not established real-world probabilities. Model features are captured at record creation; outcomes, status, payment and completion fields are excluded. No automated approvals or personnel decisions.

Lower Brier score is better. Compare against the constant-probability baseline; retain weak results. Accuracy uses a 0.50 threshold and is compared to the majority-class baseline.

## Reproduction

`npm run data` generates the same seeded records and applies the versioned exported tree. `npm run train` retrains the experiments after installing requirements.txt.

Validation checks unique IDs, supporting-record joins, arithmetic controls, linked HR/payroll records and Python/JavaScript model parity. The app provides filters, source evidence, CSV export, what-if scoring and a deterministic three-intent evidence assistant. It does not call an LLM or authorize business decisions.
