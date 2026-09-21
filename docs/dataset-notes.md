# Dataset notes

- **Version:** AEC-DEMO-2026.1; seed 20260921; 5,000 primary records per module.
- **Dates:** January–October 2024; reporting date 1 March 2025; amounts use INR.
- **Workbook sheets:** Summary, Records, Details, Events, Masters, Dictionary, Requirements, Implementation, Model.
- **Same data throughout:** workbook IDs match generated JSON, analysis, exported models and app evidence. HR and Payroll join through attendance IDs.
- **Validation:** unique IDs, related-record joins, module arithmetic, HR/payroll eligibility and Python/JavaScript scoring parity.
- **Source:** field concepts paraphrased from the supplied Xpedeon documentation; the original manual is not distributed.
- **Assumptions:** all records, workflow thresholds, rates and implementation estimates are synthetic. Plans are portfolio designs, not completed client deployments. Workbook fields are documented in Dictionary; additional configuration requirements are not claimed as populated observations.

## Model evaluation

Depth-four decision trees, minimum 60 training rows per leaf. Train on January–May records whose labels were known before August; exclude June–July; test on August–October. Status, completion, settlement and outcome fields are excluded from inputs. Repeated entities may appear in both periods.

Scores are uncalibrated tree frequencies on synthetic data. They support review, not automatic approvals or employment decisions. Accuracy uses a 0.50 threshold; lower Brier is better. Baseline comparisons and weak results are retained.

## Reproduce

[Run locally / retrain](run-locally.md). Generation code: [generate-modules.mjs](../scripts/generate-modules.mjs). Validation and training: [train-module-models.py](../scripts/train-module-models.py).

Changing a trained model does not update the included Excel files automatically; regenerate and version the workbooks together with the data.
