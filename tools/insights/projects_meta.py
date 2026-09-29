"""Project layer for the Insights notes: one note per portfolio project, in the
order of the Projects page. Facts come from each project's README."""
from build import c, bars, table, callout

GH = 'https://github.com/AtulIwale/Portfolio/tree/main/projects/'
LIVE = 'https://atuliwale.github.io/Portfolio/projects/'

def links(folder, *pages):
    out = [(label, LIVE + folder + '/' + page) for label, page in pages]
    return out + [('Code and README', GH + folder)]

# slug -> project number (Projects page order), name, data type, links and brief
META = {
 'insight-osha-severe-injuries': dict(no=1, name='Construction Safety Intelligence', data='Real public data (OSHA)',
   links=links('14-construction-safety-intelligence', ('Live app', '')),
   brief=[('Problem', 'Contractors’ injury reports stay as unread text because most firms have no trained coders.'),
          ('Decision supported', 'Where to focus safety effort, by hazard and by trade.'),
          ('Data', '19,021 OSHA severe-injury reports from construction, Jan 2015 – Nov 2025.'),
          ('Method', 'Keyword baseline, linear text models, CNN, BiLSTM and a blind LLM; trained on earlier years, tested on 2024–2025.'),
          ('Result', '84% agreement with OSHA’s coders (keywords: 55%); 89% where model and LLM agree.'),
          ('Limits', 'Severe injuries only, from one regulator’s jurisdiction; a 2024 coding-manual change needs monitoring.')]),
 'insight-permit-wait-times': dict(no=2, name='NYC Permit Approval Forecast', data='Real public data (NYC Open Data)',
   links=links('15-nyc-permit-approval-forecast', ('Live app', '')),
   brief=[('Problem', 'Approval dates for major building filings are guesses, and averages hide the slow cases.'),
          ('Decision supported', 'When to plan the start, how much float to hold, how long to budget holding costs.'),
          ('Data', '29,123 NYC DOB NOW filings, 2021–2026; a quarter still waiting.'),
          ('Method', 'Kaplan–Meier, Cox, random survival forest and XGBoost AFT, tested on later filings.'),
          ('Result', 'Approved-only median understates the wait by 47 days; probabilities within ~3.5 points of outcomes.'),
          ('Limits', 'Ranking is modest (C-index ~0.69); drawing quality and examiner are not in the data.')]),
 'insight-cost-estimates-miss': dict(no=3, name='Cost Plan Estimation (ML)', data='Synthetic data',
   links=links('13-cost-plan-estimation', ('Live app', '')),
   brief=[('Problem', 'Feasibility-stage cost plans rely on coefficients that ignore how similar projects actually turned out.'),
          ('Decision supported', 'Go/no-go and budget setting at feasibility, with an honest range.'),
          ('Data', '1,800 synthetic projects patterned on Indian cost plans, rebased to Jan-2018 prices.'),
          ('Method', 'Tree models trained on 2018–2023 starts, tested on 2024–2025; quantile ranges.'),
          ('Result', '6.6% average error vs 11.2% for the coefficient method; P10–P90 covered 81% of later projects.'),
          ('Limits', 'Synthetic data; must be re-tested on a firm’s own completed projects.')]),
 'insight-contract-clause-risk': dict(no=4, name='Contract Lifecycle Intelligence', data='Synthetic data',
   links=links('05-contract-lifecycle-intelligence', ('Live app', ''), ('Clause Risk Reader (ML)', 'ml.html')),
   brief=[('Problem', 'High-risk clauses go unreviewed while contracts approach expiry and auto-renewal.'),
          ('Decision supported', 'Which clauses and contracts need legal review first.'),
          ('Data', '200 portfolio contracts (800 clauses) plus a library of 1,300 contracts and 6,539 reviewer-rated clauses.'),
          ('Method', 'Rules engine for expiry and renewal; seven text models including a 1D-CNN that reads the wording.'),
          ('Result', 'CNN catches 95% of High-risk clauses at 85% precision (keyword checklist macro-F1 0.38 vs 0.94).'),
          ('Limits', 'Synthetic clauses are more regular than real ones; a screening aid, not legal advice.')]),
 'insight-construction-productivity': dict(no=5, name='Site Progress & Schedule Control', data='Synthetic data',
   links=links('03-site-progress-schedule-control', ('Live app', '')),
   brief=[('Problem', 'Slippage hides in weekly progress updates, and submittals sit unapproved while site work continues.'),
          ('Decision supported', 'Which activities and approvals to chase this week.'),
          ('Data', '50 activities, 750 weekly progress records and 300 submittals.'),
          ('Method', 'Explainable rules: actual ÷ planned progress below 0.85 for two consecutive weeks; submittals open over 21 days.'),
          ('Result', '31 activities flagged (100% recall, 54.8% precision against labels); 25 stuck submittals.'),
          ('Limits', 'Historical flags on synthetic data; the ratio is not an earned-value SPI.')]),
 'insight-forecasting-final-cost': dict(no=6, name='Project Cost & Margin Intelligence', data='Synthetic data',
   links=links('01-cost-margin-intelligence', ('Live app', ''), ('ML forecast', 'forecast.html')),
   brief=[('Problem', 'Final cost and margin are forecast with the CPI formula, which is least reliable early on.'),
          ('Decision supported', 'Where margin is at risk, and next quarter’s spend.'),
          ('Data', '30 live projects plus 239 completed projects (2016–2023), monthly cost history.'),
          ('Method', 'Ridge, Random Forest, XGBoost, MLP and LSTM against the CPI formula; quantile ranges with conformal calibration.'),
          ('Result', '2.8% error below 30% complete vs 4.6% for CPI; next-quarter spend error 14% vs 36%.'),
          ('Limits', 'Synthetic data; the P10–P90 band held 76% of outcomes against an 80% target.')]),
 'insight-payroll-fraud': dict(no=7, name='Construction Payroll', data='Synthetic data',
   links=links('04-construction-payroll', ('Live app', ''), ('Anomaly model', 'anomaly.html')),
   brief=[('Problem', 'Site-labour payroll leaks through ghost workers, padded overtime and unauthorised rate increases.'),
          ('Decision supported', 'Which wage lines an auditor should review before release each month.'),
          ('Data', '2,400 staff timesheet rows and 12,397 monthly site-labour wage lines over a year.'),
          ('Method', 'Pre-release calculation rules, then peer-relative features and six anomaly detectors at a fixed review budget.'),
          ('Result', 'Isolation Forest finds 73% of seeded issues by reviewing 5% of lines (audit rules: 41%).'),
          ('Limits', 'Synthetic data; catches only 8% of proxy attendance, which needs a physical control.')]),
 'insight-llms-construction-documents': dict(no=8, name='Construction ERP Intelligence Copilot', data='Synthetic data',
   links=links('02-erp-intelligence-copilot', ('Live app', ''), ('AI chat', 'chat.html')),
   brief=[('Problem', 'Managers need answers from ERP data without writing reports or queries.'),
          ('Decision supported', 'Everyday questions on projects, costs, invoices and vendors.'),
          ('Data', 'The ERP data sets from Projects 1, 6 and 7, with questions worded differently from training.'),
          ('Method', 'Retrieval for record lookups, a router, eight parameterised SQL queries and guardrails that decline.'),
          ('Result', '94.8% correct end to end: 100% of lookups, 85% of calculations, 100% of declines.'),
          ('Limits', 'Synthetic data and template questions; real users phrase things more freely.')]),
 'insight-material-price-escalation': dict(no=9, name='Procurement & Subcontracting', data='Synthetic data',
   links=[('Code and README', GH + '06-procurement-subcontracting')],
   brief=[('Problem', 'Supplier delays are reviewed only after they disrupt the schedule.'),
          ('Decision supported', 'Which orders and vendors to follow up, and future sourcing choices.'),
          ('Data', '800 purchase orders from 60 vendors.'),
          ('Method', 'Deterministic ranking: days late × (1 + the vendor’s late-delivery rate); severe = 18+ days late.'),
          ('Result', '80 severe delays and 476 minor ones; 54 vendors with two or more late deliveries.'),
          ('Limits', 'A historical review, not a forecast; agreement with synthetic labels is by construction.')]),
 'insight-construction-payments': dict(no=10, name='Accounts Receivable & Payable', data='Synthetic data',
   links=[('Code and README', GH + '07-accounts-receivable-payable')],
   brief=[('Problem', 'Unsettled customer and vendor invoices need follow-up, but not all have the same evidence behind them.'),
          ('Decision supported', 'Which receivables to chase and which payables to resolve first.'),
          ('Data', '1,000 invoices (500 AR, 500 AP), 110 of them unpaid.'),
          ('Method', 'Two separate worklists: confirmed settlement risk, and repeat-pattern review; no blended score.'),
          ('Result', '22 confirmed (12 AR, 10 AP) and 88 repeat-pattern invoices from two customers.'),
          ('Limits', 'An evidence viewer, not a predictive model; label agreement is by construction.')]),
 'insight-inventory-records': dict(no=11, name='Inventory & Warehouse Management', data='Synthetic data',
   links=[('Code and README', GH + '08-inventory-warehouse-management')],
   brief=[('Problem', 'Large negative stock adjustments can concentrate around particular items and the people who record them.'),
          ('Decision supported', 'Which adjustments, recorders and stock positions to review.'),
          ('Data', '1,200 stock transactions across 80 items and 12 warehouses.'),
          ('Method', 'A confirmed adjustment-concentration rule, plus separate unscored checks for stale stock, duplicates and reversals.'),
          ('Result', '120 confirmed transactions from two recorders on three items; 114 stale item-warehouse positions.'),
          ('Limits', 'No opening balances, so no running-balance checks; a rule, not a model.')]),
 'insight-predictive-maintenance': dict(no=12, name='Construction Assets (Fixed & Movable)', data='Synthetic data',
   links=links('09-construction-assets', ('Predictive maintenance app', 'ml.html')),
   brief=[('Problem', 'Plant breaks down on site, and the failure pattern is only confirmed after it has happened.'),
          ('Decision supported', 'Which machines the workshop should inspect this week.'),
          ('Data', '80 telematics-fitted machines, 6,270 weekly readings and 249 breakdowns over two years.'),
          ('Method', 'Seven classifiers on 33 features compared with each machine’s own normal; time-based test.'),
          ('Result', 'XGBoost catches 71% of breakdowns with 10 inspections a week (OEM alarm limits: 16%).'),
          ('Limits', 'Synthetic telemetry with known wear physics; savings depend on cost assumptions.')]),
 'insight-booking-cancellations': dict(no=13, name='Real Estate Sales', data='Synthetic data',
   links=links('11-real-estate-sales', ('Sales ML app', 'sales_ml.html')),
   brief=[('Problem', 'Flat bookings cancel, unsold stock is priced by list, and buyers are segmented only by type.'),
          ('Decision supported', 'Who the CRM team should call, what each unsold flat will fetch, and who the buyers are.'),
          ('Data', '2,159 bookings across 8 launches in 7 Indian cities, with price lists and a city price index.'),
          ('Method', 'Seven classifiers scored 45 days after booking; five price models; K-means segments.'),
          ('Result', 'Calling the riskiest 20% finds 65% of cancellations; pricing error 2.0% vs 2.3% for the price list.'),
          ('Limits', 'Synthetic data and small samples; retention impact needs an A/B test.')]),
 'insight-attendance-before-payroll': dict(no=14, name='Construction HR', data='Synthetic data',
   links=[('Code and README', GH + '10-construction-hr')],
   brief=[('Problem', 'Missing clock-outs, pending leave and very long shifts reach payroll unreviewed.'),
          ('Decision supported', 'Which attendance records to fix before payroll is run.'),
          ('Data', '2,000 attendance records for 200 employees.'),
          ('Method', 'Three deterministic checks with separate worklists and source evidence.'),
          ('Result', '67 missing clock-outs, 66 pending leave approvals and 67 shifts of 12+ hours.'),
          ('Limits', 'A rule-based review on synthetic data; no break deduction or legal-limit judgement.')]),
 'insight-rework-bad-data': dict(no=15, name='Production Planning (RCC)', data='Synthetic data',
   links=[('Code and README', GH + '12-production-planning-rcc')],
   brief=[('Problem', 'Production orders with big output shortfalls and heavy rework need traceable review.'),
          ('Decision supported', 'Which orders, items and processes to investigate.'),
          ('Data', '700 production orders for 36 RCC items.'),
          ('Method', 'Confirmed rule: shortfall of 15%+ and rework of 10%+; separate review of rework on orders that met plan.'),
          ('Result', '70 confirmed orders on three items; 203 more orders had rework despite meeting or beating plan.'),
          ('Limits', 'Thresholds chosen after seeing the data; a rule, not a model.')]),
}

