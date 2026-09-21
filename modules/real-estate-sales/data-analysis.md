# Data Analysis & Data Science — Real Estate Sales

**Work:** Compared sales values, booking stages and opportunity outcomes.

**Grain:** One unique unit sales enquiry / booking opportunity. 5,000 primary records; 10,096 supporting details and 5,000 events.

| Measured result | Value |
| --- | --- |
| Agreed consideration | 66,37,74,82,000 INR |
| Median / 90th percentile | 1,32,30,000 / 2,16,00,000 |
| Observed target events / eligible records | 1,294 / 5,000 |

| Workflow status | Records |
| --- | --- |
| Agreement signed | 819 |
| Booked | 833 |
| Cancelled | 777 |
| Enquiry | 862 |
| Handed over | 872 |
| Reserved | 837 |

**Checks performed:** unique record IDs; supporting-table joins; module arithmetic; comparisons by status, type and month. Totals include all workflow states; they are descriptive record values, not posted balances or recognized revenue.

**Outputs:** workbook Records/Details/Events and Summary; [full measured aggregates](../../models/real-estate-sales.json) under analysis; [record explorer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-real-estate-sales). Synthetic data; [dates, definitions and reproducibility](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/real-estate-sales.xlsx)
