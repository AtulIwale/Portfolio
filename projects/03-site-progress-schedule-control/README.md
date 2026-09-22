# Site Progress & Schedule Control

## Problem
Schedule slippage can hide inside weekly progress updates until a missed milestone makes it visible. Submittals can also remain unapproved while the team focuses on site production. This demo identifies sustained progress shortfalls and open approvals, with source records available for review.

## Approach

### Business Analysis
An activity is delayed when actual percentage complete / planned percentage complete is **strictly below 0.85 for two or more consecutive weekly dates**, seven days apart, anywhere in its recorded history. These are historical flags, not necessarily current delays.

A submittal is stuck when approved_date is blank and days_open is **greater than 21**. Status is displayed for context; it does not replace this rule.

“Weeks behind” means the **longest consecutive-week streak below 0.85**, not estimated finish-date slippage. An activity is answer-key positive if any of its weekly records has is_delayed = Y. These definitions were confirmed before implementation.

### Project Management
Scope: one self-contained offline HTML app, all activities and submittals, ranked delay lists, weekly evidence tables and precision/recall validation. Traceability and clear historical-versus-current wording were prioritized. No external dependencies, server, live ERP connection, project scheduling engine or automated decisions are included.

### Data Analysis & Data Science
- Join fact_progress to dim_activity by activity_id and answer_key by row_id.
- Sort each activity's weeks chronologically; calculate actual_pct_complete / planned_pct_complete without rounding before threshold comparisons.
- A missing week or zero planned percentage breaks a streak. Duplicate activity/week records and unmatched keys fail visibly.
- Rank delayed activities by longest streak, then lowest mean ratio within an equally long streak, then activity_id.
- Show latest planned/actual percentages and ratio from each activity's latest recorded week.
- Count a stuck submittal only if it has no approval date and days_open > 21. Use days_open as supplied, without recalculating against today's date.
- Use project_id for display because the workbook contains no project-name dimension.
- Source labels are used only for validation, not predictions. Activity details include every weekly row_id, date, planned percentage, actual percentage and calculated ratio.

### AI
This is an explainable rule-based detector, not a trained ML model. A future version could predict forthcoming slippage from weekly trends, approval aging and activity dependencies. It would require dated outcome labels, representative training data, time-based holdouts and evaluation against this baseline; a critical-path model would be needed to estimate finish-date delay.

## Data
Synthetic data patterned on real ERP structures. The original workbook is preserved at [data/03_Site_Progress_Schedule_Control.xlsx](data/03_Site_Progress_Schedule_Control.xlsx). All five sheets are also embedded as JSON inside index.html.

| Sheet | Records | Key / meaning |
| --- | ---: | --- |
| dim_activity | 50 | activity_id, project_id, activity_name, planned_start, planned_finish |
| fact_progress | 750 | row_id, activity_id, week_ending, planned_pct_complete, actual_pct_complete |
| fact_submittals | 300 | submittal_id, project_id, type, submission/approval dates, status, days_open |
| answer_key | 750 | Weekly row_id, is_delayed, delay_reason |
| data_dictionary | 24 | Source field definitions and units |

Source percentage values are fractions (0.25 means 25%). Source dates are embedded as ISO dates and blanks as null. The workbook is not modified. This progress ratio is not an earned-value SPI or a critical-path forecast.

## Validation
| Metric | Result |
| --- | ---: |
| Total activities | 50 |
| Historically delayed activities | **31** |
| Delayed through the latest recorded week | **0** |
| Total submittals | 300 |
| Stuck submittals | **25** |
| True positives | 17 |
| False positives | 14 |
| False negatives | 0 |
| True negatives | 19 |
| Precision | **54.8% (17/31)** |
| Recall | **100.0% (17/17)** |

There are 85 Y-labeled weekly records across 17 activities. The activity-level mapping above means these are in-sample synthetic checks, not held-out predictive performance. High recall does not remove the 14 false-positive activity flags.

Checks cover source-key uniqueness, complete joins, chronological streaks, strict threshold boundaries, missing weeks, zero planned percentages, approved submittals, the 21-day cutoff, and every activity's expandable evidence.

## How to run
Open index.html in any browser, or view it live at [Pages link](https://atuliwale.github.io/Portfolio/projects/03-site-progress-schedule-control/).


Click an activity row, or focus its button and press Enter, to expand its weekly evidence. The 19 activities without a qualifying streak are available in the separate expandable list. No installation or network connection is required.
