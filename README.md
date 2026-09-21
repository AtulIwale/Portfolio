# Atul Iwale — Connected AEC Module Projects

One dataset per construction ERP module, used consistently for Business Analysis, implementation planning, Data Analysis & Data Science, Machine Learning and a working review app.

**8 modules · 40,000 synthetic primary records · 8 Excel workbooks · 8 trained models and apps**

This repository replaces the previous portfolio examples. Previous content remains recoverable in Git history.

## Projects and datasets

| Module | Primary records | Project documentation | Excel dataset |
|---|---:|---|---|
| Tendering & Contracts | 5,000 | [Open project](modules/tender-contracts) | [Download Excel](public/data/modules/tender-contracts.xlsx) |
| Procurement & Subcontracting | 5,000 | [Open project](modules/procurement-subcontracting) | [Download Excel](public/data/modules/procurement-subcontracting.xlsx) |
| Inventory & Warehouse Management | 5,000 | [Open project](modules/inventory-warehouse) | [Download Excel](public/data/modules/inventory-warehouse.xlsx) |
| Real Estate Sales | 5,000 | [Open project](modules/real-estate-sales) | [Download Excel](public/data/modules/real-estate-sales.xlsx) |
| Construction Assets — Fixed & Movable | 5,000 | [Open project](modules/construction-assets) | [Download Excel](public/data/modules/construction-assets.xlsx) |
| Accounts Receivable & Accounts Payable | 5,000 | [Open project](modules/receivables-payables) | [Download Excel](public/data/modules/receivables-payables.xlsx) |
| Construction HR | 5,000 | [Open project](modules/construction-hr) | [Download Excel](public/data/modules/construction-hr.xlsx) |
| Construction Payroll | 5,000 | [Open project](modules/construction-payroll) | [Download Excel](public/data/modules/construction-payroll.xlsx) |

## Run locally

Node.js 24 or later is required. Python is only needed to retrain the models; the apps can use the checked-in trained models.

```bash
npm ci
npm run data
npm run build
npm test
npm start
```

Open http://localhost:4173. `npm run data` deterministically regenerates the same record IDs and values, then applies the versioned model files. The eight Excel files are included. HR and Payroll are separate employee-month datasets connected through attendance IDs.

## Repository structure

- `modules/`: module-specific business requirements, implementation plans, analysis and model evaluation.
- `src/modules/`: shared React project pages, evidence assistant, filters, record inspection, CSV export and what-if inference.
- `scripts/generate-modules.mjs`: seeded generation of primary records, related records and shared masters.
- `scripts/train-module-models.py`: training, temporal holdout evaluation and data checks.
- `models/`: actual exported decision trees and measured evaluations.
- `public/data/modules/`: downloadable Excel workbooks; generated JSON is recreated with `npm run data`.
- `tests/`: model parity, dataset and linked HR/Payroll checks.

## Retrain

```bash
python3 -m pip install -r requirements.txt
npm run data
npm run train
npm run build
npm test
```

The Python pipeline updates canonical JSON, website metrics and checked-in model exports. Excel risk scores remain tied to their documented version; changing the model does not silently alter the workbooks.

Excel source is in `scripts/build-module-workbook.mjs`. Re-authoring workbooks requires `@oai/artifact-tool` in the ChatGPT spreadsheet runtime. Set `MODULE_SITE_ROOT` to this checkout and `MODULE_OUTPUT` to an output folder, then run the script with a module ID. The supplied workbooks can be used without this authoring dependency.

## Method and limitations

Version AEC-DEMO-2026.1; seed 20260921. Records cover January–October 2024; the reporting snapshot is 1 March 2025. Each workbook includes nine sheets: Summary, Records, Details, Events, Masters, Dictionary, Requirements, Implementation and Model. Amount examples use INR.

Field concepts reference the user-supplied Xpedeon documentation. The original manual is not included. Records, business thresholds, tax/deduction rates and implementation costs are synthetic demonstration assumptions, not actual client data or statutory calculations.

ML uses depth-four decision trees with at least 60 training examples per leaf. January–May records train the model only when outcomes are known before August; June–July are excluded; August–October form the holdout. Status, completion, payment and outcome fields are not model inputs. Repeated entities can occur across periods. Metrics describe synthetic data only and do not establish real-world performance.

The apps perform local inference with the actual exported models. Their evidence assistant supports deterministic count, total and highest-score questions; it does not call a generative LLM or authorize business decisions. Portfolio implementation plans are illustrative plans, not claims of completed client implementations.

[Portfolio website](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/process-projects.html) · [AI Apps](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app.html)
