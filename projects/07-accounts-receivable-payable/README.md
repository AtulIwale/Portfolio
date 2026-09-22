# Accounts Receivable & Payable

An offline invoice evidence app with separate **AR (receivables)** and **AP (payables)** views. It keeps confirmed dataset flags separate from additional repeat-pattern reviews. There is no blended score, risk probability or combined accuracy metric.

## Results

| Category | AR invoices | AP invoices | Total | Assessment |
| --- | ---: | ---: | ---: | --- |
| Confirmed settlement risk | 12 | 10 | **22** | **Answer-key agreement: 100% precision / 100% recall** |
| Repeat-pattern review | 88 | 0 | **88** | **Not covered by answer_key — for manual review**; unscored |

The precision and recall statement means **agreement with the labeled dataset, not independent model validation**. Confirmed category membership comes directly from the supplied Y labels, so this agreement is by construction. “Confirmed” means confirmed by the workbook's answer key, not independently verified settlement risk.

## Problem and approach

### Business analysis

Unsettled customer and vendor invoices need traceable follow-up, but a repeated pattern does not have the same evidence status as a labeled settlement risk. Two distinct worklists preserve that difference. AR and AP are never netted against one another.

### Project management

Scope: a single offline HTML app, separate AR/AP views, two category worklists, search, project/status filters, amount or due-date ordering, category-specific CSV exports and invoice-level evidence. The headline category totals always describe the full workbook; worklist counts and amounts reflect the current account view and filters. GitHub Pages setup, live ERP connections and automated collection/payment actions are outside scope.

### Data analysis and classification

1. Join `fact_invoice.invoice_id` to `answer_key.invoice_id` exactly.
2. **Confirmed settlement risk:** select `is_settlement_risk = Y`. All 22 records are unpaid and have recorded status `Overdue` or `Disputed` in this snapshot. They consist of six AR invoices each from CUS0004 and CUS0023, plus ten AP invoices from V003.
3. Define an unsettled pattern record as a blank `payment_date` with recorded status `Overdue` or `Disputed`. Count these records by **account type and party ID** across the full snapshot.
4. **Repeat-pattern review:** select unsettled records from parties with at least two such invoices, excluding all confirmed-category invoice IDs. These are the remaining 44 AR invoices each from CUS0004 and CUS0023, giving 88. There are no additional AP review records.
5. Join AR parties to `dim_customer.customer_id` and AP parties to `dim_vendor.vendor_id`. Project IDs are shown as supplied; this workbook contains no project-name dimension.

Each of the two AR customers has 50 unsettled invoices, and V003 has ten. Repetition counts include the current invoice and are calculated before UI filters. A source-ID button opens the exact fact row, answer-key row, dimension row and all same-party invoices, including paid context records.

Default ordering is descending invoice amount, then invoice ID. Optional ordering uses earliest due date, then invoice ID, or invoice ID alone. These are simple worklist orders, not validated risk rankings or scores. Amounts are full invoice amounts in INR; no partial-payment or outstanding-balance field exists.

### AI and limitations

This is a deterministic dataset evidence viewer, not a trained or independently evaluated model. The confirmed category uses the answer key itself; its 100% agreement must not be presented as predictive accuracy. Repeat-pattern review has no labeled review target, and its quality is not scored. Future prediction would require features available at decision time and independent evaluation against later outcomes.

Dates and statuses are used as recorded. No current date is applied to redefine overdue status or calculate aging. Full-snapshot repetition may include records later than the invoice being reviewed and is not a point-in-time forecast. The data is synthetic, patterned on ERP structures.

## Data and provenance

The unchanged source workbook is [07_Accounts_Receivable_Payable_Corrected.xlsx](data/07_Accounts_Receivable_Payable_Corrected.xlsx), copied byte-for-byte from `projects/02-erp-intelligence-copilot/data/` in this repository. All five sheets are embedded as JSON in `index.html` for offline use. Dates are ISO strings, blank cells are null and amounts remain numeric INR values. The embedded payload also records the original workbook's SHA-256 checksum.

| Sheet | Purpose |
| --- | --- |
| fact_invoice | 1,000 invoices: 500 AR and 500 AP |
| answer_key | 1,000 settlement labels: 22 Y, 978 N |
| dim_customer | Customer names for AR joins |
| dim_vendor | Vendor names and source attributes for AP joins |
| data_dictionary | Original field definitions |

Invoice dates range from 2024-10-01 to 2026-06-19. There are 110 recorded unpaid invoices (100 AR and 10 AP) and 890 paid invoices (400 AR and 490 AP). The two worklists are disjoint and together contain those 110 unpaid records in this particular snapshot. This equality is a dataset result, not a claim that every future unpaid invoice is a repeat pattern.

Editing the workbook does **not** refresh the embedded snapshot automatically. Refreshing requires re-extracting its sheets into the `source-data` JSON element and rechecking category definitions, counts and documentation. The app deliberately blocks rendering if the embedded snapshot violates its documented counts or integrity checks.

## Verification and interpretation

Confirmed-category membership is compared with the same source Y labels: 22 matched positives, zero extra positives, zero missed positives and 978 remaining records. Precision is 22/22 and recall is 22/22. This is label reconciliation, not an independent classifier test. Repeat-pattern records carry N for **settlement risk**; that is not a ground-truth label for **manual review**. No review-category or blended precision/recall is computed.

Source checks cover unique invoice, label and party IDs; complete one-to-one invoice/label coverage; valid Y/N labels; complete type-specific party joins; nonnegative amounts; due/payment dates not before invoice dates; and consistency of payment dates with recorded Paid/Overdue/Disputed status. Category counts and the AR/AP split are checked against the source. Failed integrity checks display an error rather than an empty or apparently clean dashboard.

JavaScript checks in an isolated DOM stub verify embedded-source initialization, category membership and amounts, AR/AP splits, the empty AP manual-review state, search and project/status filters, ordering, source-evidence content, CSV content and the malformed-data error gate. Source workbook and embedded records reconcile. Visual browser rendering, keyboard interaction and native download behavior could not be verified in this environment; they remain a manual check when opening the app.

## How to run

Download this folder and open **index.html** in a modern browser. No server, package installation, internet connection or external dependency is required. Keep `data/` and `README.md` beside the HTML file to use its source-download and documentation links.

Choose Receivables or Payables, filter the worklists and click an invoice ID for source evidence. CSV exports contain only the currently displayed category and account type, with the assessment wording and source label preserved. The app does not modify the workbook or store review decisions.

No GitHub Pages configuration or deployment was added for this project.
