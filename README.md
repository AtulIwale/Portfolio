# AEC Intelligence Portfolio — Atul Iwale

Eight connected portfolio projects: business process design, implementation governance,
procurement analytics, cost/cash scenarios and predictive machine learning.

**Status: runnable synthetic-data research prototypes and fictional business case studies.
Not client engagements, a production ERP integration, or validated commercial outcomes.**
No client records, vendor manual excerpts, credentials or proprietary ERP code are included.
The schemas are original simplified designs inspired by common enterprise register concepts.

## Explore the projects

**Start here:** [Read the approach in four executed notebooks](notebooks/README.md).
Charts, tables and results are saved, so you can review the work without running code.
Each technical case study also has an **Open in Colab** link. For business analysis and
delivery, read the [ERP design walkthrough](projects/01-erp-transformation/APPROACH.md)
and [variation-governance walkthrough](projects/02-variation-governance/APPROACH.md).

| Discipline | Project | Working evidence |
|---|---|---|
| Business Analysis | [AEC ERP Process & Controls Transformation](projects/01-erp-transformation/README.md) | AS-IS/TO-BE, requirements, controls, traceability and UAT |
| Business Analysis | [Cost Plan Module Requirements for Real Estate Developers](projects/07-cost-plan-requirements/README.md) | Proposed requirements, acceptance criteria, cost-control rules and fictional worked example |
| Commercial governance / PM | [Contract Variation, Valuation & Payment Governance](projects/02-variation-governance/README.md) | Stage gates, approval matrix, RAID, rollout and acceptance plan |
| Project Management | [HR, Payroll & Accounts Module Rollout](projects/08-hr-payroll-accounts-rollout/README.md) | Proposed phased rollout, dependencies, risk controls, parallel-run gates and cutover plan |
| Data Analysis | [Procure-to-Pay & Supplier Performance Control Tower](projects/03-control-tower/README.md) | Executable SQL, reconciliation and supplier scorecard |
| Data Science | [Project Cash Flow & Estimate-at-Completion Simulator](projects/04-cash-eac/README.md) | Monte Carlo scenarios and funding sensitivity |
| Machine Learning | [Procurement Delivery Risk Early-Warning System](projects/05-delivery-risk/README.md) | Baselines, classifier comparison, threshold selection and review queue |
| Machine Learning | [Cost Overrun & Variation Risk Predictor](projects/06-cost-risk/README.md) | Final-cost regression, overrun flags and calibrated intervals |

Supporting AI/NLP: [Evidence assistant](docs/AI_EVIDENCE.md). This version implements
local extractive retrieval with citations and abstention, **not a generative LLM agent**.

## Run everything

Python 3.12 recommended. From the repository root:

```bash
python -m venv .venv
# Activate .venv using your operating system's command.
python -m pip install -r requirements.txt
python -m aec.run
python -m unittest discover -s tests -v
python -m aec.dashboard
```

Open `outputs/control_tower.html` locally for a filterable procurement report.
No API keys, cloud subscriptions or client exports are required.
The default run generates 3,600 orders, 750 fictional cost packages and their linked records.
The committed [manifest](data/manifest.json) gives the exact table counts, schema and hashes.
The committed [outputs](outputs/) contain actual computed results, not illustrative scores.
To experiment: `python -m aec.run --seed 73`. This replaces generated `data/` and the selected
output folder; keep the published seed-42 evidence in version control.

## What is implemented

- Relational synthetic data with partial receipts, payment instalments, rejection events,
  open/censored orders, variation states, time drift and separate data-quality fixtures.
- SQL at declared grains; reconciliation back to source totals; supplier KPIs.
- Median imputation, categorical encoding and scaling within train-only pipelines.
- Dummy, logistic, ridge and histogram gradient-boosting baselines/candidates.
- Outcome-mature temporal splits; no future completion information in prediction inputs.
- Validation-only model and threshold selection; separate interval calibration subset.
- ROC-AUC, average precision, Brier, precision/recall/F1, MAE/RMSE, empirical interval coverage.
- Fixed-model bootstrap uncertainty, category slices, permutation importance and KS drift.
- Scenario uncertainty, shared escalation shocks, funding gaps and one-factor stress cases.
- TF-IDF evidence retrieval with source IDs, abstention and a small regression test set.
- Business requirements, responsibility/approval rules, risk register and UAT acceptance.

These methods are chosen for the business questions. This repository does **not** claim
to cover all Data Science/ML/AI methods. Deep learning, computer vision, reinforcement
learning, production LLM RAG and live deployment monitoring are not implemented.

## Read before interpreting results

1. [Data card & register mapping](docs/DATA_CARD.md): which fields are assumptions.
2. [Methodology & model cards](docs/METHODOLOGY.md): leakage controls, evaluation and limits.
3. [Business requirements & traceability](docs/BUSINESS_DELIVERABLES.md).
4. [Actual run summary](outputs/RESULTS.md).

Performance on this dataset measures recovery of patterns built into the simulator.
It cannot establish accuracy on a real contractor, causality, savings or deployment readiness.
No automatic purchasing, payment, contract approval or employment decision is performed.

## Repository map

```text
aec/       Generator, feature pipelines, models, SQL, simulation and retrieval
data/      Entire generated JSONL dataset and manifest
outputs/   Computed evaluations, scenarios, review queues and HTML report
projects/  Eight standalone business-facing case studies
notebooks/ Four executed analytical walkthroughs with saved charts and Colab links
scripts/   Rebuild and execute the notebooks in fresh kernels
docs/      Data card, model cards, governance and AI boundaries
tests/     Determinism, joins, leakage, reconciliation and evidence tests
```

No licence has been selected by the owner. Public visibility does not itself grant an
open-source licence. Dependency licences remain those of their respective projects.
