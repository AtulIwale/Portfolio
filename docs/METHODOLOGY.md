# Methods and model cards

## Delivery classifier

Decision: which orders need buyer follow-up at order issue time?
Label: full gross receipt date later than required-by date. Partial open orders have no label.
Features: quantity/value, lead days, month, resource category and supplier completed-history
features. No current-order receipts, payment status, actual delay or future outcomes are inputs.

Training orders and outcomes must predate 2023-01-01. Validation orders are issued from
2023-01-01 to 2024-06-30 and must complete before 2024-07-01. Test orders are issued from
2024-07-01; only completed outcomes at the export cutoff are scored. Boundary-spanning
unmatured labels are purged. This is not random train/test splitting.

Online supplier history may incorporate newly completed earlier test-period orders because
those outcomes would already be known at the next order date. The fitted model stays frozen.
This evaluates an online history feature, not a frozen bulk prediction at the first test day.

Dummy prior, logistic regression and two small histogram-boosting configurations compete on
validation average precision. Threshold minimises the explicitly assumed validation loss:
5 units for a missed late order; 1 for unnecessary follow-up. These are not rupee savings.
The test set is used once for final reporting. No claim that boosting must win.

Reported: PR/AP, ROC-AUC, Brier, precision/recall/F1, calibration bins, material slices,
permutation importance and KS distribution distance. Bootstrap AP bounds resample test
orders with the model fixed; they ignore training uncertainty and correlated supplier clusters.
Permutation associations are not causes. Drift is descriptive, not an automatic retraining trigger.

## Final-cost regressor

Decision: which packages merit a commercial forecast review at 50% assumed physical progress?
One snapshot per package/project prevents repeated snapshots leaking across splits.
Target = final cost/original budget. Inputs contain only budget, snapshot cost/commitments,
known variations, sector and explicit progress assumption. Final cost is never an input.
Same issue/snapshot and outcome-maturity cutoffs as delivery apply.

Median dummy, ridge and shallow boosting compete on the first half of chronological validation.
The second half is reserved for split-conformal absolute-residual calibration at nominal 90%.
The finite-sample residual quantile is rounded up. Empirical test coverage and MAE/RMSE
are reported; temporal shift can invalidate exchangeability and any theoretical guarantee.
Budget-scaled intervals can be wide. Overrun flag means predicted ratio >1.05;
**this is a regression-derived flag, not a calibrated overrun probability**.

No synthetic project-group repeats exist across splits. This does not establish transferability
to real project types. One synthetic package per commercial project simplifies dependencies.

## Data Science versus ML

The cash simulator is not trained. It samples shared escalation shocks and pending-variation
acceptance, spreads remaining cost over six months and shifts payments/receipts. P10/P50/P90
are scenario quantiles, not predictive confidence validated against actual cash flows.
The cost ML project estimates a learned final-cost ratio; these are distinct deliverables.

## Security and operation boundaries

All computations run locally. SQL is fixed, no generated SQL or arbitrary user execution.
The evidence assistant quotes a fixed fictional corpus and cannot approve transactions.
Models do not execute actions. No production API, authentication, authorisation layer,
model registry, alert service or scheduled monitoring is supplied. For deployment, add
identity, access controls, audit logging, retention policy, approval gates, rollback and monitoring.

## Production evaluation gates (not achieved here)

1. Reconcile authorised real inputs and audit event-time availability.
2. Lock untouched later-period and unseen-project evaluation sets.
3. Compare against operational rules and assess subgroup/calibration stability.
4. Validate intervention costs and buyer review capacity prospectively.
5. Run shadow mode; document false positives, overrides and drift.
6. Obtain process-owner approval before any decision integration.

Useful implementation references: scikit-learn's
[data leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html),
[permutation importance](https://scikit-learn.org/stable/modules/permutation_importance.html)
and [model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html).
