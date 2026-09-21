# Machine Learning & AI — Tendering & Contracts

**Work:** Trained an award-delay model and built a tender review app.

**Target:** Award delayed beyond planned evaluation days (award_delay).

**Inputs:** Bids received (`bid_count`); Scope changes at review (`scope_changes`); Approval levels (`approval_levels`); Planned evaluation days (`planned_days`).

**Model:** depth-four decision tree, minimum 60 training rows per leaf. January–May training; August–October holdout; creation-time inputs only.

| Holdout result | Value |
| --- | --- |
| Training / test records | 1,067 / 671 |
| ROC AUC | 0.649 |
| Brier / constant baseline | 0.218 / 0.230 |
| Accuracy / majority baseline | 65.6% / 64.7% |

**App:** filter records, inspect supporting evidence, change inputs for what-if scores and export CSV. Its assistant answers counts, totals and highest-score questions deterministically; it does not use a generative LLM.

**Limits:** synthetic holdout only; repeated entities may occur across periods; scores are uncalibrated. Review aid, not automated authorization. [Evaluation details](../../docs/dataset-notes.md).

[Open Award Risk Reviewer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-tender-contracts) · [Model and full metrics](../../models/tender-contracts.json) · [Training code](../../scripts/train-module-models.py) · [App source](../../src/modules/ModulePages.js)

[Module overview](README.md) · [Excel dataset](../../public/data/modules/tender-contracts.xlsx)
