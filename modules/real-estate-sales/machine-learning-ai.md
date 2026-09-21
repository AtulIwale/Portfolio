# Machine Learning & AI — Real Estate Sales

**Work:** Trained a booking-loss model and built a sales follow-up app.

**Target:** Opportunity lost or cancelled within 60 days (booking_loss).

**Inputs:** Response time (days) (`response_days`); Requested discount rate (`discount_pct`); Prior contacts (`prior_contact_count`); Financing required (0/1) (`financing_required`).

**Model:** depth-four decision tree, minimum 60 training rows per leaf. January–May training; August–October holdout; creation-time inputs only.

| Holdout result | Value |
| --- | --- |
| Training / test records | 2,500 / 1,500 |
| ROC AUC | 0.550 |
| Brier / constant baseline | 0.191 / 0.191 |
| Accuracy / majority baseline | 74.4% / 74.4% |

**App:** filter records, inspect supporting evidence, change inputs for what-if scores and export CSV. Its assistant answers counts, totals and highest-score questions deterministically; it does not use a generative LLM.

**Limits:** synthetic holdout only; repeated entities may occur across periods; scores are uncalibrated. Review aid, not automated authorization. [Evaluation details](../../docs/dataset-notes.md).

[Open Sales Follow-up Reviewer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-real-estate-sales) · [Model and full metrics](../../models/real-estate-sales.json) · [Training code](../../scripts/train-module-models.py) · [App source](../../src/modules/ModulePages.js)

[Module overview](README.md) · [Excel dataset](../../public/data/modules/real-estate-sales.xlsx)
