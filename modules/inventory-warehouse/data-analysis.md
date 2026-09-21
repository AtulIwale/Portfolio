# Data Analysis & Data Science — Inventory & Warehouse Management

**Work:** Analysed stock movements, record statuses and count exceptions.

**Grain:** One dated stock movement in an item/store ledger. 5,000 primary records; 5,000 supporting details and 5,000 events.

| Measured result | Value |
| --- | --- |
| Movement value (absolute) | 21,22,33,900 INR |
| Median / 90th percentile | 31,612.5 / 99,459 |
| Observed target events / eligible records | 1,316 / 5,000 |

| Workflow status | Records |
| --- | --- |
| Count verified | 1,947 |
| Posted | 1,519 |
| Quarantined | 1,534 |

**Checks performed:** unique record IDs; supporting-table joins; module arithmetic; comparisons by status, type and month. Totals include all workflow states; they are descriptive record values, not posted balances or recognized revenue.

**Outputs:** workbook Records/Details/Events and Summary; [full measured aggregates](../../models/inventory-warehouse.json) under analysis; [record explorer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-inventory-warehouse). Synthetic data; [dates, definitions and reproducibility](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/inventory-warehouse.xlsx)
