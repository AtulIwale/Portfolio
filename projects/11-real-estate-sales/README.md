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

---

## Machine-learning upgrade: cancellations, pricing and buyer segments

**Live app:** [sales_ml.html](https://atuliwale.github.io/Portfolio/projects/11-real-estate-sales/sales_ml.html) · **Notebook:** [notebooks/sales_cancellation_pricing.ipynb](notebooks/sales_cancellation_pricing.ipynb) · **Data:** [data/11_Real_Estate_Sales_v2.xlsx](data/11_Real_Estate_Sales_v2.xlsx)

The rules above reproduce two labelled booking patterns. A residential developer's sales team has three forward-looking questions:
1. **Which new bookings will cancel within a year**, so the CRM team can step in (loan help, a payment-plan change, a site visit)?
2. **What will each unsold flat actually fetch** after the discount the market demands?
3. **Who are our buyers**, beyond "end user" and "investor"?

### Data added (original workbook unchanged)
| Sheet | Rows | What it holds |
| --- | ---: | --- |
| dim_project_re | 8 | Residential launches in Pune, Mumbai (Thane), Bengaluru, Hyderabad, Noida, Ahmedabad and Chennai: launch date, launch rate, escalation, RERA possession, progress |
| dim_unit_re | 2,661 | Every flat: tower, launch phase, floor, 1–4 BHK, carpet area, facing (including premium views), corner, sold/unsold |
| dim_buyer | 2,159 | Buyer type (end user, investor, NRI), age band, income, residence, co-applicant, repeat customer |
| fact_booking_re | 2,159 | Channel, payment plan (construction-linked, down payment, subvention), list rate, floor rise, PLC, discount, achieved rate, agreement value, booking amount %, home loan and sanction, LTV, site visits, days to decide, lateness on the first demand, cancellation date and reason |
| price_list_monthly | 291 | Base price-list rate per project per month |
| city_price_index | 56 | Monthly resale price index by city, including a 2025 slowdown in Noida and Hyderabad |

The data is synthetic but follows real Indian residential sales patterns. Broker deals carry bigger discounts and thinner booking amounts. Subvention plans attract investors. Diwali and March quarter-end bring offers, and loan rejections drive cancellations. Across 1,723 bookings at least a year old, 12.9% cancelled within the year, with 2% of the agreement value forfeited.

### Method
- **Cancellation model:** each booking is scored **45 days after booking**, once the first instalment is due, using only facts known by then (23 features). Seven classifiers are compared: **Logistic Regression, KNN, SVM (RBF), Naive Bayes, Decision Tree, Random Forest and XGBoost**. They are tuned by PR-AUC on Jul to Dec 2024 and tested once on Jan to Aug 2025, a period that includes a market slowdown.
- **Price model:** Ridge, KNN regression, SVR, Random Forest and **XGBoost** predict the achieved rate per sq ft from the price list, floor rise, view premium, deal type, project age and market trend. They train on bookings before Jul 2025, test on Jul 2025 to Aug 2026, and are compared with the price list less the average discount.
- **Segments:** **K-means** on buying behaviour (income, age, ticket size, loan-to-value, EMI burden, booking amount, site visits and days to decide), with buyer type deliberately left out.

### Results
**Cancellations (test: 465 bookings, 60 cancelled):**

| Model | PR-AUC | ROC-AUC | Cancellations found calling the riskiest 20% |
| --- | ---: | ---: | ---: |
| **Random Forest** | **0.518** | 0.825 | **65%** |
| XGBoost | 0.506 | 0.811 | 60% |
| Naive Bayes | 0.488 | 0.827 | 65% |
| Logistic Regression | 0.472 | 0.816 | 60% |
| SVM (RBF) | 0.429 | 0.763 | 58% |
| KNN | 0.401 | 0.767 | 58% |
| Decision Tree | 0.367 | 0.789 | 47% |
| Random call list | 0.129 | 0.500 | 20% |

The strongest drivers, as logistic odds ratios, are:
- days late on the first demand (×1.73 per standard deviation),
- EMI-to-income (×1.44),
- investor buyers (×1.40),
- a loan not yet sanctioned (×1.37),
- broker deals (×1.16).

A sanctioned loan, more site visits and a larger booking amount lower the risk. The browser app uses the logistic model because it is within noise of the best model and every score can be explained.

**Pricing (test: 550 bookings):** XGBoost prices flats with a 2.0% error, against 2.3% for the price list less the average discount. It also removes the baseline's +1.2% bias. KNN regression was worst, at 9.6%, because distance treats very different flats as neighbours. Applied to the 760 unsold flats, the model expects **₹890 crore** against ₹946 crore at list prices. The implied discount ranges from about 0% for Aurum Bay, the newest launch, to 9% for Harbour Heights.

**Segments (5):**
- *Stretched buyers (high EMI)* cancel 28% of the time.
- *Budget first-home buyers* cancel 14% of the time.
- *Careful researchers* and *Affluent upgraders* cancel 11% of the time.
- *Cash buyers* cancel just 6% of the time. They turn out to be mostly investors and NRIs, even though buyer type was never an input.

### What I learned
- **Small data favours simple models.** With under 900 training bookings, logistic regression, Naive Bayes and Random Forest are within noise of each other. The explainable model is the sensible choice for a CRM team.
- **Timing is the feature.** How late the first payment is, and whether the loan is sanctioned, say more than anything known on booking day.
- **A good price list is hard to beat.** The model's gain comes from knowing which deals need a bigger discount.

### Limits
The data is synthetic. The model ranking is fragile at this sample size and should be re-checked each quarter. A risk score says who to call, not what the call achieves: retention impact needs an A/B test.

### Files added
| File | Purpose |
| --- | --- |
| `sales_ml.html` | CRM call list with reasons and what-if (loan sanction, payment lateness, booking amount), a pricer for every unsold flat with a deal-type what-if, inventory value, model comparisons, segments and odds ratios. The logistic model and 800 XGBoost price trees run in the browser, and a self-check matches the Python results |
| `notebooks/sales_cancellation_pricing.ipynb` | Audit, cancellation analysis, seven classifiers, calibration, odds ratios, five price models, K-means segments, live scoring and export |
| `model/sales_export.json` | Logistic model, XGBoost price trees, live bookings, unsold flats and results |
| `data/11_Real_Estate_Sales_v2.xlsx` | Projects, flats, buyers, bookings, monthly price list and city price index |

Author: Atul Iwale