# extra sections that tie a research note to its project, inserted before the evidence table
EXTRA = {
 'insight-construction-productivity': ('on-site-signals', 'The signals a project can watch', f'''
<p>National productivity is the sum of thousands of projects losing time in the same few places. My Site Progress &amp; Schedule Control project turns two of them into weekly worklists{c(8)}:</p>
<ul>
<li><strong>Sustained slippage.</strong> An activity is flagged when actual progress is below 85% of planned progress for two or more consecutive weeks. One bad week is noise; two in a row is a pattern.</li>
<li><strong>Stuck approvals.</strong> A submittal is flagged when it has no approval date after more than 21 days open. Waiting for approvals is exactly the kind of lost time the productivity research points to.</li>
</ul>
{table(['Check', 'Result', 'What it means'], [
    ['Activities with sustained slippage', '31 of 50', 'Historical flags, anywhere in the activity’s record'],
    ['Agreement with labelled delays', '100% recall, 54.8% precision', 'Catches every labelled delay, with 14 extra flags'],
    ['Submittals stuck over 21 days', '25 of 300', 'Approvals holding up work']],
    'Synthetic data patterned on ERP structures [8]. The progress ratio is actual ÷ planned percentage complete, not an earned-value SPI.')}
<p>The 54.8% precision is worth dwelling on. A simple rule that never misses a real delay will also raise some false alarms, and the team has to decide whether that trade is worth it. For weekly site meetings it usually is: a false alarm costs a five-minute conversation, while a missed slip costs a milestone.</p>
''', ['Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects/03-site-progress-schedule-control">Site Progress &amp; Schedule Control</a>. GitHub.']),
 'insight-material-price-escalation': ('delivery-risk', 'The other procurement risk: late deliveries', f'''
<p>Price is only half of procurement risk. The other half is time: a material that arrives late stops work, however well it was priced. My Procurement &amp; Subcontracting project ranks purchase orders by delivery risk, using a deliberately simple and explainable score{c(5)}:</p>
{callout('Delivery-risk score', '<strong>days late × (1 + the vendor’s late-delivery rate)</strong>', 'A 20-day delay from a vendor who is usually on time ranks below a 20-day delay from a vendor who is late on most orders, because the second is a pattern to act on.')}
{bars('Purchase orders by delivery outcome (800 POs, 60 vendors)', [
    ('On time or early', 244, '244', False), ('Minor delay (1–17 days)', 476, '476', False),
    ('Severe delay (18+ days)', 80, '80', True)],
    'Synthetic data patterned on ERP structures [5]. 54 vendors had two or more late deliveries.')}
<p>Two lessons carry over. First, most late deliveries were minor, so a “late” flag on its own is too noisy to act on; severity and repetition are what make a worklist usable. Second, this is a historical review. Predicting which open orders will be late needs features known before delivery (vendor history up to that date, order size, lead time, season) and a time-based test, which is the next step for the project.</p>
''', ['Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects/06-procurement-subcontracting">Procurement &amp; Subcontracting</a>. GitHub.']),
 'insight-rework-bad-data': ('rework-in-production', 'Rework in an RCC production yard', f'''
<p>Rework is easiest to see where production is measured order by order. My Production Planning (RCC) project reviews 700 production orders for 36 reinforced-concrete items, and separates two kinds of evidence{c(4)}:</p>
{bars('Production orders by rework pattern (700 orders)', [
    ('Shortfall 15%+ and rework 10%+ (confirmed)', 70, '70', True), ('Rework despite meeting plan', 15, '15', False),
    ('Rework despite beating plan', 188, '188', False)],
    'Synthetic data patterned on ERP structures [4].')}
<p>The confirmed group is the obvious problem: large shortfalls with heavy rework, concentrated on just three items. The more interesting group is the <strong>203 orders that met or beat their planned output and still had rework</strong>. On a production report they look fine. The rework only shows up if someone records it and looks for it, which is exactly why rework needs its own cost code and its own review.</p>
''', ['Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects/12-production-planning-rcc">Production Planning (RCC)</a>. GitHub.']),
 'insight-forecasting-final-cost': ('range-and-spend', 'Ranges and next-quarter spend', f'''
<p>A final-cost forecast is only half of what a cost manager needs. The other half is how sure the forecast is, and how much cash the project will draw next. In my Cost &amp; Margin project, the same model family produces both{c(4)}:</p>
{bars('Next-quarter spend forecast error (WAPE, lower is better)', [
    ('Holt’s exponential smoothing', 55, '55%', False), ('Naive (last three months)', 40, '40%', False),
    ('Plan × CPI', 36, '36%', False), ('Global XGBoost model', 14, '14%', True)],
    'Synthetic data [4]. WAPE: weighted absolute percentage error across projects.')}
<ul>
<li><strong>Margin accuracy.</strong> At about 50% complete, the forecast margin was off by 1.9 percentage points of contract value, against 2.8 for the CPI formula, and closer on 14 of 20 projects.</li>
<li><strong>Range honesty.</strong> The P10–P90 band held the final cost 76% of the time against an 80% target, with a median width of 7% of budget. Slightly too narrow, and reported as such.</li>
</ul>
''', ['Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects/01-cost-margin-intelligence">Project Cost &amp; Margin Intelligence</a>. GitHub.']),
}

