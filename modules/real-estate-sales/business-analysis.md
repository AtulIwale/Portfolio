# Business analysis — Real Estate Sales

## AS-IS discovery scenario

Sales teams track enquiries in spreadsheets and reservation messages. Payment schedules and discount approvals are reconciled manually with finance.

Hypothetical scenario, not a claim about an actual company.

## TO-BE workflow

Enquiry → Availability → Reservation → Discount approval → Booking → Agreement → Installments → Handover

Process owner: Sales operations manager.

| Requirement | Data concepts | Rule | Acceptance test |
|---|---|---|---|
| Unit availability | unit_id, booking_status | One active booking per unit; cancellation must explicitly release the unit. | Attempt two active bookings for one unit and verify the second is blocked. |
| Price and discount | list_price, discount_pct | Store approved discount separately from the list price. | An excessive discount must route to the sales head. |
| Payment schedule | booking_id, installment_no | Schedule amounts must add to the contracted consideration. | Round installment amounts and reconcile the final residual. |
| Collection allocation | collected_amount, scheduled_amount | Allocate receipts to identified installments; keep unapplied cash separate. | Partial collections cannot mark the full installment settled. |
| Cancellation | booking_status, refund_amount | A cancellation requires a reason and reviewed refund calculation. | Cancel a partly paid booking and verify receivable reversal/release. |

## Deliverables

- Lead-to-booking process and unit controls
- Discount and installment rules
- Sales-to-AR handoff tests

Booked unit schedules can reference AR installments; customer IDs are fictional.
