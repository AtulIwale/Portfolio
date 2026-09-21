# Machine Learning & AI — Construction Payroll

**Work:** Trained a payroll-correction model and built a pay review app.

**Target:** A payroll line needs correction before release (payroll_adjustment).

**Inputs:** Approved overtime hours (`overtime_hours`); Allowance (INR) (`allowance`); Manual adjustments (`manual_adjustments`); Input exceptions (`input_exceptions`).

**Model:** depth-four decision tree, minimum 60 training rows per leaf. January–May training; August–October holdout; creation-time inputs only.

| Holdout result | Value |
| --- | --- |
| Training / test records | 2,500 / 1,500 |
| ROC AUC | 0.673 |
| Brier / constant baseline | 0.208 / 0.226 |
| Accuracy / majority baseline | 65.5% / 65.4% |

**App:** filter records, inspect supporting evidence, change inputs for what-if scores and export CSV. Its assistant answers counts, totals and highest-score questions deterministically; it does not use a generative LLM.

**Limits:** synthetic holdout only; repeated entities may occur across periods; scores are uncalibrated. Review aid, not automated authorization. [Evaluation details](../../docs/dataset-notes.md).

[Open Payroll Exception Reviewer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-construction-payroll) · [Model and full metrics](../../models/construction-payroll.json) · [Training code](../../scripts/train-module-models.py) · [App source](../../src/modules/ModulePages.js)

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-payroll.xlsx)
