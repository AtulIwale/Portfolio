from build import c, bars, table, pull, callout, checklist

DATE, DATE_LABEL = '2026-09-29', 'Sept 2026'

FORECAST = dict(
    slug='insight-forecasting-final-cost', topic='Project controls', topics='controls ai',
    title='Forecasting final cost: when the CPI formula works, and when it doesn’t',
    dek='Earned value’s favourite shortcut assumes that a project’s cost efficiency settles early and stays put. That holds on some projects and not on others. Here is what the research says, and where machine learning adds something real.',
    meta='The evidence on CPI stability in earned value management, why the EAC = BAC / CPI formula misleads on many construction projects, and how ML forecasts should be tested.',
    blurb='Earned value assumes cost efficiency settles by 20% complete. On defence contracts it did; on other projects it often didn’t.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('20%', 'complete: after this point, cumulative CPI moved by less than ±0.10 on 155 US defence contracts', 1),
          ('41%', 'complete before CPI stabilised on 136 environmental remediation projects', 2),
          ('2.8%', 'error of my ML forecast below 30% complete, against 4.6% for the CPI formula (synthetic data)', 0)],
    takeaways=[
        'The standard forecast, <strong>EAC = BAC ÷ CPI</strong>, assumes the cost efficiency to date will continue for the rest of the job.',
        'On 155 US defence contracts, cumulative CPI barely moved after <strong>20% complete</strong>. That result is the basis of the “CPI stability” rule.',
        'It does not transfer automatically: on 136 environmental remediation projects, CPI did not settle until <strong>41% complete</strong>, and it is rarely stable on smaller commercial projects.',
        'Construction front-loads procurement, change orders and subcontract packages, which is exactly what breaks the assumption.',
        'ML can learn from completed projects which early patterns predict overrun, but only if it is tested on later projects and compared honestly with the CPI baseline.',
    ],
    sections=[
        ('the-formula', 'The formula everyone uses', f'''
<p>Earned value management compares three numbers at any point in a project: the budgeted cost of work planned, the budgeted cost of work actually performed (earned value, EV) and the actual cost of that work (AC). The <strong>cost performance index</strong>, CPI = EV ÷ AC, says how much budgeted work you get for each unit spent. A CPI of 0.9 means every ₹100 spent has earned ₹90 of planned work.</p>
<p>The most common forecast of final cost divides the budget at completion by the CPI to date: <strong>EAC = BAC ÷ CPI</strong>. It is simple, explainable and built into most project controls software. It also carries a strong assumption: the efficiency of the work done so far is the efficiency of the work still to do.</p>
'''),
        ('the-evidence-for', 'The evidence for CPI stability', f'''
<p>The assumption has a respectable origin. In 1993, David Christensen and Scott Heise analysed cost performance reports from <strong>155 US defence contracts across 44 programmes</strong> from 1971 to 1991: aircraft, missiles, electronics, ships, software and more. They found that from the 20% completion point to contract completion, the range of the cumulative CPI was less than 0.20 on every contract{c(1)}. That is usually summarised as “after 20% complete, cumulative CPI does not change by more than ±0.10”.</p>
<p>If that holds, the CPI formula gives a usable forecast early in a project, and a CPI of 0.85 at 20% complete is an early warning that is unlikely to fix itself.</p>
'''),
        ('the-evidence-against', 'The evidence against assuming it', f'''
<p>Later research tested whether the rule transfers to other kinds of projects. It often doesn’t.</p>
<ul>
<li>Clayson, Thal and White studied monthly earned value data for <strong>136 environmental remediation projects</strong> at a US federal agency (fiscal years 2012–2013). CPI did not stabilise until the projects were <strong>41% complete</strong> by duration, and stability depended on factors such as contractor qualifications, communication, stakeholder engagement and contracting strategy{c(2)}.</li>
<li>Research by Henderson and Zwikael, discussed by Patrick Weaver, found CPI stability is not a given and rarely exists on smaller commercial projects. Where stability does appear, it is better read as a sign of a good plan, stable scope and effective management than as a law of nature{c(3)}.</li>
</ul>
{bars('Completion point after which cumulative CPI settled', [
    ('US defence contracts (155)', 20, '20%', False), ('Environmental remediation projects (136)', 41, '41%', True),
    ('Smaller commercial projects', 100, 'rarely', False)],
    'Sources: Christensen and Heise (1993) [1]; Clayson, Thal and White (2018) [2]; Henderson and Zwikael, via Weaver [3]. The last bar indicates that stability was often not reached.', max_value=100)}
{pull('CPI stability is better read as a sign of a good plan and stable scope than as a law of nature.')}
'''),
        ('why-construction-breaks-it', 'Why construction breaks the assumption', f'''
<p>A building project’s cost curve is not a steady stream of similar work. Several features common in construction make early CPI a weak guide to late CPI:</p>
<ul>
<li><strong>Front-loaded commitments.</strong> Early packages such as piling, frame and long-lead procurement are often bought competitively and may perform well, while finishes and services come later with more interfaces and more variation.</li>
<li><strong>Change orders.</strong> Scope added mid-project changes both the budget and the actual cost; if the budget isn’t updated promptly, CPI moves for reasons unrelated to productivity.</li>
<li><strong>Subcontract timing.</strong> Cost is often recognised when a subcontractor bills, not when the work happens, which moves AC relative to EV.</li>
<li><strong>Price movement.</strong> Material escalation during the job raises actual cost without any change in site efficiency.</li>
</ul>
<p>None of this makes the CPI formula useless. It makes it a <strong>baseline</strong>: the forecast any better method has to beat.</p>
'''),
        ('where-ml-helps', 'Where machine learning genuinely helps', f'''
<p>A model trained on completed projects can learn which early patterns preceded overruns: the mix of cost codes, the pace of commitments, variation history, the gap between billed and certified work. It can also output a <strong>range</strong> rather than a single number. But three disciplines separate a useful forecast from an impressive-looking one:</p>
<ol>
<li><strong>Test on later projects.</strong> Train on projects that finished earlier and test on projects that came later. A random split lets the model see the future.</li>
<li><strong>Beat the baseline where it matters.</strong> The early stage, below about 30% complete, is where a forecast is most useful and where CPI is least reliable. Report accuracy there separately.</li>
<li><strong>Stay explainable.</strong> A cost manager needs to see why the forecast moved (which packages, which codes), or they won’t act on it.</li>
</ol>
{callout('What to watch for', 'Leakage is the classic mistake: using any field that is only known at completion (final account status, closing adjustments) as an input. The model then looks brilliant in testing and fails in use.')}
'''),
        ('what-to-do', 'A practical forecasting routine', checklist([
            '<strong>Report CPI-based EAC as the baseline,</strong> and say how stable CPI has been over the last few periods.',
            '<strong>Add at least one independent forecast:</strong> bottom-up estimate to complete, a model, or both, and explain any gap.',
            '<strong>Keep budgets current.</strong> Approve and load change orders promptly so CPI reflects performance, not paperwork.',
            '<strong>Show a range.</strong> P10–P90 on final cost is more honest than one EAC figure, especially early.',
            '<strong>Track forecast accuracy over time</strong> on completed projects, by project stage, so you know which method to trust when.',
        ])),
    ],
    applied=dict(title='Project Cost & Margin Intelligence',
                 text=['An XGBoost forecast of each project’s final cost and margin, trained on 239 completed projects and compared with the CPI formula: <strong>2.8%</strong> average error below 30% complete against 4.6% for CPI, with P10–P90 ranges and next-quarter spend.',
                       'Built on synthetic data patterned on real ERP structures, so no client data is exposed.'],
                 href='/projects.html', label='See the project'),
    sources=[
        'Christensen, D. S. and Heise, S. R. (1993). <a href="https://www.humphreys-assoc.com/uploads/commerce/images/pdf/Christensen_and_Heise_CPI_Stability.pdf">Cost performance index stability</a>. Paper analysing 155 US defence contracts, 1971–1991.',
        'Clayson, D. S., Thal, A. E. and White, E. D. (2018). <a href="https://www.emerald.com/jdal/article/2/2/94/206554/Cost-performance-index-stability-insights-from">Cost performance index stability: insights from environmental remediation projects</a>. Journal of Defense Analytics and Logistics, 2(2).',
        'Weaver, P. <a href="https://mosaicprojects.com.au/Mag_Articles/N002_CPI_Stability_Myth.pdf">The CPI stability myth</a>. Mosaic Projects.',
    ],
    next=['insight-cost-estimates-miss', 'insight-rework-bad-data'],
)

