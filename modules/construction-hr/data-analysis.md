# Data Analysis & Data Science — Construction HR

**Work:** Analysed worked days, attendance statuses and clerical corrections.

**Grain:** One employee-month attendance summary for 500 employees across 10 months. 5,000 primary records; 5,000 supporting details and 5,000 events.

| Measured result | Value |
| --- | --- |
| Worked days | 1,15,011 days |
| Median / 90th percentile | 23 / 25 |
| Observed target events / eligible records | 1,943 / 5,000 |

| Workflow status | Records |
| --- | --- |
| Approved | 1,281 |
| Draft | 1,193 |
| Returned | 1,257 |
| Submitted | 1,269 |

**Checks performed:** unique record IDs; supporting-table joins; module arithmetic; comparisons by status, type and month. Worked days measure recorded attendance; correction flags concern record quality, not employee performance.

**Outputs:** workbook Records/Details/Events and Summary; [full measured aggregates](../../models/construction-hr.json) under analysis; [record explorer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-construction-hr). Synthetic data; [dates, definitions and reproducibility](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-hr.xlsx)
