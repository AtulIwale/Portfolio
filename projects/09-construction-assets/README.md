# Construction Assets — Fixed & Movable

Coverage-tier, self-contained offline maintenance-review app. GitHub-only delivery; no Pages configuration is included.

## Problem

Declining condition and recurring symptoms can identify a maintenance pattern worth investigating. Purchase-date and usage-meter inconsistencies need a different review, while overdue-service and excessive-usage claims require thresholds this workbook does not supply. The app keeps these categories separate, with source evidence and no blended score.

## Approach

### Business Analysis

**Confirmed pre-failure pattern:** sort each asset's complete maintenance history by service date and inspect every consecutive three-log window. Dates must strictly increase, ratings must be exactly **3 → 2 → 1**, and **each log** must contain all three symptom terms: overheating, vibration and hydraulic leakage. Matching is case-insensitive and accepts whitespace or a hyphen between hydraulic and leakage. Flag all three logs, taking the union of IDs if windows overlap. No asset IDs are hard-coded.

The phrase matcher is literal, not natural-language understanding: it does not interpret negation or alternative symptom descriptions. This is appropriate to the observed source wording, not a general diagnostic claim.

**Data quality review — unscored, not covered by answer_key:**

- Service date strictly before recorded purchase date: **132 logs across 75 assets**. These may represent pre-acquisition history or inaccurate dates; no source dates are altered.
- Cumulative usage hours lower than the immediately preceding log for the same asset: **50 transitions**. Meter resets, replacement or errors may explain these; they are not automatically maintenance failures.

**Proactive review — unscored, not covered by answer_key:**

- Past expected useful life: **0 assets** as of **2026-08-27**, the latest service date. Compare the report date strictly after the purchase-date anniversary plus `expected_life_years`. February 29 anniversaries use February 28 in non-leap years.
- Overdue service interval: **Not evaluated** because no required interval is defined.
- Usage above allowable limit: **Not evaluated** because no usage-hour limit is defined. Expected life in years cannot be converted to allowed hours without an operating-duty assumption, which is not invented.

The categories may overlap, and their counts use different units: logs, transitions and assets. They must not be added into a total risk score. Zero proactive matches does not establish asset health.

### Project Management

Scope: one offline app, unchanged workbook in `data/`, confirmed-pattern worklist, separate data-quality worklists, proactive-check status, Fixed/Movable and search filters, source dialogs and category-specific CSV exports. No live maintenance-system connection, record modification, automated decisions, external scripts or Pages hosting setup.

### Data Analysis & Data Science

Join maintenance logs to assets by `asset_id` and to labels by `log_id`. Check unique IDs, complete label and asset joins, valid source dates, ratings 1–5 and nonnegative numeric cumulative hours. Tied service dates block pattern interpretation rather than being assigned an arbitrary order. No ties occur in the source.

The classifier uses raw maintenance fields only; answer-key labels are joined afterward for comparison. Classification runs on the full snapshot before UI filters. Evidence shows the original asset record, selected maintenance row and label, qualifying sequence IDs and complete chronological asset history with labels. Decreasing usage and pre-purchase service are retained as explicit review findings rather than excluded or repaired.

The reporting date is the latest service date, **2026-08-27**, not the current system date. The entire snapshot is used for pattern recognition. CSV exports preserve assessment wording and the displayed category/filter scope.

### AI

**Deterministic, not a trained model.** There is no ML, training, probability or forecast. The displayed metric is **“Answer-key agreement: 100% precision / 100% recall.”** This means agreement with the labeled dataset, **not independent discrimination or model validation**.

Symptom-keyword matching alone also selects exactly the same 60 Y-labeled logs. The consecutive-decline requirement adds no discrimination in this workbook. The rule was audited against the same synthetic labels, not independently validated on unseen data.

Flagging the first two logs is retrospective: it depends on observing the third log. This is not advance failure prediction or proof of actual asset failure. Any future predictive use would need information available at decision time and independent outcome-based evaluation.

## Data

[09_Construction_Assets.xlsx](data/09_Construction_Assets.xlsx) is copied byte-for-byte from the supplied attachment. All four sheets are embedded as JSON in `index.html`, with ISO date strings, numeric quantities and the workbook's SHA-256 checksum for provenance.

| Sheet | Rows |
| --- | ---: |
| dim_asset | 100 |
| fact_maintenance_log | 600 |
| answer_key | 600 |
| data_dictionary | 18 |

This is synthetic ERP-style demonstration data. Service dates span 2024-10-01 to 2026-08-27. The answer key has 60 Y and 540 N rows. Each of the 20 qualifying assets, AST0001 through AST0020, has one qualifying three-log sequence; membership is calculated from fields, not that ID range.

Editing the workbook does not automatically refresh the embedded app. Refreshing requires re-extracting the sheets and checksum into `source-data` and rerunning rule/count reconciliation. The app fails visibly if its embedded source no longer supports the documented confirmed-category agreement.

## Validation

### Confirmed pre-failure pattern only

| True positives | False positives | False negatives | True negatives | Precision | Recall |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 60 | 0 | 0 | 540 | **100%** | **100%** |

The comparison unit is the maintenance log across all 600 records, not the asset or sequence. All three logs of each qualifying sequence are counted.

| Asset type | Qualifying assets | Confirmed logs |
| --- | ---: | ---: |
| Fixed | 5 | 15 |
| Movable | 15 | 45 |
| Total | **20** | **60** |

### Separate unscored reviews

| Section | Check | Result | Precision / recall |
| --- | --- | --- | --- |
| Data quality | Service before purchase | 132 logs / 75 assets | Not covered by answer_key |
| Data quality | Decreasing cumulative usage | 50 transitions | Not covered by answer_key |
| Proactive | Past expected useful life | 0 assets | Not covered by answer_key |
| Proactive | Overdue service interval | Not evaluated | No defined interval or supporting labels |
| Proactive | Usage limit | Not evaluated | No defined hour limit or supporting labels |

No category other than the confirmed pattern receives precision or recall. No blended metric is calculated. An N label for pre-failure patterns is not a negative ground-truth label for data quality or proactive review.

Read-only workbook audit confirmed unique IDs, complete joins and no tied service dates. DOM-based JavaScript checks verified counts, Fixed/Movable filters, search/reset, full-sequence evidence, symptom matching and leap-year anniversaries. These checks do not substitute for visual browser QA.

## How to run

Download this folder and open **index.html** in a modern browser. No installation, server or internet connection is required. Keep `README.md` and `data/` beside the HTML file for the source and documentation links.

Filter by Fixed/Movable or search for an asset or log. Click a log ID for full source evidence and asset history. Export each displayed confirmed or data-quality worklist separately. Proactive checks remain a clearly labeled status table. The app never edits the workbook.
