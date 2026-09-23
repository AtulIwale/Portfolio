# Cost Plan Estimation with Machine Learning

**Author:** Atul Iwale · Project 13 · [Live app](https://atuliwale.github.io/Portfolio/projects/13-cost-plan-estimation/) · [Notebook](notebooks/cost_plan_estimation.ipynb)

## Problem
At feasibility stage, developers and contractors need a construction cost estimate long before drawings are detailed enough for a quantity-based cost plan. The usual shortcut is a **coefficient method**: a base rate for the building type, multiplied by coefficients for specification and location. It is quick, but it ignores everything else that moves cost, such as height, basements, foundations, facade, HVAC, site conditions and price escalation.

This project tests whether machine learning trained on completed projects can give a more accurate estimate, and a trustworthy range, from the same early-stage information.

## Approach

### Business Analysis
- **Decision supported:** a feasibility-stage cost estimate per square metre and in total, with a P10–P90 range for contingency planning.
- **Inputs:** only what is known before design: city, building type, specification grade, built-up area, floors, basements, structure, foundation, soil, facade, HVAC, green rating, site condition, contract route, planned duration and start month.
- **Baseline to beat:** the coefficient method, fitted fairly on the same training data. I built coefficient-based cost plan automation earlier in my career, so this is the method I know practitioners rely on.
- **Portfolio link:** the model is applied to the 21 building projects in Project 01 to check whether their contract values look tight or generous against historical cost.

### Project Management
Scope: one reproducible Jupyter notebook, one self-contained web app running the exported model in the browser, a documented dataset and this README. Out of scope: land, professional fees and GST; quantity take-off; forecasting future material prices.

### Data Analysis & Data Science
1. **Audit:** duplicates, spellings against the location table, missing values, and unit errors (area typed in sq ft instead of sq m makes the rate look ~10.8× too low).
2. **Clean:** 6 duplicate rows removed; 18 sq-ft entries corrected; Bangalore/Gurgaon/Bombay standardised; upper-case building types fixed; missing soil and green rating kept as explicit "Not investigated" / "Not recorded" categories; missing facade and duration filled from similar projects.
3. **Feature engineering:** joins to `dim_location` (city tier, seismic zone) and `material_price_index` (steel, cement, labour at the start month); log of area; one-hot encoding (72 features).
4. **Rebasing:** costs converted to January-2018 prices with a composite index (25% steel, 20% cement, 40% labour, 15% other), as quantity surveyors do when comparing projects across years. This also solves a real ML problem: tree models cannot extrapolate to price levels they never saw.
5. **Target:** log of the rebased cost per sq m, so errors behave like percentages.
6. **Time-based split:** train on 1334 projects that started 2018–2023; test on 466 projects that started 2024–2025. No random split, so no future prices leak into training.

### Machine Learning & AI
| Method | Why it's included |
| --- | --- |
| Linear regression | Transparent reference model |
| Ridge regression | Regularised linear model; coefficients read directly as % cost uplifts |
| Decision tree | Most explainable tree; shows the first splits an estimator would make |
| Random forest | Bagging of many trees to reduce variance |
| XGBoost (gradient boosting) | Learns interactions such as specification effects that differ by building type |
| Neural network (MLP) | Multi-layer perceptron with standardised inputs and target, tuned for size and regularisation |
| Ensemble (Ridge + XGBoost) | Averages a linear and a tree model, which make different errors |
| XGBoost quantile regression + conformal calibration | P10 and P90 estimates, calibrated on 2023 projects to cover about 80% of outcomes |

Hyper-parameters are tuned with 5-fold cross-validation on training years only. Explainability: XGBoost gain importance, SHAP values and Ridge uplifts are all in the notebook, and the app shows the biggest cost drivers for each estimate.

## Data
Synthetic data, generated to behave like real cost data (noise, heavy-tailed errors, outliers, missing fields, legacy spellings), patterned on Indian cost-plan structures. File: [`data/13_Cost_Plan_Estimation.xlsx`](data/13_Cost_Plan_Estimation.xlsx).

| Sheet | Rows | Contents |
| --- | ---: | --- |
| fact_building_cost | 1,806 | Completed building projects: attributes, start date and final construction cost (INR) |
| dim_location | 15 | Cities matching the portfolio, with state, tier and seismic zone |
| material_price_index | 96 | Monthly steel, cement and labour indices, Jan-2018 to Dec-2025 |
| portfolio_building_projects | 21 | The building projects from Project 01 with building attributes and contract values |
| data_dictionary | 28 | Field definitions |

## Validation
Results on 466 unseen projects that started in 2024–2025:

| Model | MAPE | Avg error per sq m | R² | Within ±10% | Within ±20% |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ensemble (Ridge + XGBoost) | 6.61% | ₹2,980 | 0.975 | 79.2% | 96.8% |
| Linear regression | 6.64% | ₹3,020 | 0.974 | 76.8% | 97.0% |
| Ridge regression | 6.64% | ₹3,010 | 0.974 | 77.3% | 97.0% |
| Neural network (MLP) | 6.88% | ₹3,050 | 0.974 | 76.4% | 96.4% |
| XGBoost | 7.41% | ₹3,370 | 0.970 | 75.1% | 96.1% |
| Random forest | 9.29% | ₹4,320 | 0.947 | 61.6% | 90.6% |
| Decision tree | 11.17% | ₹5,020 | 0.929 | 55.6% | 83.9% |
| Coefficient method (baseline) | 11.17% | ₹5,220 | 0.917 | 58.4% | 83.3% |

- The best model, **Ensemble (Ridge + XGBoost)**, cuts average error from **11.2%** (coefficient method) to **6.6%**, and puts **79%** of estimates within ±10% of actual cost, against 58% for the coefficient method.
- Linear models do well because, once costs are rebased and logged, most cost drivers act as percentage uplifts. XGBoost adds interactions, and averaging the two is the most accurate.
- The single decision tree is the weakest ML model: easy to read, but too coarse alone. The random forest and XGBoost fix that by combining hundreds of trees.
- The neural network only worked well once small and strongly regularised. With ~1,300 training projects, neural networks have no advantage over well-tuned linear and boosted models; they need much more data to pull ahead.
- **Range:** the raw XGBoost quantile band covered 70.6% of 2024–2025 actual costs. After conformal calibration on 2023 projects, it covers **81.3%** (target 80%), with a median width of 28% of the estimate.

**Accuracy by building type (test set)**

| Building type | Projects | Model MAPE | Coefficient MAPE |
| --- | ---: | ---: | ---: |
| Industrial Plant | 42 | 5.2% | 6.3% |
| Affordable Housing | 53 | 5.6% | 9.5% |
| Premium Residential | 45 | 6.0% | 21.9% |
| Commercial Office | 62 | 6.1% | 12.9% |
| Retail Mall | 24 | 6.6% | 7.0% |
| School / Institutional | 34 | 6.9% | 10.2% |
| Mid-Segment Residential | 98 | 7.1% | 10.3% |
| Hospital | 35 | 7.2% | 9.4% |
| Warehouse / Logistics | 39 | 7.6% | 10.5% |
| Data Centre | 34 | 8.4% | 11.4% |

**Portfolio check (21 projects from Project 01):** 14 within the expected range, 3 below P10 (review for under-pricing), 4 above P90 (check scope and margin). These are review prompts, not errors: contract values can include scope the model does not see.

### Model card and limits
- **Synthetic data:** real-world accuracy must be re-measured on a client's own completed projects before use.
- **Assumptions:** cost-index weights are assumed; costs exclude land, fees and GST.
- **Time:** starts after Dec-2025 use the latest index, so future escalation is not forecast. Retrain as new projects complete.
- **Use:** an early-stage estimate to support, not replace, a quantity surveyor's cost plan.

## How to run
- **App:** open `index.html` in any browser, or use the [live app](https://atuliwale.github.io/Portfolio/projects/13-cost-plan-estimation/). It runs the exported Ridge + XGBoost model locally; no data leaves the browser. The JavaScript predictions match the notebook to within 0.001%.
- **Notebook:** `pip install pandas numpy scikit-learn xgboost shap matplotlib openpyxl`, then run `notebooks/cost_plan_estimation.ipynb` from the `notebooks` folder. It regenerates `model/model_export.json`, which the app uses.
