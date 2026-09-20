# Executed synthetic-data results — seed 42

These are actual outputs of the committed pipeline, not client results. Re-run before
comparing changes. The seed and row counts are recorded in run_manifest.json.

| Evaluation | Selected model | Test result | Dummy baseline |
|---|---|---|---|
| Late-delivery ranking | logistic | AP 0.602; ROC-AUC 0.642 | AP 0.462 |
| Delivery probability error | logistic | Brier 0.288 | Brier 0.260 |
| Final-cost ratio | ridge | MAE 0.094 | MAE 0.121 |

Delivery test n=1243; cost test n=116.
Cost interval observed coverage: 95.7%, nominal 90%.
Cost interval half-width: 0.220 × original budget.

## Interpretation, including weaknesses

The delivery model improves ranking over the dummy baseline, but its probability error
must be compared separately. Lower Brier is better. In the seed-42 run the chosen model's
Brier is worse than the dummy under the simulated later-period shift. Do not treat its
probabilities as deployment-ready. A high-recall threshold creates a large follow-up queue;
review workload and test-period utility need operational validation.

The cost model's lower ratio MAE is evidence of learning the synthetic process, not real
commercial forecasting accuracy. Wide intervals remain important; do not cherry-pick the
coverage number without their width. Neither project establishes prevented delays or savings.

## Procurement analysis

- Orders: 3,600
- Gross-completed orders: 3,500
- On-time rate among completed orders: 61.0%
- Overdue open orders: 6
- Invoiced value: INR 393,833,031.86
- Overdue invoice balance at 2025-12-31: INR 3,749,467.82

See the JSON files for all metrics, slices, calibration bins, assumptions and review queues.
All three financial sums reconcile to their clean synthetic source tables in automated tests.
