# Business analysis — Tendering & Contracts

## AS-IS discovery scenario

Tender registers in spreadsheets, scope revisions over email, and paper bid approvals make it difficult to prove which BOQ was evaluated.

Hypothetical scenario, not a claim about an actual company.

## TO-BE workflow

Package and BOQ → Enquiry → Bid normalization → Technical review → Commercial recommendation → Award approval → Contract and variations

Process owner: Contracts manager.

| Requirement | Data concepts | Rule | Acceptance test |
|---|---|---|---|
| Revision control | boq_revision, tender_id | Freeze the evaluated BOQ revision; a later revision triggers renewed review. | Revise a package after evaluation and verify the award is blocked until reviewed. |
| Bid normalization | bid_count, bid_amount, technical_score | Compare bids in one currency and scope; record exclusions explicitly. | A low-price noncompliant bid must remain ineligible. |
| Award authority | approval_level, approved_amount | Commercial approval and technical acceptance must both precede award. | An unapproved recommendation cannot create an active contract. |
| Contract terms | retention_pct, payment_days, contract_id | Carry approved payment terms and retention into the signed contract. | Verify terms survive the tender-to-contract handoff. |
| Variation register | variation_amount, variation_status | Unapproved variations remain separate from the approved contract value. | Pending variation must not inflate the approved commitment. |

## Deliverables

- BOQ revision matrix and tender workflow
- Bid normalization and authority rules
- Contract/variation traceability and UAT evidence

Approved contract IDs feed orders and receivable records; variation values remain versioned.
