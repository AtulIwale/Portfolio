export const moduleSummaries={
  "tender-contracts": [
    "Defined bid comparisons, award approvals and contract variation controls.",
    "Planned tender migration, approval setup, UAT and rollout costs.",
    "Compared package values, tender outcomes and monthly award activity.",
    "Trained an award-delay model and built a tender review app."
  ],
  "procurement-subcontracting": [
    "Mapped requisitions, order types, approvals and invoice-matching requirements.",
    "Planned supplier migration, order configuration, UAT and implementation costs.",
    "Analysed order values, delivery outcomes and procurement status patterns.",
    "Trained a delivery-risk model and built an order review app."
  ],
  "inventory-warehouse": [
    "Defined receipt, issue, location and stock-count controls.",
    "Planned opening-stock migration, warehouse setup, testing and cutover.",
    "Analysed stock movements, record statuses and count exceptions.",
    "Trained a stock-exception model and built a movement review app."
  ],
  "real-estate-sales": [
    "Mapped enquiry-to-booking workflows, discounts and collection controls.",
    "Planned unit migration, booking configuration, UAT and rollout costs.",
    "Compared sales values, booking stages and opportunity outcomes.",
    "Trained a booking-loss model and built a sales follow-up app."
  ],
  "construction-assets": [
    "Defined asset registration, custody, maintenance and retirement controls.",
    "Planned asset migration, maintenance setup, testing and implementation costs.",
    "Analysed depreciation, asset status and monthly operating records.",
    "Trained a breakdown-risk model and built an asset review app."
  ],
  "receivables-payables": [
    "Defined invoice matching, settlement allocation and aging controls.",
    "Planned balance migration, finance configuration, UAT and cutover.",
    "Analysed invoice values and settlement states across AR and AP.",
    "Trained a late-settlement model and built an invoice review app."
  ],
  "construction-hr": [
    "Mapped attendance, leave, overtime approvals and payroll handoffs.",
    "Planned employee migration, attendance setup, UAT and rollout costs.",
    "Analysed worked days, attendance statuses and clerical corrections.",
    "Trained a record-quality model and built an attendance review app."
  ],
  "construction-payroll": [
    "Defined pay calculations, deductions, reconciliation and release controls.",
    "Planned pay-element setup, parallel runs, UAT and cutover costs.",
    "Reconciled net pay, attendance links and payroll processing states.",
    "Trained a payroll-correction model and built a pay review app."
  ]
};
export const areaFiles={'business-analysis':'business-analysis.md',implementation:'implementation.md',analysis:'data-analysis.md','machine-learning':'machine-learning-ai.md'};
export const moduleAreaGithubPath=(m,area)=>'https://github.com/AtulIwale/Portfolio/blob/main/modules/'+m.id+'/'+areaFiles[area];
