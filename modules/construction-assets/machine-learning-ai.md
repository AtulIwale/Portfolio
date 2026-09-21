# Machine Learning & AI — Construction Assets — Fixed & Movable

**Work:** Trained a breakdown-risk model and built an asset review app.

**Target:** Unplanned breakdown in the following month (breakdown_next_month).

**Inputs:** Age (months) (`age_months`); Utilization rate (`utilization_rate`); Days since service (`days_since_service`); Prior breakdowns (`prior_breakdowns`).

**Model:** depth-four decision tree, minimum 60 training rows per leaf. January–May training; August–October holdout; creation-time inputs only.

| Holdout result | Value |
| --- | --- |
| Training / test records | 2,500 / 1,410 |
| ROC AUC | 0.640 |
| Brier / constant baseline | 0.199 / 0.211 |
| Accuracy / majority baseline | 69.2% / 69.8% |

**App:** filter records, inspect supporting evidence, change inputs for what-if scores and export CSV. Its assistant answers counts, totals and highest-score questions deterministically; it does not use a generative LLM.

**Limits:** synthetic holdout only; repeated entities may occur across periods; scores are uncalibrated. Review aid, not automated authorization. [Evaluation details](../../docs/dataset-notes.md).

[Open Asset Maintenance Reviewer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-construction-assets) · [Model and full metrics](../../models/construction-assets.json) · [Training code](../../scripts/train-module-models.py) · [App source](../../src/modules/ModulePages.js)

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-assets.xlsx)
