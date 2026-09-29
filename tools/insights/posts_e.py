from build import c, bars, table, pull, callout, checklist

DATE, DATE_LABEL = '2026-09-29', 'Sept 2026'
GH = 'https://github.com/AtulIwale/Portfolio/tree/main/projects/'

ASSETS = dict(
    slug='insight-predictive-maintenance', topic='Plant & equipment', topics='ai controls',
    title='Predicting equipment breakdowns: what the maintenance research promises, and what a model delivered',
    dek='A breakdown on site costs the repair, the hire of a replacement and the crew standing idle. Predictive maintenance promises to catch failures early. Here is what the guidance claims, and what happened when I tested it on two years of telematics.',
    meta='Maintenance strategies and the evidence for predictive maintenance, and a case study of seven models predicting construction plant breakdowns four weeks ahead from telematics.',
    blurb='Predictive maintenance promises 8–12% savings over preventive. A model caught 71% of breakdowns with 10 inspections a week; fixed alarm limits caught 16%.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('8–12%', 'savings of a well-run predictive programme over preventive maintenance alone, per government maintenance guidance', 1),
          ('71%', 'of breakdowns caught by XGBoost with 10 inspections a week (synthetic telematics)', 3),
          ('16%', 'caught by the manufacturer’s fixed alarm limits, which fire too late', 3)],
    takeaways=[
        'A widely used government maintenance guide puts the saving of a working predictive programme at <strong>8–12% over preventive maintenance</strong>, and describes it as nearly eliminating catastrophic failures.',
        'Fixed alarm limits fire too late: in my test they caught only <strong>16%</strong> of breakdowns in advance.',
        'Comparing each machine with its <strong>own normal</strong> is what gives the early warning, not absolute thresholds.',
        'At a realistic workshop capacity of 10 inspections a week, XGBoost caught <strong>71%</strong> of breakdowns; at its cost-optimal threshold, 84% with a median of four weeks’ warning.',
        'Some failures give no warning. A model reduces breakdowns; it does not end them.',
    ],
    sections=[
        ('maintenance-strategies', 'Four ways to maintain a machine', f'''
<p>One of the most widely used references is the <em>Operations &amp; Maintenance Best Practices</em> guide from the Federal Energy Management Program (FEMP). It describes a ladder of maintenance strategies{c(1)}{c(2)}:</p>
{table(['Strategy', 'When work happens', 'Trade-off'], [
    ['Reactive', 'After a failure', 'No planning cost, but the most downtime and collateral damage'],
    ['Preventive', 'On a calendar or hour interval', 'Fewer failures, but parts are replaced whether or not they need it'],
    ['Predictive', 'When condition data shows developing wear', 'Work only when needed, but needs sensors, data and analysis'],
    ['Reliability-centred', 'A mix chosen per failure mode', 'Most effective, most analysis']],
    'Summarised from the FEMP O&amp;M Best Practices Guide [1][2].')}
<p>For predictive maintenance the guide is explicit about the prize: a properly functioning programme can save <strong>8% to 12% over a preventive programme alone</strong>, and a well-run one will all but eliminate catastrophic equipment failures{c(1)}. Those are claims about well-run programmes in facilities. The question for a contractor is whether the same signals work on mobile plant moving between dusty sites.</p>
'''),
        ('the-test', 'The test: two years of plant telematics', f'''
<p>My Construction Assets project started with a rule that confirms a failure pattern (three declining condition ratings with the same symptoms) only once it has fully happened. Useful for records, useless for Monday morning. The upgrade asks the plant manager’s real question: <strong>which machines are likely to break down in the next four weeks?</strong>{c(3)}</p>
<ul>
<li><strong>Fleet:</strong> 80 telematics-fitted machines, 6,270 weekly readings over two years (hours, load, vibration, temperature, hydraulic pressure, fault codes, monthly oil-iron samples) and 249 breakdowns.</li>
<li><strong>Features:</strong> 33, built only from past data, including each reading compared with the machine’s <strong>own normal level</strong> over the previous months, hours since service and weeks since the last repair.</li>
<li><strong>Test:</strong> trained to December 2025, tuned on January–March 2026, tested once on April–August 2026.</li>
<li><strong>Baselines:</strong> the manufacturer’s alarm limits and a service-overdue rule.</li>
</ul>
'''),
        ('results', 'What the models caught', f'''
{bars('Breakdowns caught in advance with 10 inspections a week (test months)', [
    ('OEM alarm limits', 16, '16%', False), ('Random ranking', 47, '47%', False), ('Logistic regression', 57, '57%', False),
    ('SVM (RBF kernel)', 60, '60%', False), ('Neural network (MLP)', 65, '65%', False),
    ('Random forest', 66, '66%', False), ('XGBoost (in the app)', 71, '71%', True)],
    'Synthetic telematics with realistic wear behaviour; all figures as reported in the project [3].', max_value=100)}
<p>Fixed alarm limits did worst because they fire when the reading is already abnormal in absolute terms, by which time the failure is close. The models watch for a machine drifting away from its own normal, weeks earlier.</p>
<p>In cost terms, at its cost-optimal threshold XGBoost caught <strong>69 of 82</strong> test-period breakdowns (84%) with a median of <strong>four weeks’ warning</strong>, cutting breakdown-related cost in the simulation from Rs 422 lakh to Rs 212 lakh. By cause, it caught all bearing and gear wear and 95% of overheating, but far fewer sudden failures, which by nature give little warning{c(3)}.</p>
{pull('The warning comes from a machine drifting away from its own normal, not from crossing a fixed limit.')}
'''),
        ('lessons', 'Why trees beat the SVM here', f'''
<ul>
<li><strong>Messy data favours tree models.</strong> A third of the fleet has no hydraulic sensor, oil results arrive monthly and telematics drops out. XGBoost learns what a missing value means; an SVM needs values imputed, and an imputed median looks like a real reading.</li>
<li><strong>Context interacts.</strong> A temperature rise means different things for an electric hoist and a diesel excavator in a hot summer. Trees split on both; a single distance measure treats them alike.</li>
<li><strong>Ranking beats thresholds.</strong> A workshop has fixed capacity, so “inspect the top ten each week” is the realistic operating rule, and it is where the gap between models shows most clearly.</li>
<li><strong>A second opinion helps.</strong> Where XGBoost and the SVM disagree strongly, that machine deserves a closer look.</li>
</ul>
{callout('Limits', 'The telemetry is synthetic with known wear physics, so a real fleet will be noisier. The rupee savings depend on the assumed inspection and repair costs and a five-month test window. A real deployment would retrain quarterly against actual breakdown reports.')}
'''),
        ('what-to-do', 'Starting predictive maintenance on a fleet', checklist([
            '<strong>Record every breakdown properly</strong>: date, machine, root cause, downtime and cost. Without outcomes there is nothing to learn from.',
            '<strong>Collect condition data you already have</strong> (hour meters, fault codes, oil samples) before buying new sensors.',
            '<strong>Compare each machine with its own history,</strong> not only with fixed limits.',
            '<strong>Plan to workshop capacity:</strong> rank machines and inspect the top N each week.',
            '<strong>Price both errors:</strong> the cost of an unnecessary inspection against the cost of a missed breakdown, including hire and idle crews.',
            '<strong>Test on later months than you trained on,</strong> and retrain as the fleet and sites change.',
        ])),
    ],
    applied=dict(title='Construction Assets (Fixed & Movable)',
                 text=['A weekly inspection worklist for plant, with machine history charts, what-if sliders, a model comparison and a cost simulator. XGBoost and the SVM run in the browser. Built on synthetic telematics with realistic wear behaviour.'],
                 href='https://atuliwale.github.io/Portfolio/projects/09-construction-assets/ml.html', label='Open the maintenance app'),
    sources=[
        'US Department of Energy, Federal Energy Management Program (2010). <a href="https://www.energy.gov/sites/prod/files/2020/04/f74/omguide_complete_w-eo-disclaimer.pdf">Operations &amp; Maintenance Best Practices: A Guide to Achieving Operational Efficiency, Release 3.0</a>.',
        'Pacific Northwest National Laboratory. <a href="https://www.pnnl.gov/projects/om-best-practices/maintenance-approaches">O&amp;M best practice issue discussion: maintenance approaches</a>.',
        f'Iwale, A. (2026). <a href="{GH}09-construction-assets">Construction Assets</a>, including the predictive-maintenance upgrade. GitHub.',
    ],
    next=['insight-forecasting-final-cost', 'insight-booking-cancellations'],
)

