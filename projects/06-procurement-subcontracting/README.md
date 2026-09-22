# Procurement & Subcontracting

## Problem
Supplier delays are often reviewed only after they disrupt a project schedule. A shared view of delivery exceptions and vendor history helps teams prioritize follow-up and future sourcing decisions.

## Approach

### Business Analysis
Severe delay means 18+ calendar days late; minor delay means 1–17 days late and is an unscored proactive review. A repeat-late vendor has at least two late POs, of any severity.

### Project Management
Scope: one offline HTML app with two ranked worklists, vendor evidence, search and separate severe-delay validation. Live ERP integration, open-order forecasting and purchasing actions are outside scope.

### Data Analysis & Data Science
Join vendors by vendor_id; days late = actual delivery date − promised date, using UTC dates. Within each category, rank descending by **days late × (1 + vendor late-delivery rate)**, where the rate is all late POs / all POs for that vendor, including the current PO; ties use days late then po_id.

### AI
This is a deterministic historical review, not a trained predictive model; ratings are context, not score inputs. A future model would need features available before delivery and independent, time-based evaluation to predict future delays without leakage.

## Data
Synthetic data patterned on real ERP structures. The unchanged source is `data/06_Procurement_Subcontracting.xlsx`; the HTML embeds its sheets as JSON and needs no external dependencies.

| Sheet | Rows | Fields |
|---|---:|---|
| dim_vendor | 60 | vendor_id, vendor_name, vendor_category, vendor_rating |
| fact_purchase_order | 800 | po_id, project_id, vendor_id, item_description, order_date, promised_date, actual_delivery_date, po_value |
| answer_key | 800 | po_id, is_at_risk, risk_reason |
| data_dictionary | 19 | sheet_name, column_name, data_type, meaning |

Workbook edits do not automatically refresh the embedded snapshot. All POs already have actual delivery dates; full-snapshot vendor history can include deliveries after an individual PO, so the score is not a historical forecast or a probability.

## Validation
**Severe delay only: precision 100.0% (80/80), recall 100.0% (80/80).** True positives 80, false positives 0, false negatives 0, true negatives 720. The supplied labels exactly match the 80 severe delays (18–55 days); perfect agreement is expected for these aligned synthetic rule examples, not evidence of real-world predictive accuracy. Labels are used for validation only.

**Minor delay: 476 POs, unscored proactive review—not covered by the answer key.** No minor-delay or blended precision/recall is reported. Minor POs are not-severe when testing the severe-delay classifier; that does not evaluate the proactive-review category.

Across 800 POs, 556 arrived late and 244 arrived on time or early. **54 vendors** have 2+ late deliveries. The actual minor delays are 1–9 days; this snapshot contains no examples at 10–17 days.

Checks found no duplicate IDs, missing vendor/label joins, missing delivery dates or delivery/promise dates before order dates. The original label mismatch for “any late delivery” is addressed by the approved category split without altering data. Ranking is tested separately from classification; precision/recall does not establish ranking quality.

## How to run
Open index.html in any browser.
