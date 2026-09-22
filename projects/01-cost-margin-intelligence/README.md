# Project Cost & Margin Intelligence

## Problem
Construction margin erosion often becomes visible only after cost reports, progress measurements and site records are reconciled. A single bad month may be noise, but sustained cost or progress underperformance warrants earlier review. This demo ranks those sustained signals and exposes the monthly evidence.

## Approach

### Business Analysis
Margin risk is defined as project-month CPI below 0.90 for at least two consecutive calendar months, **or** SPI below 0.90 for at least two consecutive calendar months. The user-specified 0.90 threshold identifies material performance shortfalls; the persistence requirement avoids flagging isolated dips. These are demo assumptions, not empirically optimized or industry-mandated thresholds.

### Project Management
Scope: one offline HTML app, all supplied records, dimension joins, monthly aggregation, ranked explanations, expandable evidence, and answer-key validation. Priority went to transparent calculations and traceability. No server, authentication, external libraries, live ERP connection or automated financial decisions are included.

### Data Analysis & Data Science
Sum budgeted_cost, earned_value and actual_cost per project/calendar month before calculating:
- CPI = total earned_value / total actual_cost.
- SPI = total earned_value / total budgeted_cost (a schedule proxy).
- Missing calendar months or unavailable ratios break streaks. Ratios are compared before rounding.
- At-risk months are the union of months in qualifying CPI/SPI streaks.
- Flags cover any qualifying historical streak, not just current risk.
- Average CPI = arithmetic mean of the 30 latest project-month CPIs: **0.939527**, displayed **0.94**.

### AI
This is an explainable rule-based system, not a trained ML model. Ranking score = longest qualifying streak length + that streak's mean shortfall below 0.90; the fractional part remains below 1. Equal-length streaks use the deeper average shortfall; final project ties use project name. Higher scores rank first. Scores are priorities, not probabilities or predicted margin losses.

A future ML version could predict future margin deterioration from cost, progress and commitment histories. It would need representative positive and negative project outcomes, time-based train/test splits, leakage controls, calibrated probabilities and comparison against this rule baseline.

## Data
Synthetic data patterned on real ERP structures, supplied as `01_Project_Cost_Margin_Intelligence.xlsx`. The `data/` folder preserves all five sheets as CSVs, with dates serialized as ISO dates and blank cells left empty.

| Sheet | Grain and key | Contents |
| --- | --- | --- |
| dim_project | 30 projects; project_id | Project name, region, contract value, start/end dates |
| dim_cost_code | 25 codes; cost_code | Cost-code description and category |
| fact_cost_value | 1,200 records; row_id | Project/cost code, accounting month, budgeted cost, earned value, actual cost, source CPI/SPI |
| answer_key | 1,200 labels; row_id | is_margin_risk and risk_reason |
| data_dictionary | 25 field definitions | Source types, units and meanings |

The app embeds every sheet as JSON and joins every fact row to project and cost-code dimensions. Answer-key labels are isolated from scoring and used only after predictions for validation. Data spans October 2024–September 2026; amounts are INR. Each project-month has only 1–2 cost-code records, so the data is not a complete project ledger. Some accounting periods fall outside project start/end dates; source rows are preserved, not silently removed. Source ratios are rounded; project-month ratios are recomputed from underlying amounts.

## Validation
**Model accuracy as requested (precision): 100.0% = 24 confirmed flagged projects / 24 flagged projects.**

A project is answer-key positive when **any** of its records has is_margin_risk = Y, as agreed. All 30 projects are positive under this mapping.

| Result | Count |
| --- | ---: |
| True positives | 24 |
| False positives | 0 |
| False negatives | 6 |
| True negatives | 0 |

Recall is **80.0%** (24/30). Conventional overall classification accuracy is also **80.0%**, not 100%. There are no negative projects, so specificity and reliable false-positive performance cannot be established. This is an in-sample synthetic rule check, not held-out ML validation.

Checks cover unique keys, complete joins, 720 project-month aggregates, chronological continuity, strict threshold boundaries, missing-month breaks, overlapping streak counts, and offline row expansion. The worst-ranked project is **Bengaluru Industrial Plant 1**: CPI below 0.90 for four consecutive months, August–November 2025.

## How to run
Open index.html in any browser, or view it live at [Pages link](https://atuliwale.github.io/Portfolio/projects/01-cost-margin-intelligence/).

No installation or internet connection is needed for the local file. Click a project row or focus its button and press Enter to expand the monthly table.

For GitHub Pages, select **Settings → Pages → Deploy from a branch → main → /(root)**. The URL above becomes live after a successful Pages deployment.
