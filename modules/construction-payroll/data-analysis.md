# Data Analysis & Data Science — Construction Payroll

**Work:** Reconciled net pay, attendance links and payroll processing states.

**Grain:** One employee-month pay record linked 1:1 to HR attendance. 5,000 primary records; 5,000 supporting details and 5,000 events.

| Measured result | Value |
| --- | --- |
| Calculated net pay | 27,67,30,321.44 INR |
| Median / 90th percentile | 54,032.33 / 86,837.39 |
| Observed target events / eligible records | 1,669 / 5,000 |

| Workflow status | Records |
| --- | --- |
| Approved | 340 |
| Calculated | 320 |
| Held for attendance | 3,719 |
| Paid | 307 |
| Under review | 314 |

**Checks performed:** unique record IDs; supporting-table joins; module arithmetic; comparisons by status, type and month. Calculated net pay is not cash paid; check payment status and approved HR attendance.

**Outputs:** workbook Records/Details/Events and Summary; [full measured aggregates](../../models/construction-payroll.json) under analysis; [record explorer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-construction-payroll). Synthetic data; [dates, definitions and reproducibility](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-payroll.xlsx)
