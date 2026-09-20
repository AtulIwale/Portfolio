# Cost Overrun & Variation Risk Predictor

**Machine Learning · regression · uncertainty · commercial review**

## Business decision

At 50% assumed physical progress, which packages warrant investigation for final cost above
105% of original budget? This is a portfolio research prototype, not a live project forecast.

## Data contract

One decision snapshot per package/project: initial budget, actual-cost ratio, remaining
commitment ratio, known approved/pending variations and sector. Final cost is a separate
synthetic outcome. Physical progress and ground-truth final cost are assumed extensions;
their availability is not implied by the vendor register documentation.

## Modelling approach

Median dummy, ridge and shallow histogram gradient boosting predict final-cost/budget ratio.
Packages and outcomes are split chronologically with outcome-maturity purging. The first
validation half selects the model; the second calibrates absolute-residual intervals.
The test set reports ratio MAE/RMSE, monetary MAE, interval coverage and overrun-flag F1.

The overrun flag derives from a regression threshold; it is **not** a calibrated probability.
Nominal 90% split-conformal intervals require assumptions that temporal drift can violate.
Measured coverage is published even when below nominal coverage.

## Executed evidence

- [Model comparison and test metrics](../../outputs/cost_metrics.json)
- [Thirty held-out package examples](../../outputs/cost_review_queue.json)
- [Past-only snapshot features](../../aec/features.py)
- [Training and interval calibration](../../aec/models.py)
- [Data assumptions](../../docs/DATA_CARD.md)

## Working decision example

For a package flagged above threshold, review original scope, quantity/rate growth and pending
variation evidence. A wide interval is a reason to investigate uncertainty, not to assert an
exact completion cost. The model does not automatically revise budgets or commercial positions.

## Limitations

Data generation creates learnable relationships; test performance is not evidence of real-world
forecast skill. Three idealised progress stages and one package per project simplify dependencies.
No actual schedule, certified physical progress, cost ledger or contract document integration
exists. No prevented cost overruns or realised client savings are claimed.

[Back to portfolio](../../README.md)
