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

---

## Machine-learning upgrade: forecasting final cost and margin

**Live app:** [forecast.html](https://atuliwale.github.io/Portfolio/projects/01-cost-margin-intelligence/forecast.html) · **Notebook:** [notebooks/cost_forecasting.ipynb](notebooks/cost_forecasting.ipynb) · **Data:** [data/01_Cost_Margin_Forecasting_v2.xlsx](data/01_Cost_Margin_Forecasting_v2.xlsx)

The rule above says a project *has* underperformed. A commercial manager needs a forward view: **what will this job finally cost, what margin will we make, and how much will we spend next quarter?** The standard earned-value answer is EAC = AC + (BAC − EV) ÷ CPI, which assumes the rest of the job performs like the past. This upgrade tests whether machine learning, trained on completed projects, does better.

### Data added (original CSVs unchanged)
| Sheet | Rows | What it holds |
| --- | ---: | --- |
| project_register | 269 | The 30 portfolio projects (same IDs, names, contract values and planned dates as `dim_project`) plus 239 completed historical projects from 2016 to 2023: type, client, contract type, tender margin, budget, design maturity, complexity, PM experience, status and final cost |
| fact_monthly_cost | 30,715 | Monthly cost report per project and category (Labor, Material, Equipment, Subcontract, Overhead, the same as `dim_cost_code`): planned value, earned value, actual cost |
| material_price_index | 140 | Steel, cement and labour wage indices, Jan 2015 to Aug 2026, including the 2021–22 steel spike |

The original `fact_cost_value` holds only one or two cost codes per project-month, so it is not a complete ledger (see Data above). The v2 workbook adds a full monthly cost report. The data is synthetic but built on realistic cost behaviour: overheads burn with time, not progress; material price risk depends on the contract type; progress is lumpy, with monsoon and festival slowdowns; accruals are booked and reversed; and late claims and rework arrive near completion. The latest cost report is August 2026: 21 portfolio projects have finished and 9 are still in progress.

### Method
1. **Snapshots:** each project at each month-end from 5% to 99% complete, using only data up to that month. The target is final cost ÷ budget.
2. **Features:** % complete, time vs plan, CPI (cumulative, last 3 months and trend), SPI, CPI by category, overhead spent vs progress, material index change since tender, plus facts known at award (type, client, contract type, design maturity, complexity, PM experience, size). 37 features in total.
3. **Split by time:** trained on projects started before July 2021 (184), tuned on later historical projects (55), and tested on the 21 finished portfolio projects: every monthly forecast they had is scored.
4. **Baselines:** earned-value formulas: remaining work at budget, the CPI formula, and CPI × SPI.
5. **Models:** Ridge regression, Random Forest, **XGBoost**, Neural Network (MLP) and an **LSTM** reading each project's monthly history as a sequence.
6. **Range:** XGBoost quantile models (P10/P90), widened by conformal calibration on the validation projects.
7. **Next-quarter spend:** naive (last 3 months), plan × CPI, **Holt's exponential smoothing** (time series) and a global XGBoost model.
8. **Explainability:** SHAP values for XGBoost.

### Results on the 21 finished portfolio projects
| Method | Error (MAPE) all stages | < 30% complete | 30–60% | > 60% | Bias |
| --- | ---: | ---: | ---: | ---: | ---: |
| **XGBoost** | **2.30%** | **2.8%** | 2.4% | 2.0% | +0.6% |
| Random Forest | 2.35% | 3.0% | 2.4% | 2.0% | +1.2% |
| Ridge regression | 2.48% | 3.3% | 2.6% | 1.9% | +0.5% |
| EVM: CPI formula | 3.01% | 4.6% | 2.8% | 2.2% | −0.8% |
| Neural Network (MLP) | 3.22% | 3.3% | 3.4% | 3.1% | +1.2% |
| LSTM | 3.43% | 3.7% | 3.2% | 3.4% | +1.4% |
| EVM: remaining at budget | 3.51% | 4.6% | 3.9% | 2.7% | −3.5% |

- **Early warning:** below 30% complete, XGBoost's error is 2.8% against 4.6% for the CPI formula.
- **Margin accuracy:** at about 50% complete, the forecast margin is off by 1.9 percentage points of contract value, vs 2.8 for the CPI formula. XGBoost was closer on 14 of 20 projects.
- **The CPI formula flips from pessimistic to optimistic.** Early on it runs 2.1% high, because site set-up costs make CPI look poor. From mid-stage it runs about 3% low, with 86% of mid-stage and 99% of late-stage forecasts below the final cost.
- **Range:** the P10–P90 band held the final cost 76% of the time on the test projects (the target was 80%), with a median width of 7% of budget.
- **Next-quarter spend:** the global XGBoost model has 14% error (WAPE), against 36% for plan × CPI, 40% for naive and 55% for Holt's smoothing.
- **Live projects:** for all 9 projects still in progress, the ML forecast margin is below the CPI-formula margin. Surat Water Treatment Plant 3 is forecast to make a loss (−3.9%, range −6.1% to −0.2%).

### What I learned
- The value is in correcting the formula, not replacing it. CPI is still the strongest input, but schedule slippage, overhead burn, category CPIs (especially subcontract) and contract type explain where the formula goes wrong.
- More complex is not better here. With about 240 projects, the tree models and even Ridge beat the MLP and the LSTM. A sequence model needs far more project histories.
- Across 260 completed projects, a 10.9% tender margin ended as 4.1% on average, and 22% made a loss. That margin fade is the business case for forecasting early.

### Limits
The data is synthetic with a known cost process, and the test set is 21 projects. A real deployment needs the company's own completed-project history, and a retrain every quarter as projects close.

### Files added
| File | Purpose |
| --- | --- |
| `forecast.html` | Portfolio margin forecast, month-by-month forecast replay for each project, S-curves, next-quarter spend and model comparison. XGBoost runs in the browser, and a self-check matches the Python forecasts |
| `notebooks/cost_forecasting.ipynb` | Audit, margin fade, snapshots, EVM baselines, five ML models including an LSTM, ranges, SHAP, next-quarter forecasting and export |
| `model/forecast_export.json` | 900 XGBoost trees (median, P10, P90) and the monthly forecast history for the 30 portfolio projects |
| `data/01_Cost_Margin_Forecasting_v2.xlsx` | Project register, monthly cost reports by category and material price index |

Author: Atul Iwale
