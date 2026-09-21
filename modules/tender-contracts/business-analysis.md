# Business Analysis — Tendering & Contracts

**Work:** Defined bid comparisons, award approvals and contract variation controls.

**Current-process scenario:** Tender registers in spreadsheets, scope revisions over email, and paper bid approvals make it difficult to prove which BOQ was evaluated.

**Proposed flow:** Package and BOQ → Enquiry → Bid normalization → Technical review → Commercial recommendation → Award approval → Contract and variations.

| Control | Rule | Acceptance check |
| --- | --- | --- |
| Revision control | Freeze the evaluated BOQ revision; a later revision triggers renewed review. | Revise a package after evaluation and verify the award is blocked until reviewed. |
| Bid normalization | Compare bids in one currency and scope; record exclusions explicitly. | A low-price noncompliant bid must remain ineligible. |
| Award authority | Commercial approval and technical acceptance must both precede award. | An unapproved recommendation cannot create an active contract. |
| Contract terms | Carry approved payment terms and retention into the signed contract. | Verify terms survive the tender-to-contract handoff. |
| Variation register | Unapproved variations remain separate from the approved contract value. | Pending variation must not inflate the approved commitment. |

**Deliverables:** BOQ revision matrix and tender workflow; Bid normalization and authority rules; Contract/variation traceability and UAT evidence.

**Owner / handoff:** Contracts manager. Approved contract IDs feed orders and receivable records; variation values remain versioned.

Hypothetical discovery and proposed configuration; [dataset fields and assumptions](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/tender-contracts.xlsx)
