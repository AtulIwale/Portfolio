# Contract Lifecycle Intelligence

## Problem
High-risk clauses can remain unreviewed while contracts approach expiry. Automatic renewals can then reduce the opportunity to renegotiate or exit on suitable terms. This demo places clause risks and upcoming expiries in one evidence-based review worklist.

## Approach

### Business Analysis
High-risk means the supplied risk_category is High. Proactive renewal review means auto_renew = Y and end_date is between the dataset reference date and 90 days later, inclusive. The categories are separate: High-risk flags are validated against the answer key; renewal reviews are explicitly unscored because the answer key does not cover them.

The checks are domain-neutral: contract clauses, counterparties, expiry dates and renewal provisions apply to services, equipment, property and other commercial agreements outside construction too. No legal judgment is inferred or automated.

### Project Management
Scope: one offline HTML app, all 200 contracts and 800 clauses, ranked review findings, full-contract clause views and separate validation and proactive-review summaries. Priorities were source traceability, stable date handling and honest interpretation of the answer key. Contract editing, notifications, legal decisions and live system integration are outside this build.

### Data Analysis & Data Science
Join fact_clause to dim_contract on contract_id. Validate uniqueness, foreign keys, categories and date order. The reference date is the maximum of all start_date and end_date values: **2026-09-22**. The inclusive forward-looking window ends **2026-12-21**. Dates are compared at UTC midnight and are independent of the browser's current date.

Flag High-risk clauses and, separately, every clause belonging to a qualifying auto-renewing contract. Count the union once for the overall worklist. Rank High-risk first, then renewal-only; ties use end date ascending, contract value descending and clause_id. A contract value is repeated context, not an amount at risk or a savings estimate.

### AI
This is a deterministic category-and-date rules engine, not a statistical model. It does not read clause text to infer risk and does not use answer-key labels to generate flags. A future NLP version could extract notice periods, identify problematic wording and cite supporting text, evaluated against independently reviewed contracts and subject to human review. No such model is included here.

## Data
Synthetic data patterned on real contract structures. The unchanged source workbook is `data/05_Contract_Lifecycle_Intelligence.xlsx`; its contents are embedded as JSON in index.html, with no external dependencies.

| Sheet | Rows | Schema |
|---|---:|---|
| dim_contract | 200 | contract_id, contract_name, counterparty, contract_value (INR), start_date, end_date, auto_renew |
| fact_clause | 800 | clause_id, contract_id, clause_type, clause_text_summary, risk_category |
| answer_key | 800 | clause_id, is_flagged, flag_reason |
| data_dictionary | 19 | sheet_name, column_name, data_type, meaning |

Editing the workbook does not automatically refresh the HTML's embedded snapshot.

## Validation
### High-risk clauses only
**Precision: 100.0% (80/80). Recall: 100.0% (80/80).** True positives: 80; false positives: 0; false negatives: 0; true negatives: 720. The answer key flags exactly the 80 clauses whose supplied risk_category is High. Perfect agreement is expected for this deterministic category check on aligned synthetic labels. It does not establish independent legal-risk detection, statistical-model quality or real-world generalization.

### Proactive renewal review — not scored
**32 clauses across 8 contracts**, not covered by the answer key. No precision or recall is assigned to this category, and no combined precision/recall is reported. Two clauses are also High-risk; the other 30 are renewal-only reviews, not classification false positives.

Together, the categories create **110 unique flagged clauses across 47 contracts**.

### Data checks and limits
- No duplicate primary keys, missing clause/contract joins, missing answer-key matches or contracts ending before their start dates were found.
- The workbook contains no reporting/as-of field. The approved reference uses its latest date, which is itself an end date. All eight qualifying auto-renewals expire on that exact date; none expires later. The app displays this limitation explicitly and does not substitute today's date.
- Expiry review is not notice-deadline detection. One supplied clause summary specifies 120 days' notice, so a 90-day expiry window may be too late for that action. The app makes no claim that cancellation remains available.
- Renewal flags are contract-level prompts repeated on all clauses for context. Opening a contract shows all four clauses, including any without a High-risk flag.

## How to run
Open index.html in any browser, or view it live at [Pages link](https://atuliwale.github.io/Portfolio/projects/05-contract-lifecycle-intelligence/).
