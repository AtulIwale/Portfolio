# Inventory & Warehouse Management

Coverage-tier, self-contained offline app. GitHub-only delivery; no GitHub Pages setup or hosting is requested.

## Problem

Large negative stock adjustments can concentrate around particular item/recorder pairs. Operational stock-review questions also matter, but they have different evidence requirements. This app separates the workbook's validated adjustment pattern from assumption-based manual review, without inventing opening balances or blending accuracy scores.

## Approach

### Business Analysis

**Confirmed adjustment-concentration risk:** a transaction must satisfy all three conditions:

1. `txn_type = Adjustment` and `quantity <= -50`.
2. Its `(item_id, recorded_by)` pair has at least two negative Adjustment transactions.
3. The pair's absolute negative-adjustment quantity is at least **40%** of the item's total absolute negative-adjustment quantity across all recorders and warehouses.

Both volume sums include all negative adjustments, including small ones. Positive adjustments do not offset negative volume. Calculations use the full snapshot before UI filtering; no item or employee IDs are hard-coded. The pattern is two dominant recorders per item, not one recorder exceeding every other recorder.

**Stock-level review:** entirely unscored and labeled **“assumption-based, not covered by answer_key”**. It has four separate worklists/checks:

- **Below reorder:** compare a user-entered on-hand quantity as of 2026-09-22 with an editable threshold for that item × warehouse. The starting threshold is explicitly assumed to be **10 units in the item's unit of measure**, not a supplied business policy. The user can replace it. Only strictly lower quantities trigger review; equality does not. Blank input means not evaluated. All quantities are session-only and clear on reload. No opening balance or on-hand quantity is inferred from transactions.
- **Stale:** at least **90 calendar days** since the latest nonzero transaction for each observed item × warehouse, as of **2026-09-22**. Adjustments count as movement. Combinations absent from the source are not evaluated. Staleness does not imply remaining physical stock.
- **Possible duplicates:** different transaction IDs with identical item, warehouse, transaction type, raw quantity, date and recorder. All rows of a matching group are shown. Legitimate repeat movements may have identical fields.
- **Possible reversals:** same item × warehouse, equal-and-opposite movement effects within **seven calendar days inclusive**. Inward effect is `+abs(quantity)`, Outward is `-abs(quantity)`, and Adjustment uses signed quantity. Recorder may differ. Every matching unordered pair is shown, including same-day candidates; no one-to-one allocation or reversal certainty is asserted. This window is an assumption, and the workbook has no reversal-reference field.

Negative/impossible running-balance checks are intentionally omitted: the workbook supplies no opening balance. It also has no reorder points or on-hand snapshots. Review worklists can overlap with one another and confirmed transactions; counts have different units and must not be summed into a risk total.

### Project Management

Scope: one offline `index.html`, unchanged source workbook in `data/`, separate confirmed and manual-review sections, search and warehouse filters, source-evidence dialogs, session-only below-reorder inputs and category-specific CSV exports for the transaction/staleness worklists. No live ERP connection, stock posting, automated decisions, server, external scripts or Pages configuration is included.

### Data Analysis & Data Science

Use exact `txn_id` joins to the answer key, `item_id` joins to `dim_item`, and `warehouse_id` joins to `dim_warehouse`. Validate unique IDs, label coverage, dimension joins, transaction types, numeric quantities and snapshot date bounds before displaying results. The confirmed classifier reads transaction fields only; labels are used afterward for the agreement calculation. Its thresholds were chosen after inspecting the same data and labels.

Dates use UTC calendar-day differences. No quantities are summed across different items or units. Source Outward quantities are positive even though the dictionary says negative values reduce stock; the explicit type-based movement convention applies only to reversal matching. No running balance is computed.

Click a transaction ID to see its original transaction, answer-key label, item and warehouse records, concentration numerator/denominator and same-item/warehouse transaction history. Filters change displayed rows, not classification or concentration denominators. CSV exports preserve category-specific assessment wording.

