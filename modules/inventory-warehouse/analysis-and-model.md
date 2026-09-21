# Analysis and ML — Inventory & Warehouse Management

Data version AEC-DEMO-2026.1; 5,000 primary rows; 5,000 details and 5,000 capture events. Reporting date 2025-03-01.

## Descriptive results

Movement value (absolute): 212,233,900.00. Median 31,612.50; 90th percentile 99,459.00. All statuses are included: these record totals are not recognized revenue or posted-ledger balances. Monetary examples use INR.

| Status | Records | Value |
|---|---:|---:|
| Count verified | 1,947 | 81,315,206.00 |
| Posted | 1,519 | 64,518,232.00 |
| Quarantined | 1,534 | 66,400,462.00 |

## Model

Target: Cycle-count discrepancy discovered after posting. Creation-time inputs: days_since_count, movement_qty, manual_entry, item_value. Decision tree: maximum depth 4; minimum leaf 60 training rows.

| Metric | Value |
|---|---:|
| trainRows | 2500 |
| testRows | 1500 |
| excludedRows | 1000 |
| trainCutoff | 2024-06-01 |
| testStart | 2024-08-01 |
| labelCutoff | 2024-08-01 |
| auc | 0.6593 |
| accuracy | 0.7347 |
| precision | 0.6316 |
| recall | 0.0872 |
| brier | 0.1866 |
| baselineBrier | 0.1999 |
| baselineAccuracy | 0.7247 |
| testEventRate | 0.2753 |
| confusionMatrix | [[1066, 21], [377, 36]] |

Temporal holdout on synthetic data only. January–May training; June–July excluded; August–October test. Training labels must be known before August. Repeated entities may occur in both periods: this tests future records for known populations, not unseen suppliers or employees. Scores are uncalibrated tree frequencies, not established real-world probabilities. Model features are captured at record creation; outcomes, status, payment and completion fields are excluded. No automated approvals or personnel decisions.

Lower Brier score is better. Compare against the constant-probability baseline; retain weak results. Accuracy uses a 0.50 threshold and is compared to the majority-class baseline.

## Reproduction

`npm run data` generates the same seeded records and applies the versioned exported tree. `npm run train` retrains the experiments after installing requirements.txt.

Validation checks unique IDs, supporting-record joins, arithmetic controls, linked HR/payroll records and Python/JavaScript model parity. The app provides filters, source evidence, CSV export, what-if scoring and a deterministic three-intent evidence assistant. It does not call an LLM or authorize business decisions.
