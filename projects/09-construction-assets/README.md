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

---

## Machine-learning upgrade: predicting breakdowns before they happen

**Live app:** [ml.html](https://atuliwale.github.io/Portfolio/projects/09-construction-assets/ml.html) · **Notebook:** [notebooks/predictive_maintenance.ipynb](notebooks/predictive_maintenance.ipynb) · **Data:** [data/09_Construction_Assets_v2.xlsx](data/09_Construction_Assets_v2.xlsx)

The rule above confirms a failure pattern only once it has fully happened. The upgrade asks the question a plant manager actually has on Monday morning: **which machines are likely to break down in the next four weeks, and which ones should the workshop inspect this week?**

### Data added (same asset register, original sheets unchanged)
| Sheet | Rows | What it holds |
| --- | ---: | --- |
| dim_asset_telematics | 80 | Telematics-fitted plant from `dim_asset`: make/model, year, diesel or electric, hydraulic system, opening hour meter, OEM service interval, hire-in rate |
| fact_telemetry_weekly | 6,270 | Weekly readings Oct 2024 to Sep 2026: hours, load, vibration, operating temperature, hydraulic pressure, fault codes, monthly oil-iron samples, site city and project |
| fact_maintenance_event | 1,186 | 725 preventive services, 70 planned corrective repairs, 249 breakdowns (root cause, downtime, cost) and 142 site transfers |

Total stations and bar-cutting machines are not telematics-fitted, so they are excluded. The data is synthetic but built on realistic wear behaviour: faults develop over several weeks, heat and dust speed up wear, late servicing costs life, sensors drop out, and some damage is sudden and gives no warning.

### Method
1. **Label:** a breakdown in the next 4 weeks. Weeks when the machine is broken down or in transit are not scored.
2. **Features (past data only):** 4-week averages, 6-week trends and readings compared with the machine's *own* normal level (weeks t−16 to t−4), last oil-iron result and its change, fault codes, hours since service, weeks since last repair, age, hour meter and class. 33 features in total.
3. **Time-based split:** train Oct 2024 to Dec 2025, validation Jan to Mar 2026 (tuning, SVM calibration, threshold), test Apr to Aug 2026 (used once).
4. **Baselines:** OEM alarm limits (vibration > 7.1 mm/s, temperature > 105 °C, pressure < 85%, 8+ fault codes) and a PM-overdue rule.
5. **Models:** Logistic Regression, K-Nearest Neighbours, Decision Tree, Random Forest, **XGBoost**, **SVM (RBF kernel, Platt-calibrated)** and a Neural Network (MLP), each tuned on the validation months by PR-AUC.
6. **Business evaluation:** missed breakdown = actual repair + replacement hire for the downtime; caught breakdown = planned repair at 35% of the repair cost + 1 day of hire; every alert = a Rs 6,000 inspection + half a day of hire.
7. **Explainability:** SHAP values for XGBoost, globally and for each machine in the live worklist.

### Results on the test months (Apr to Aug 2026)
| Model | PR-AUC | ROC-AUC | Breakdowns caught with 10 inspections a week | Saving vs run-to-failure (cost-optimal threshold) |
| --- | ---: | ---: | ---: | ---: |
| **XGBoost** | **0.582** | 0.838 | **71%** | 50% |
| Random Forest | 0.577 | 0.862 | 66% | 53% |
| Neural Network (MLP) | 0.531 | 0.823 | 65% | 50% |
| **SVM (RBF kernel)** | 0.514 | 0.820 | 60% | 49% |
| Logistic Regression | 0.486 | 0.831 | 57% | 47% |
| K-Nearest Neighbours | 0.446 | 0.800 | – | – |
| Decision Tree | 0.397 | 0.760 | – | – |
| OEM alarm limits | – | – | 16% caught (fires too late) | 4% |
| Random ranking | 0.18 | 0.50 | 47% | – |

At its cost-optimal threshold, XGBoost caught 69 of 82 test-period breakdowns (84%) with a median of 4 weeks' warning. That brought breakdown-related cost down from Rs 422 lakh to Rs 212 lakh. By root cause it caught 100% of bearing/gear wear, 95% of overheating, 87% of hydraulic and 85% of electrical failures, but only 20% of sudden external damage, which no sensor model can predict.

### XGBoost vs SVM: what I learned
- **Tree models suit this data better.** A third of the fleet has no hydraulic sensor, oil results come monthly, and telematics drops out. XGBoost learns what a missing value means. The SVM needs values imputed and every feature scaled, and an imputed median looks like a real reading.
- **Interactions matter.** A temperature rise means different things for an electric hoist and a diesel excavator in a Nagpur summer. Trees split on both; an RBF kernel treats everything as one distance.
- **The SVM is still useful.** It is far better than the alarm limits, and it gives an independent second opinion. When the two models disagree strongly, that machine is worth a closer look.
- **Ranking beats thresholds.** A workshop has limited capacity, so "inspect the top 10 each week" is the realistic operating rule, and that is where the gap between models shows most clearly.

### Limits
The telemetry is synthetic with known wear physics, so real fleets will be noisier. The rupee savings depend on the inspection and planned-repair cost assumptions and on a five-month test window. The models are trained up to Dec 2025 and should be retrained quarterly against real breakdown reports.

### Files added
| File | Purpose |
| --- | --- |
| `ml.html` | Live worklist, machine history charts, what-if sliders, model comparison and cost simulator. XGBoost and the SVM run in the browser, and a self-check matches the Python scores |
| `notebooks/predictive_maintenance.ipynb` | Audit, sensor analysis, features, seven models, business evaluation, SHAP and export |
| `model/pdm_export.json` | 400 XGBoost trees, 1,285 SVM support vectors, calibration, test predictions and machine histories |
| `data/09_Construction_Assets_v2.xlsx` | Original four sheets unchanged, plus telematics, maintenance events and a data dictionary |

Author: Atul Iwale
