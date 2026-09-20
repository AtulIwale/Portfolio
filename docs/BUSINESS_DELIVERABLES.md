# Fictional business requirements, controls and traceability

Organisation: a fictional multi-entity AEC contractor. All roles, pain points, thresholds,
targets and delivery plans below are authored scenario assumptions, not client findings.

## AS-IS diagnosis

Site requests are emailed to buyers; commercial teams maintain a separate change list;
goods receipts arrive late; finance holds invoices without a shared exception owner.
Effects to investigate: duplicate requests, open commitments, disputed quantities, late
certification and unreliable forecast visibility. No baseline improvement is asserted.

## TO-BE process and responsibilities

| Stage | Responsible | Accountable | Required evidence / exit |
|---|---|---|---|
| Identify need | Site engineer | Project manager | Scope, date required, resource and budget code |
| Validate request | Buyer | Procurement lead | Availability, duplicates, sourcing route |
| Approve commitment | Budget owner | Delegated approver | Budget check, quotation/justification and approved requisition |
| Receive materials | Storekeeper | Site manager | Order link, received/rejected quantities and date |
| Match invoice | AP analyst | Finance controller | Order/receipt match; exception ownership |
| Release payment | Treasury | Finance controller | Approved liability; segregated preparation/release |
| Review performance | Analyst | Project director | Reconciled dashboard and dated source references |

Requester must not approve their own commitment. Payment preparer and releaser must differ.
Role separation and value thresholds require configuration and enforcement in a real system;
this repository documents them but does not implement ERP access control.

## Requirements and UAT matrix

| ID | Requirement / business rule | Acceptance scenario | Evidence here |
|---|---|---|---|
| REQ-01 | Every order identifies a valid supplier and requisition | Reject unknown supplier; flag missing relationship | Relational test; dirty supplier fixture |
| REQ-02 | Required-by date precedes neither request nor order issue | Flag impossible date | `REQUIRED_BEFORE_ORDER` fixture |
| REQ-03 | Partial receipts retain separate event IDs | Two receipts total to ordered quantity without duplicate order totals | Receipt and SQL reconciliation tests |
| REQ-04 | Instalments aggregate before invoice-to-order joins | Two payments do not duplicate invoice value | `test_sql_no_join_inflation` |
| REQ-05 | Overdue exposure uses unpaid balance at export cutoff | Due unpaid invoice flagged; fully paid invoice excluded | SQL billing CTE; dashboard source totals |
| REQ-06 | Model inputs contain only information known at prediction | Future receipts cannot alter prior-history features | Historical-feature test; temporal split test |
| REQ-07 | Approval segregation is enforced | Requester attempting self-approval is rejected | Design-only; requires ERP UAT |
| REQ-08 | Risk scores require human review | Score creates a review item, never an order/payment | JSON review queue; no write integration |
| REQ-09 | Reports state currency, cutoff and synthetic provenance | User sees INR, export date and synthetic label | Data manifest and HTML report |
| REQ-10 | Business sign-off precedes rollout | Block go-live with unreconciled balances or critical defects | Design-only release gate below |

## Delivery plan: staged implementation

| Phase | Indicative duration | Deliverable | Exit gate |
|---|---|---|---|
| Discovery | Weeks 1–2 | Stakeholder interviews, AS-IS and scoped register inventory | Sponsor confirms scope and data owners |
| Design | Weeks 3–4 | TO-BE, rules, security roles and report definitions | Process owners sign design |
| Configure and prototype | Weeks 5–7 | Mapping, controls and reporting prototype | Configuration review complete |
| Migration rehearsal | Weeks 8–9 | Trial extracts, reconciliation and exception resolution | Totals and key counts reconciled |
| UAT and training | Weeks 10–11 | Scripts, defects and role-based walkthroughs | Critical tests pass; owners sign |
| Cutover and stabilisation | Weeks 12–13 | Runbook, freeze plan, support ownership and rollback | Sponsor go/no-go and handover |

Durations illustrate planning logic, not a promised implementation timeline. Dependencies:
approved scope, authorised exports, domain owners, configuration access and trained users.

## RAID register

| ID | Type | Item | Owner | Mitigation / trigger |
|---|---|---|---|---|
| R1 | Risk | Inconsistent resource and supplier codes | Data owner | Profile first; approve mapping; hold unmatched rows |
| R2 | Risk | Invoice double counting through joins | Reporting lead | Grain contract; aggregate child tables; reconcile totals |
| R3 | Risk | Late or missing GRNs distort risk labels | Procurement lead | Label audit; censor unknown outcomes; verify a sample |
| A1 | Assumption | Progress and remaining scope available | Commercial lead | Treat as synthetic until separately verified |
| D1 | Dependency | Business users available for UAT | Project manager | Named testers and protected review slots |
| I1 | Issue | Prototype lacks ERP role enforcement | Solution owner | Design-only flag; not eligible for production release |

## Cutover, rollback and value measurement

Freeze approved extracts; retain checksums and mappings; reconcile record counts and currency
totals; obtain business signatures; release to a pilot cohort. Roll back the application/report
version if totals fail or critical defects appear; never restore or delete client transactions
automatically. Keep an exception owner and daily pilot review.

Measure requisition-to-order time, unmatched invoice value, overdue-open orders, reconciliation
exceptions and UAT defect escape rate. Compare consistent pre/post windows and control for
volume, project mix and process changes. Targets are to be agreed with a sponsor; **no achieved
savings or efficiency percentages are claimed**.