REWORK = dict(
    slug='insight-rework-bad-data', topic='Data & quality', topics='data',
    title='Rework and bad data: the cost line nobody budgets',
    dek='Surveys and benchmarking studies agree that rework is a large, recurring cost, and that poor project information is one of its biggest causes. The fix starts long before the site: at the point where data is first entered.',
    meta='Research on the cost of rework and poor project data in construction (FMI/PlanGrid, CII), the data problems behind it, and practical controls to prevent it.',
    blurb='Poor data and miscommunication drove an estimated $31.3bn of US rework in one year. What the research says, and what bad data looks like.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('14+ hrs', 'a week per project team member spent on non-optimal activities: fixing mistakes, looking for data, resolving conflict', 1),
          ('$31.3bn', 'of US rework in 2018 attributed to poor project data and miscommunication', 1),
          ('2–20%', 'of a project’s contract amount is typically lost to rework, per CII research', 2)],
    takeaways=[
        'In a survey of about 600 construction leaders, poor project data and miscommunication were blamed for <strong>48% of rework</strong>, an estimated <strong>$31.3bn</strong> in the US in 2018.',
        'Team members reported spending <strong>14+ hours a week</strong> on non-optimal activities, worth an estimated $177.5bn a year in US labour cost.',
        'Construction Industry Institute research puts rework at <strong>2–20%</strong> of contract value and finds it can be predicted before construction starts.',
        'Bad data has recognisable shapes: duplicates, spelling variants, mixed units, codes from different standards and impossible dates. Every dataset in my portfolio had them.',
        'The cheapest place to fix data is where it is entered, with validation, ownership and one source of truth.',
    ],
    sections=[
        ('what-surveys-found', 'What the surveys found', f'''
<p>In 2018, FMI and PlanGrid surveyed nearly 600 construction leaders about how project teams spend their time and where things go wrong. Their report, <em>Construction Disconnected</em>, estimated that team members spend more than <strong>14 hours a week</strong> on non-optimal activities such as looking for project data, fixing mistakes and managing conflict, worth about <strong>$177.5bn</strong> a year in US labour cost{c(1)}.</p>
<p>On rework specifically, respondents attributed <strong>48%</strong> of it to poor project data and miscommunication: 26% to poor communication between team members and 22% to poor project information. That share represented an estimated <strong>$31.3bn</strong> of rework in the US in 2018{c(1)}.</p>
{bars('Share of rework attributed to each cause (survey estimate)', [
    ('Poor communication between team members', 26, '26%', True), ('Poor project information / data', 22, '22%', True),
    ('All other causes', 52, '52%', False)],
    'Source: FMI and PlanGrid, Construction Disconnected (2018) [1]. Survey-based estimates from US construction leaders.', max_value=100)}
{callout('How to read survey figures', 'These are estimates from respondents, not measured costs, and the report was produced with a software vendor. Treat the exact dollar values with care. The direction is consistent with independent benchmarking research, which is why they are worth taking seriously.')}
'''),
        ('what-benchmarking-says', 'What rework benchmarking says', f'''
<p>The Construction Industry Institute (CII), a research consortium based at the University of Texas at Austin, has studied field rework for decades. Its research puts rework on a typical project at between <strong>2% and 20%</strong> of the contract amount{c(2)}.</p>
<p>More usefully, CII developed the <strong>Field Rework Index</strong>, a short questionnaire completed before construction that predicts rework and cost growth. The factors with the strongest relationship to field rework are{c(2)}:</p>
<ul>
<li>owner alignment,</li>
<li>design rework,</li>
<li>constructability commitment,</li>
<li>interdisciplinary design coordination,</li>
<li>the degree of project execution planning.</li>
</ul>
<p>Projects with low index scores experienced low rework and even negative cost growth. Rework, in other words, is largely decided in design and planning, and it can be seen coming.</p>
{pull('Rework is largely decided in design and planning, and it can be seen coming.')}
'''),
        ('what-bad-data-looks-like', 'What bad data actually looks like', f'''
<p>“Poor project information” sounds abstract. In practice it has a small number of recognisable shapes. These are real examples from datasets in my own portfolio, two built on public government data and one on synthetic data designed to behave like real cost records{c(3)}:</p>
{table(['Problem', 'Example found', 'What it breaks'], [
    ['Codes from different standards', '348 OSHA event codes stored at 2, 3 or 4 digits from more than one coding manual', 'Trend reports compare different things under one label'],
    ['A rule change mid-series', 'OSHA’s January 2024 manual change moved the caught-in / struck-by line', 'A “trend” that is really a definition change'],
    ['Duplicates', '128 duplicate NYC permit records; 6 duplicate rows in cost data', 'Double-counted cost, work or risk'],
    ['Impossible dates', '21 NYC approvals dated before their filing', 'Negative durations, broken schedules'],
    ['Mixed units', '18 cost entries recorded in sq ft instead of sq m', 'Rates wrong by a factor of about 10.8'],
    ['Spelling variants', 'Legacy city names (Bangalore, Bombay, Gurgaon) mixed with other spellings', 'One place split into several'],
    ['Silent blanks', 'Missing soil or green-rating fields', 'Quietly dropped rows, biased averages']],
    'Sources: my project documentation [3]. OSHA and NYC data are real public data; the cost data is synthetic.')}
<p>None of these is exotic. Each one was either entered inconsistently or changed definition over time, and each one silently changes the answer to a management question unless someone catches it.</p>
'''),
        ('why-it-compounds', 'Why bad data compounds', f'''
<p>In an ERP-connected business, a record doesn’t stay in one place. A wrong cost code on a purchase order flows into commitments, then into the cost report, then into the forecast and the margin review. A supplier set up twice splits its spend and hides its delivery record. A drawing revision that doesn’t reach the site becomes rework.</p>
<p>That is why cleaning data at the reporting end is so expensive: every downstream report inherits the error, and every fix has to be repeated. It is far cheaper to stop the error where the data is first entered.</p>
'''),
        ('what-to-do', 'Controls that prevent it', checklist([
            '<strong>Validate at entry.</strong> Pick-lists for locations and categories, unit checks, date rules (approval cannot precede filing), mandatory fields that matter.',
            '<strong>Give master data an owner.</strong> Someone is accountable for the supplier, item and cost-code masters, and for merging duplicates.',
            '<strong>Version your definitions.</strong> When a coding standard changes, record the date, so analysis can separate the definition change from a real trend.',
            '<strong>One source for drawings and RFIs.</strong> Rework often starts when the site builds from a superseded revision.',
            '<strong>Measure rework explicitly.</strong> Give it a cost code. What isn’t measured is absorbed into “overrun” and never fixed.',
            '<strong>Score rework risk before construction.</strong> Use a structured check such as CII’s Field Rework Index at the end of design.',
        ])),
    ],
    applied=dict(title='Cleaning comes first, in every project',
                 text=['Each of my fifteen portfolio projects documents its data checks before any model: duplicates, joins, date order, units and category rules, with the counts reported. It is the least glamorous step and the one that most changes the answer.'],
                 href='/projects.html', label='See the projects'),
    sources=[
        'FMI and PlanGrid (2018). <a href="http://pg.plangrid.com/rs/572-JSV-775/images/Construction_Disconnected.pdf">Construction Disconnected: the high cost of poor data and miscommunication</a>.',
        'Construction Industry Institute. <a href="https://www.construction-institute.org/the-field-rework-index-early-warning-for-field-rework-and-cost-growth">The Field Rework Index: early warning for field rework and cost growth</a>.',
        'Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects">Portfolio project documentation</a> (projects 13, 14 and 15: data-cleaning sections). GitHub.',
    ],
    next=['insight-construction-productivity', 'insight-osha-severe-injuries'],
)

