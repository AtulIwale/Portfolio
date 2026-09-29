"""'How strong is the evidence?' tables, one per post. Only restates claims
already made and cited in each post; strength is my editorial judgement."""
from build import table

INTRO = ('<p>Not every finding in this note rests on the same kind of evidence. This is how I would weigh each one before acting on it.</p>')

def grade(rows):
    tag = {'Strong': 'Strong', 'Moderate': 'Moderate', 'Indicative': 'Indicative'}
    body = [[r[0], r[1], f'<strong>{tag[r[2]]}</strong>', r[3]] for r in rows]
    return INTRO + table(['Finding', 'Evidence', 'Strength', 'Main caveat'], body,
                         'Strong: large official data sets or peer-reviewed studies. Moderate: a single study or a specific population. Indicative: surveys, vendor-backed reports or synthetic tests.')

EVIDENCE = {
 'insight-osha-severe-injuries': grade([
   ['Falls are the largest cause of severe injuries', '19,021 official OSHA reports over ten years', 'Strong', 'Federal-OSHA states and severe injuries only'],
   ['Caught-in accidents drive most amputations', 'Same data, amputation recorded per report', 'Strong', 'Coding line with struck-by moved in 2024'],
   ['Falls, slips and trips lead construction fatalities', 'BLS Census of Fatal Occupational Injuries', 'Strong', 'Counts, not rates per hour worked'],
   ['A simple model codes causes about as well as coders agree', 'Time-split test on 3,204 later reports', 'Moderate', 'US narratives; re-test on your own reports']]),
 'insight-permit-wait-times': grade([
   ['Approved-only averages understate the wait', 'Statistical property of censored data; 29,123 NYC filings', 'Strong', 'Size of the gap varies by place and year'],
   ['Survival models give calibrated probabilities', 'Out-of-time test on 5,708 NYC filings', 'Moderate', 'One city, one department, one period'],
   ['Long permit times go with weaker productivity', 'Federal Reserve analysis of US metro areas', 'Moderate', 'Association, not proof of cause'],
   ['Regulation is about a quarter of a new home’s price', 'NAHB builder survey, 2021', 'Indicative', 'Industry-association estimate']]),
 'insight-cost-estimates-miss': grade([
   ['Most large projects overrun cost and schedule', 'Database of 16,000+ projects across sectors', 'Strong', 'Large projects; mix of sectors and countries'],
   ['Early estimates are biased low, not randomly wrong', 'Consistent finding across the overrun literature', 'Strong', 'Size of bias differs by project type'],
   ['Reference-class uplifts correct the bias', 'UK Treasury guidance built on project data', 'Moderate', 'Uplift values come from UK public projects'],
   ['ML estimates with calibrated ranges beat coefficients', 'My test on later projects', 'Indicative', 'Synthetic data; needs a firm’s own history']]),
 'insight-forecasting-final-cost': grade([
   ['Cumulative CPI settles by 20% complete', '155 US defence contracts, 1971–1991', 'Moderate', 'Defence programmes with mature EVM'],
   ['CPI can take much longer to settle elsewhere', '136 environmental remediation projects', 'Moderate', 'One agency, two fiscal years'],
   ['CPI stability is rare on smaller commercial work', 'Later research, summarised by a practitioner', 'Indicative', 'Secondary summary of the studies'],
   ['ML beats the CPI formula early in a project', 'My test on 239 completed projects', 'Indicative', 'Synthetic data; validate on real history']]),
 'insight-rework-bad-data': grade([
   ['Rework costs 2–20% of contract value', 'Construction Industry Institute research', 'Moderate', 'Wide range; depends on project type'],
   ['Rework can be predicted before construction', 'CII Field Rework Index studies', 'Moderate', 'Mainly industrial projects'],
   ['Poor data and communication cause ~half of rework', 'Survey of ~600 US construction leaders', 'Indicative', 'Self-reported; vendor-sponsored report'],
   ['Real data sets carry duplicates, unit and code errors', 'Counts from my own cleaning pipelines', 'Strong', 'Examples, not a rate across the industry']]),
 'insight-construction-productivity': grade([
   ['Construction productivity has grown far slower than the economy', 'MGI global analysis; US national accounts', 'Strong', 'Output is hard to measure in construction'],
   ['The decline is not just a measurement artefact', 'Federal Reserve test of deflator bias', 'Strong', 'Relies on assumptions about quality change'],
   ['Physical output per worker in housing is flat or falling', 'NBER study of physical measures', 'Moderate', 'Housing only'],
   ['Long permit times go with the biggest declines', 'Federal Reserve metro-area estimates', 'Moderate', 'Association, not proof of cause']]),
 'insight-llms-construction-documents': grade([
   ['General-purpose LLMs hallucinate often on legal questions', 'Peer-reviewed study, large verifiable question set', 'Strong', '2023 models; newer models may differ'],
   ['Retrieval reduces but does not remove hallucination', 'Preregistered study of commercial legal tools', 'Strong', 'Legal research, not construction documents'],
   ['Bounded tasks with checks are far more accurate', 'My OSHA and ERP chatbot tests', 'Moderate', 'Two projects; ERP test on synthetic data'],
   ['Confabulation is a core generative-AI risk', 'NIST AI 600-1 framework', 'Strong', 'A framework, not a measurement']]),
 'insight-payroll-fraud': grade([
   ['Frauds run about a year and are found mostly by tips', 'ACFE study of 1,921 cases in 138 countries', 'Moderate', 'Cases investigated by fraud examiners'],
   ['Organisations lose about 5% of revenue to fraud', 'ACFE survey estimate', 'Indicative', 'Survey-based estimate, not measured'],
   ['Isolation Forest isolates anomalies efficiently', 'Peer-reviewed method (ICDM 2008)', 'Strong', 'Finds unusual lines, not proof of fraud'],
   ['Peer-relative features beat audit rules on payroll', 'My test with seeded issues', 'Indicative', 'Synthetic data; misses proxy attendance']]),
 'insight-material-price-escalation': grade([
   ['Input prices rose far faster than bid prices in 2020–21', 'BLS producer price indices, AGC analysis', 'Strong', 'US market; one exceptional period'],
   ['Prices can fall as fast as they rise', 'BLS monthly lumber prices', 'Strong', 'Lumber is more volatile than most inputs'],
   ['Index-based clauses share price risk by formula', 'FIDIC 2017 and CPWD contract conditions', 'Strong', 'Only if the clause is included and indices named'],
   ['Rebasing prices improves cost models', 'Standard QS practice; my estimating model', 'Moderate', 'Index weights must match your cost mix']]),
}

