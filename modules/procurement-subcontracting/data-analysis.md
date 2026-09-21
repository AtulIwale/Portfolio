# Data Analysis & Data Science — Procurement & Subcontracting

**Work:** Analysed order values, delivery outcomes and procurement status patterns.

**Grain:** One purchase order or subcontract work order. 5,000 primary records; 5,000 supporting details and 5,000 events.

| Measured result | Value |
| --- | --- |
| Order value | 3,26,39,92,784 INR |
| Median / 90th percentile | 5,04,982 / 14,59,549.8 |
| Observed target events / eligible records | 1,910 / 4,011 |

| Workflow status | Records |
| --- | --- |
| Approved | 243 |
| Cancelled | 233 |
| Completed | 3,497 |
| Draft | 234 |
| Part delivered | 271 |
| Pending approval | 276 |
| Rejected | 246 |

**Checks performed:** unique record IDs; supporting-table joins; module arithmetic; comparisons by status, type and month. Totals include all workflow states; they are descriptive record values, not posted balances or recognized revenue.

**Outputs:** workbook Records/Details/Events and Summary; [full measured aggregates](../../models/procurement-subcontracting.json) under analysis; [record explorer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-procurement-subcontracting). Synthetic data; [dates, definitions and reproducibility](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/procurement-subcontracting.xlsx)
