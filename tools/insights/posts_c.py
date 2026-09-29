from build import c, bars, table, pull, callout, checklist

DATE, DATE_LABEL = '2026-09-29', 'Sept 2026'

LLM = dict(
    slug='insight-llms-construction-documents', topic='AI & automation', topics='ai safety',
    title='LLMs on construction documents: what the evidence says about accuracy',
    dek='Language models read contracts, specifications and incident reports fluently. Peer-reviewed research on the closest comparable field, legal documents, shows how often fluent is not the same as right, and which designs reduce the risk.',
    meta='What peer-reviewed research says about LLM hallucination on legal documents, what it implies for construction contracts and reports, and how to design and test AI tools that stay accurate.',
    blurb='Research on legal documents found hallucination rates from 17% to 88%. Bounded tasks, retrieval, refusal and testing are the defence.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('69–88%', 'hallucination rates of general-purpose LLMs on verifiable questions about real court cases', 1),
          ('17–33%', 'hallucination rates of commercial legal AI research tools built with retrieval (RAG)', 2),
          ('89%', 'accuracy where a trained model and an LLM agreed on OSHA injury coding (my analysis, real data)', 4)],
    takeaways=[
        'On verifiable questions about real court cases, general-purpose LLMs hallucinated <strong>69% to 88%</strong> of the time in a peer-reviewed Stanford study.',
        'Commercial legal research tools built with retrieval still hallucinated <strong>17% to 33%</strong> of the time. Retrieval reduces the problem; it does not remove it.',
        'The National Institute of Standards and Technology (NIST) lists <strong>confabulation</strong> as a core risk of generative AI.',
        'Accuracy improves sharply when the task is bounded, answers are grounded in cited source text, the system can decline, and a second method checks the first.',
        'Every AI tool on project documents needs an evaluation set drawn from your own documents before anyone relies on it.',
    ],
    sections=[
        ('why-legal-research', 'Why legal research is the right benchmark', f'''
<p>Construction runs on documents: contracts and their clauses, specifications, RFIs, submittals, method statements, incident reports, minutes. The obvious AI use case is to ask a model questions about them. The obvious risk is that it answers confidently and wrongly.</p>
<p>There is little peer-reviewed research on LLM accuracy with construction documents specifically. The closest well-studied field is law: long, precise texts where a wrong answer has real consequences and where answers can be checked against a source. Two studies from Stanford’s RegLab are the most rigorous evidence so far.</p>
'''),
        ('what-studies-found', 'What the studies found', f'''
<p><strong>General-purpose models.</strong> Matthew Dahl and colleagues asked widely used LLMs verifiable questions about real court cases, questions with a checkable right answer such as who wrote an opinion or what a case held. Hallucination rates ranged from <strong>69% for GPT-3.5 to 88% for Llama 2</strong>. Models also tended to accept false premises in the question, and were poor at judging their own confidence{c(1)}.</p>
<p><strong>Specialist tools with retrieval.</strong> Vendors responded that retrieval-augmented generation (RAG), which fetches relevant source documents and asks the model to answer from them, solves the problem. Varun Magesh and colleagues ran the first preregistered test of leading legal AI research tools from LexisNexis and Thomson Reuters. They hallucinated between <strong>17% and 33%</strong> of the time{c(2)}.</p>
{bars('Share of answers containing a hallucination, by system type', [
    ('General-purpose LLM, best case (GPT-3.5)', 69, '69%', False), ('General-purpose LLM, worst case (Llama 2)', 88, '88%', False),
    ('Legal RAG tools, best case', 17, '17%', True), ('Legal RAG tools, worst case', 33, '33%', True)],
    'Sources: Dahl et al. (2024) [1]; Magesh et al. (2025) [2]. Different question sets, so compare the ranges rather than individual bars.', max_value=100)}
<p>Retrieval helps a lot, but a one-in-six to one-in-three error rate is not something you would accept from a quantity surveyor or a contracts manager. NIST’s Generative AI Profile of its AI Risk Management Framework names <strong>confabulation</strong> (confidently stated false content) as one of twelve core generative-AI risks{c(3)}.</p>
{pull('Retrieval reduces hallucination. It does not remove it.')}
'''),
        ('what-reduces-error', 'Designs that reduce the error', f'''
<p>The studies above tested open-ended questions. Accuracy is very different when the system is designed around a narrow, checkable task. Five design choices matter most:</p>
<ol>
<li><strong>Bound the task.</strong> “Classify this incident narrative into one of nine causes” or “find the liquidated-damages clause” is far more reliable than “summarise the risks in this contract”.</li>
<li><strong>Ground every answer in source text.</strong> Show the clause, record or paragraph the answer came from, so a person can check it in seconds.</li>
<li><strong>Calculate with code, not with the model.</strong> Totals, counts and dates should come from a database query the user can see, not from generated text.</li>
<li><strong>Let it decline.</strong> A system that says “the data doesn’t answer that” is more useful than one that always answers.</li>
<li><strong>Use two readers.</strong> Where two independent methods agree, confidence is higher; where they disagree, send it to a person.</li>
</ol>
'''),
        ('my-tests', 'What this looked like in my own tests', f'''
<p>I have applied these principles in two projects, and the results show how much the design matters{c(4)}{c(5)}.</p>
{table(['Test', 'Data', 'Result'], [
    ['LLM coding injury causes, no training, definitions only', 'Real OSHA reports, 3,204 test cases', '81.4% vs 83.8% for a model trained on 14,000 reports'],
    ['Trained model and LLM agree → auto-code', 'Same', '89.1% correct, covering 85% of reports'],
    ['LLM extracting fall height from narratives', 'Same', 'Band matches OSHA in 98.5% of cases where it gives one'],
    ['ERP chatbot: record lookups via retrieval', 'Synthetic ERP data, reworded questions', '100% correct'],
    ['ERP chatbot: totals via parameterised SQL', 'Same', '85.0% correct'],
    ['ERP chatbot: declining unanswerable questions', 'Same', '100% declined'],
    ['ERP chatbot: end to end', 'Same', '94.8% correct']],
    'Sources: [4][5]. The OSHA tests use real public data; the ERP tests use synthetic data and template questions, so real users will phrase things more freely.')}
<p>The pattern is consistent with the research. Open-ended generation is where errors live. Classification against fixed definitions, extraction of a specific fact, retrieval of an exact record and calculation by query are where these tools become dependable, and where they can be tested properly. The whole OSHA run, 3,204 reports twice, cost under $1.20 at list price, so the barrier is evaluation effort, not model cost.</p>
'''),
        ('what-to-do', 'Before you rely on an AI document tool', checklist([
            '<strong>Write down the task in one sentence.</strong> If you can’t, it is too open-ended to trust.',
            '<strong>Build an evaluation set from your own documents</strong>: 100–300 questions with answers checked by a person, including questions that should be declined.',
            '<strong>Measure against a simple baseline,</strong> such as keyword search or a checklist, not against nothing.',
            '<strong>Require citations to source text</strong> for every answer, and spot-check them.',
            '<strong>Keep calculations out of the model.</strong> Totals and dates come from queries the user can see.',
            '<strong>Route disagreement and low confidence to a person,</strong> and track the error rate monthly after go-live.',
        ])),
    ],
    applied=dict(title='Construction ERP Intelligence Copilot',
                 text=['A chatbot over ERP data that retrieves exact records, calculates totals with visible SQL and declines what the data can’t answer: 94.8% correct end to end on reworded questions. Built on synthetic ERP data.'],
                 href='/projects.html', label='See the project'),
    sources=[
        'Dahl, M., Magesh, V., Suzgun, M. and Ho, D. E. (2024). <a href="https://academic.oup.com/jla/article/16/1/64/7699227">Large legal fictions: profiling legal hallucinations in large language models</a>. Journal of Legal Analysis, 16(1), 64–93.',
        'Magesh, V., Surani, F., Dahl, M., Suzgun, M., Manning, C. D. and Ho, D. E. (2025). <a href="https://onlinelibrary.wiley.com/doi/full/10.1111/jels.12413">Hallucination-free? Assessing the reliability of leading AI legal research tools</a>. Journal of Empirical Legal Studies.',
        'NIST (2024). <a href="https://airc.nist.gov/docs/NIST.AI.600-1.GenAI-Profile.ipd.pdf">Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)</a>.',
        'Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects/14-construction-safety-intelligence">Construction Safety Intelligence</a>: LLM versus trained model on OSHA reports. GitHub.',
        'Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects/02-erp-intelligence-copilot">Construction ERP Intelligence Copilot</a>: retrieval, text-to-SQL and guardrails evaluation. GitHub.',
    ],
    next=['insight-osha-severe-injuries', 'insight-payroll-fraud'],
)

