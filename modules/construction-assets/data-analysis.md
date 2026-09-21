# Data Analysis & Data Science — Construction Assets — Fixed & Movable

**Work:** Analysed depreciation, asset status and monthly operating records.

**Grain:** One asset-month snapshot for 500 assets across 10 months. 5,000 primary records; 5,000 supporting details and 5,000 events.

| Measured result | Value |
| --- | --- |
| Monthly depreciation | 7,37,40,000 INR |
| Median / 90th percentile | 14,625 / 27,375 |
| Observed target events / eligible records | 1,429 / 4,880 |

| Workflow status | Records |
| --- | --- |
| Available | 1,626 |
| Deployed | 1,625 |
| Retired | 120 |
| Under maintenance | 1,629 |

**Checks performed:** unique record IDs; supporting-table joins; module arithmetic; comparisons by status, type and month. Sum monthly depreciation, not repeated asset acquisition-cost snapshots.

**Outputs:** workbook Records/Details/Events and Summary; [full measured aggregates](../../models/construction-assets.json) under analysis; [record explorer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-construction-assets). Synthetic data; [dates, definitions and reproducibility](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-assets.xlsx)
