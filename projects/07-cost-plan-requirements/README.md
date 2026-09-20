# Cost Plan Module Requirements for Real Estate Developers

**Business Analysis · illustrative requirements case study**

This portfolio brief describes a proposed approach, not a completed client engagement.
No client requirements, confidential records, interviews or measured outcomes are claimed.

## The problem

Developer teams need a consistent way to structure project cost plans, approve baselines,
control revisions and compare budgets with commitments and actual expenditure.
Disconnected spreadsheets can leave cost ownership, version history and approval status unclear.

## Stakeholders and discovery

| Stakeholder | Questions to validate |
|---|---|
| Development director | Which investment stages need approval, and who owns the baseline? |
| Cost planning / quantity surveying | How are quantities, rates, contingencies and assumptions maintained? |
| Project manager | Which phase, building, work package and cost code must be tracked? |
| Procurement / contracts | How do awarded packages consume the approved allocation? |
| Finance | Which posted costs and commitments reconcile to the cost plan, and at what cutoff? |
| Approvers / system administrators | Which approval limits, permissions and audit controls apply? |

## My approach

Business need → Stakeholder elicitation → AS-IS mapping → Pain points → Gap analysis →
TO-BE workflow → Requirements and business rules → Traceability → UAT → Evaluation.

Discovery would distinguish acquisition, construction, infrastructure, consultant fees and
other project costs. Treatment of financing, tax, escalation and contingency must be agreed
with the developer rather than assumed to be identical across projects.

## Proposed requirements and acceptance criteria

| ID | Requirement | Acceptance example |
|---|---|---|
| CP-01 | Maintain project, phase, building, package and cost-code hierarchy | Each detail line maps to an authorised hierarchy; parent totals reconcile to detail |
| CP-02 | Capture quantity, unit, rate, amount and estimate basis | A quantity/rate line calculates consistently; lump-sum items require an explicit basis |
| CP-03 | Version and approve cost-plan baselines | An approved baseline cannot be silently edited; a revision records reason and approver |
| CP-04 | Configure approval ownership and delegated limits | An unauthorised user cannot approve a revision; rejected drafts retain decision history |
| CP-05 | Map commitments and posted costs to cost codes | Every imported transaction is mapped or routed to an exception queue; totals reconcile |
| CP-06 | Separate approved changes from pending exposure | Pending changes appear in a forecast view without increasing the approved budget |
| CP-07 | Show budget, consumed commitments and remaining forecast separately | Actuals are not added twice when already included in a commitment |
| CP-08 | Preserve an auditable change history | Reviewer can inspect previous value, new value, actor, timestamp and reason |

## Worked fictional example

A package has an approved budget of INR 10 million. Its INR 6 million commitment
includes INR 2 million already posted as actual cost. Forecast uncommitted work is
INR 3 million. With no other adjustments, expected completion cost is INR 9 million:
2 million actuals + 4 million remaining commitment + 3 million uncommitted work.
Adding the full commitment to actuals would double-count INR 2 million.

This example assumes commitments include the posted costs and remain fully forecast to be
consumed. Real designs must handle cancellations, accruals, retention and forecast revisions explicitly.

## Deliverables

- Stakeholder map, elicitation questions and agreed scope.
- AS-IS and TO-BE process maps with responsibility and approval handoffs.
- Business requirements, field definitions, business rules and interface mapping.
- Requirements traceability matrix linking CP-01–CP-08 to UAT scenarios.
- Prototype views: cost-plan editor, revision comparison, approval inbox and variance report.

## UAT and evaluation

Test rejected revisions, unauthorised edits, unmapped cost codes, duplicate transaction
imports and reconciliation failures—not only the happy path. Proposed acceptance requires
business-owner sign-off and agreed handling of every critical exception.

Evaluate reconciliation differences, revision turnaround and unresolved mapping exceptions
against an agreed baseline. No reduction or savings is asserted here. This is a requirements
brief; it does not include an implemented ERP module or executed UAT evidence.

[Back to portfolio](../../README.md)