PAYROLL = dict(
    slug='insight-payroll-fraud', topic='Workforce & finance', topics='commercial ai',
    title='Payroll leakage on construction sites: what the fraud research says, and how to find it',
    dek='Occupational fraud typically runs for a year before anyone notices, and most of it is found by a tip, not a control. Site labour payroll, with its contractors, crews and manual attendance, is where the patterns hide.',
    meta='What the ACFE’s 2024 Report to the Nations says about occupational fraud, why construction site payroll is exposed, and how peer-relative anomaly detection finds ghost workers and padded overtime.',
    blurb='Frauds typically run 12 months before detection. How peer-relative anomaly detection finds ghost workers and padded overtime.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('5%', 'of revenue: the share organisations lose to fraud each year, as estimated by the ACFE', 1),
          ('12 mo', 'the typical duration of an occupational fraud before it was detected', 1),
          ('43%', 'of frauds were first detected by a tip, more than three times any other method', 1)],
    takeaways=[
        'The ACFE’s 2024 study of <strong>1,921 cases</strong> in 138 countries found a median loss of <strong>$145,000</strong> per case, with total losses above $3.1bn.',
        'The typical fraud ran about <strong>12 months</strong> before detection, and <strong>43%</strong> were first found by a tip, more than half of them from employees.',
        'Construction site labour is exposed: labour contractors, large crews, manual attendance, overtime and frequent rate changes.',
        'Fixed audit rules miss context. Comparing each wage line with its site, its crew and the worker’s own history separates a concrete-pour weekend from padded overtime.',
        'In my synthetic-data test, an Isolation Forest found <strong>73%</strong> of seeded issues by reviewing 5% of lines, against 41% for audit rules.',
    ],
    sections=[
        ('the-research', 'What the fraud research says', f'''
<p>The Association of Certified Fraud Examiners publishes the largest regular study of occupational fraud: fraud committed by people against the organisations that employ them. Its 2024 <em>Report to the Nations</em> analysed <strong>1,921 cases from 138 countries and territories</strong>, with total losses of more than <strong>$3.1bn</strong>{c(1)}.</p>
<ul>
<li>The <strong>median loss</strong> per case was <strong>$145,000</strong>.</li>
<li>The ACFE estimates that organisations lose about <strong>5% of revenue</strong> to fraud each year.</li>
<li>A typical fraud lasted about <strong>12 months</strong> before it was detected.</li>
<li><strong>43%</strong> of frauds were first detected by a tip, and frauds were at least three times more likely to be found by a tip than by any other method. More than half of those tips came from employees.</li>
</ul>
{pull('A typical fraud runs for a year, and it is more often found by a tip than by a control.')}
<p>The last two numbers matter most for controls. If routine checks were catching fraud early, tips would not dominate and frauds would not last a year. The implication is that many organisations’ detective controls are not looking in the right way.</p>
'''),
        ('why-site-payroll', 'Why site labour payroll is exposed', f'''
<p>Staff payroll in a head office is relatively easy to control. Site labour payroll is not. On many construction projects, especially where labour is supplied by labour contractors, the payroll combines:</p>
<ul>
<li>large crews that change week to week;</li>
<li>attendance recorded partly by biometric devices and partly by hand;</li>
<li>overtime and Sunday work that is legitimately heavy around concrete pours and deadlines;</li>
<li>rates that are revised on a schedule, and sometimes outside it;</li>
<li>approvals by site staff who are also under pressure to keep the job moving.</li>
</ul>
<p>The typical leakage patterns follow from that: <strong>ghost workers</strong> on the roll, <strong>proxy attendance</strong>, <strong>padded overtime</strong>, <strong>unauthorised rate increases</strong> and <strong>wages paid after a worker has left</strong>. Each one looks normal as a single line. It only looks wrong in context.</p>
'''),
        ('why-rules-miss', 'Why fixed audit rules miss it', f'''
<p>The usual first control is a checklist of rules: flag overtime above a threshold, flag manual attendance, flag rate changes. Rules are transparent, but they have two weaknesses on site payroll. They fire constantly in legitimate situations (a whole crew working a Sunday pour will trip every overtime rule), and people who know the rules can stay just inside them.</p>
<p>Unsupervised anomaly detection takes a different approach. Instead of fixed thresholds, it asks how unusual each line is compared with similar lines. The <strong>Isolation Forest</strong>, introduced by Liu, Ting and Zhou in 2008, works by randomly partitioning the data; unusual records get isolated in fewer splits than normal ones, which gives a simple anomaly score with no need for labelled examples of fraud{c(2)}.</p>
{callout('Context is the feature', 'The method matters less than what you compare each line with. A worker’s overtime compared with their own crew on the same site that month, their attendance compared with their site, their rate compared with the same trade across sites and with their own history: these peer-relative features are what separate a genuine concrete-pour weekend from padding.')}
'''),
        ('what-my-test-showed', 'What my test showed', f'''
<p>I built a synthetic site-labour payroll of 12,397 monthly wage lines over a year, with realistic seasonality (festival absences, monsoon slowdowns, April wage revisions, weekend pours, biometric device failures) and seeded leakage patterns. I compared a seven-rule audit checklist with several anomaly detectors, measuring what an auditor would find by reviewing only the top 5% of lines each month{c(3)}.</p>
{bars('Share of seeded payroll issues found by reviewing the top 5% of lines', [
    ('Random review', 5, '5%', False), ('Audit rules (count of rules hit)', 41, '41%', False),
    ('Isolation Forest, peer-relative features', 73, '73%', True)],
    'Recall at a 5% monthly review budget. Synthetic data with seeded issues; source: [3].', max_value=100)}
<p>By type, the Isolation Forest caught 100% of pay after exit, 87% of rate increases, 85% of ghost workers and 74% of padded overtime, but only <strong>8% of proxy attendance</strong>. That last number is the honest limit: when one worker signs in for another, the wage line itself can look perfectly normal. Some fraud needs a physical control, such as a headcount on site, not a better model.</p>
<p>The most useful output was not the list of lines but the pattern behind them. Three labour contractors were flagged at more than twice the average rate, and they were exactly the three that had placed ghost workers; two approvers accounted for every mid-year rate increase. That turns an anomaly list into a control finding.</p>
'''),
        ('what-to-do', 'Controls worth putting in place', checklist([
            '<strong>Reconcile headcount physically,</strong> with periodic unannounced roll calls against the payroll, especially for labour-contractor crews.',
            '<strong>Compare each line with its peers</strong> (site, crew, trade, own history) rather than only with fixed thresholds.',
            '<strong>Review a fixed budget of the riskiest lines each month</strong> and record the outcome, so the ranking improves over time.',
            '<strong>Aggregate findings by contractor and approver.</strong> Patterns across lines reveal the control weakness.',
            '<strong>Lock rate changes to the revision calendar</strong> and require a second approver outside it.',
            '<strong>Make tipping-off easy and safe.</strong> Tips remain the most common detection method; a hotline workers trust is a control.',
        ])),
    ],
    applied=dict(title='Construction Payroll',
                 text=['Pre-release payroll checks for staff timesheets, plus an unsupervised model for site-labour wage lines: 73% of seeded issues found by reviewing 5% of lines, with findings rolled up by contractor and approver. Built on synthetic data patterned on real site payroll.'],
                 href='/projects.html', label='See the project'),
    sources=[
        'Association of Certified Fraud Examiners (2024). <a href="https://www.acfe.com/-/media/files/acfe/pdfs/rttn/2024/2024-report-to-the-nations.pdf">Occupational Fraud 2024: A Report to the Nations</a>.',
        'Liu, F. T., Ting, K. M. and Zhou, Z.-H. (2008). <a href="https://www.semanticscholar.org/paper/Isolation-Forest-Liu-Ting/00a1077d298f2917d764eb729ab1bc86af3bd241">Isolation forest</a>. Proceedings of the 8th IEEE International Conference on Data Mining (ICDM).',
        'Iwale, A. (2026). <a href="https://github.com/AtulIwale/Portfolio/tree/main/projects/04-construction-payroll">Construction Payroll</a>: site-labour anomaly detection on synthetic data. GitHub.',
    ],
    next=['insight-llms-construction-documents', 'insight-material-price-escalation'],
)

