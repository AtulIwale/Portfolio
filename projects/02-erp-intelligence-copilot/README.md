# Construction ERP Intelligence Copilot

## Problem
Cost performance, delivery issues and invoice settlements usually sit in separate ERP views. A project can look healthy in one view while unresolved exposure remains in another. This app brings the three domains together and lets a reviewer open the exact source transaction behind every flag.

## Approach

### Business Analysis
Cost, procurement and settlement were chosen because they connect earned progress, material delivery and cash flow. “Multi-risk” means **at least one active flag in any domain**, following the requested definition; it does not require flags in two or three domains.

| Domain | Active flag | History shown |
| --- | --- | --- |
| Cost & Margin | answer_key.is_margin_risk = Y in the project's latest available cost month | Earlier Y records, in an expandable history |
| Procurement | answer_key.is_at_risk = Y and actual_delivery_date is blank | All delivered Y orders remain visible as historical delivery flags |
| Receivables & Payables | answer_key.is_settlement_risk = Y, payment_date is blank, and status is not Paid, Cancelled, Canceled or Void | Both AR and AP Y records; settled records would remain visible as history |

“Fully clean” means **no active source flags in this snapshot**, not an absence of historical issues or proof that every business risk has been tested. Latest-month cost risk comes from source labels; it does not rerun Project 1's historical two-month-streak model. A source-level flag can coexist with an aggregate CPI above 0.90.

### Project Management
Scope: a single offline HTML file, all 30 projects, three domain panels, a project selector, portfolio summary and transaction-level evidence. Priority was complete joins and accurate active-versus-historical status before narrative generation. No server, external dependencies, live ERP connection or automated decisions are included. The project folder contains index.html, this README and the corrected AR/AP source workbook in data/.

### Data Analysis & Data Science
- Join **all** fact_cost_value, fact_purchase_order and fact_invoice rows directly on project_id, using dim_project for project_name and region.
- The Copilot cross_reference sample is kept and checked for provenance. Its 450 sample IDs do **not** filter the full 3,000 fact rows.
- Join source answer keys using row_id, po_id and invoice_id. Join vendors and customers through their dimension IDs; join cost-code descriptions by cost_code.
- For the latest cost month, sum earned_value, actual_cost and budgeted_cost before calculating CPI = earned / actual and SPI = earned / budgeted. SPI is a budget-based schedule proxy. Display the source IDs for every aggregate.
- Each flagged item has a clickable exact source ID. It opens the full original fact record, matching answer_key row and relevant dimension record.
- Fail visibly on duplicate IDs, invalid labels, missing dimension joins or mismatched cross-reference IDs; do not treat unmatched data as clean.

Dates and statuses are read as recorded, without applying today's date as a cutoff. The workbooks are snapshots with different accounting and transaction dates, not a synchronized live feed. A recorded delivery/payment date indicates completion in that supplied snapshot. No synthetic rows or risk labels are invented.

### AI
This version is a deterministic evidence viewer, not a trained model or generative AI. A future version could generate a short risk narrative from the selected project's verified active flags. Every sentence would need source-ID citations, status-aware wording and checks against unsupported amounts or claims.

## Data
This project has **no separate synthetic dataset of its own**. It reads and joins the supplied data already built for Projects 1, 6 and 7; all source sheets are embedded as JSON inside index.html for offline use.

| Supplied workbook | Role | Fact rows |
| --- | --- | ---: |
| 01_Project_Cost_Margin_Intelligence(1).xlsx | Project/cost-code dimensions, cost facts and cost labels | 1,200 |
| 06_Procurement_Subcontracting.xlsx | Vendor dimension, purchase orders and delivery-risk labels | 800 |
| [07_Accounts_Receivable_Payable_Corrected.xlsx](data/07_Accounts_Receivable_Payable_Corrected.xlsx) | Customer/vendor dimensions, AR/AP invoices and corrected settlement-risk labels; embedded in index.html | 1,000 |
| 02_Construction_ERP_Intelligence_Copilot.xlsx | 30-project cross-reference sample and its dictionary | No new facts |

Synthetic data patterned on real ERP structures. Dates are embedded as ISO dates, blank cells as null, and monetary values remain INR. The source files are not modified.

## Validation
Under the active-flag definitions above:

| Measure | Result |
| --- | ---: |
| Total projects | 30 |
| Multi-risk projects (at least one active flag) | **9** |
| Fully clean (no active flags) | **21** |
| Active cost flags / affected projects | 5 / 5 |
| Historical delivery flags | 80 |
| Unresolved delivery flags | 0 |
| Active settlement flags / affected projects | 22 / 6 |

The five cost-risk projects and six settlement-risk projects overlap on two projects, giving nine distinct affected projects. The 120 total cost flags include 115 historical records. All 80 delivery-risk orders have delivery dates, so they are shown but excluded from active risk.

Active-risk project IDs: PRJ001, PRJ006, PRJ010, PRJ011, PRJ016, PRJ019, PRJ021, PRJ025, PRJ026.

This is reconciliation against supplied labels, not a measurement of predictive model accuracy. All 30 project selections, source citations, join coverage and active/history rules are checked.

## How to run
Open index.html in any browser, or view it live at [Pages link](https://atuliwale.github.io/Portfolio/projects/02-erp-intelligence-copilot/).

GitHub Pages serves this project from the main branch and /(root), once the repository's Pages deployment succeeds.

Select a project, review the three panels, and click any source-ID button to inspect its record. Press Escape or Close to dismiss the evidence dialog. No installation or internet connection is needed for the local file.
