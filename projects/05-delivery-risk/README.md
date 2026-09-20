# Procurement Delivery Risk Early-Warning System

**Machine Learning · classification · calibrated decision review**

## Problem and action

At order issue time, which purchases should a buyer investigate for late-delivery risk?
Output is a ranked human-review queue, not an automatic supplier penalty or expedite order.

## Inputs and target

Original synthetic order, supplier-history and GRN events. Target = full gross delivery after
required-by date. Incomplete orders are censored, not labelled negative. Current-order receipt
and invoice information is excluded from predictors. Historical supplier metrics use only
orders already completed before the new order date.

## Methods implemented

1. Date/grain validation and past-only feature engineering.
2. Train-only median imputation, scaling and one-hot encoding.
3. Dummy prior and logistic regression baselines.
4. Two shallow histogram gradient-boosting candidates.
5. Outcome-mature chronological train/validation/test split.
6. Validation selection by average precision, with a cost-sensitive review threshold.
7. Test discrimination, calibration, category slices and bootstrap uncertainty.
8. Permutation feature importance and feature-distribution drift checks.

The title refers to evaluating probability calibration; no post-hoc calibration model is fitted.
Threshold costs are fictional 5:1 missed-late versus unnecessary-follow-up units.

## Executed evidence

- [Actual metrics and selected model](../../outputs/delivery_metrics.json)
- [Thirty scored held-out examples](../../outputs/delivery_review_queue.json)
- [Feature construction](../../aec/features.py)
- [Training and evaluation](../../aec/models.py)
- [Model card and temporal assumptions](../../docs/METHODOLOGY.md)

## Explanation and oversight

Permutation importance describes global predictive association, not why a particular supplier
will be late and not a causal recommendation. Buyer reviews current commitments, alternatives
and programme priority before acting. This version has no individual SHAP explanation or
capacity-constrained intervention optimiser.

## Limitations

Synthetic labels reflect the generator's assumptions. Completed-order evaluation may favour
shorter deliveries at the end of the observation window. Three years of historical examples
do not validate performance in another organisation. No prevented delays or money saved
is claimed. Monitor false alarms and calibration in a real shadow pilot before operational use.

[Back to portfolio](../../README.md)
