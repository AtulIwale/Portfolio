# Construction Safety Intelligence (real OSHA data)

**Author:** Atul Iwale · Project 14 · [Live app](https://atuliwale.github.io/Portfolio/projects/14-construction-safety-intelligence/) · [Notebook 1: cleaning](notebooks/01_data_cleaning_and_eda.ipynb) · [Notebook 2: models](notebooks/02_cause_classification_models.ipynb) · [Notebook 3: LLM](notebooks/03_llm_vs_classic.ipynb)

This is the portfolio's first project on **real, public data**, not synthetic data. Everything from download to app is in this folder: the cleaning code, the notebooks with their outputs, the LLM script and the exported model.

## Problem
A contractor's safety team receives injury reports as free text. To see trends, such as which hazards cause the worst injuries and in which trades, each report has to be coded by cause. OSHA employs trained coders for this; most contractors don't, so their incident data stays unread text.

This project asks: **can a model read an injury narrative and code its cause as consistently as an OSHA coder?** And what does ten years of real data say about where serious construction injuries come from?

## Approach

### Business Analysis
- **Decision supported:** where to focus safety effort (fall protection, machine guarding, heat plans, traffic management) and by which trade, based on consistently coded incident data.
- **Users:** a safety manager or HSE analyst coding incident reports and producing monthly trend reports.
- **Baseline to beat:** a keyword checklist, the first thing a safety team would build.
- **Success measure:** agreement with OSHA's own coders on reports from later years than the model was trained on.

### Project Management
Scope: a reproducible cleaning script, three notebooks, an LLM labelling script, a browser app and this README. Out of scope: injury severity prediction (the narrative usually states it), non-construction industries, and state-plan OSHA states (not in the data).

### Data Analysis & Data Science
1. **Load and filter** (`src/cleaning.py`, notebook 1): 105,996 reports from all industries → **19,021 construction reports** (NAICS sector 23), January 2015 to November 2025.
2. **Quality checks:** 0 bad dates, 0 duplicate IDs, 3 duplicate narratives, 22 narratives under 40 characters, secondary source missing in 47%, and **348 event codes stored with 2, 3 or 4 digits from more than one version of OSHA's coding manual**, where the same prefix can mean different things.
3. **Privacy:** employer name, street address, ZIP code and coordinates are removed, and the employer's own name is replaced with `[EMPLOYER]` in 51 narratives. The data is public on osha.gov, but the portfolio doesn't need to name companies next to injuries.
4. **Labels:** the 348 codes are grouped into **nine cause groups** from their titles (rules in `src/cleaning.py`, full mapping in `data/cause_group_map.csv`). 381 reports with no usable cause ("Nonclassifiable") are left out of modelling.
5. **Finding: OSHA changed its coding manual in January 2024.** The most common caught-in title stops in December 2023, and the same accident is now often coded differently. The time split was designed around it: **train 2015–2022, tune on 2023 (old manual), test on 2024–2025 (new manual)**.
6. **Exploratory risk analysis:** see Results.

### Machine Learning & AI
| Method | Why it's included |
| --- | --- |
| Keyword rules | Baseline: what a safety team would build first |
| TF-IDF + Naive Bayes | Fast probabilistic text classifier |
| TF-IDF + logistic regression | Linear model with one readable weight per word per cause; **used in the app** |
| TF-IDF (words + characters) + logistic regression / linear SVM | Character n-grams cope with typos and word forms |
| 1D-CNN (Keras) | Learned word embeddings with phrase-detecting filters |
| BiLSTM (Keras) | Reads the narrative in sequence, both directions |
| OpenAI LLM, zero-shot and few-shot | Codes the cause blind from instructions (and 10 training examples), and also extracts fall height, equipment and task |

Settings are tuned on the 2023 validation year only. The LLM gets the report ID and narrative only, never OSHA's code.

## Data
**Source:** U.S. Department of Labor, OSHA, Severe Injury Reports, January 2015 to November 2025. [OSHA Severe Injury Dashboard](https://www.osha.gov/severe-injury-reports) → "Download the full SIR data set" (`January2015toNovember2025.zip`, file dated 7 Aug 2026). Federal employers under OSHA must report every work-related amputation, in-patient hospitalisation or loss of an eye.

**Licence:** US federal government work. The Department of Labor states its materials "may be used, reproduced and distributed without permission". OSHA does not endorse this project.

| File | Rows | Contents |
| --- | ---: | --- |
| `data/raw/` (not in the repo) | 105,996 | The original OSHA file. Download it from the link above; it contains employer names and addresses, so it isn't republished here |
| [`data/osha_construction_clean.csv`](data/osha_construction_clean.csv) | 19,021 | Cleaned construction reports: date, split, state, trade, narrative, severity, OSHA codes and titles, cause group, fall height band |
| [`data/cause_group_map.csv`](data/cause_group_map.csv) | 403 | Every OSHA event code and title, with the cause group it was mapped to |
| [`data/llm_input_test.csv`](data/llm_input_test.csv) | 3,204 | What the LLM saw: report ID and narrative only |
| [`data/test_labels_and_classic_predictions.csv`](data/test_labels_and_classic_predictions.csv) | 3,204 | OSHA labels and the classic model's predictions for the test years |
| `data/llm_output_zero.jsonl`, `data/llm_output_few.jsonl` | 3,204 each | Raw LLM answers, one JSON line per report |

## Code
| File | What it does |
| --- | --- |
| [`src/cleaning.py`](src/cleaning.py) | All cleaning steps as small functions: load, filter construction, tidy types, redact employer names, cause-group rules, fall height bands, quality report |
| [`src/clean.py`](src/clean.py) | Runs the cleaning end to end: `python src/clean.py` rebuilds the clean CSV, the mapping table and `reports/data_quality.json` |
| [`src/llm_prompt.py`](src/llm_prompt.py) | The LLM instructions, cause-group definitions, 10 few-shot examples from the training years, and the output validator |
| [`src/llm_label.py`](src/llm_label.py) | Sends each test narrative to OpenAI, with retries, resume and token counts. The API key is read from a local `.env` file that is never uploaded |
| [`notebooks/01_data_cleaning_and_eda.ipynb`](notebooks/01_data_cleaning_and_eda.ipynb) | Every cleaning step with its effect shown, the coding-manual finding, and the risk analysis |
| [`notebooks/02_cause_classification_models.ipynb`](notebooks/02_cause_classification_models.ipynb) | Baseline, five classic and neural models, drift analysis, explainability, error analysis, fall-height rules, export |
| [`notebooks/03_llm_vs_classic.ipynb`](notebooks/03_llm_vs_classic.ipynb) | LLM results against OSHA's codes and the classic model: accuracy, cost, speed, fall height, equipment |
| [`index.html`](index.html) | The app: runs the exported logistic regression in the browser and checks itself against Python's probabilities |

**Reproduce:** `pip install -r requirements.txt`, download and unzip the OSHA file into `data/raw/`, run `python src/clean.py`, then the notebooks in order. For the LLM step, create `.env` with `OPENAI_API_KEY=...` and run `python src/llm_label.py --mode zero` and `--mode few`.

## Results

### Where serious construction injuries come from (18,640 reports with a known cause)
| Cause | Reports | Share with an amputation |
| --- | ---: | ---: |
| Fall to lower level | 6,806 | 0.4% |
| Struck by or against object | 4,706 | 24.8% |
| Caught in or crushed | 2,285 | 62.8% |
| Vehicle or mobile equipment | 1,429 | 6.7% |
| Electrical | 959 | 2.3% |
| Slip, trip or same-level fall | 881 | 2.7% |
| Heat stress | 605 | 0% |
| Fire, explosion or burn | 497 | 1.6% |
| Other | 472 | 0% |

- **Falls** are the most frequent severe injury (37%). One in four falls with a recorded height band was from **under 6 feet**, so ladders and low platforms matter, not only roofs.
- **Caught-in and crushing** accidents cause the most amputations: 63% of them involve one, mostly fingers.
- The **hazard mix changes by trade**: over half of injuries in foundation/structure/roofing and in finishing trades are falls; utility contractors have the most struck-by and caught-in injuries; electrical, plumbing and HVAC contractors account for 57% of electrical injuries.
- **Heat:** 80% of heat-stress injuries happen from June to August, mostly in Texas and Florida.

### Coding the cause (test years 2024 – Nov 2025, 3,204 reports)
| Model | Test macro-F1 | Test accuracy | Macro-F1 on 2023 |
| --- | ---: | ---: | ---: |
| Linear SVM (words + characters) | 0.840 | 83.9% | 0.869 |
| Logistic regression (words + characters) | 0.837 | 83.8% | 0.876 |
| **Logistic regression (words), in the app** | **0.832** | **83.8%** | 0.859 |
| 1D-CNN | 0.818 | 83.4% | 0.851 |
| Naive Bayes | 0.758 | 78.7% | 0.789 |
| BiLSTM | 0.752 | 78.7% | 0.787 |
| Keyword rules (baseline) | 0.495 | 55.1% | 0.519 |

### LLM versus the trained model (same 3,204 test reports, coded blind by gpt-6-luna)
| Method | Accuracy | Macro-F1 | Training data needed | Cost per 1,000 reports |
| --- | ---: | ---: | --- | ---: |
| Logistic regression (in the app) | 83.8% | 0.832 | 14,000 coded reports | free |
| LLM zero-shot | 81.4% | 0.827 | none, definitions only | about $0.14 |
| LLM few-shot | 81.6% | 0.826 | 10 examples | about $0.23 |
| **Both agree → auto-code** | **89.1%** | | covers 85% of reports | |

- **From definitions alone, the LLM comes within about 2 points of a model trained on 14,000 reports.** It is better on falls, slips, fire and "Other", and worse on struck-by and vehicles, where it follows the plain meaning of the definitions rather than OSHA's coding conventions.
- **Used together, they make a review queue.** Where the two agree (85% of reports), the coding matches OSHA 89% of the time; only the 15% where they disagree go to a person.
- **Fall height:** when the LLM gives a height, its band matches OSHA's in **98.5%** of cases, against 75.8% for a "first height in the text" rule, because it tells the fall height apart from the ladder or wall height. It gives a height less often (67% of falls against 78%).
- **Extraction the codes can't do:** the LLM also returned the equipment and task. In 2024–2025, ladders were involved in 407 falls (median fall 8.5 ft), roofs in 193 (16 ft) and scaffolds in 111 (10.5 ft).
- **Cost:** 2.3 million input and 0.4 million output tokens zero-shot, 5.4 million and 0.4 million few-shot. That is under $1.20 for both runs at the model's list price, at about 2 seconds per report.

## How to explain it
- **Linear models beat neural networks here.** Narratives are short (median 190 characters) and there are 14,000 training reports, too few for a network to learn word meanings from scratch. In Project 5 the CNN won because legal risk sits in exact phrases; here the right words carry the signal.
- **Macro-F1, not accuracy.** Falls are 36% of reports; a model that always said "fall" would be 36% accurate and useless. Macro-F1 weighs rare causes like fire equally.
- **Label drift is real.** Accuracy held steady for falls, heat, fire and electrical, but caught-in F1 dropped from 0.78 to 0.59 after OSHA redrew the caught-in/struck-by line in 2024. Adding a year of new-manual data, even weighted up to 10×, did not recover it. The narratives didn't change; the labelling rules did. In production this needs monthly monitoring by cause group.
- **Explainable by design.** Every word has a weight per cause. The strongest words read like a safety manager's vocabulary ("pinched", "between", "amputation" for caught-in; "backed", "forklift" for vehicles), and the app highlights them for each report.
- **Time split, not random split.** The model is trained on the past and tested on later years, as it would be used.

## Honest limits
- OSHA's codes are human judgements, and the 2024 manual change moved the caught-in/struck-by line. Some "errors" are reports a second coder would also split on.
- Severe injuries only (amputation, hospitalisation, loss of an eye) in states under federal OSHA. Minor injuries and state-plan states (such as California) are not in the data.
- US narratives in US English. A contractor in India or the UK would need to re-test on their own reports before relying on it.
- A tool for consistent coding and trend reporting, not a substitute for incident investigation.

## What a real deployment would add
Coding of the contractor's own historical incidents by a safety professional to re-measure accuracy; a review queue for low-confidence reports; monthly monitoring of accuracy by cause group; retraining when the coding rules change.

## Talking point
> "I took 19,000 real OSHA injury reports, found that OSHA had changed its coding manual in 2024, and built a model that codes injury causes from free text with 84% agreement on later years it never saw, against 55% for a keyword list. Then I tested an LLM on the same reports, blind: it came within 2 points with no training data, read fall heights far better, and where the two agreed the coding was right 89% of the time."