SALES = dict(
    slug='insight-booking-cancellations', topic='Real estate sales', topics='commercial ai',
    title='Why flat bookings cancel: payment timing, home loans and what a call list can do',
    dek='A cancelled booking costs a developer the sale, the marketing spent to win it and months of carrying the flat again. The warning signs usually appear in the first weeks, if someone is watching the right ones.',
    meta='What drives residential booking cancellations, how a model scored 45 days after booking ranks who to call, and pricing and buyer segments for unsold flats, with a case study on synthetic data.',
    blurb='Calling the riskiest 20% of buyers found 65% of cancellations. Late first payments and unsanctioned loans are the strongest early signals.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('65%', 'of cancellations found by calling the riskiest 20% of bookings (synthetic data)', 2),
          ('×1.73', 'odds of cancelling per standard deviation of lateness on the first demand', 2),
          ('10%', 'the most a promoter may take as advance before a registered agreement for sale (RERA s.13)', 1)],
    takeaways=[
        'Under RERA, a promoter cannot take more than <strong>10%</strong> of the price as an advance without first registering an agreement for sale, so the first payment demands after agreement are a key moment.',
        'In my synthetic data, the strongest early signals were <strong>lateness on the first demand</strong>, a high EMI-to-income ratio, investor buyers and a <strong>loan not yet sanctioned</strong>.',
        'Scored 45 days after booking, a model found <strong>65%</strong> of cancellations by calling the riskiest 20% of buyers.',
        'With under 900 training bookings, simple models were as good as complex ones, so the explainable one was used.',
        'A risk score says who to call, not what the call achieves. Measuring retention needs an A/B test.',
    ],
    sections=[
        ('the-frame', 'The regulatory frame', f'''
<p>Housing regulation shapes the booking journey. India’s Real Estate (Regulation and Development) Act, 2016 (RERA) is a good example: under <strong>Section 13</strong>, a promoter may not accept more than <strong>10% of the cost</strong> of an apartment as an advance or application fee without first entering into a written agreement for sale and registering it{c(1)}. The agreement must set out the payment schedule, the possession date and the interest payable by either side on default.</p>
<p>That makes the weeks after agreement critical. The buyer now faces the first construction-linked demands, the home loan must be sanctioned and disbursed, and the gap between enthusiasm at booking and affordability in practice becomes visible.</p>
'''),
        ('what-drives-cancellations', 'What drives cancellations', f'''
<p>My Real Estate Sales project models 2,159 bookings across eight launches in seven Indian cities, with realistic patterns: broker deals carrying bigger discounts and thinner booking amounts, subvention plans attracting investors, festival and quarter-end offers, and loan rejections driving cancellations. Across bookings at least a year old, <strong>12.9%</strong> cancelled{c(2)}.</p>
<p>Each booking is scored <strong>45 days after booking</strong>, once the first instalment is due, using only what is known by then. The logistic model’s odds ratios show what moves the risk:</p>
{bars('Change in odds of cancelling, per standard deviation or when present', [
    ('Broker deal', 1.16, '×1.16', False), ('Loan not yet sanctioned', 1.37, '×1.37', False),
    ('Investor buyer', 1.40, '×1.40', False), ('EMI-to-income ratio', 1.44, '×1.44', False),
    ('Days late on the first demand', 1.73, '×1.73', True)],
    'Logistic-regression odds ratios on synthetic bookings [2]. A sanctioned loan, more site visits and a larger booking amount lower the risk.', max_value=2)}
{pull('Timing is the feature. How late the first payment is says more than anything known on booking day.')}
'''),
        ('the-call-list', 'From a score to a call list', f'''
<p>Seven classifiers were compared on 465 later bookings, 60 of which cancelled. The practical test is how many cancellations a CRM team finds by calling the riskiest fifth of buyers:</p>
{bars('Cancellations found by calling the riskiest 20% of bookings', [
    ('Random call list', 20, '20%', False), ('Decision tree', 47, '47%', False), ('SVM (RBF)', 58, '58%', False),
    ('Logistic regression (in the app)', 60, '60%', True), ('XGBoost', 60, '60%', False),
    ('Naive Bayes', 65, '65%', False), ('Random forest', 65, '65%', False)],
    'Test: 465 bookings, 60 cancelled; synthetic data [2].', max_value=100)}
<p>With under 900 training bookings, logistic regression, Naive Bayes and random forest were within noise of each other. The app uses the logistic model because every score can be explained to the person making the call: “the first demand is 20 days late and the loan isn’t sanctioned” is something a relationship manager can act on.</p>
'''),
        ('pricing-and-segments', 'Pricing unsold flats and knowing the buyers', f'''
<p>The same project asks two more questions of the data{c(2)}:</p>
<ul>
<li><strong>What will each unsold flat actually fetch?</strong> An XGBoost model priced flats with a <strong>2.0%</strong> error against 2.3% for the price list less the average discount, and removed the list’s +1.2% bias. A good price list is hard to beat; the gain comes from knowing which deals need a bigger discount.</li>
<li><strong>Who are the buyers?</strong> K-means on buying behaviour (income, age, ticket size, loan-to-value, EMI burden, booking amount, visits and time to decide) found five segments, with buyer type deliberately left out.</li>
</ul>
{table(['Segment', 'Cancellation rate'], [
    ['Stretched buyers (high EMI)', '28%'], ['Budget first-home buyers', '14%'],
    ['Careful researchers', '11%'], ['Affluent upgraders', '11%'], ['Cash buyers', '6%']],
    'Synthetic data [2]. Cash buyers turned out to be mostly investors and NRIs, although buyer type was never an input.', num_cols=(1,))}
'''),
        ('what-to-do', 'Using this in a sales team', checklist([
            '<strong>Watch the first demand closely.</strong> Lateness on the first payment is the strongest early signal.',
            '<strong>Track loan sanction status</strong> for every booking and follow up before the first demand, not after.',
            '<strong>Check affordability at booking:</strong> a high EMI-to-income ratio is a risk worth discussing openly.',
            '<strong>Call from a ranked list</strong> with the reasons shown, so each call addresses the actual problem.',
            '<strong>Test the calls.</strong> Hold back a random group to measure whether outreach actually reduces cancellations.',
        ])),
    ],
    applied=dict(title='Real Estate Sales',
                 text=['A CRM call list with reasons and what-if sliders, a pricer for every unsold flat, inventory value, model comparisons and buyer segments. The logistic model and XGBoost price trees run in the browser. Built on synthetic data following Indian residential sales patterns.'],
                 href='https://atuliwale.github.io/Portfolio/projects/11-real-estate-sales/sales_ml.html', label='Open the sales app'),
    sources=[
        'Real Estate (Regulation and Development) Act, 2016, section 13. Text in <a href="https://ibclaw.in/section-13-of-real-estate-regulation-and-development-act-2016-rera-no-deposit-or-advance-to-be-taken-by-promoter-without-first-entering-into-agreement-for-sale/">IBC Laws: Section 13 of RERA</a>.',
        f'Iwale, A. (2026). <a href="{GH}11-real-estate-sales">Real Estate Sales</a>, including the cancellation, pricing and segmentation upgrade. GitHub.',
    ],
    next=['insight-cost-estimates-miss', 'insight-construction-payments'],
)

