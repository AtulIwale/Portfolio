# Data Analysis & Data Science — Tendering & Contracts

**Work:** Compared package values, tender outcomes and monthly award activity.

**Grain:** One tender package and its contract outcome. 5,000 primary records; 17,602 supporting details and 5,000 events.

| Measured result | Value |
| --- | --- |
| Package value | 21,33,38,80,000 INR |
| Median / 90th percentile | 42,70,000 / 72,51,000 |
| Observed target events / eligible records | 704 / 2,178 |

| Workflow status | Records |
| --- | --- |
| Awarded | 733 |
| Cancelled | 718 |
| Contract active | 716 |
| Contract closed | 729 |
| Draft | 724 |
| In evaluation | 690 |
| Lost | 690 |

**Checks performed:** unique record IDs; supporting-table joins; module arithmetic; comparisons by status, type and month. Totals include all workflow states; they are descriptive record values, not posted balances or recognized revenue.

**Outputs:** workbook Records/Details/Events and Summary; [full measured aggregates](../../models/tender-contracts.json) under analysis; [record explorer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-tender-contracts). Synthetic data; [dates, definitions and reproducibility](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/tender-contracts.xlsx)
