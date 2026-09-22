# Real Estate Sales

Coverage-tier offline booking review. GitHub-only delivery; no Pages configuration or hosting setup is included.

## Problem

The supplied labels describe two separate booking patterns: recorded cancellations and enquiries within a broker-led project cohort. Combining them into one risk score would obscure their different meanings. Claims about stalled progression or recent inactivity also require evidence that this snapshot does not contain.

## Approach

### Business Analysis

Apply two deterministic raw-field rules:

1. **Cancellation-cluster risk:** `stage = Cancelled`, customer `lead_source = Broker`, and unit `project_id` in `{PRJ001, PRJ011, PRJ021}`.
2. **Stalled-enquiry risk:** `stage = Enquiry`, `lead_source = Broker`, and the same project allowlist.

The allowlist is explicit and **dataset-specific, identified from the labeled data, not a general risk cohort**. No amount, age or learned threshold is used. Both categories are disjoint and each contains 25 bookings: ten PRJ001, ten PRJ011 and five PRJ021 records.

“Stalled-enquiry” is the dataset category name. The rule does not independently establish inactivity, duration of delay or low booking value, despite those descriptions appearing in the answer-key reasons. Cancellation is an observed recorded stage, not a prediction of future cancellation.

**Proactive review** is separate and unscored, labeled **Not covered by answer_key**:

| Check | Status | Missing support |
| --- | --- | --- |
| Agreement/Registered stage stalled | **Not evaluated** | No progression history or duration threshold |
| High-value booking with no recent activity | **Not evaluated** | No last-activity field, high-value threshold or inactivity threshold |

Registered stage alone is not evidence of a stalled sale. No missing thresholds or activity history are invented.

### Project Management

Scope: one self-contained HTML app, unchanged workbook in `data/`, two separate worklists, project/search filters, date/amount/ID ordering, source-evidence dialogs, separate CSV exports and a proactive-check status table. No live CRM integration, record editing, automated customer decisions, external scripts or blended metric.

### Data Analysis & Data Science

Join `fact_booking.unit_id` to `dim_unit.unit_id` to obtain project and unit details; join `customer_id` to `dim_customer.customer_id` for lead source and customer name. Run classification using those raw fields. Join `answer_key` by `booking_id` afterward for evaluation.

The answer key contains one `is_at_risk` target and a reason field. For separate category evaluation, Y labels with reasons beginning “Cancellation cluster linked to …” identify cancellation targets. Y labels with the exact reason “Low booking amount on a long-stalled enquiry in a repeat-risk project cohort.” identify enquiry targets. All Y reasons are accounted for. Each rule is compared with its own reason-defined target across all 500 bookings; the other category's positive labels count as negatives for that specific category. This is not blended evaluation.

Reporting reference: **2026-09-20**, the latest `stage_date`. It is a **recorded-stage date, not a verified last-activity date**. The workbook has no separate activity-date field, so no activity-based aging or current-clock calculation is performed.

Filters affect displayed records and booking/token-amount totals only, not the whole-workbook metrics. Ordering by amount is a display option, not a risk ranking. Amounts remain INR. `booking_amount` is a booking/token amount, not sale value, outstanding receivables or confirmed loss; `list_price` is a separate unit attribute shown in source evidence.

### AI

**Deterministic, not a trained model.** No ML, training, probability or forecast. Both categories display **“Answer-key agreement: 100% precision / 100% recall.”** This is agreement with the labeled dataset, **not independent validation**. The allowlist was identified from the same labeled data.

All 25 Cancelled bookings in this snapshot are Y-labeled, so `stage = Cancelled` alone also reproduces the cancellation category. The Broker and project conditions add no discrimination for that category in this workbook. The enquiry rule does not independently test the label reason's claims about low amounts or long-stalled enquiries.

## Data

[11_Real_Estate_Sales.xlsx](data/11_Real_Estate_Sales.xlsx) is copied byte-for-byte from the supplied attachment. All five sheets are embedded as JSON in `index.html`, with numeric amounts, ISO date strings and the source SHA-256 checksum for provenance.

| Sheet | Rows |
| --- | ---: |
| dim_unit | 350 |
| dim_customer | 300 |
| fact_booking | 500 |
| answer_key | 500 |
| data_dictionary | 20 |

Stage dates span 2024-10-01 through 2026-09-20. The snapshot contains 150 Enquiry, 125 Agreement, 100 Registered, 100 Booked and 25 Cancelled records. The answer key has 50 Y and 450 N labels. This is synthetic ERP-style demonstration data, not evidence of real-world customer risk.

Editing the workbook does not refresh the embedded snapshot. Refreshing requires re-extracting its sheets and checksum into `source-data` and reconciling the reason mapping, rules, counts and caveats. The app blocks rendering if integrity checks fail or the snapshot no longer supports the documented category agreement.

## Validation

| Category | Flagged bookings | TP | FP | FN | TN | Precision | Recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Cancellation-cluster | **25** | 25 | 0 | 0 | 475 | **100%** | **100%** |
| Stalled-enquiry | **25** | 25 | 0 | 0 | 475 | **100%** | **100%** |

Each category is evaluated independently over all 500 bookings. There are no overlapping bookings between the two categories. No combined precision/recall or risk score is reported.

| Project | Cancellation-cluster | Stalled-enquiry |
| --- | ---: | ---: |
| PRJ001 | 10 | 10 |
| PRJ011 | 10 | 10 |
| PRJ021 | 5 | 5 |

Neither proactive check has supporting labels or sufficient inputs. Both remain **Not evaluated**, with no precision/recall assigned. “Not evaluated” must not be interpreted as zero risk.

Source checks confirm unique booking, unit, customer and answer-key IDs; complete dimension and label joins; valid stage/date/amount fields; and recognized Y-label reasons. DOM-based JavaScript checks verify category counts and agreement, project/search/reset filters, evidence content, amount ordering, CSV content and reporting date. These checks do not substitute for visual browser QA.

## How to run

Download this folder and open **index.html** in a modern browser. No server, installation or internet connection is required. Keep `README.md` and `data/` beside the app for source and documentation links.

Search by booking, unit, customer name/ID or project ID; select a project or change display order. Click a booking ID for its original booking, unit, customer and answer-key records. Export each displayed category separately. The app does not modify the source workbook.
