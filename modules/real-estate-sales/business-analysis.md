# Business Analysis — Real Estate Sales

**Work:** Mapped enquiry-to-booking workflows, discounts and collection controls.

**Current-process scenario:** Sales teams track enquiries in spreadsheets and reservation messages. Payment schedules and discount approvals are reconciled manually with finance.

**Proposed flow:** Enquiry → Availability → Reservation → Discount approval → Booking → Agreement → Installments → Handover.

| Control | Rule | Acceptance check |
| --- | --- | --- |
| Unit availability | One active booking per unit; cancellation must explicitly release the unit. | Attempt two active bookings for one unit and verify the second is blocked. |
| Price and discount | Store approved discount separately from the list price. | An excessive discount must route to the sales head. |
| Payment schedule | Schedule amounts must add to the contracted consideration. | Round installment amounts and reconcile the final residual. |
| Collection allocation | Allocate receipts to identified installments; keep unapplied cash separate. | Partial collections cannot mark the full installment settled. |
| Cancellation | A cancellation requires a reason and reviewed refund calculation. | Cancel a partly paid booking and verify receivable reversal/release. |

**Deliverables:** Lead-to-booking process and unit controls; Discount and installment rules; Sales-to-AR handoff tests.

**Owner / handoff:** Sales operations manager. Booked unit schedules can reference AR installments; customer IDs are fictional.

Hypothetical discovery and proposed configuration; [dataset fields and assumptions](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/real-estate-sales.xlsx)
