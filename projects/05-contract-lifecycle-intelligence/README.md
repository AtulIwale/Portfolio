# Contract Lifecycle Intelligence

## Problem
High-risk clauses can remain unreviewed while contracts approach expiry. Automatic renewals can then reduce the opportunity to renegotiate or exit on suitable terms. This demo places clause risks and upcoming expiries in one evidence-based review worklist.

## Approach

### Business Analysis
High-risk means the supplied risk_category is High. Proactive renewal review means auto_renew = Y and end_date is between the dataset reference date and 90 days later, inclusive. The categories are separate: High-risk flags are validated against the answer key; renewal reviews are explicitly unscored because the answer key does not cover them.

The checks are domain-neutral: contract clauses, counterparties, expiry dates and renewal provisions apply to services, equipment, property and other commercial agreements outside construction too. No legal judgment is inferred or automated.

### Project Management
Scope: one offline HTML app, all 200 contracts and 800 clauses, ranked review findings, full-contract clause views and separate validation and proactive-review summaries. Priorities were source traceability, stable date handling and honest interpretation of the answer key. Contract editing, notifications, legal decisions and live system integration are outside this build.

### Data Analysis & Data Science
Join fact_clause to dim_contract on contract_id. Validate uniqueness, foreign keys, categories and date order. The reference date is the maximum of all start_date and end_date values: **2026-09-22**. The inclusive forward-looking window ends **2026-12-21**. Dates are compared at UTC midnight and are independent of the browser's current date.

Flag High-risk clauses and, separately, every clause belonging to a qualifying auto-renewing contract. Count the union once for the overall worklist. Rank High-risk first, then renewal-only; ties use end date ascending, contract value descending and clause_id. A contract value is repeated context, not an amount at risk or a savings estimate.

### AI
This is a deterministic category-and-date rules engine, not a statistical model. It does not read clause text to infer risk and does not use answer-key labels to generate flags. A future NLP version could extract notice periods, identify problematic wording and cite supporting text, evaluated against independently reviewed contracts and subject to human review. No such model is included here.

## Data
Synthetic data patterned on real contract structures. The unchanged source workbook is `data/05_Contract_Lifecycle_Intelligence.xlsx`; its contents are embedded as JSON in index.html, with no external dependencies.

| Sheet | Rows | Schema |
|---|---:|---|
| dim_contract | 200 | contract_id, contract_name, counterparty, contract_value (INR), start_date, end_date, auto_renew |
| fact_clause | 800 | clause_id, contract_id, clause_type, clause_text_summary, risk_category |
| answer_key | 800 | clause_id, is_flagged, flag_reason |
| data_dictionary | 19 | sheet_name, column_name, data_type, meaning |

Editing the workbook does not automatically refresh the HTML's embedded snapshot.

## Validation
### High-risk clauses only
**Precision: 100.0% (80/80). Recall: 100.0% (80/80).** True positives: 80; false positives: 0; false negatives: 0; true negatives: 720. The answer key flags exactly the 80 clauses whose supplied risk_category is High. Perfect agreement is expected for this deterministic category check on aligned synthetic labels. It does not establish independent legal-risk detection, statistical-model quality or real-world generalization.

### Proactive renewal review — not scored
**32 clauses across 8 contracts**, not covered by the answer key. No precision or recall is assigned to this category, and no combined precision/recall is reported. Two clauses are also High-risk; the other 30 are renewal-only reviews, not classification false positives.

Together, the categories create **110 unique flagged clauses across 47 contracts**.

### Data checks and limits
- No duplicate primary keys, missing clause/contract joins, missing answer-key matches or contracts ending before their start dates were found.
- The workbook contains no reporting/as-of field. The approved reference uses its latest date, which is itself an end date. All eight qualifying auto-renewals expire on that exact date; none expires later. The app displays this limitation explicitly and does not substitute today's date.
- Expiry review is not notice-deadline detection. One supplied clause summary specifies 120 days' notice, so a 90-day expiry window may be too late for that action. The app makes no claim that cancellation remains available.
- Renewal flags are contract-level prompts repeated on all clauses for context. Opening a contract shows all four clauses, including any without a High-risk flag.

