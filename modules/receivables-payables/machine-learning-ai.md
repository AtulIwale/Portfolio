# Machine Learning & AI — Accounts Receivable & Accounts Payable

**Work:** Trained a late-settlement model and built an invoice review app.

**Target:** Settlement later than contractual payment terms (late_settlement).

**Inputs:** Payment terms (days) (`payment_days`); Prior entity late-payment rate (`prior_late_rate`); Match variance rate (`match_variance`); Approval levels (`approval_levels`).

**Model:** depth-four decision tree, minimum 60 training rows per leaf. January–May training; August–October holdout; creation-time inputs only.

| Holdout result | Value |
| --- | --- |
| Training / test records | 2,185 / 1,317 |
| ROC AUC | 0.618 |
| Brier / constant baseline | 0.241 / 0.250 |
| Accuracy / majority baseline | 58.4% / 50.3% |

**App:** filter records, inspect supporting evidence, change inputs for what-if scores and export CSV. Its assistant answers counts, totals and highest-score questions deterministically; it does not use a generative LLM.

**Limits:** synthetic holdout only; repeated entities may occur across periods; scores are uncalibrated. Review aid, not automated authorization. [Evaluation details](../../docs/dataset-notes.md).

[Open Invoice Priority Reviewer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-receivables-payables) · [Model and full metrics](../../models/receivables-payables.json) · [Training code](../../scripts/train-module-models.py) · [App source](../../src/modules/ModulePages.js)

[Module overview](README.md) · [Excel dataset](../../public/data/modules/receivables-payables.xlsx)
