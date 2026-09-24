# NYC Permit Approval Forecast (real NYC Open Data)

**Author:** Atul Iwale · Project 15 · [Live app](https://atuliwale.github.io/Portfolio/projects/15-nyc-permit-approval-forecast/) · [Notebook 1: cleaning](notebooks/01_data_cleaning_and_eda.ipynb) · [Notebook 2: survival models](notebooks/02_survival_models.ipynb)

The portfolio's second project on **real, public data**. It forecasts how long the New York City Department of Buildings (DOB) will take to approve a major job's plans, using **survival analysis** because a quarter of the filings are still waiting.

## Problem
A developer or contractor files a New Building, a major alteration or a demolition with DOB. Until the plans are approved, the programme, financing and holding costs are all guesses. Permit expediters quote rules of thumb; nobody gives a probability.

**Question:** on the filing day, what is the realistic approval date, the range around it, and the chance of approval within 90, 180 and 365 days?

## Approach

### Business Analysis
- **Decision supported:** when to plan the construction start, how much float to hold, and how long to budget for holding costs.
- **Users:** a developer's project manager, a contractor's planner or a lender's monitor.
- **Baseline to beat:** a rule of thumb by job type ("New Buildings take about 8–9 months").
- **Success measure:** ranking and calibrated probabilities on later filings than the model was trained on.

### Project Management
Scope: a download script, a cleaning pipeline, two notebooks, a browser app and this README. Out of scope: self-certified (professional certification) filings, the time from approval to permit, and minor alterations.

### Data Analysis & Data Science
1. **Extract** (`src/download.py`): 131,515 filing records for four major job types, 55 columns. Applicant and owner names, house numbers and streets were never downloaded.
2. **One row per job** (`src/cleaning.py`, notebook 1): each job's initial filing (`-I1`); 128 duplicate records removed (latest state kept), 180 undated filings dropped, 21 approvals dated before filing flagged and excluded.
3. **Outcome with censoring:** approved filings get days to approval; open filings are *censored*, meaning "not approved after X days"; withdrawn filings are censored at withdrawal.
4. **Finding: ignoring open filings is badly biased.** The median of approved filings only is **107 days**; the Kaplan–Meier median of all filings is **154 days**. For 2026 filings the naive number is 74 days against 182.
5. **Features:** only what is known on the filing day: job and building type, borough, declared cost, floor area, dwelling units, 24 work-type flags, applicant licence, owner type. DOB's workload (the open queue in the borough) and the job description were built and tested.
6. **Time split:** train on filings from September 2021 to December 2023, choose settings on January–June 2024, test on July 2024 – June 2025 (at least 15 months of follow-up).

### Machine Learning & AI
| Method | Why it's included |
| --- | --- |
| Kaplan–Meier by job type | Baseline: the expediter's rule of thumb, done properly |
| Naive XGBoost regression on approved filings only | Shows what goes wrong if censoring is ignored |
| Cox proportional hazards | Classic, linear survival model |
| Random survival forest | Tree ensemble of Kaplan–Meier curves |
| XGBoost accelerated failure time (AFT) | Boosted trees on log(days); open filings enter the loss as "at least this long"; **used in the app** |

Scored with the C-index (Harrell and Uno), time-dependent AUC at 90/180/365 days and the integrated Brier score, plus calibration at 180 days and P10–P90 coverage, all on the unseen test filings.

## Data
**Source:** NYC Open Data, [DOB NOW: Build – Job Application Filings](https://data.cityofnewyork.us/Housing-Development/DOB-NOW-Build-Job-Application-Filings/w9ak-ipjd) (dataset `w9ak-ipjd`), extract downloaded 24 September 2026, filtered to New Building, Alteration CO, ALT-CO (New Building with Existing Elements to Remain) and Full Demolition.

**Licence and changes:** NYC's Open Data Law makes public datasets available without registration, licence or usage restrictions; the City asks re-publishers to name the source, version and changes, and gives no warranty. Changes made here: filtered to four job types, reduced to one initial filing per job, duplicates removed, names never downloaded, and block, lot, building ID, coordinates, census tract and ZIP code left out of the published file. The City of New York does not endorse this project.

| File | Rows | Contents |
| --- | ---: | --- |
| `data/raw/` (not in the repo) | 131,515 | The raw extract; rebuild it with `python src/download.py` |
| [`data/dob_initial_filings_clean.csv.gz`](data/dob_initial_filings_clean.csv.gz) | 31,880 | One row per job: filing-day features, outcome (`event`, `duration`), split |
| [`reports/data_quality.json`](reports/data_quality.json) | – | The counts quoted here, recomputed by `src/clean.py` |

## Code
| File | What it does |
| --- | --- |
| [`src/download.py`](src/download.py) | The exact NYC Open Data API query used for the extract |
| [`src/cleaning.py`](src/cleaning.py) | Initial filings, duplicates, types, the censored outcome, filing-day features and DOB workload |
| [`src/clean.py`](src/clean.py) | Runs the pipeline: `python src/clean.py` rebuilds the clean file and the quality report |
| [`notebooks/01_data_cleaning_and_eda.ipynb`](notebooks/01_data_cleaning_and_eda.ipynb) | Every cleaning step, the censoring bias, Kaplan–Meier curves, workload and a declared-cost check |
| [`notebooks/02_survival_models.ipynb`](notebooks/02_survival_models.ipynb) | Five models, scoring, calibration, P10–P90 coverage, drivers, text and workload tests, export |
| [`index.html`](index.html) | The app: runs the exported XGBoost AFT trees in the browser and checks itself against Python |

**Reproduce:** `pip install -r requirements.txt`, then `python src/download.py`, `python src/clean.py` and the two notebooks in order.

## Results

### What the data says
| Job type | Plan-exam filings | Kaplan–Meier median days to approval |
| --- | ---: | ---: |
| New Building | 8,044 | 262 |
| ALT-CO (New Building with existing elements) | 2,693 | 213 |
| Alteration CO | 13,156 | 147 |
| Full Demolition | 5,209 | 39 |

- **A quarter of plan-exam filings are still open**, and even among 2021 filings about one in eight never got approved.
- **Queens is fastest** (median 130 days); the other boroughs are around 167–171.
- **After approval, the first permit follows a median of about two months later.**
- **Declared cost check:** 6% of Alteration CO filings declare under \$5 per sq ft. About 30% of those are certificate-of-occupancy amendments with no physical work; the other 561 form a review list.

### Forecasting approval (test filings July 2024 – June 2025, 5,708 jobs)
| Model | C-index | AUC 90 d | AUC 180 d | AUC 365 d | Integrated Brier score |
| --- | ---: | ---: | ---: | ---: | ---: |
| Random survival forest | 0.702 | 0.801 | 0.745 | 0.712 | 0.164 |
| **XGBoost AFT (normal, σ 1.2), in the app** | 0.689 | 0.802 | 0.727 | 0.668 | 0.167 |
| Cox proportional hazards | 0.680 | 0.779 | 0.713 | 0.669 | 0.171 |
| Naive regression, approved only | 0.679 | 0.794 | 0.718 | 0.647 | 0.188 |
| Baseline: Kaplan–Meier by job type | 0.661 | 0.768 | 0.694 | 0.643 | 0.172 |

- **Calibration at 180 days:** the AFT model's probabilities are within about 3.5 points of what happened, on average across ten groups. The naive model predicts a 73% chance of approval within 180 days when 59% happened, and overstates by 12 to 27 points in its middle groups.
- **P10–P90 range:** covers 89% of resolved test filings (a little cautious against the 80% target). It is wide, about a month to two years for a typical job, because approval times are.
- **Drivers:** building work versus demolition (the general-construction flag), then job type, dwelling units added, floor area and borough. The job description and DOB's workload each improved the C-index by under 0.01.

## How to explain it
- **Why survival analysis?** A filing still waiting after 400 days is information, not missing data. Dropping it makes DOB look a third faster than it is; giving it a made-up end date is worse. Survival models use "at least 400 days" directly.
- **Ranking versus probabilities.** The naive model ranks filings almost as well as the survival models, so the C-index alone would hide the problem. Its probabilities are over-optimistic because it never saw the filings that stall. Always check calibration, not just ranking.
- **Why the app uses XGBoost AFT and not the random survival forest.** The forest scores slightly better, but it is large; the AFT model is 62 small trees, gives calibrated probabilities and an explicit range, and runs in a browser. On a server I'd use the forest.
- **Read the top feature before trusting it.** The most important feature is called "general construction work", but a cross-tab showed it is set on every building job and on no demolition, so it really means "building work or demolition".
- **Report what didn't work.** DOB's workload looked like an obvious driver in the charts but added almost nothing to the model, because the queue rises with time and its effect can't be separated from everything else that changed.

## Honest limits
- Ranking is modest (C-index about 0.69–0.70). Much of the wait depends on drawing quality, how fast objections are answered and which examiner picks the job up, none of which is in the filing.
- Plan approval isn't the permit, and the permit isn't the start on site.
- DOB NOW data from March 2021 only; a change in DOB process or staffing would need re-testing.

## Talking point
> "I took 29,000 real NYC building filings, a quarter of them still waiting, and showed that the usual shortcut understates the wait by 47 days. Using survival analysis, the model gives a calibrated chance of approval by 90, 180 and 365 days for a new filing, within about 3.5 points of what happened on filings it never saw."
