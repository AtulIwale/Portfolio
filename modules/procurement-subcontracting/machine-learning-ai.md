# Machine Learning & AI — Procurement & Subcontracting

**Work:** Trained a delivery-risk model and built an order review app.

**Target:** Completion after the promised date (late_delivery).

**Inputs:** Promised lead days (`lead_days`); Prior supplier delay rate (`prior_delay_rate`); Approval levels (`approval_levels`); Urgency (1–3) (`urgency`).

**Model:** depth-four decision tree, minimum 60 training rows per leaf. January–May training; August–October holdout; creation-time inputs only.

| Holdout result | Value |
| --- | --- |
| Training / test records | 1,915 / 1,192 |
| ROC AUC | 0.601 |
| Brier / constant baseline | 0.242 / 0.250 |
| Accuracy / majority baseline | 56.1% / 51.3% |

**App:** filter records, inspect supporting evidence, change inputs for what-if scores and export CSV. Its assistant answers counts, totals and highest-score questions deterministically; it does not use a generative LLM.

**Limits:** synthetic holdout only; repeated entities may occur across periods; scores are uncalibrated. Review aid, not automated authorization. [Evaluation details](../../docs/dataset-notes.md).

[Open Delivery Risk & Order Review](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-procurement-subcontracting) · [Model and full metrics](../../models/procurement-subcontracting.json) · [Training code](../../scripts/train-module-models.py) · [App source](../../src/modules/ModulePages.js)

[Module overview](README.md) · [Excel dataset](../../public/data/modules/procurement-subcontracting.xlsx)
