# Production Planning — RCC

Coverage-tier, self-contained offline production review. GitHub-only delivery; no Pages configuration is included.

## Problem

Production orders with substantial output shortfall and rework need traceable review. Rework can also occur on orders that meet or exceed plan, but those orders have a different evidence status. The app separates confirmed dataset patterns from proactive review without a blended score or invented trend alerts.

## Approach

### Business Analysis

**Confirmed output-gap risk:** require both conditions globally, with **no item allowlist**:

- Shortfall `(planned_qty - actual_qty) / planned_qty >= 0.15`.
- Rework `rework_qty / actual_qty >= 0.10`.

Decisions use unrounded ratios. Percentages are displayed to two decimals. The 70 matches naturally belong to RCC003 (24), RCC007 (23) and RCC012 (23); those IDs are not inputs to classification.

**Proactive review — unscored, Not covered by answer_key — for manual review:** positive rework quantity with actual output at or above plan, excluding confirmed flags. It contains **203 orders across 36 items**, split into **15 meets-plan** orders (`actual_qty == planned_qty`) and **188 exceeds-plan** orders (`actual_qty > planned_qty`). Negative shortfall percentages indicate output above plan. An N output-gap label does not validate or invalidate proactive review.

**Trend alerts:** **Not evaluated — trend definition not specified.** Dated history is present, but no window, aggregation rule or significance threshold is defined, and completion dates can tie. No trend thresholds or alerts are invented.

### Project Management

Scope: a single offline HTML app, unchanged workbook in `data/`, confirmed and separately split proactive worklists, item/search filters, completion/shortfall/rework/ID ordering, source-evidence dialogs and worklist-specific CSV exports. No production posting, live integration, external scripts or automated decisions. No blended metric or combined risk score.

### Data Analysis & Data Science

Join `fact_production_order.item_id` to `dim_item_bom.item_id`. Apply the global two-threshold rule to raw order fields, then join `answer_key` by `order_id` for agreement evaluation. Labels do not feed classification. Filtering changes displayed worklists, not classification or full-snapshot validation.

The dictionary defines `actual_qty` as accepted production quantity. It is **not reduced again** by `rework_qty`. The requested rework ratio is rework divided by accepted actual output; the workbook does not supply a total-throughput denominator. Quantities are not summed across items because units of measure are unspecified. BOM quantity is shown as source context, not used to infer material waste without actual material-consumption data.

Snapshot reference is **2026-09-11**, the latest completion date. No current-clock aging is used. Source evidence shows the original order, item/BOM row, answer-key row and calculation numerators, denominators and unrounded ratios.

### AI

**Deterministic, not a trained model.** No ML, training, probability, forecasting or independent model evaluation. The confirmed category displays **“Answer-key agreement: 100% precision / 100% recall.”** This is agreement with the labeled dataset, **not independent validation**.

Thresholds were selected after inspecting the data and labels. Either shortfall >=15% alone or rework >=10% alone also reproduces all 70 labels. Requiring both implements the approved rule but adds no discrimination in this workbook. This result does not establish performance on unseen production data.

## Data

[12_Production_Planning_RCC.xlsx](data/12_Production_Planning_RCC.xlsx) is copied byte-for-byte from the supplied workbook. All four sheets are embedded as JSON in `index.html`, with numeric quantities, ISO dates and the source SHA-256 checksum for provenance.

| Sheet | Rows |
| --- | ---: |
| dim_item_bom | 40 |
| fact_production_order | 700 |
| answer_key | 700 |
| data_dictionary | 17 |

There are 36 items with production orders. Order dates span 2024-10-02 to 2026-08-23; completion dates span 2024-10-06 to 2026-09-11. The source is synthetic ERP-style demonstration data. Labels contain 70 Y and 630 N rows.

Editing the workbook does not refresh the embedded app automatically. Refreshing requires re-extracting the sheets/checksum into `source-data` and reconciling the rules, counts and documentation. The app fails visibly if its snapshot no longer supports the documented agreement or proactive split.

## Validation

### Confirmed output-gap risk only

| TP | FP | FN | TN | Precision | Recall |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 70 | 0 | 0 | 630 | **100%** | **100%** |

Evaluation covers all 700 orders, globally, without an item allowlist.

| Source label | Orders | Shortfall range | Rework range |
| --- | ---: | ---: | ---: |
| Y | 70 | 21.1511%–38.1579% | 18.1818%–36.9369% |
| N | 630 | −4.0404%–8.8889% | 0%–5.6604% |

Every threshold combination within **10–15% shortfall** and **8–10% rework** produces the same 70 IDs. All four boundary combinations were checked; the nonoverlapping numeric ranges establish the interior result. The chosen app thresholds are **15% and 10%**, inclusive, joined by AND.

### Proactive review — unscored

| Check | Result | Precision / recall |
| --- | ---: | --- |
| Rework, exactly meets plan | 15 orders | Not covered by answer_key |
| Rework, exceeds plan | 188 orders | Not covered by answer_key |
| Total rework without shortfall | 203 orders | Unscored; no combined accuracy metric |
| Trend alerts | Not evaluated | Trend definition not specified |

Confirmed and proactive sets are disjoint. The proactive count is a worklist total, not a blended risk score.

Read-only source checks found unique IDs, complete item/label joins, positive planned and actual denominators, nonnegative rework no greater than actual quantity, and no completion dates before order dates. DOM-based JavaScript checks verified counts, inclusive threshold boundaries and AND behavior, filters/reset, sorting, source evidence, proactive CSV content and snapshot date. These checks do not substitute for visual browser QA.

## How to run

Download this folder and open **index.html** in a modern browser. No installation, server or internet connection is needed. Keep the README and `data/` beside it to use their links.

Filter by item, search by order/item ID or item name, or change display order. Click an order ID for source records and calculations. Export each displayed confirmed, meets-plan or exceeds-plan worklist separately. Exports retain raw quantities, numeric ratios and the appropriate assessment wording. The app does not modify the workbook.
