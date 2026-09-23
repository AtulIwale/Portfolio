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

---

## AI upgrade: ERP Copilot chatbot (RAG + text-to-SQL)

**Live chat:** [chat.html](https://atuliwale.github.io/Portfolio/projects/02-erp-intelligence-copilot/chat.html) · **Notebook:** [notebooks/copilot_rag.ipynb](notebooks/copilot_rag.ipynb) · **Data:** [data/02_ERP_Copilot_v2.xlsx](data/02_ERP_Copilot_v2.xlsx)

The dashboard above shows risk for a project you pick. The Copilot lets a project controls or finance user ask a question in plain English instead, for example "status of invoice no 45", "how much receivable is unpaid for Surat Hospital Campus 1?", "which projects have CPI below 0.9?" or "any high-risk clauses in CON012?". It answers from the same ERP tables used across this portfolio (projects, purchase orders, invoices, earned value and contract clauses) and shows the records behind every answer.

### How it works
1. **Knowledge base.** 2,630 records from four ERP modules are turned into one plain-language document each, with linked IDs (project, vendor, contract) kept as metadata.
2. **Query clean-up.** Short IDs are normalised ("PO 85" → PO000085, "invoice no 45" → INV000045) and typos are corrected against the knowledge-base vocabulary, with protected words so "worth" is never changed to "north".
3. **Intent router.** A logistic-regression classifier, trained on masked question shapes (IDs and names replaced by placeholders) plus a small domain lexicon for synonyms, decides whether the question is a record lookup, a calculation or out of scope.
4. **Retrieval (lookups).** Entity-aware BM25: extract IDs and names, boost the record itself and its linked documents, then rank the rest by BM25.
5. **Text-to-SQL (calculations).** Slots are filled from the question and one of eight parameterised SQL queries runs on SQLite. The SQL and the source rows are shown to the user.
6. **Guardrails and grounding.** Questions outside the data, and IDs that do not exist, are declined rather than guessed. Every number in an answer must appear in a cited source.

The browser app is a JavaScript port of the same pipeline and runs fully offline with no API key. A parity check replays 174 notebook questions in the browser and matches the Python route, answer and sources on all 174.

### Results (held-out questions with wordings not used in training)

| Component | Result |
| --- | ---: |
| Retrieval Recall@1: pure vector search (LSA) | 0.352 |
| Retrieval Recall@1: hybrid BM25 + LSA (RRF) | 0.463 |
| Retrieval Recall@1: TF-IDF cosine | 0.826 |
| Retrieval Recall@1: BM25 | 0.878 |
| Retrieval Recall@1: **entity-aware BM25 (used)** | **1.000** |
| Intent router test accuracy | 0.921 |
| SQL answer matches gold (given the correct intent) | 100% of 224 |
| Off-topic or not-in-data questions declined | 14 of 14 |
| In-scope questions wrongly declined | 0 of 215 |
| Answers whose numbers are traceable to a source | 100% |
| **End-to-end correct: overall / lookups / calculations / declines** | **94.8% / 100% / 85.0% / 100%** |

### What I learned
- Pure embedding-style search is weak on ERP data because the questions are about IDs, not meaning. Extracting the entity first and filtering on it matters more than the choice of vector model.
- The main remaining error is the router on wordings it never saw. "What is PRJ004 worth?" is routed to a lookup of the project record instead of the contract-value calculation. The value is still in the retrieved record, but the evaluation counts it as wrong. More real question logs would fix this more reliably than a bigger model.
- **Data-quality finding:** the vendor master holds each supplier twice (30 names, 60 vendor IDs), so supplier history is aggregated by name.

### Limits
The data is synthetic and the evaluation questions come from templates, so real users will phrase things more freely. A production version would add real question logs, a larger router training set and, optionally, an LLM to word answers more fluently under the same citation rules.

### Files added
| File | Purpose |
| --- | --- |
| `chat.html` | Offline chatbot with route label, SQL used, source rows, retrieved records and evaluation tables |
| `notebooks/copilot_rag.ipynb` | Knowledge base, retrieval comparison, router, text-to-SQL, guardrails and evaluation |
| `model/copilot_export.json` | Index, router weights, SQL templates and tables exported for the browser |
| `data/02_ERP_Copilot_v2.xlsx` | Source tables plus retrieval, SQL and out-of-scope evaluation sets |

Author: Atul Iwale
