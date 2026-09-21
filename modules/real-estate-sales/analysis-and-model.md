# Analysis and ML — Real Estate Sales

Data version AEC-DEMO-2026.1; 5,000 primary rows; 10,096 details and 5,000 capture events. Reporting date 2025-03-01.

## Descriptive results

Agreed consideration: 66,377,482,000.00. Median 13,230,000.00; 90th percentile 21,600,000.00. All statuses are included: these record totals are not recognized revenue or posted-ledger balances. Monetary examples use INR.

| Status | Records | Value |
|---|---:|---:|
| Agreement signed | 819 | 10,858,704,000.00 |
| Booked | 833 | 10,935,364,000.00 |
| Cancelled | 777 | 10,376,117,000.00 |
| Enquiry | 862 | 11,668,975,000.00 |
| Handed over | 872 | 11,474,466,000.00 |
| Reserved | 837 | 11,063,856,000.00 |

## Model

Target: Opportunity lost or cancelled within 60 days. Creation-time inputs: response_days, discount_pct, prior_contact_count, financing_required. Decision tree: maximum depth 4; minimum leaf 60 training rows.

| Metric | Value |
|---|---:|
| trainRows | 2500 |
| testRows | 1500 |
| excludedRows | 1000 |
| trainCutoff | 2024-06-01 |
| testStart | 2024-08-01 |
| labelCutoff | 2024-08-01 |
| auc | 0.5498 |
| accuracy | 0.744 |
| precision | 0.0 |
| recall | 0.0 |
| brier | 0.1911 |
| baselineBrier | 0.1905 |
| baselineAccuracy | 0.744 |
| testEventRate | 0.256 |
| confusionMatrix | [[1116, 0], [384, 0]] |

Temporal holdout on synthetic data only. January–May training; June–July excluded; August–October test. Training labels must be known before August. Repeated entities may occur in both periods: this tests future records for known populations, not unseen suppliers or employees. Scores are uncalibrated tree frequencies, not established real-world probabilities. Model features are captured at record creation; outcomes, status, payment and completion fields are excluded. No automated approvals or personnel decisions.

Lower Brier score is better. Compare against the constant-probability baseline; retain weak results. Accuracy uses a 0.50 threshold and is compared to the majority-class baseline.

## Reproduction

`npm run data` generates the same seeded records and applies the versioned exported tree. `npm run train` retrains the experiments after installing requirements.txt.

Validation checks unique IDs, supporting-record joins, arithmetic controls, linked HR/payroll records and Python/JavaScript model parity. The app provides filters, source evidence, CSV export, what-if scoring and a deterministic three-intent evidence assistant. It does not call an LLM or authorize business decisions.