ESCALATION = dict(
    slug='insight-material-price-escalation', topic='Commercial', topics='commercial controls',
    title='Material price shocks and escalation: building estimates that survive volatility',
    dek='In the 2020–21 price shock, lumber prices more than doubled and steel rose by three-quarters within a year, while contractors’ bid prices barely moved. What the price data shows, how escalation clauses share the risk, how to estimate with it, and a case study on late deliveries.',
    meta='Construction material price volatility (BLS and AGC data), how FIDIC and CPWD escalation clauses work, and how to rebase and index costs in estimates and models.',
    blurb='Lumber prices more than doubled in a year while bid prices barely moved. What the data shows and how escalation clauses share the risk.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('+24.3%', 'rise in producer prices for construction inputs over the 12 months to May 2021', 2),
          ('+111%', 'lumber and plywood producer prices over the same period', 2),
          ('−29%', 'softwood lumber prices in the single month of July 2021, after the spike', 1)],
    takeaways=[
        'Material prices can move far faster than contract prices. Over 12 months to May 2021, construction input prices rose <strong>24.3%</strong>, lumber and plywood <strong>111%</strong> and steel mill products <strong>75.6%</strong>.',
        'Volatility runs both ways: softwood lumber prices fell <strong>29%</strong> in one month in July 2021.',
        'Contractors carrying fixed prices absorbed the gap, because bid prices moved far less than input costs.',
        'Escalation clauses such as <strong>FIDIC Sub-Clause 13.7</strong> and India’s <strong>CPWD clauses 10CA and 10CC</strong> share the risk using published indices and fixed weights.',
        'Estimates and cost models need prices rebased to a common date with a weighted index, or inflation will be mistaken for overrun.',
    ],
    sections=[
        ('the-shock', 'The 2020–2021 price shock', f'''
<p>The pandemic years gave a clear demonstration of how fast construction input prices can move. Official producer price data show it clearly: prices for lumber rose <strong>89.7%</strong> in the year to April 2021, with softwood lumber up <strong>121.1%</strong>{c(1)}. A contractors’ association (AGC), analysing the same producer price data, reported that prices for construction inputs rose <strong>24.3%</strong> over the 12 months to May 2021, nearly twice the largest annual increase previously recorded, with steep rises across materials{c(2)}:</p>
{bars('Change in producer prices over the 12 months to May 2021', [
    ('All construction inputs', 24.3, '+24.3%', True), ('Aluminium mill shapes', 28.6, '+28.6%', False),
    ('Copper and brass mill shapes', 60.4, '+60.4%', False), ('Steel mill products', 75.6, '+75.6%', False),
    ('Lumber and plywood', 111, '+111%', False)],
    'Source: AGC analysis of BLS producer price indices [2].')}
<p>The problem for contractors was the gap. AGC noted that input costs far outstripped what contractors could charge: bid prices for nonresidential buildings moved very little while material costs climbed{c(2)}. On a fixed-price contract, that gap comes straight out of margin.</p>
'''),
        ('both-ways', 'Volatility runs both ways', f'''
<p>Price shocks are not one-way escalators. Having more than doubled, softwood lumber prices fell <strong>29% in the single month of July 2021</strong>{c(1)}. For an estimator, that means the risk is not only “prices will rise” but “prices will be different from the estimate, in either direction, by more than the contingency assumes”.</p>
{pull('The risk is not only that prices will rise, but that they will be different from the estimate by more than the contingency assumes.')}
<p>It also means that an escalation mechanism should work in both directions. A clause that only pays out on rises is a one-sided bet, and owners know it.</p>
'''),
        ('how-clauses-share-risk', 'How escalation clauses share the risk', f'''
<p>Standard-form contracts handle this with price adjustment formulas: the contract value is split into weighted components (labour, specific materials, fuel, a fixed non-adjustable part), and each component is adjusted by the movement of a named published index between the base date and the date the work is valued.</p>
<h3>FIDIC</h3>
<p>In the 2017 FIDIC Red and Yellow Books, <strong>Sub-Clause 13.7, Adjustments for Changes in Cost</strong>, is opt-in: it applies only if the contract includes a Schedule of cost indexation. Where it does, the amounts payable are adjusted for rises or falls in the cost of labour, goods and other inputs by the formula in that schedule, and the schedule is a complete statement of the adjustment; any other cost movements are deemed included in the contract price{c(3)}.</p>
<h3>Public works conditions: a two-part example</h3>
<p>Some public works conditions split escalation in two. India’s CPWD conditions are a clear example. <strong>Clause 10CA</strong> covers price variation for specified key materials such as cement and reinforcement steel against base prices. <strong>Clause 10CC</strong> covers the rest (labour, other materials and fuel) with a component formula of the form{c(4)}:</p>
{callout('Clause 10CC component formula', '<strong>V = W × (Y ÷ 100) × (Q − Q<sub>0</sub>) ÷ Q<sub>0</sub></strong>', 'where W is the value of work done in the period, Y the percentage weight of the component, Q<sub>0</sub> the index at the base date and Q the index for the period.')}
<p>Both approaches share the same logic: fix the weights and the indices when the contract is signed, so that later adjustment is arithmetic, not negotiation.</p>
'''),
        ('estimating-with-indices', 'Estimating and modelling with indices', f'''
<p>The same idea matters inside an estimating team. Historical cost data is priced in the year each project was built. Compare a 2019 project with a 2024 project without adjustment and inflation looks like a difference in design or performance. The standard remedy is to <strong>rebase</strong> every project to a common base date with a composite index weighted to the cost structure of the work.</p>
<p>It matters even more for machine learning. Tree-based models such as random forests and gradient boosting cannot extrapolate beyond the range of prices they were trained on, so a model trained on older, cheaper years will systematically under-estimate new projects. Rebasing to a common date, training in constant prices and re-inflating the forecast to today with the current index solves both problems.</p>
{callout('A worked weighting', 'In my Cost Plan Estimation project, costs are rebased to January 2018 prices with a composite index weighted 25% steel, 20% cement, 40% labour and 15% other, the way a quantity surveyor compares projects across years. The weights should reflect your own cost breakdown by building type.')}
'''),
        ('what-to-do', 'What to put in place', checklist([
            '<strong>Know your exposure.</strong> Break the estimate into index-able components and identify the few materials that carry most of the price risk.',
            '<strong>Name the indices in the contract.</strong> Use published, independent indices and fix the base date and weights at signing.',
            '<strong>Make adjustment symmetric,</strong> so it works for falls as well as rises.',
            '<strong>Lock prices where you can,</strong> with early purchase or supplier agreements for the most volatile items, and weigh that against holding cost.',
            '<strong>Rebase historical data</strong> before benchmarking or training any model, and re-inflate forecasts with the current index.',
            '<strong>Track actual versus index monthly</strong> during the job, so escalation claims and forecasts use the same numbers.',
        ])),
    ],
    applied=dict(title='Cost Plan Estimation (ML)',
                 text=['A feasibility-stage estimator that rebases every project to January 2018 prices before training, and is tested on later projects than it learned from: 6.6% average error against 11.2% for the coefficient method. Built on synthetic data patterned on Indian cost plans.'],
                 href='https://atuliwale.github.io/Portfolio/projects/13-cost-plan-estimation/', label='Open the live app'),
    sources=[
        'U.S. Bureau of Labor Statistics (2021). <a href="https://www.bls.gov/opub/ted/2021/producer-prices-for-lumber-up-89-7-percent-for-the-year-ended-april-2021.htm">Producer prices for lumber up 89.7 percent for the year ended April 2021</a>. The Economics Daily.',
        'Associated General Contractors of America (2021). <a href="https://www.agc.org/news/2021/06/15/producer-prices-construction-materials-and-services-jump-24-percent-over-12-months">Producer prices for construction materials and services jump 24 percent over 12 months</a>.',
        'Fenwick Elliott. <a href="https://www.fenwickelliott.com/research-insight/newsletters/international-quarterly/inflation-adjustment-changes-cost-fidic-books">Inflation and adjustment for changes in cost in the FIDIC Red and Yellow Books</a>.',
        'Central Public Works Department (India). Clauses 10CA and 10CC, General Conditions of Contract; summary in <a href="https://iohlaw.com/article.php?id=18">Analysis of clause 10CC, CPWD contracts</a>.',
    ],
    next=['insight-cost-estimates-miss', 'insight-forecasting-final-cost'],
)

POSTS = [LLM, PAYROLL, ESCALATION]
