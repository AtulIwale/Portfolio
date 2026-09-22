# Construction HR

Coverage-tier, self-contained offline attendance review. GitHub-only delivery; no Pages hosting configuration.

## Problem

Missing clock-outs, pending leave approvals and long recorded shifts need review before payroll preparation. Each requires its own explanation and worklist. This app identifies three deterministic dataset patterns and reports answer-key agreement separately, with no blended score.

## Approach

### Business Analysis

- **Missing Clock-Out:** clock_in present, clock_out blank, leave_type blank — **67 rows**.
- **Unapproved Leave:** leave_type present and approval_status exactly Pending — **66 rows**. This is an administrative review flag, not employee misconduct. Approved leave is excluded; there is no Rejected status in this workbook.
- **Excessive Overtime:** raw elapsed clock-in-to-clock-out duration **≥12 hours**, inclusive — **67 rows**. No break deduction. This is the dataset's duration-based category, not a conclusion about payable overtime or legal limits.

Blank means a null or empty source value. Categories do not overlap in this snapshot. No employee allowlist or answer-key field is used to classify rows. No unsupported proactive checks are added.

### Project Management

Scope: one offline HTML app, unchanged source workbook, three separately scored worklists, employee/search filters, date/ID/duration ordering, row-level source evidence and separate CSV exports of displayed rows. Headline counts and agreement always describe the full snapshot. No automated payroll changes, live integration or external scripts.

### Data Analysis & Data Science

Apply each rule to `fact_attendance`, then join `answer_key` by `row_id` for evaluation. For each category, truth is `is_anomaly = Y` with that exact `anomaly_type`. All other rows, including the other two categories, are negatives for that category. Evaluation therefore covers all 2,000 rows independently for each rule.

Time extraction preserves fractional seconds. Duration is `(clock_out_seconds - clock_in_seconds) / 3600`; decisions use the unrounded value, while the app displays hours to two decimals. All 67 excessive-duration labels equal **14.25 hours**. The maximum N-labeled duration is **10.67908833333333 hours**, rounded to **10.68 hours** (correcting the earlier 10.67 figure). The 12-hour threshold lies in the clean gap.

There are **zero clock_out-earlier-than-clock_in rows**. Overnight-shift handling is intentionally omitted; unexpected negative elapsed durations block rendering rather than being rolled into the following day. Missing times show “Not available,” never zero elapsed hours.

### AI

**Deterministic, not a trained model.** No ML, training, probability, forecasting or independent model evaluation. Each category displays **“Answer-key agreement: 100% precision / 100% recall.”** This is agreement with the labeled dataset, **not independent validation**. Rules were specified with knowledge of this dataset and its labels; these results do not establish performance on unseen attendance data or independent discrimination.

## Data

[10_Construction_HR.xlsx](data/10_Construction_HR.xlsx) is copied byte-for-byte from the supplied source. All three sheets are embedded as JSON in `index.html`, with ISO attendance dates, clock-time strings retaining fractional seconds and a source SHA-256 checksum.

| Sheet | Rows |
| --- | ---: |
| fact_attendance | 2,000 |
| answer_key | 2,000 |
| data_dictionary | 14 |

There are 200 distinct employee IDs. Attendance dates span **2024-10-01 to 2026-09-20**. The latest attendance date is a snapshot reference, not a live reporting clock. This is synthetic ERP-style demonstration data. No employee dimension or names are invented. Approval statuses are Approved (1,934) and Pending (66). Labels contain 200 Y and 1,800 N rows.

Editing the workbook does not refresh the embedded app automatically. Refreshing requires re-extracting sheets/checksum and reconciling rules, counts and documentation. Invalid source fields, duplicate/missing IDs, incomplete labels, unexpected statuses, overnight rows or disagreement with the audited snapshot produce a visible error instead of a misleading clean dashboard.

## Validation

Each category is evaluated separately across all 2,000 attendance rows.

| Category | TP | FP | FN | TN | Precision | Recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Missing Clock-Out | 67 | 0 | 0 | 1,933 | 100% | 100% |
| Unapproved Leave | 66 | 0 | 0 | 1,934 | 100% | 100% |
| Excessive Overtime | 67 | 0 | 0 | 1,933 | 100% | 100% |

The union contains 200 unique rows with no category overlap. This count is not a blended metric. No proactive precision/recall is implied.

Read-only source checks confirmed unique attendance/answer-key IDs, complete one-to-one joins, valid dates and clock times, and zero overnight rows. DOM-based JavaScript checks verified category counts and confusion matrices, inclusive 12-hour boundary behavior, blank/leave exclusions, pending-only behavior, fractional-second calculations, search and employee filters, reset/sort, source evidence and separate CSV output. The workbook and embedded records were checked for exact source preservation. These checks do not substitute for visual browser QA.

## How to run

Download this folder and open **index.html** in a modern browser. No installation, server or internet connection is needed. Keep the README and `data/` beside it for their links.

Search by attendance or employee ID, filter by employee, and choose date, ID or duration ordering. Click an attendance ID to inspect the raw record, elapsed duration, matching rules and answer-key row. Export each displayed category separately; CSV includes the unrounded elapsed hours where available and the answer-key-agreement caveat. The app does not modify the source workbook.
