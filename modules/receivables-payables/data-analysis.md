# Data Analysis & Data Science — Accounts Receivable & Accounts Payable

**Work:** Analysed invoice values and settlement states across AR and AP.

**Grain:** One AR or AP invoice with settlement allocations. 5,000 primary records; 3,857 supporting details and 5,000 events.

| Measured result | Value |
| --- | --- |
| Gross invoice value (AR + AP) | 9,18,30,78,600 INR |
| Median / 90th percentile | 18,40,800 / 32,21,400 |
| Observed target events / eligible records | 2,126 / 4,412 |

| Workflow status | Records |
| --- | --- |
| Disputed | 314 |
| Draft | 274 |
| Overdue | 555 |
| Part settled | 285 |
| Settled | 3,572 |

**Checks performed:** unique record IDs; supporting-table joins; module arithmetic; comparisons by status, type and month. Keep AR and AP separate; combined gross amounts are not a net receivable or payable balance.

**Outputs:** workbook Records/Details/Events and Summary; [full measured aggregates](../../models/receivables-payables.json) under analysis; [record explorer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-receivables-payables). Synthetic data; [dates, definitions and reproducibility](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/receivables-payables.xlsx)
