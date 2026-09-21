# Business Analysis — Procurement & Subcontracting

**Work:** Mapped requisitions, order types, approvals and invoice-matching requirements.

**Current-process scenario:** Site engineers send requirements through WhatsApp and paper requisitions. Buyers compare quotes in separate spreadsheets; signed work orders and valuation sheets are hard to reconcile.

**Proposed flow:** Requisition → RFQ and comparison → Budget check → Approval → PO / work order → GRN / valuation → Invoice matching.

| Control | Rule | Acceptance check |
| --- | --- | --- |
| Order types | Separate materials, plant hire, services, call-offs, labour and measured-work orders. | A labour work order requires a trade and valuation basis rather than a stock item. |
| Approval workflow | Demo authority: buyer prepares; project manager reviews; commercial manager approves up to INR 500,000; director above that. No self-approval. | Test values of 499,999, 500,000 and 500,001 and verify routing. |
| Budget availability | Commit only approved orders within the available budget or with an authorized override. | An over-budget draft cannot be released without the override record. |
| Receipt and certification | Material receipts and subcontract valuations use separate acceptance evidence. | A rejected receipt cannot be included in a payable invoice. |
| Retention and advance | Record contract-specific retention and advance recovery without double counting. | Verify a partial certificate retains and recovers the correct amounts. |

**Deliverables:** AS-IS/TO-BE requisition and approval maps; Order-type and authority configuration; GRN, valuation and invoice-match acceptance pack.

**Owner / handoff:** Procurement manager. Order IDs connect to inventory receipts and AP invoices; work orders connect to valuations.

Hypothetical discovery and proposed configuration; [dataset fields and assumptions](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/procurement-subcontracting.xlsx)
