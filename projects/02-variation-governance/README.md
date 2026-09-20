# Contract Variation, Valuation & Payment Governance

[Read the illustrated approach](APPROACH.md) · [Requirements, UAT and delivery pack](../../docs/BUSINESS_DELIVERABLES.md)


**Business process design · commercial governance · project-management delivery plan**

## Problem and intended value

A change may be executed before approval, excluded from forecasts, certified without a
clear evidence trail or disconnected from payment. The objective is explicit decision rights
and a controlled route from change notice to financial closeout.

This is a fictional governance case, not legal advice, interpretation of an actual contract,
or evidence that Atul delivered a named client implementation.

## Workflow

Identify change → register notice → assess scope/time/cost → obtain approval → update
authorised budget → value completed work → certify → match payment → reconcile closeout.

## Stage gates and control requirements

| Gate | Required inputs | Decision owner | Hold / rejection condition |
|---|---|---|---|
| Notice logged | Unique reference, date, source instruction, affected scope | Commercial manager | Missing source or duplicate notice |
| Evaluation complete | Quantity/rate basis, cost/time effect, assumptions | Quantity surveyor lead | Unsupported basis or unresolved scope |
| Approval | Evaluated amount, budget impact, delegated authority | Authorised approver | Self-approval or authority exceeded |
| Valuation | Approved scope, independently verified work evidence | Certifier | Unverified quantity or unapproved change |
| Payment | Certificate, deductions/retention basis, invoice match | Finance controller | Reconciliation difference or payment hold |
| Closeout | Agreed final values, open-item resolution, audit trail | Project director | Open disputes or unreconciled balances |

## Illustrative authority matrix

| Proposed change | Required authorisation |
|---|---|
| Within approved scope and delegated budget | Commercial manager, subject to segregation |
| Changes total authorised budget | Project director plus finance approval |
| Changes contractual terms or involves a dispute | Designated contract/legal reviewer |

Actual monetary limits and contract notice deadlines are deliberately not invented. They
must be derived from the organisation's delegation policy and governing contract.

## Worked fictional variation

V-DEMO-01: revised MEP routing. Estimated change INR 180,000. The engineer records the
instruction and scope; the quantity surveyor checks quantities/rates; the budget owner
assesses exposure. Until approval, it stays a pending forecast scenario, not approved budget.
If 60% is independently verified, the eligible base valuation is INR 108,000 before any
contract-specific retention, tax, deductions or previous certification. Finance must reconcile
those items separately. This example is arithmetic only, not an entitlement determination.

## Project-management evidence

Use the [delivery plan, RAID, UAT and cutover gates](../../docs/BUSINESS_DELIVERABLES.md).
The PM contribution is scope, dependencies, owners, testing, training, release decisions and
stabilisation; the BA contribution is workflow, rules, fields and traceability.

## UAT scenarios

1. Missing instruction reference prevents submission for evaluation.
2. Unapproved change stays outside approved budget while visible in pending exposure.
3. Self-approval attempt is rejected by the future ERP workflow.
4. Repeated certification cannot exceed cumulative verified value without an exception.
5. Part payment retains a remaining certified balance.
6. Rejection preserves the original record and decision reason in the audit trail.

These are acceptance specifications; no live approval engine or legal compliance system
is implemented. The synthetic [variation data](../../data/variations.jsonl) supports examples,
but does not contain actual contract text, status transitions or payment-certificate events.

[Back to portfolio](../../README.md)