EVIDENCE.update({
 'insight-contract-clause-risk': grade([
   ['Poor contracting erodes about 8.6% of value', 'WorldCC cross-industry research', 'Indicative', 'Survey-based estimate across industries'],
   ['Contract document errors are the top dispute cause', 'Arcadis annual disputes survey', 'Moderate', 'North American cases reported to one firm'],
   ['A CNN reading wording beats keyword rules', 'My test on 800 later clauses', 'Indicative', 'Synthetic clauses are more regular than real ones'],
   ['Reviewer judgement caps model accuracy', 'Model agreement with six reviewers, 85–89%', 'Moderate', 'Measured on synthetic reviewer labels']]),
 'insight-construction-payments': grade([
   ['US construction payment cycles are long', 'Rabbet 2024 industry survey', 'Indicative', 'Vendor-sponsored survey'],
   ['Small suppliers must be paid within 45 days', 'MSMED Act 2006, s.15–16', 'Strong', 'Applies to registered micro and small enterprises'],
   ['Confirmed risk and patterns should stay separate', 'Design principle shown in my AR/AP app', 'Moderate', 'Evidence viewer, not a tested predictor']]),
 'insight-inventory-records': grade([
   ['Most inventory records are inaccurate', 'Peer-reviewed study of ~370,000 records', 'Strong', 'Retail, one company; construction untested'],
   ['Auditing reduces inaccuracy', 'Same study', 'Moderate', 'Association within one retailer'],
   ['Adjustment concentration flags where to look', 'My rule on synthetic stock data', 'Indicative', 'Size alone reproduced the labels here']]),
 'insight-predictive-maintenance': grade([
   ['Predictive maintenance saves 8–12% over preventive', 'US DOE FEMP guidance', 'Moderate', 'Facility equipment, not mobile plant'],
   ['Fixed alarm limits warn too late', 'My test against OEM-style limits', 'Indicative', 'Synthetic telematics'],
   ['Tree models suit patchy sensor data', 'Seven-model comparison, time-split test', 'Indicative', 'Five-month synthetic test window']]),
 'insight-booking-cancellations': grade([
   ['Advance capped at 10% before a registered agreement', 'RERA 2016, s.13', 'Strong', 'State rules add detail'],
   ['Late first payment is the strongest early signal', 'Odds ratios on my synthetic bookings', 'Indicative', 'Synthetic data built with these patterns'],
   ['Simple models match complex ones at this size', 'Seven classifiers on 465 later bookings', 'Moderate', 'Small sample; ranking is fragile']]),
 'insight-attendance-before-payroll': grade([
   ['One in five payrolls has errors, $291 each', 'EY survey of 508 US payroll staff', 'Indicative', 'US firms of 250–10,000 employees'],
   ['Overtime on building work is paid at double rate', 'BOCW Act 1996, s.29', 'Strong', 'Normal hours set by state rules'],
   ['Three checks catch attendance errors before payroll', 'Rules on my synthetic attendance data', 'Indicative', 'Agreement with labels is by construction']]),
})