PRODUCTIVITY = dict(
    slug='insight-construction-productivity', topic='Productivity', topics='data',
    title='The construction productivity puzzle: what fifty years of data actually say',
    dek='Construction is the one major industry whose measured productivity has gone backwards. Is that real or a measurement artefact? The research is clearer than the headlines, and it points at process and regulation as much as technology.',
    meta='What the research says about construction productivity: McKinsey Global Institute, Goolsbee and Syverson, BLS and Federal Reserve studies, the measurement debate, and what it means for projects.',
    blurb='Construction labour productivity grew about 1% a year while the economy managed 2.8%. Is it real, and what drives it?',
    date=DATE, date_label=DATE_LABEL,
    keys=[('1%', 'a year: construction labour-productivity growth over two decades, against 2.8% for the world economy', 1),
          ('~40%', 'lower value added per full-time worker in US construction in 2020 than in 1970', 2),
          ('1987', 'since then, construction is the only major US industry with negative average productivity growth', 3)],
    takeaways=[
        'McKinsey Global Institute found construction labour productivity grew about <strong>1% a year</strong> for two decades, against 2.8% for the world economy and 3.6% for manufacturing.',
        'In the US, value added per construction worker was roughly <strong>40% lower</strong> in 2020 than in 1970, and physical measures of housebuilding productivity are flat or falling.',
        'It is not just a measurement error: Federal Reserve economists found the likely bias is <strong>too small</strong> to change the conclusion.',
        'Productivity fell most where building is hardest: dense urban cores, tight supply constraints and <strong>long permit times</strong>.',
        'The gap shows up on projects as waiting, rework and re-keyed information, which is why process and data fixes pay before new technology does.',
    ],
    sections=[
        ('the-headline-numbers', 'The headline numbers', f'''
<p>In 2017 the McKinsey Global Institute published <em>Reinventing construction: a route to higher productivity</em>. Its headline finding was that global construction labour-productivity growth had averaged about <strong>1% a year</strong> over the previous two decades, against 2.8% for the total world economy and 3.6% for manufacturing. If construction caught up with the wider economy, it estimated, the sector’s value added could rise by about <strong>$1.6 trillion a year</strong>{c(1)}.</p>
{bars('Annual labour-productivity growth, about 1995–2015', [
    ('Construction', 1.0, '1.0%', True), ('Total world economy', 2.8, '2.8%', False), ('Manufacturing', 3.6, '3.6%', False)],
    'Source: McKinsey Global Institute (2017) [1].')}
<p>The US picture is starker. Austan Goolsbee and Chad Syverson, in a 2023 NBER paper titled <em>The Strange and Awful Path of Productivity in the U.S. Construction Sector</em>, found that value added per full-time employee in US construction was about <strong>40% lower in 2020 than in 1970</strong>. Had it instead grown at a modest 1% a year, aggregate US labour productivity would have been about 10% higher{c(2)}.</p>
'''),
        ('is-it-real', 'Is it real, or a measurement problem?', f'''
<p>This is the right question to ask. Productivity is output divided by input, and construction output is hard to measure: every project is different, and turning spending into “real” output needs a price index that separates inflation from better buildings. If the price index rises too fast, measured productivity falls even when crews are working as well as ever.</p>
<p>The Bureau of Labor Statistics took this seriously. BLS economists led by Leo Sveikauskas developed new, better quality-adjusted productivity measures for four construction industries (single-family and multifamily housing, highways and bridges, and industrial construction), noting that reliable output deflators are the core difficulty{c(4)}. BLS now publishes these measures{c(5)}.</p>
<p>The most direct test came from Federal Reserve economists Daniel Garcia and Raven Molloy. Construction is the only major US industry to have recorded <strong>negative average productivity growth since 1987</strong>, and they asked how much of that could be explained by unmeasured improvements in building quality. Their answer: even under generous assumptions, the bias is <strong>not large enough</strong> to overturn the conclusion that construction productivity growth has been weak{c(3)}.</p>
{pull('Even under generous assumptions, measurement bias is not large enough to overturn the conclusion.')}
'''),
        ('what-the-data-point-to', 'What the data point to', f'''
<p>If the decline is real, the next question is why. The research offers several pieces of evidence:</p>
<ul>
<li><strong>Physical output per worker is flat.</strong> Goolsbee and Syverson look past price indices to physical measures in housing, such as homes or square feet built per worker, and find productivity falling or at best stagnant over decades{c(2)}.</li>
<li><strong>Materials are used less efficiently.</strong> The same paper finds a decline in how efficiently firms turn materials into output{c(2)}.</li>
<li><strong>Productive firms don’t grow.</strong> In most industries, more productive producers win market share. Across US states, construction shows no sign of this: states with more productive construction sectors do not gain share of national activity{c(2)}.</li>
<li><strong>Constraints matter.</strong> Garcia and Molloy find productivity fell most in areas with more building in the urban core and tighter supply constraints, <strong>especially where permit times are long</strong>{c(3)}.</li>
</ul>
<p>The short-run numbers show how sensitive the measure is to demand. BLS reports that single-family housebuilding productivity rose 12.4% a year from 2019 to 2021 as output grew much faster than hours worked, then declined in 2022 and 2023 as output fell and hours held steady{c(5)}{c(6)}. Productivity in construction moves with how smoothly work flows, not only with how hard people work.</p>
'''),
        ('on-a-project', 'Where the gap shows up on a project', f'''
<p>National statistics are abstract; site productivity is not. The same McKinsey report grouped its recommendations into seven areas: regulation, contracts, design and engineering, procurement and supply chain, on-site execution, digital technology and materials, and workforce skills{c(1)}. Three years later, McKinsey described construction as one of the least digitised industries of all{c(7)}.</p>
<p>In ERP implementation work, the losses that show up most clearly in the data are rarely in the craft work itself. They are in the gaps between steps:</p>
<ul>
<li>waiting for an approval, a drawing revision, a material delivery or a permit;</li>
<li>re-keying the same information into site reports, spreadsheets and the ERP;</li>
<li>rework caused by building from the wrong information;</li>
<li>decisions made late because the cost or progress report arrives after the fact.</li>
</ul>
<p>Each of these is a process and data problem before it is a technology problem, which is why mapping the process comes before choosing a tool.</p>
'''),
        ('what-to-do', 'What a project team can act on', checklist([
            '<strong>Measure flow, not just effort.</strong> Track waiting time for approvals, RFIs, submittals and deliveries alongside labour hours.',
            '<strong>Enter information once.</strong> Map where the same data is typed in more than once and connect those steps.',
            '<strong>Attack rework at design stage,</strong> where most of it is decided.',
            '<strong>Plan approvals as a risk,</strong> with probabilities and float, not a fixed date.',
            '<strong>Standardise and repeat.</strong> Repeatable details, packages and processes let a team learn from one project to the next.',
        ])),
    ],
    applied=dict(title='Process first. Always.',
                 text=['My approach starts by mapping how work and information actually flow (the handoffs, approvals and re-keyed data) before any system or model is chosen. The Approach page shows how that sequence runs from business analysis to ML.'],
                 href='/approach.html', label='See the approach'),
    sources=[
        'McKinsey Global Institute (2017). <a href="https://www.mckinsey.com/capabilities/operations/our-insights/reinventing-construction-through-a-productivity-revolution">Reinventing construction: a route to higher productivity</a>.',
        'Goolsbee, A. and Syverson, C. (2023). <a href="https://www.nber.org/papers/w30845">The strange and awful path of productivity in the U.S. construction sector</a>. NBER Working Paper 30845.',
        'Garcia, D. and Molloy, R. (2023, revised 2025). <a href="https://www.federalreserve.gov/econres/feds/files/2023052r1pap.pdf">Reexamining lackluster productivity growth in construction</a>. Finance and Economics Discussion Series 2023-052, Federal Reserve Board.',
        'Sveikauskas, L., Rowe, S., Mildenberger, J., Price, J. and Young, A. (2016). <a href="https://ascelibrary.org/doi/10.1061/%28ASCE%29CO.1943-7862.0001138">Productivity growth in construction</a>. Journal of Construction Engineering and Management, 142(10).',
        'U.S. Bureau of Labor Statistics. <a href="https://www.bls.gov/productivity/highlights/construction-labor-productivity.htm">Construction labor productivity</a> (productivity highlights).',
        'U.S. Bureau of Labor Statistics (2022). <a href="https://www.bls.gov/opub/ted/2022/labor-productivity-rose-in-single-and-multi-family-residential-construction-during-pandemic.htm">Labor productivity rose in single- and multi-family residential construction during pandemic</a>. The Economics Daily.',
        'McKinsey & Company (2020). <a href="https://www.mckinsey.com/~/media/McKinsey/Industries/Capital%20Projects%20and%20Infrastructure/Our%20Insights/The%20next%20normal%20in%20construction/The-next-normal-in-construction.pdf">The next normal in construction</a>.',
    ],
    next=['insight-permit-wait-times', 'insight-rework-bad-data'],
)

POSTS = [FORECAST, REWORK, PRODUCTIVITY]
