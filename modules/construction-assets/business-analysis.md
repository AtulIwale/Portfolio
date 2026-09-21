# Business analysis — Construction Assets — Fixed & Movable

## AS-IS discovery scenario

Asset registers, paper logbooks and informal site transfers make location, operating hours and maintenance responsibility difficult to verify.

Hypothetical scenario, not a claim about an actual company.

## TO-BE workflow

Acquire → Capitalize → Assign custodian → Deploy → Log use → Maintain → Depreciate → Retire

Process owner: Plant and asset manager.

| Requirement | Data concepts | Rule | Acceptance test |
|---|---|---|---|
| Asset register | asset_id, asset_type, acquisition_cost | Separate fixed assets from movable plant while retaining one unique ID. | Reject duplicate serial/asset registrations. |
| Custody and transfer | project_id, custodian_id | Transfers require receiving-site acceptance and effective dates. | Verify no overlapping active location for one asset. |
| Maintenance | maintenance_due_hours, operating_hours | Prevent deployment of unavailable equipment and track planned servicing. | A maintenance status blocks a new deployment. |
| Depreciation | useful_life_months, residual_value | Use an explicit demonstration straight-line policy; preserve book/period. | Never depreciate below the residual value. |
| Retirement | status, retirement_date | Retired assets cannot accrue new utilization. | Subsequent retired snapshots must show zero available/operating hours. |

## Deliverables

- Asset lifecycle and custody controls
- Maintenance and depreciation design
- Transfer and retirement UAT

Plant operator IDs share the HR master; asset cost is a snapshot, depreciation is a monthly flow.