# titles and dek adjusted where the note now centres on a different project
RETITLE = {
 'insight-construction-productivity': dict(topic='Site progress',
   title='Where site productivity leaks: the fifty-year puzzle and the weekly signals',
   blurb='Construction productivity grew about 1% a year while the economy managed 2.8%. The research, and the slippage and approval signals a site can watch.'),
 'insight-material-price-escalation': dict(topic='Procurement',
   title='Procurement risk: material price shocks, escalation clauses and late deliveries',
   blurb='Lumber prices more than doubled in a year while bid prices barely moved. Escalation clauses, and ranking late deliveries by vendor pattern.'),
 'insight-rework-bad-data': dict(topic='Production & quality',
   title='Rework and bad data: the cost line nobody budgets',
   blurb='Poor data and miscommunication were blamed for nearly half of all rework in one large survey. What the research says, and rework hidden behind on-plan output.'),
}

# sections of each note that belong to the case study (everything else is general research)
CASE = {
 'insight-osha-severe-injuries': ['the-data', 'where-injuries-come-from', 'three-findings', 'reading-the-text'],
 'insight-permit-wait-times': ['the-nyc-evidence', 'forecasting'],
 'insight-cost-estimates-miss': [],
 'insight-contract-clause-risk': ['what-the-model-does', 'human-disagreement'],
 'insight-construction-productivity': ['on-site-signals'],
 'insight-forecasting-final-cost': ['range-and-spend'],
 'insight-payroll-fraud': ['what-my-test-showed'],
 'insight-llms-construction-documents': ['my-tests'],
 'insight-material-price-escalation': ['delivery-risk'],
 'insight-construction-payments': ['evidence-not-scores', 'toward-prediction'],
 'insight-inventory-records': ['what-to-check', 'zero-is-not-clean'],
 'insight-predictive-maintenance': ['the-test', 'results', 'lessons'],
 'insight-booking-cancellations': ['what-drives-cancellations', 'the-call-list', 'pricing-and-segments'],
 'insight-attendance-before-payroll': ['three-checks'],
 'insight-rework-bad-data': ['what-bad-data-looks-like', 'rework-in-production'],
}

# alt text for post images (used when an image file is present)
IMAGE_ALT = {
 'insight-osha-severe-injuries': 'A worker on a step ladder fixing services to a concrete ceiling inside a building under construction, with a mobile scaffold tower behind.',
 'insight-payroll-fraud': 'A supervisor with a clipboard facing a line of construction workers in hard hats and hi-vis vests at a morning roll call.',
 'insight-llms-construction-documents': 'Open contract binders and specification folders on a site table, with a faint teal scanning light across the pages.',
 'insight-construction-productivity': 'Aerial view of a large construction site with rows of concrete building blocks at different stages, workers and machines between them and a tower crane.',
 'insight-forecasting-final-cost': 'A partly built reinforced-concrete frame at dusk, with two lit tower cranes and two workers in hi-vis walking across the wet slab.',
 'insight-material-price-escalation': 'A materials yard with bundles of steel reinforcement bars, stacked timber and covered cement bags, and a delivery truck at the gate.',
 'insight-construction-payments': 'A site office desk at dusk with stacked folders, a calculator, a mug and a hard hat, looking out onto a lit construction site.',
}
