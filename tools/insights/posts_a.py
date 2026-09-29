from build import c, bars, table, pull, callout, checklist

DATE, DATE_LABEL = '2026-09-29', 'Sept 2026'

SAFETY = dict(
    slug='insight-osha-severe-injuries', topic='Safety', topics='safety data',
    title='Where serious construction injuries come from, and what incident reports can tell you',
    dek='Falls get most of the attention in safety plans, and rightly so. But the hazards that put construction workers in hospital are not always the ones plans are written around, and the detail that explains them sits unread in incident reports. What the evidence shows, with a ten-year case study of 19,021 severe-injury reports.',
    meta='Where serious construction injuries come from, why severity matters as much as frequency, and how to read incident reports at scale, with a case study of 19,021 severe-injury reports (2015–2025).',
    blurb='Falls lead, but caught-in accidents cause most amputations. What the evidence shows, with a case study of 19,021 severe-injury reports.',
    feature_stat=('37%', 'of severe construction injuries were falls to a lower level, in a ten-year study of 19,021 reports.'),
    date=DATE, date_label=DATE_LABEL,
    keys=[('37%', 'of severe construction injuries were falls to a lower level, in a ten-year case study of 19,021 reports', 1),
          ('63%', 'of caught-in and crushing injuries involved an amputation, mostly fingers', 1),
          ('No. 1', 'fall protection is, year after year, the most frequently cited construction safety standard', 4)],
    takeaways=[
        'Falls are the most common severe injury in construction, and in the case study one in four falls with a recorded height was from <strong>under six feet</strong>. Ladders and low platforms matter, not only roofs.',
        'Caught-in and crushing accidents are rarer but cause most amputations: <strong>63%</strong> of them involve one.',
        'The hazard mix changes sharply by trade and by season. <strong>80%</strong> of heat-stress injuries happen from June to August.',
        'Incident narratives can be coded consistently by a simple, explainable model: <strong>84%</strong> agreement with OSHA’s coders against 55% for a keyword list.',
        'Coding rules change. OSHA’s January 2024 manual change moved the caught-in/struck-by line, so any model needs monitoring by cause.',
    ],
    sections=[
        ('what-safety-data-misses', 'What most safety data misses', f'''
<p>Most contractors track incident counts, lost-time injury rates and near misses. Those numbers are useful, but they are dominated by frequent, less severe events, and they say little about <em>why</em> people are hurt. The detail that explains an injury (the task, the equipment, the height, the sequence of events) sits in the free-text narrative of the incident report.</p>
<p>That text is rarely analysed. Coding each report consistently by cause takes trained people and time, so in most firms the narratives are read once, filed and never compared. The result is a safety plan built on the hazards everyone expects, rather than on the pattern the firm’s own reports would show.</p>
{pull('The detail that explains an injury sits in the narrative, and the narrative is rarely read twice.')}
'''),
        ('the-data', 'The data: ten years of severe-injury reports', f'''
<p>Since 1 January 2015, employers under OSHA’s federal jurisdiction must report any work-related in-patient hospitalisation, amputation or loss of an eye within 24 hours{c(2)}. Each report includes a short free-text narrative of what happened, and OSHA’s staff code it by event, source and body part. OSHA publishes the full file on its Severe Injury Reports page{c(3)}.</p>
<p>I downloaded the January 2015 to November 2025 file (105,996 reports across all industries) and kept the <strong>19,021 reports from construction</strong> (NAICS sector 23). The cleaning mattered more than the modelling. The file holds 348 event codes stored at two, three or four digits, from more than one version of OSHA’s coding manual, where the same prefix can mean different things. I grouped them into nine cause groups from their titles, removed employer names, addresses and coordinates, and set aside 381 reports with no usable cause{c(1)}.</p>
{callout('Scope', 'These are <strong>severe</strong> injuries only, and only from regions under OSHA’s federal jurisdiction; regions that run their own state plans are not in the file, and neither are minor injuries. The shares below describe what puts people in hospital, not everything that happens on site.')}
'''),
        ('where-injuries-come-from', 'Where serious injuries come from', f'''
<p>Of the 18,640 reports with a known cause, falls to a lower level are the largest group by a distance. But the share of each cause that ends in an amputation tells a different story about severity{c(1)}.</p>
{bars('Severe construction injuries by cause, Jan 2015 – Nov 2025 (case study)', [
    ('Fall to lower level', 6806, '6,806', True), ('Struck by or against object', 4706, '4,706', False),
    ('Caught in or crushed', 2285, '2,285', False), ('Vehicle or mobile equipment', 1429, '1,429', False),
    ('Electrical', 959, '959', False), ('Slip, trip or same-level fall', 881, '881', False),
    ('Heat stress', 605, '605', False), ('Fire, explosion or burn', 497, '497', False)],
    'Source: my analysis of OSHA Severe Injury Reports [1][3]. 18,640 reports with a known cause; "Other" (472) not shown.')}
{table(['Cause', 'Reports', 'With an amputation'], [
    ['Fall to lower level', '6,806', '0.4%'], ['Struck by or against object', '4,706', '24.8%'],
    ['Caught in or crushed', '2,285', '62.8%'], ['Vehicle or mobile equipment', '1,429', '6.7%'],
    ['Electrical', '959', '2.3%'], ['Slip, trip or same-level fall', '881', '2.7%'],
    ['Heat stress', '605', '0%'], ['Fire, explosion or burn', '497', '1.6%']],
    'Share of each cause’s reports that record an amputation. Source: [1].', num_cols=(1, 2))}
<p>Falls put the most people in hospital; caught-in accidents take the most fingers and hands. A safety plan that ranks hazards only by frequency will under-weight the machinery, pinch points and rotating parts behind the second group.</p>
'''),
        ('three-findings', 'Three findings a safety manager can use', f'''
<h3>1. Low falls are a large share of serious falls</h3>
<p>One in four falls with a recorded height band was from <strong>under six feet</strong>{c(1)}. Fall-protection effort naturally goes to roofs and leading edges, but ladders, trestles and low platforms produce a steady stream of hospitalisations. When I asked a language model to extract the equipment from 2024–2025 narratives, ladders were involved in 407 falls (median fall 8.5 ft), roofs in 193 (16 ft) and scaffolds in 111 (10.5 ft){c(1)}.</p>
<h3>2. The hazard mix depends on the trade</h3>
<p>Over half of injuries in foundation, structure and roofing contractors, and in finishing trades, are falls. Utility contractors have the most struck-by and caught-in injuries, and electrical, plumbing and HVAC contractors account for 57% of electrical injuries{c(1)}. A company-wide top-ten hazard list hides this; a per-trade view does not.</p>
<h3>3. Heat is seasonal and regional</h3>
<p>80% of heat-stress injuries in the file happened from June to August, mostly in Texas and Florida{c(1)}. That makes heat one of the few hazards you can plan for by calendar: water, shade, rest cycles and acclimatisation for new starters, scheduled before the season rather than after the first incident.</p>
{pull('Falls put the most people in hospital. Caught-in accidents take the most fingers and hands. A plan ranked only by frequency misses the second.')}
'''),
        ('the-fatal-picture', 'The most serious hazards are well known', f'''
<p>Fatality statistics tell a consistent story. In detailed national fatality data such as the Bureau of Labor Statistics’ census, construction and extraction workers account for about one in five of all workplace deaths, and <strong>falls, slips and trips</strong> are their leading cause of death{c(5)}. Roofing work alone accounts for about a quarter of construction’s fatal falls{c(6)}.</p>
<p>Enforcement records point the same way. Fall protection is routinely the most frequently cited construction safety standard; OSHA reported it at the top of its list for the fourteenth year running in 2024{c(4)}. The main hazards are not a secret. What varies between firms is whether their own data shows where those hazards are hurting their people.</p>
'''),
        ('reading-the-text', 'Reading incident text at scale', f'''
<p>Most contractors don’t employ trained coders, so their own incident reports stay as unread text. I tested whether a model could code the cause of an injury from the narrative as consistently as OSHA’s coders, training on 2015–2022, tuning on 2023 and testing on 2024–2025 so the model is always judged on later years than it learned from{c(1)}.</p>
{bars('Agreement with OSHA’s coders on 3,204 test reports (2024 – Nov 2025)', [
    ('Keyword checklist (baseline)', 55.1, '55.1%', False), ('LLM, zero-shot (no training)', 81.4, '81.4%', False),
    ('Logistic regression (in the app)', 83.8, '83.8%', True), ('Model and LLM agree (85% of reports)', 89.1, '89.1%', True)],
    'Accuracy against OSHA’s own cause codes. Source: my analysis [1].', max_value=100)}
<p>Three lessons carry over to any contractor:</p>
<ul>
<li><strong>Simple models are enough and explainable.</strong> Narratives are short (median 190 characters), and a linear model with one weight per word beat neural networks. The strongest words read like a safety manager’s vocabulary: “pinched”, “between”, “amputation” for caught-in; “backed”, “forklift” for vehicles.</li>
<li><strong>Two readers make a review queue.</strong> Where the trained model and a language model agree (85% of reports), they match OSHA 89% of the time; only the 15% where they disagree need a person.</li>
<li><strong>Labels drift.</strong> OSHA changed its coding manual in January 2024 and redrew the caught-in/struck-by line. The narratives didn’t change but the codes did, and caught-in F1 fell from 0.78 to 0.59. Any production model needs monthly monitoring by cause.</li>
</ul>
'''),
        ('what-to-do', 'What to do with this on your projects', checklist([
            '<strong>Rank hazards by severity as well as frequency.</strong> Track amputations and hospitalisations separately; caught-in risks rise up the list.',
            '<strong>Treat ladders and low work as fall hazards.</strong> Include step ladders, trestles and platforms under six feet in fall-protection planning and inspections.',
            '<strong>Split the dashboard by trade.</strong> A roofing crew and a utility crew need different top-three hazards.',
            '<strong>Put heat on the calendar.</strong> Plan water, shade and acclimatisation before June, not after the first incident.',
            '<strong>Code your own incident text consistently.</strong> A small, explainable model plus a person reviewing disagreements turns narratives into trend data.',
            '<strong>Monitor the codes, not just the model.</strong> When definitions change, re-measure accuracy by cause before trusting the trend line.',
        ])),
    ],
    applied=dict(title='Construction Safety Intelligence',
                 text=['Built on the real OSHA file described above: cleaning code, three notebooks, an LLM comparison and a browser app that codes a new narrative and highlights the words that drove the call.'],
                 href='https://atuliwale.github.io/Portfolio/projects/14-construction-safety-intelligence/', label='Open the live app'),
    sources=[
        'Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects/14-construction-safety-intelligence">Construction Safety Intelligence: analysis of OSHA Severe Injury Reports, January 2015 – November 2025</a>. GitHub.',
        'OSHA. <a href="https://www.osha.gov/laws-regs/regulations/standardnumber/1904/1904.39">29 CFR 1904.39 — Reporting fatalities, hospitalizations, amputations, and losses of an eye</a>.',
        'OSHA. <a href="https://www.osha.gov/severeinjury">Severe Injury Reports</a> (data set and dashboard).',
        'OSHA. <a href="https://www.osha.gov/top10citedstandards">Top 10 Most Frequently Cited Standards</a>, fiscal year 2024.',
        'U.S. Bureau of Labor Statistics (2025). <a href="https://www.bls.gov/opub/ted/2025/fatal-work-injuries-fell-in-2023.htm">Fatal work injuries fell in 2023</a>. The Economics Daily.',
        'U.S. Bureau of Labor Statistics (2025). <a href="https://www.bls.gov/opub/ted/2025/fatal-falls-in-the-construction-industry-in-2023.htm">Fatal falls in the construction industry in 2023</a>. The Economics Daily.',
    ],
    next=['insight-llms-construction-documents', 'insight-rework-bad-data'],
)

