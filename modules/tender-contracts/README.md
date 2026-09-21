# Tendering & Contracts

**5,000 synthetic primary records. Version AEC-DEMO-2026.1.** One tender package and its contract outcome.

The same record IDs connect the workbook, business requirements, implementation plan, analysis, trained model and app.

- [Excel dataset](../../public/data/modules/tender-contracts.xlsx)
- [Business analysis](business-analysis.md)
- [Implementation plan](implementation.md)
- [Analysis and model evaluation](analysis-and-model.md)
- [Working app](https://atul-iwale-fieldwork.iwaleatul.chatgpt.site/ai-app/module-tender-contracts)
- [App source](../../src/modules/ModulePages.js)
- [Dataset generator](../../scripts/generate-modules.mjs)
- [Training pipeline](../../scripts/train-module-models.py)
- [Exported trained model](../../models/tender-contracts.json)

Reference concepts: Contract Management.txt, pp. 1–4; Procurement.txt, Purchase Enquiry. The supplied manual is not republished. All records, outcomes, thresholds and project estimates are demonstration assumptions.

Run `npm ci && npm run data && npm run build && npm start` from the repository root to use the application locally.
