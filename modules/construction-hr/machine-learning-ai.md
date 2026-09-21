# Machine Learning & AI — Construction HR

**Work:** Trained a record-quality model and built an attendance review app.

**Target:** Attendance record needs clerical correction at review (attendance_correction).

**Inputs:** Manual entry (0/1) (`manual_entry`); Missing punches (`missing_punches`); Overtime hours (`overtime_hours`); Shift changes (`shift_changes`).

**Model:** depth-four decision tree, minimum 60 training rows per leaf. January–May training; August–October holdout; creation-time inputs only.

| Holdout result | Value |
| --- | --- |
| Training / test records | 2,500 / 1,500 |
| ROC AUC | 0.701 |
| Brier / constant baseline | 0.210 / 0.239 |
| Accuracy / majority baseline | 66.7% / 60.7% |

**App:** filter records, inspect supporting evidence, change inputs for what-if scores and export CSV. Its assistant answers counts, totals and highest-score questions deterministically; it does not use a generative LLM.

**Limits:** synthetic holdout only; repeated entities may occur across periods; scores are uncalibrated. Review aid, not automated authorization. [Evaluation details](../../docs/dataset-notes.md).

[Open Attendance Quality Reviewer](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-construction-hr) · [Model and full metrics](../../models/construction-hr.json) · [Training code](../../scripts/train-module-models.py) · [App source](../../src/modules/ModulePages.js)

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-hr.xlsx)