PERMITS = dict(
    slug='insight-permit-wait-times', topic='Pre-construction', topics='data controls',
    title='Waiting for a permit: why the average approval time is wrong',
    dek='Ask how long a building department takes and most people quote the average for approved applications. That shortcut ignores every application still waiting, so it always makes approvals look faster than they are. The fix is a method medicine has used since 1958, shown here on a case study of 29,123 building filings.',
    meta='Why approved-only averages understate permit approval times, how survival analysis gives honest approval probabilities, and a case study of 29,123 building filings.',
    blurb='Approved-only averages always make permits look faster than they are. In a case study of 29,123 filings, the gap was 47 days.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('47 days', 'how much the approved-only median understated the real wait, in a case study of 29,123 filings (107 vs 154 days)', 1),
          ('1 in 4', 'filings in the same case study were still waiting for approval, invisible to a simple average', 1),
          ('1958', 'the year Kaplan and Meier published the method that counts still-waiting cases properly', 2)],
    takeaways=[
        'Averages of <strong>approved</strong> filings leave out every filing still waiting, which are exactly the slow ones. In a case study of 29,123 filings, the median moved from <strong>107 to 154 days</strong> once they were counted.',
        'The bias gets worse for recent filings: for 2026 filings the naive median is 74 days against 182.',
        'Survival analysis (Kaplan–Meier, Cox, survival forests) uses “still waiting after 400 days” as information instead of throwing it away.',
        'Check calibration, not just ranking. A naive model ranked filings almost as well but promised a 73% chance of approval within 180 days when 59% happened.',
        'Permit time is not a side issue: Federal Reserve research finds construction productivity fell most in places with long permit times.',
    ],
    sections=[
        ('why-it-matters', 'Why approval time is a cost line', f'''
<p>Until plans are approved, the construction start, the financing draw and the holding costs are all guesses. Every month of waiting is a month of interest, overheads and escalation, and regulation and approvals together are a material share of what a building costs: one home builders’ association estimated regulation at 23.8% of the average price of a new home in its market{c(3)}.</p>
<p>The variation between places is large, even between neighbouring cities. Research on housing approvals found that more than 80% of proposed multifamily developments in the jurisdictions studied needed a discretionary approval, and that the median time for similar projects ranged from about six months in one city to more than 25 months in the next{c(4)}.</p>
<p>And it shows up in productivity statistics. Federal Reserve economists found that single-family construction productivity declined most in areas with tighter supply constraints, <strong>especially locations with long permit times</strong>{c(5)}.</p>
'''),
        ('the-shortcut', 'The shortcut that everyone uses', f'''
<p>The usual way to answer “how long does approval take?” is to take filings that were approved and average the days from filing to approval. It feels reasonable. It is biased, always in the same direction.</p>
{callout('A simple example', 'Five filings, observed today. Three were approved after 60, 90 and 120 days. Two were filed 300 days ago and are still waiting.', 'The approved-only average is 90 days. But two of the five filings have already waited 300 days and counting. The true typical wait is well above 90 days; the shortcut simply cannot see the slow cases, because they have not finished yet.')}
<p>Statisticians call the still-waiting filings <strong>right-censored</strong>: we know the wait is <em>at least</em> 300 days, not what it will be. Dropping them makes the process look faster than it is. Giving them a made-up end date is worse. Kaplan and Meier solved this in 1958 with an estimator that uses each censored case for exactly as long as it was observed{c(2)}.</p>
{pull('A filing still waiting after 400 days is information, not missing data.')}
'''),
        ('the-nyc-evidence', 'What 29,123 real filings show', f'''
<p>I took New York City’s public DOB NOW filing data{c(6)} for four major job types (New Building, two kinds of major alteration, and full demolition): 29,123 filings from 2021 to 2026, one row per job, with only the information known on the filing day{c(1)}. A quarter were still open, and even among 2021 filings about one in eight had never been approved.</p>
{bars('Median days from filing to plan approval, Kaplan–Meier (all filings)', [
    ('New Building', 262, '262', True), ('ALT-CO (new building with existing elements)', 213, '213', False),
    ('Alteration CO', 147, '147', False), ('Full demolition', 39, '39', False)],
    'Source: my analysis of NYC Open Data, DOB NOW: Build – Job Application Filings [1][6].')}
{bars('Approved-only median vs survival median, all four job types', [
    ('Approved filings only (the shortcut)', 107, '107 days', False), ('All filings, Kaplan–Meier', 154, '154 days', True)],
    'For 2026 filings alone: 74 days (shortcut) vs 182 days (Kaplan–Meier). Source: [1].')}
<p>Other findings from the same data: Queens was fastest (median 130 days, against about 167–171 elsewhere), and after plan approval the first permit followed a median of about two months later. Approval is not the permit, and the permit is not the start on site.</p>
'''),
        ('forecasting', 'From a median to a forecast', f'''
<p>A median by job type is a better rule of thumb. A forecast for one filing needs a model that learns from filing-day features and handles censoring properly. I compared five approaches on filings from July 2024 to June 2025 that the models never saw: Kaplan–Meier by job type, a naive regression trained only on approved filings, Cox proportional hazards, a random survival forest and an XGBoost accelerated-failure-time model{c(1)}.</p>
<p>The instructive result is the naive model. It <strong>ranked</strong> filings almost as well as the survival models, so a ranking metric alone would have hidden the problem. But its probabilities were over-optimistic: it predicted a 73% chance of approval within 180 days when 59% actually happened, because it never saw the filings that stall. The survival model’s probabilities landed within about 3.5 points of what happened, on average across ten groups.</p>
{callout('Honest limits', 'Ranking is modest (C-index about 0.69–0.70). Much of the wait depends on drawing quality, how quickly objections are answered and which examiner picks up the job, none of which is on the filing. The P10–P90 range is wide, about a month to two years for a typical job, because approval times are.')}
'''),
        ('what-to-do', 'How to use this in planning', checklist([
            '<strong>Never average only the finished cases.</strong> For approvals, RFIs, change orders or submittals, count the open items as “at least this long”.',
            '<strong>Quote a probability, not a date.</strong> “60% chance of approval within six months” supports float and financing decisions; a single date hides the risk.',
            '<strong>Plan to the P80, not the median,</strong> when holding costs are high, and review the forecast when objections arrive.',
            '<strong>Separate the milestones.</strong> Plan approval, permit issue and site start are different events with different delays.',
            '<strong>Check calibration.</strong> Of the jobs your model gave a 70% chance, did about 70% happen? Ranking metrics alone won’t tell you.',
        ])),
    ],
    applied=dict(title='NYC Permit Approval Forecast',
                 text=['Real NYC Open Data, a documented cleaning pipeline, five survival models and a browser app that gives the chance of approval by 90, 180 and 365 days for a new filing.'],
                 href='https://atuliwale.github.io/Portfolio/projects/15-nyc-permit-approval-forecast/', label='Open the live app'),
    sources=[
        'Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects/15-nyc-permit-approval-forecast">NYC Permit Approval Forecast: survival analysis of DOB NOW filings, 2021–2026</a>. GitHub.',
        'Kaplan, E. L. and Meier, P. (1958). <a href="https://www.tandfonline.com/doi/abs/10.1080/01621459.1958.10501452">Nonparametric estimation from incomplete observations</a>. Journal of the American Statistical Association, 53(282), 457–481.',
        'Emrath, P. (2021). <a href="https://www.nahb.org/-/media/NAHB/news-and-economics/docs/housing-economics-plus/special-studies/2021/special-study-government-regulation-in-the-price-of-a-new-home-may-2021.pdf">Government regulation in the price of a new home: 2021</a>. National Association of Home Builders.',
        'Terner Center for Housing Innovation, UC Berkeley. <a href="https://ternercenter.berkeley.edu/wp-content/uploads/2020/08/Cost_of_Building_Housing_Series_Framing.pdf">The Cost of Building Housing research series</a> (framing paper).',
        'Garcia, D. and Molloy, R. (2023, revised 2025). <a href="https://www.federalreserve.gov/econres/feds/files/2023052r1pap.pdf">Reexamining lackluster productivity growth in construction</a>. Finance and Economics Discussion Series 2023-052, Federal Reserve Board.',
        'NYC Open Data. <a href="https://data.cityofnewyork.us/Housing-Development/DOB-NOW-Build-Job-Application-Filings/w9ak-ipjd">DOB NOW: Build – Job Application Filings</a> (dataset w9ak-ipjd).',
    ],
    next=['insight-construction-productivity', 'insight-cost-estimates-miss'],
)

