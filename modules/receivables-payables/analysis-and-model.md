# Analysis and ML — Accounts Receivable & Accounts Payable

Data version AEC-DEMO-2026.1; 5,000 primary rows; 3,857 details and 5,000 capture events. Reporting date 2025-03-01.

## Descriptive results

Gross invoice value (AR + AP): 9,183,078,600.00. Median 1,840,800.00; 90th percentile 3,221,400.00. All statuses are included: these record totals are not recognized revenue or posted-ledger balances. Monetary examples use INR.

| Status | Records | Value |
|---|---:|---:|
| Disputed | 314 | 584,678,200.00 |
| Draft | 274 | 498,644,400.00 |
| Overdue | 555 | 1,067,144,800.00 |
| Part settled | 285 | 507,671,400.00 |
| Settled | 3,572 | 6,524,939,800.00 |

## Model

Target: Settlement later than contractual payment terms. Creation-time inputs: payment_days, prior_late_rate, match_variance, approval_levels. Decision tree: maximum depth 4; minimum leaf 60 training rows.

| Metric | Value |
|---|---:|
| trainRows | 2185 |
| testRows | 1317 |
| excludedRows | 1498 |
| trainCutoff | 2024-06-01 |
| testStart | 2024-08-01 |
| labelCutoff | 2024-08-01 |
| auc | 0.6183 |
| accuracy | 0.5839 |
| precision | 0.5974 |
| recall | 0.4969 |
| brier | 0.2414 |
| baselineBrier | 0.2504 |
| baselineAccuracy | 0.5034 |
| testEventRate | 0.4966 |
| confusionMatrix | [[444, 219], [329, 325]] |

Temporal holdout on synthetic data only. January–May training; June–July excluded; August–October test. Training labels must be known before August. Repeated entities may occur in both periods: this tests future records for known populations, not unseen suppliers or employees. Scores are uncalibrated tree frequencies, not established real-world probabilities. Model features are captured at record creation; outcomes, status, payment and completion fields are excluded. No automated approvals or personnel decisions.

Lower Brier score is better. Compare against the constant-probability baseline; retain weak results. Accuracy uses a 0.50 threshold and is compared to the majority-class baseline.

## Reproduction

`npm run data` generates the same seeded records and applies the versioned exported tree. `npm run train` retrains the experiments after installing requirements.txt.

Validation checks unique IDs, supporting-record joins, arithmetic controls, linked HR/payroll records and Python/JavaScript model parity. The app provides filters, source evidence, CSV export, what-if scoring and a deterministic three-intent evidence assistant. It does not call an LLM or authorize business decisions.
