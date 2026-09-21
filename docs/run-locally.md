# Run the projects

## Quick start

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