## How to run
Open index.html in any browser, or view it live at [Pages link](https://atuliwale.github.io/Portfolio/projects/05-contract-lifecycle-intelligence/).

---

## Machine learning upgrade (v2): reading risk from the clause wording

**Author:** Atul Iwale · [Clause Risk Reader app](https://atuliwale.github.io/Portfolio/projects/05-contract-lifecycle-intelligence/ml.html) · [Notebook](notebooks/clause_risk_nlp.ipynb)

The original app above relies on a risk category someone has already assigned. In practice that rating is the expensive part, because a reviewer has to read every clause. Version 2 adds NLP and neural-network models that rate a clause from its **wording**, as the NLP idea in the AI section above proposed.

### Business Analysis
- **Decision supported:** which clauses and contracts need legal review first, before signature.
- **Output:** Low, Medium or High risk for each clause, the words that drove the rating, key commercial terms, and a contract-level priority list.
- **Cost of errors:** a missed High clause (unlimited liability, pay-when-paid, 120-day payment) costs far more than an extra review, so High recall is tracked separately.

### Project Management
Scope: one reproducible notebook, one in-browser app page (`ml.html`) and the v2 dataset. The original `index.html`, its data and its validation are unchanged.

### Data Analysis & Data Science
- **Data (v2 workbook):** `data/05_Contract_Lifecycle_Intelligence_v2.xlsx` keeps every original sheet and ID, adds full `clause_text` to the 800 portfolio clauses, and adds a historical library of **1,300 contracts and 6,539 clauses** signed Jan-2019 to Sep-2024, each rated by one of six legal reviewers. Synthetic, patterned on Indian construction contracts, with realistic variation in wording, 26 unreadable scans and reviewer disagreement.
- **Cleaning:** unreadable clauses removed; text lower-cased; party names (Employer/Owner/Client/Company, Contractor/Subcontractor/Vendor/Supplier) normalised so models learn risk, not template style.
- **Design:** train on the historical library, test on the 800 portfolio clauses (Oct-2024 onwards). Tuning uses 5-fold cross-validation **grouped by contract**. Metrics: macro-F1, plus precision and recall for High.

### Machine Learning & AI
| Method | Role |
| --- | --- |
| Keyword rules | Baseline red-flag checklist |
| TF-IDF + Complement Naive Bayes | Classic probabilistic text classifier |
| TF-IDF + Logistic Regression | Strong, explainable linear model |
| TF-IDF + Linear SVM | Margin-based linear classifier |
| MLP on TF-IDF | Feed-forward neural network |
| BiLSTM (Keras) | Recurrent network reading words in order, learned embeddings |
| **1D-CNN (Keras)** | Convolutional network detecting risky phrases; best model, used in the app |
| K-means + truncated SVD | Unsupervised topic discovery (recovers the six clause types, ARI 0.999) |
| Regex extraction | Payment days, notice periods, retention, escalation, pay-when-paid |
| Occlusion | Explains the CNN by blanking each word and measuring the change in P(High) |

### Validation (800 unseen portfolio clauses)
| Model | Macro-F1 | Accuracy | High precision | High recall |
| --- | ---: | ---: | ---: | ---: |
| Neural network (1D-CNN) | 0.942 | 95.6% | 85.4% | 95.0% |
| Neural network (MLP on TF-IDF) | 0.917 | 94.0% | 92.6% | 78.7% |
| Neural network (BiLSTM) | 0.912 | 93.8% | 78.3% | 90.0% |
| Logistic regression | 0.858 | 90.6% | 63.7% | 81.2% |
| Linear SVM | 0.845 | 90.0% | 63.2% | 75.0% |
| Naive Bayes | 0.599 | 65.6% | 26.4% | 65.0% |
| Keyword rules (baseline) | 0.379 | 38.8% | 18.0% | 75.0% |

- The **1D-CNN** is best: macro-F1 **0.94**, catching **95%** of High clauses with **85%** precision, against 0.38 macro-F1 for the keyword checklist.
- The neural networks beat the linear models because they read word order: "within 30 days" versus "within 120 days", "shall be limited" versus "shall not be limited".
- A threshold analysis on validation clauses (F2, recall-weighted) confirmed the default decision threshold is the best trade-off.
- **Worklist:** the model puts 52 of 200 contracts on the priority list, including 40 of the 40 contracts that contain a reviewer-rated High clause.
- **Label noise:** cross-validated agreement with individual reviewers ranges from 85% to 89%; one reviewer rates borderline clauses High more often. Part of the remaining error is human disagreement.

### Limits
Synthetic clauses are more regular than real contracts, so accuracy must be re-measured on a client's own reviewed clauses. Words never seen in training are treated as unknown. This is a screening aid for legal review, not legal advice.

### How to run (v2)
- **App:** open `ml.html` in a browser, or use the [live page](https://atuliwale.github.io/Portfolio/projects/05-contract-lifecycle-intelligence/ml.html). The CNN runs in JavaScript from exported weights; its probabilities match Keras to within 0.002 percentage points.
- **Notebook:** `pip install pandas numpy scikit-learn tensorflow matplotlib openpyxl`, then run `notebooks/clause_risk_nlp.ipynb` from the `notebooks` folder. It regenerates `model/clause_model_export.json` and `model/clause_cnn.keras`.
