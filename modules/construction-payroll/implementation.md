# Project Management — Construction Payroll

**Work:** Planned pay-element setup, parallel runs, UAT and cutover costs. Illustrative two-site pilot; implementation has not been claimed as a client deployment.

**Scope:** Monthly staff, Monthly site; masters, approvals, interfaces, UAT and training.

| Phase | Weeks | Days | Cost (INR) |
| --- | --- | --- | --- |
| Discover | 1–2 | 10 | 90,000 |
| Configure | 3–5 | 15 | 1,50,000 |
| Migrate & integrate | 6–8 | 15 | 1,65,000 |
| UAT & train | 9–10 | 10 | 80,000 |
| Cutover & stabilize | 11–12 | 10 | 1,20,000 |

**Budget:** 60 person-days; INR 6,05,000 base + 90,750 contingency = **6,95,750**. Excludes hardware, licenses, taxes and statutory localization.

**Migrate:** Salary structures, approved attendance, open deductions and opening balances. Reconcile counts, balances and source IDs.

**Main risk:** Cut-off changes after sign-off can invalidate the payroll parallel run.

**Controls:** Payroll lead signs off the process; sponsor approves scope changes and go-live. Signed requirements → approved mappings → reconciled migration → critical [UAT checks](business-analysis.md) passed. Freeze and back up source data before cutover; restore the source process if reconciliation fails. Close hypercare after ten working days without critical issues and with an agreed support owner.

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-payroll.xlsx)
