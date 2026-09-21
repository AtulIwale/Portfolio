# Business analysis — Inventory & Warehouse Management

## AS-IS discovery scenario

Paper GRNs, handwritten bin cards and spreadsheet issue registers leave stock balances and lot locations out of date.

Hypothetical scenario, not a claim about an actual company.

## TO-BE workflow

Receive → Inspect → Accept / quarantine → Put away → Issue / return → Cycle count → Reconcile

Process owner: Warehouse manager.

| Requirement | Data concepts | Rule | Acceptance test |
|---|---|---|---|
| Item and UOM | item_id, uom | Maintain one stock unit per item and explicit purchase conversion. | A receipt in bags must convert to the approved stock unit. |
| Chronology | record_date, store_id, item_id | Post each item/store ledger in date order; reject a backdated movement before the last transaction. | Backdate a new issue and confirm it cannot change prior weighted averages. |
| Location control | warehouse_id, locator, lot_id | Track stock location and lot separately from the resource master. | Find a lot by locator and reconcile its quantity. |
| Stock availability | opening_qty, movement_qty, closing_qty | Issues cannot make available stock negative. Quarantined quantities are unavailable. | An issue above available quantity is blocked. |
| Stock correction | movement_type, approval_status | Quantity/value corrections require approval and a cycle-count reference. | A pending correction cannot alter a posted balance. |

## Deliverables

- Stock ledger and locator model
- Receipt-to-issue controls
- Cycle-count and correction UAT

Receipts reference purchase orders; store/item balances reconcile by movement, not by summing snapshots.
