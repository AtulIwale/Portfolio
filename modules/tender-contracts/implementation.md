# Implementation — Tendering & Contracts

Illustrative 12-week, two-site pilot; 60 person-days. Scope: the specified module types, master data, approval roles, migration, source-ID interfaces, UAT, training and cutover.

| Phase | Weeks | Effort | Rate INR/day | Cost INR | Exit gate |
|---|---|---|---|---|---|
| Discover | 1–2 | 10 days | 9,000 | 90,000 | Sign requirements and scope |
| Configure | 3–5 | 15 days | 10,000 | 150,000 | Approve masters, types and authority |
| Migrate & integrate | 6–8 | 15 days | 11,000 | 165,000 | Reconcile counts, balances and ID joins |
| UAT & train | 9–10 | 10 days | 8,000 | 80,000 | Pass critical tests and train owners |
| Cutover & stabilize | 11–12 | 10 days | 12,000 | 120,000 | Sponsor approves go-live and support |

Base estimate INR 605,000; 15% contingency INR 90,750; total INR 695,750. Excludes licenses, hardware, taxes and statutory localization.

## Migration

Tender packages, BOQ revisions, open bids, signed terms and approved variations. Retain source-to-target ID mapping, reconcile totals, log rejected rows and obtain the process owner's sign-off.

## Risk and acceptance

Late scope revisions invalidate a commercial comparison. Use a trial migration and the module's [acceptance tests](business-analysis.md). Contracts manager owns process acceptance; the data engineer owns migration; the controller owns financial reconciliation; the sponsor authorizes go/no-go.

Changes require a logged request, scope/time/cost impact and sponsor approval before revising the baseline. Configuration follows signed requirements; migration follows signed mappings; failed critical UAT blocks cutover.

Freeze source entry, back up extracts and configuration, reconcile open records and approve release. If critical reconciliation fails, stop release and restore the approved source process. Exit hypercare after ten working days without a critical issue, reconciled daily totals and a named support owner.
