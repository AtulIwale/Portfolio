# Business Analysis — Construction Assets — Fixed & Movable

**Work:** Defined asset registration, custody, maintenance and retirement controls.

**Current-process scenario:** Asset registers, paper logbooks and informal site transfers make location, operating hours and maintenance responsibility difficult to verify.

**Proposed flow:** Acquire → Capitalize → Assign custodian → Deploy → Log use → Maintain → Depreciate → Retire.

| Control | Rule | Acceptance check |
| --- | --- | --- |
| Asset register | Separate fixed assets from movable plant while retaining one unique ID. | Reject duplicate serial/asset registrations. |
| Custody and transfer | Transfers require receiving-site acceptance and effective dates. | Verify no overlapping active location for one asset. |
| Maintenance | Prevent deployment of unavailable equipment and track planned servicing. | A maintenance status blocks a new deployment. |
| Depreciation | Use an explicit demonstration straight-line policy; preserve book/period. | Never depreciate below the residual value. |
| Retirement | Retired assets cannot accrue new utilization. | Subsequent retired snapshots must show zero available/operating hours. |

**Deliverables:** Asset lifecycle and custody controls; Maintenance and depreciation design; Transfer and retirement UAT.

**Owner / handoff:** Plant and asset manager. Plant operator IDs share the HR master; asset cost is a snapshot, depreciation is a monthly flow.

Hypothetical discovery and proposed configuration; [dataset fields and assumptions](../../docs/dataset-notes.md).

[Module overview](README.md) · [Excel dataset](../../public/data/modules/construction-assets.xlsx)
