# AEC ERP Process & Controls Transformation

[Read the illustrated approach](APPROACH.md) · [Requirements, UAT and delivery pack](../../docs/BUSINESS_DELIVERABLES.md)


**Business Analysis · fictional design case study**

## Problem and value

Disconnected requisition, purchasing, stores and finance processes make ownership unclear
and conceal exceptions. The proposed value is a traceable operating model with explicit
handoffs and controls—not a claim of a completed client transformation.

## Users and scope

Site teams, buyers, stores, commercial managers, AP and finance controllers. Scope covers
procure-to-pay and reporting requirements; payroll, tax compliance and proprietary ERP
configuration are excluded.

## Approach

Business need → stakeholder analysis → AS-IS → pain points → control gaps → TO-BE →
requirements → traceability → UAT → solution evaluation.

The AS-IS story is a fictional scenario, not fabricated interview research. Requirements are
checked against a relational synthetic dataset to make selected reporting rules executable.

## Deliverables

- [AS-IS, TO-BE and responsibility matrix](../../docs/BUSINESS_DELIVERABLES.md#to-be-process-and-responsibilities)
- [Ten traced requirements and UAT scenarios](../../docs/BUSINESS_DELIVERABLES.md#requirements-and-uat-matrix)
- [Staged implementation and RAID register](../../docs/BUSINESS_DELIVERABLES.md#delivery-plan-staged-implementation)
- [Data dictionary and register boundaries](../../docs/DATA_CARD.md)
- [Executable reconciliation rules](../../aec/analytics.py)
- [Executed example findings](../../outputs/reconciliation_findings.json)

## Design decision example

An order can have several receipts; an invoice can have several payments. The reporting
requirement is one order row, so receipt and payment details must be aggregated before
joining. Otherwise the same order or invoice value appears several times. This business
rule is implemented and tested, rather than left as a diagram only.

## Acceptance and limitations

Automated tests cover selected data/reporting requirements. Self-approval prevention,
role permissions, configuration and user acceptance require a real system and authorised
stakeholders. They are design deliverables, not implemented ERP functionality.

Success measures to agree in a real pilot: cycle time, reconciliation exceptions, unmatched
invoice balance and control compliance. There are no realised client results in this case.

[Back to portfolio](../../README.md)
