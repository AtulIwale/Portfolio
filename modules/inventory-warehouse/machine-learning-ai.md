# Machine Learning & AI — Inventory & Warehouse Management

**Work:** Trained a stock-exception model and built a movement review app.

**Target:** Cycle-count discrepancy discovered after posting (stock_exception).

**Inputs:** Days since count (`days_since_count`); Movement quantity (`movement_qty`); Manual entry (0/1) (`manual_entry`); Unit value (`item_value`).

**Model:** depth-four decision tree, minimum 60 training rows per leaf. January–May training; August–October holdout; creation-time inputs only.

| Holdout result | Value |
| --- | --- |
| Training / test records | 2,500 / 1,500 |
| ROC AUC | 0.659 |
| Brier / constant baseline | 0.187 / 0.200 |
| Accuracy / majority baseline | 73.5% / 72.5% |

**App:** filter records, inspect supporting evidence, change inputs for what-if scores and export CSV. Its assistant answers counts, totals and highest-score questions deterministically; it does not use a generative LLM.

**Limits:** synthetic holdout only; repeated entities may occur across periods; scores are uncalibrated. Review aid, not automated authorization. [Evaluation details](../../docs/dataset-notes.md).

[Open Stock Exception Reviewer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-inventory-warehouse) · [Model and full metrics](../../models/inventory-warehouse.json) · [Training code](../../scripts/train-module-models.py) · [App source](../../src/modules/ModulePages.js)

[Module overview](README.md) · [Excel dataset](../../public/data/modules/inventory-warehouse.xlsx)