ESTIMATES = dict(
    slug='insight-cost-estimates-miss', topic='Estimating', topics='controls',
    title='Why construction estimates miss — and why a range beats a single number',
    dek='Cost overruns are not bad luck. Decades of research show they are predictable, biased in one direction and correctable with a method that governments have used for twenty years: look at how similar projects actually turned out.',
    meta='The research on construction cost overruns, optimism bias and reference class forecasting, and how to move from a single-point estimate to a calibrated P10–P90 range.',
    blurb='Only 8.5% of 16,000 big projects hit budget and schedule. Optimism bias, reference classes, and why a calibrated range beats one number.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('8.5%', 'of more than 16,000 large projects were delivered on budget and on time', 1),
          ('0.5%', 'were on budget, on time and delivered the benefits promised', 1),
          ('24–51%', 'government-recommended uplift to early cost estimates for standard vs non-standard buildings', 2)],
    takeaways=[
        'Overruns are the norm: in Bent Flyvbjerg’s database of 16,000+ projects, <strong>8.5%</strong> met both budget and schedule.',
        'The errors are biased, not random. Early estimates are systematically too low, driven by optimism bias and, sometimes, strategic misrepresentation.',
        '<strong>Reference class forecasting</strong> corrects the bias by starting from the actual outcomes of similar past projects, then adjusting.',
        'Government appraisal guidance can build this in: one widely used version adds up to <strong>24%</strong> to early capital cost for standard buildings and up to <strong>51%</strong> for non-standard ones.',
        'A single number hides the risk. A calibrated P10–P90 range, checked against what later happened, is more honest and more useful.',
    ],
    sections=[
        ('overruns-are-normal', 'Overruns are the norm, not the exception', f'''
<p>Bent Flyvbjerg has spent three decades collecting cost and schedule data on large projects: buildings, rail, roads, bridges, IT, energy and more. In <em>How Big Things Get Done</em> (2023, with Dan Gardner), he reports that of more than 16,000 projects in the database, only <strong>8.5%</strong> were delivered on budget and on time, and only <strong>0.5%</strong> were on budget, on time and delivered the benefits promised{c(1)}.</p>
{bars('Share of 16,000+ large projects that hit their targets', [
    ('All projects in the database', 100, '100%', False), ('On budget and on time', 8.5, '8.5%', True),
    ('On budget, on time and on benefits', 0.5, '0.5%', True)],
    'Share of more than 16,000 projects. Source: Flyvbjerg and Gardner (2023) [1].', max_value=100)}
<p>Flyvbjerg calls this the <strong>“iron law”</strong>: over budget, over time, under benefits, over and over again. The important word is <em>systematic</em>. If estimating errors were random, some projects would come in well under and the average would be close to zero. They don’t. The distribution is skewed towards overruns, with a long tail of very large ones.</p>
'''),
        ('why-estimates-are-low', 'Why early estimates are too low', f'''
<p>The research points to two causes that usually act together{c(3)}:</p>
<ul>
<li><strong>Optimism bias</strong>, the planning fallacy described by Daniel Kahneman and Amos Tversky. We build the estimate from the “inside view”: this project’s scope, this team’s plan, the risks we can see. We underweight the risks we can’t see yet, which on a building project include design development, ground conditions, approvals, scope growth and price movement.</li>
<li><strong>Strategic misrepresentation.</strong> Where a low number helps a project get approved, there is pressure towards the low number. This is not always deliberate, but it pulls in the same direction as optimism.</li>
</ul>
<p>Neither cause is fixed by working harder on the same estimate. A more detailed inside view is still an inside view. What corrects it is outside information.</p>
{pull('A more detailed inside view is still an inside view. What corrects it is outside information.')}
'''),
        ('reference-class-forecasting', 'Reference class forecasting: start from what happened', f'''
<p>Reference class forecasting, developed for projects by Flyvbjerg from Kahneman and Tversky’s work, takes the “outside view”{c(3)}. It has three steps:</p>
<ol>
<li><strong>Choose a reference class</strong> of past projects similar enough to be comparable: type, size, location, procurement route.</li>
<li><strong>Establish the distribution</strong> of their outcomes, for example actual cost against the estimate at the same stage.</li>
<li><strong>Place your project in that distribution</strong> and adjust only for differences you can actually justify.</li>
</ol>
<p>Some governments build this into their appraisal rules. The best-known example, HM Treasury’s supplementary Green Book guidance, on optimism bias gives upper-bound uplifts to apply to capital cost at the earliest business-case stage, reducing as project-specific risks are identified and managed{c(2)}:</p>
{bars('HM Treasury optimism-bias upper bounds for capital expenditure', [
    ('Standard buildings', 24, '24%', True), ('Standard civil engineering', 44, '44%', False),
    ('Non-standard buildings', 51, '51%', True), ('Non-standard civil engineering', 66, '66%', False),
    ('Equipment / development (incl. IT)', 200, '200%', False)],
    'Upper bounds at outline business-case stage; lower bounds range from about 2% to 10%. Source: HM Treasury [2].')}
<p>The point is not the exact percentages, which come from one government’s study of its public projects. It is the discipline: an early estimate should carry an explicit, evidence-based allowance, and that allowance should shrink only as risk is actually removed.</p>
'''),
        ('from-number-to-range', 'From one number to a calibrated range', f'''
<p>A single-point estimate says nothing about its own uncertainty. A range does, if it is honest. The usual way to express it is with percentiles:</p>
<ul>
<li><strong>P50</strong>: half of comparable outcomes came in below this figure, half above.</li>
<li><strong>P10 to P90</strong>: the band that should contain about 80% of outcomes.</li>
</ul>
<p>“Should” is the key word. A range is only useful if it is <strong>calibrated</strong>, meaning that when you check it against projects that later completed, about 80% of their actual costs fall inside the P10–P90 band. Too narrow and it gives false confidence; too wide and nobody can use it. Coverage on later projects is the test.</p>
{callout('Rebase before you compare', 'Past projects were priced in past years. Before building a reference class, convert costs to a common base date with a construction cost index. Otherwise inflation looks like overrun, and a model trained on old prices will under-estimate new ones.')}
'''),
        ('what-to-do', 'What to change in your estimating workflow', checklist([
            '<strong>Keep an outcomes register.</strong> For every completed project, record the estimate at each stage and the final cost. This is your reference class.',
            '<strong>Rebase costs to a common date</strong> before comparing projects from different years.',
            '<strong>Start from the reference class, then adjust.</strong> Write down every adjustment and the evidence behind it.',
            '<strong>Report P10, P50 and P90</strong>, not just a figure, and say what drives the width.',
            '<strong>Test calibration yearly.</strong> Did about 80% of completed projects land inside your P10–P90 bands? If not, widen or narrow them.',
            '<strong>Test on later projects, not a random sample.</strong> Evaluate any estimating model on projects that started after its training data, as it will be used.',
        ])),
    ],
    applied=dict(title='Cost Plan Estimation (ML)',
                 text=['A feasibility-stage estimator tested against the coefficient method I automated earlier in my career. Costs are rebased to January 2018 prices and the model is tested on later projects: <strong>6.6%</strong> average error against 11.2% for the coefficient method, with a P10–P90 range that covered 81% of later projects.',
                       'Built on synthetic data designed to behave like Indian cost-plan data (noise, outliers, missing fields); a real deployment would re-test on a firm’s own completed projects.'],
                 href='https://atuliwale.github.io/Portfolio/projects/13-cost-plan-estimation/', label='Open the live app'),
    sources=[
        'Flyvbjerg, B. and Gardner, D. (2023). <a href="https://www.penguinrandomhouse.com/books/672118/how-big-things-get-done-by-bent-flyvbjerg-and-dan-gardner/">How Big Things Get Done</a>. Currency / Penguin Random House.',
        'HM Treasury. <a href="https://assets.publishing.service.gov.uk/media/5a74dae740f0b65f61322c72/Optimism_bias.pdf">Supplementary Green Book guidance: optimism bias</a>.',
        'Flyvbjerg, B. (2006). <a href="https://arxiv.org/abs/1302.3642">From Nobel Prize to project management: getting risks right</a>. Project Management Journal, 37(3), 5–15.',
    ],
    next=['insight-forecasting-final-cost', 'insight-material-price-escalation'],
)

POSTS = [SAFETY, PERMITS, ESTIMATES]