### AI

**Deterministic, not a trained model.** No ML, fitting, probabilities or predictive claims. The displayed metric is **“Answer-key agreement: 100% precision / 100% recall.”** This is agreement with the labeled dataset, **not independent discrimination or model validation**.

`quantity <= -50` alone, restricted to Adjustment transactions, also reproduces all 120 Y labels. The concentration and repeat-count conditions add no discrimination in this workbook. Threshold selection after seeing the labels means the result is not an independent evaluation. The full-snapshot calculation includes future records relative to earlier transactions and is not a historical forecast.

## Data

[08_Inventory_Warehouse_Management.xlsx](data/08_Inventory_Warehouse_Management.xlsx) is copied unchanged from the supplied attachment. All five sheets are embedded as JSON in `index.html`; dates are ISO strings, numbers remain numeric, and the source SHA-256 checksum is embedded for provenance.

| Sheet | Rows |
| --- | ---: |
| dim_item | 80 |
| dim_warehouse | 12 |
| fact_stock_transaction | 1,200 |
| answer_key | 1,200 |
| data_dictionary | 21 |

Transaction dates run from 2024-10-01 through 2026-09-22. There are 480 Adjustment, 360 Inward and 360 Outward rows, and 221 observed item × warehouse combinations. The answer key contains 120 Y and 1,080 N labels. This is synthetic ERP-style demonstration data; it does not establish real-world losses or misconduct.

Editing the workbook does not automatically refresh the embedded app. Refreshing requires re-extracting the five sheets and checksum into `source-data`, then reconciling the rule, counts, assumptions and documentation. The current app fails visibly if the snapshot no longer supports its documented confirmed-category agreement.

## Validation

### Confirmed adjustment-concentration risk

| True positives | False positives | False negatives | True negatives | Precision | Recall |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 120 | 0 | 0 | 1,080 | **100%** | **100%** |

Agreement is measured at transaction level across all 1,200 rows. Every labeled adjustment is between -450 and -83; every N-labeled adjustment is between -25 and +25. The magnitude-only rule selects exactly the same IDs as the approved three-condition rule.

| Item | Recorder | Confirmed transactions | Share of item's negative-adjustment volume |
| --- | --- | ---: | ---: |
| ITM0005 | EMP0042 | 20 | 48.18% |
| ITM0005 | EMP0088 | 20 | 51.28% |
| ITM0012 | EMP0042 | 20 | 54.15% |
| ITM0012 | EMP0088 | 20 | 45.52% |
| ITM0021 | EMP0042 | 20 | 52.59% |
| ITM0021 | EMP0088 | 20 | 47.41% |

### Stock-level review — unscored

| Check | Initial result | Precision / recall |
| --- | --- | --- |
| Below reorder | **Not evaluated**: 0 of 221 positions have supplied on-hand quantities | Not covered by answer_key |
| Stale, 90+ days | **114 item × warehouse combinations** | Not covered by answer_key |
| Possible duplicates | **0 transaction rows** | Not covered by answer_key |
| Possible reversals, seven-day window | **0 transaction pairs** | Not covered by answer_key |

Zero candidates means no matches under these particular assumptions, not proof of clean stock records. No precision/recall is reported for these checks, and no blended metric is calculated. A settlement-style confirmed-versus-review distinction is preserved without treating all N labels as review negatives.

Source checks and DOM-based JavaScript checks verify agreement, review counts, filtering, evidence content, below-reorder input behavior and rule boundaries. These checks do not substitute for a visual browser review.

## How to run

Download this folder and open **index.html** in a modern browser. No installation, server or internet connection is required. Keep `README.md` and `data/` alongside the app for the documentation and workbook links.

Use search or the warehouse filter, inspect a transaction ID, or export a displayed worklist. To run below-reorder review, select an observed item × warehouse, enter its on-hand quantity and verify/change the assumed threshold. These entries are temporary and do not modify the workbook. Reloading clears them.