HR = dict(
    slug='insight-attendance-before-payroll', topic='HR & attendance', topics='data commercial',
    title='Fix attendance before payroll: the cheapest payroll error is the one never paid',
    dek='Payroll errors are common, expensive and mostly start as attendance errors. On a construction site, where overtime is paid at double rates, a missing clock-out or a mis-recorded shift turns straight into money.',
    meta='What payroll errors cost, why construction attendance feeds them, statutory overtime rules, and three simple checks to run on attendance before payroll.',
    blurb='One in five payrolls has errors, at $291 each. Time and attendance errors are the most common. Three checks to run before payroll.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('1 in 5', 'payrolls contain errors, in a 2022 EY survey of 508 payroll professionals', 1),
          ('$291', 'average cost of each payroll error in the same survey', 1),
          ('2×', 'ordinary wages for overtime on building work under construction labour law, for example India’s BOCW Act', 2)],
    takeaways=[
        'An EY survey found <strong>one in five</strong> payrolls contains errors, each costing about <strong>$291</strong>, with an average of 15 corrections per payroll period.',
        '<strong>Time and attendance errors</strong> were the most common, occurring more than once per employee per year.',
        'Under construction labour laws such as India’s BOCW Act, building workers are paid <strong>twice the ordinary rate</strong> for work beyond the normal working day, so attendance errors become wage errors quickly.',
        'Three checks catch much of it before payroll: missing clock-outs, leave still pending approval and implausibly long shifts.',
        'The goal is review before release. Correcting a paid error costs far more than fixing an attendance record.',
    ],
    sections=[
        ('what-errors-cost', 'What payroll errors cost', f'''
<p>In 2022, EY surveyed 508 payroll professionals at companies with 250 to 10,000 employees. It found that about <strong>one in five payrolls contains errors</strong>, that each error costs an average of <strong>$291</strong> to fix, and that the average organisation makes <strong>15 corrections per payroll period</strong>{c(1)}.</p>
<p>The most common errors were in <strong>time and attendance</strong> and expenses, occurring on average more than once per employee per year and costing about $250,000 per 1,000 employees. A 1,000-employee organisation spent an estimated 29 workweeks a year fixing the most common payroll errors{c(1)}.</p>
{pull('Most payroll errors start as attendance errors, and attendance is cheapest to fix before anyone is paid.')}
'''),
        ('construction-attendance', 'Why construction attendance is error-prone', f'''
<p>Site attendance has every ingredient for errors: large, changing crews; shifts that start before dawn and run late around concrete pours; biometric devices that fail; manual registers kept by supervisors under pressure; and workers who move between sites during a week.</p>
<p>Labour law raises the stakes. India’s Building and Other Construction Workers (BOCW) Act, 1996 is a typical example. Under <strong>Section 28</strong>, the government fixes by rule the hours of a normal working day and a weekly day of rest. Under <strong>Section 29</strong>, a building worker who works beyond the normal working day is entitled to wages at <strong>twice the ordinary rate</strong>{c(2)}. A shift recorded two hours too long is therefore paid at double rate, and a missing clock-out forces someone to guess.</p>
'''),
        ('three-checks', 'Three checks before payroll', f'''
<p>My Construction HR project runs three simple, explainable checks on 2,000 synthetic attendance records for 200 employees, each with its own worklist and source evidence{c(3)}:</p>
{bars('Attendance records needing review before payroll (2,000 records)', [
    ('Missing clock-out', 67, '67', True), ('Leave still pending approval', 66, '66', True),
    ('Shift of 12 hours or more', 67, '67', True)],
    'Synthetic data patterned on ERP structures [3]. The three categories do not overlap.')}
<ul>
<li><strong>Missing clock-out:</strong> a clock-in with no clock-out and no leave recorded. Without it, hours are a guess.</li>
<li><strong>Leave pending approval:</strong> leave recorded but not yet approved. An administrative flag, not misconduct.</li>
<li><strong>Very long shift:</strong> 12 or more hours between clock-in and clock-out, with no break deducted. It may be genuine overtime, a missed clock-out on the right day, or a recording error.</li>
</ul>
{callout('What the checks don’t decide', 'The long-shift check does not decide whether the hours are payable or legal; that needs the applicable rules and the site’s break policy. It says which records need a person to confirm them before they become wages.')}
'''),
        ('staff-and-site', 'Attendance and payroll together', f'''
<p>These checks work on direct employees’ attendance. On most construction projects the larger exposure is labour supplied by contractors, where ghost workers, proxy attendance and padded overtime are the typical leakage. That is covered in the Construction Payroll note, which compares each wage line with its site, crew and history. The two controls work best together: clean attendance before payroll, then anomaly review of the wage lines before release.</p>
'''),
        ('what-to-do', 'A pre-payroll routine', checklist([
            '<strong>Close attendance before payroll,</strong> with a cut-off and a named person to resolve every open record.',
            '<strong>Resolve missing clock-outs with the supervisor,</strong> not by default hours.',
            '<strong>Clear pending leave approvals</strong> before the payroll run, so leave is paid or deducted correctly.',
            '<strong>Confirm long shifts</strong> against the site diary or pour log before paying overtime.',
            '<strong>Record the normal working day and break policy</strong> per site, so overtime is calculated from rules, not judgement.',
            '<strong>Measure corrections after payroll</strong> each period; a falling count is the proof the routine works.',
        ])),
    ],
    applied=dict(title='Construction HR',
                 text=['An offline attendance review with three separate worklists (missing clock-outs, pending leave and long shifts), employee and date filters, row-level source evidence and exports. Built on synthetic ERP data.'],
                 href=GH + '10-construction-hr', label='See the code and README'),
    sources=[
        'EY (2022). <a href="https://www.businesswire.com/news/home/20221222005093/en/EY-survey-Payroll-errors-average-291-each-impacting-the-economy">EY survey: payroll errors average $291 each, impacting the economy</a>. Business Wire.',
        'Building and Other Construction Workers (Regulation of Employment and Conditions of Service) Act, 1996, sections 28–29. <a href="https://indiankanoon.org/doc/55218578/">Section 28 text (Indian Kanoon)</a>; <a href="https://clc.gov.in/clc/acts-rules/building-and-other-construction-workers">Chief Labour Commissioner</a>.',
        f'Iwale, A. (2026). <a href="{GH}10-construction-hr">Construction HR</a>. GitHub.',
    ],
    next=['insight-payroll-fraud', 'insight-rework-bad-data'],
)

POSTS = [ASSETS, SALES, HR]
