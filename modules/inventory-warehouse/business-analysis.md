# Business Analysis — Inventory & Warehouse Management

**Work:** Defined receipt, issue, location and stock-count controls.

**Current-process scenario:** Paper GRNs, handwritten bin cards and spreadsheet issue registers leave stock balances and lot locations out of date.

**Proposed flow:** Receive → Inspect → Accept / quarantine → Put away → Issue / return → Cycle count → Reconcile.

| Control | Rule | Acceptance check |
| --- | --- | --- |
| Item and UOM | Maintain one stock unit per item and explicit purchase conversion. | A receipt in bags must convert to the approved stock unit. |
| Chronology | Post each item/store ledger in date order; reject a backdated movement before the last transaction. | Backdate a new issue and confirm it cannot change prior weighted averages. |
| Location control | Track stock location and lot separately from the resource master. | Find a lot by locator and reconcile its quantity. |
| Stock availability | Issues cannot make available stock negative. Quarantined quantities are unavailable. | An issue above available quantity is blocked. |
| Stock correction | Quantity/value corrections require approval and a cycle-count reference. | A pending correction cannot alter a posted balance. |

**Deliverables:** Stock ledger and locator model; Receipt-to-issue controls; Cycle-count and correction UAT.

**Owner / handoff:** Warehouse manager. Receipts reference purchase orders; store/item balances reconcile by movement, not by summing snapshots.

Hypothetical discovery and proposed configuration; [dataset fields and assumptions](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/inventory-warehouse.xlsx)
