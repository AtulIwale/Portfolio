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

---

## Machine-learning upgrade: anomaly detection on site-labour payroll

**Live app:** [anomaly.html](https://atuliwale.github.io/Portfolio/projects/04-construction-payroll/anomaly.html) · **Notebook:** [notebooks/payroll_anomaly_detection.ipynb](notebooks/payroll_anomaly_detection.ipynb) · **Data:** [data/04_Site_Labour_Payroll_v2.xlsx](data/04_Site_Labour_Payroll_v2.xlsx)

The rules above check staff timesheets for calculation errors. In construction, most payroll leakage is in **site labour supplied by labour contractors**. The typical issues are ghost workers, proxy attendance, padded overtime, unauthorised rate increases and wages paid after a worker has left. The pay arithmetic on these lines is correct, so formula checks can't see them, and nobody labels them in advance. This upgrade treats the problem as **unsupervised anomaly detection**: learn what normal looks like, then rank what doesn't fit.

### Data added (original workbook unchanged)
| Sheet | Rows | What it holds |
| --- | ---: | --- |
| dim_worker | 1,317 | Site workers: trade, skill, labour contractor, site (the same 12 sites as `dim_employee`), join/exit month, daily wage, masked bank account, Aadhaar and PF status |
| dim_labour_contractor | 18 | Labour contractors (15 active in the period) |
| fact_payroll_month | 12,397 | Monthly wage lines, Sep 2025 to Aug 2026: working days, days present, Sundays, biometric vs manual days, overtime, rate, gross, PF, ESI, net, payment mode, approver (a staff member from `dim_employee`) |
| site_calendar | 144 | Legitimate site events: concrete-pour pushes and biometric device faults |
| audit_outcome | 12,397 | Internal-audit result per line. **Used only to evaluate the detectors, never to train them** |

The data is synthetic but follows real site patterns. Workers go home for Diwali and Chhath, and coastal sites slow in the monsoon. Wages are revised in April. Concrete pours bring Sunday work and heavy overtime for whole crews, and biometric devices fail. Against that background, 4.5% of lines are real issues: ghost workers placed by three contractors (paid into shared or new accounts), proxy attendance, padded overtime, mid-year rate increases pushed through two approvers, and pay after exit.

### Method
1. **Peer-relative features (17):** each line is compared with its site that month (manual days, attendance, Sundays), its trade crew on site (overtime), its trade across sites (rate), and the worker's own past (attendance, rate jumps outside the April revision). Identity signals are added: shared bank account, KYC/PF gaps, cash payment and pay after exit.
2. **Split by time:** the detectors learn normal from Sep 2025 to Feb 2026 and are scored on Mar to Aug 2026. Settings are chosen using the earlier period's audit results only.
3. **Detectors:** a seven-rule audit checklist, a robust z-score, **Isolation Forest**, **Local Outlier Factor**, **One-Class SVM**, an **autoencoder** (a neural network that flags lines it can't rebuild) and an ensemble.
4. **Evaluation at an audit budget:** precision and recall when the auditor reviews the top 2% or 5% of lines each month.
5. **Reason codes:** each line lists its rarest features compared with the learning period, for example *Paid after exit month (high, rarest 0.1%)*.

### Results on Mar to Aug 2026 (6,372 lines, 364 confirmed issues)
| Detector | PR-AUC | Precision, top 5% | Recall, top 5% |
| --- | ---: | ---: | ---: |
| **Isolation Forest** | **0.837** | **83%** | **73%** |
| Ensemble (IF + autoencoder + z-score) | 0.783 | 75% | 66% |
| Robust z-score | 0.780 | 74% | 66% |
| One-Class SVM | 0.772 | 76% | 67% |
| Local Outlier Factor | 0.684 | 68% | 60% |
| Autoencoder | 0.681 | 68% | 60% |
| Audit rules (count of rules hit) | 0.373 | 46% | 41% |
| Random order | 0.057 | 6% | 5% |

- **The rules produce a flood of alerts.** Together they flag 24% of all lines, and 86% of those flags are false alarms (missing PF links, concrete-pour pushes, biometric faults). They are exact only for hard facts, such as pay after exit.
- **The Isolation Forest finds most issues with little effort.** Reviewing just 51 of 1,012 lines in August 2026 found 48 real issues.
- **By type (Isolation Forest, top 5%):** it caught 100% of pay after exit, 87% of rate increases, 85% of ghost workers, 74% of padded overtime and 8% of proxy attendance.
- **From lines to control findings:** three contractors are flagged at more than twice the fleet rate, and they are exactly the three that placed ghost workers. Two approvers account for every mid-year rate increase.

### What I learned
- **Context is everything.** Comparing each line with its site, crew and own history is what separates a concrete-pour weekend from padded overtime.
- **Simpler won here.** The Isolation Forest beat the autoencoder and the ensemble. The autoencoder learns to rebuild overtime from the other features, so it partly explains away a single extreme value.
- **Density methods can be fooled by organised fraud.** Ghost workers from one contractor look alike, so the Local Outlier Factor sees them as a normal cluster (masking).
- **Proxy attendance needs better data**, such as gate or face-recognition logs. A few extra manual days look like normal absence in payroll alone.

### Limits
The data is synthetic. In real life audit outcomes exist only for the lines reviewed, so precision would be measured on that sample. A flag is a reason to check, not proof of fraud.

### Files added
| File | Purpose |
| --- | --- |
| `anomaly.html` | Monthly audit list with a detector choice and a budget slider, reason codes, comparison with normal, detector comparison, rule analysis, contractors and approvers. The Isolation Forest (200 trees) and the autoencoder run in the browser, and a self-check matches the Python scores |
| `notebooks/payroll_anomaly_detection.ipynb` | Audit, rule analysis, features, seven detectors, evaluation at an audit budget, reason codes, contractor/approver roll-up and export |
| `model/anomaly_export.json` | Isolation Forest trees, autoencoder weights, scaling and the scored lines for Mar to Aug 2026 |
| `data/04_Site_Labour_Payroll_v2.xlsx` | Workers, contractors, monthly payroll, site calendar and audit outcomes |

Author: Atul Iwale
