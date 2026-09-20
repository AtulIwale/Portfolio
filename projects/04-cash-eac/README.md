# Project Cash Flow & Estimate-at-Completion Simulator

**Data Science · Monte Carlo simulation · sensitivity · uncertainty**

## Business question

How might remaining-cost escalation, pending variations and payment/receipt timing affect
completion cost and peak funding need? Intended users: commercial and project finance teams.

## Input assumptions

One fictional package snapshot supplies original budget, actual cost, assumed physical
progress and pending variation exposure. Remaining base cost = budget × (1 − progress).
Actual cost is assumed paid before simulation month 1. Remaining client receipts are assumed
to equal 1.1 × the remaining base budget. These are **explicit modelling assumptions**, not
verified register-derived EAC or actual AR data.

## Model

5,000 seeded draws; common escalation shock N(mean, 0.08), bounded below by multiplier .5;
pending variations accepted as one package-level Bernoulli event with probability .6.
Remaining cost is spread with monthly weights [.10, .20, .25, .20, .15, .10]. Payments and
receipts can be shifted by 0–6 months in a twelve-month horizon.

EAC = actual cost + simulated remaining cost + simulated accepted pending variations.
Peak funding = max(0, largest cumulative net cash deficit). Opening cash is assumed zero.
Committed remaining amount is not added again to the base remaining cost, avoiding double count.

## Scenarios and interpretation

| Scenario | Mean escalation | Receipt lag | What changes |
|---|---:|---:|---|
| Base | 6% | 2 months | Planning reference |
| Cost stress | 18% | 2 months | Greater final cost and funding exposure |
| Receipt delay | 6% | 4 months | Timing-related funding need; EAC unchanged |

Payment lag stays one month. Common random numbers keep scenario comparisons stable.
P10/P50/P90 are quantiles of chosen assumptions, not empirically validated confidence levels.

## Working evidence

- [Scenario inputs and results](../../outputs/cash_scenarios.json)
- [Simulation implementation](../../aec/analytics.py)
- [Sensitivity and validation tests](../../tests/test_portfolio.py)

## Limitations and next decision

No empirical cash-flow backtest, cost-to-complete estimate from quantity surveyors, retained
payments, taxes, actual invoicing schedules, correlations between projects or funding interest
is modelled. Change these assumptions with domain owners before interpreting the outputs.
Potential value: explain funding sensitivity; no actual funding savings are claimed.

[Back to portfolio](../../README.md)
