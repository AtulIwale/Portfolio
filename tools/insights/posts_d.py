from build import c, bars, table, pull, callout, checklist

DATE, DATE_LABEL = '2026-09-29', 'Sept 2026'
GH = 'https://github.com/AtulIwale/Portfolio/tree/main/projects/'

CONTRACTS = dict(
    slug='insight-contract-clause-risk', topic='Contracts', topics='commercial ai',
    title='Reading contract risk from the wording: what a neural network catches, and what it can’t',
    dek='Contract value leaks through clauses nobody read closely enough, and construction disputes now run to tens of millions of dollars. A model that reads clause wording can put the riskiest clauses in front of a reviewer first, if it is built and tested with care.',
    meta='The cost of poor contract management and construction disputes, and how a text model that reads clause wording can prioritise legal review. Tested on synthetic construction contracts.',
    blurb='Poor contracting erodes about 8.6% of value. How a CNN that reads clause wording caught 95% of high-risk clauses, and where human reviewers disagree.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('8.6%', 'average value erosion from poor contracting, per World Commerce & Contracting', 1),
          ('14.4 mo', 'average length of a construction dispute in North America, per Arcadis’s 2024 report', 2),
          ('95%', 'of high-risk clauses caught by a CNN reading the wording (synthetic data), against a 0.38 macro-F1 keyword list', 3)],
    takeaways=[
        'World Commerce & Contracting estimates poor contracting erodes <strong>8.6%</strong> of expected value on average, and 15% or more in complex industries.',
        'In North America, Arcadis reports construction disputes averaging <strong>$43m</strong> and lasting <strong>14.4 months</strong>; errors and omissions in contract documents are the top cause.',
        'Risk lives in word order: “within 30 days” versus “within 120 days”, “shall be limited” versus “shall not be limited”. Keyword lists miss it.',
        'On synthetic construction contracts, a 1D-CNN caught <strong>95%</strong> of reviewer-rated high-risk clauses at 85% precision.',
        'Agreement with individual reviewers ranged from <strong>85% to 89%</strong>, and one reviewer rated borderline clauses High more often: part of any model’s “error” is human disagreement.',
    ],
    sections=[
        ('why-it-matters', 'What poor contracting costs', f'''
<p>World Commerce & Contracting (WorldCC), the international association for contracting professionals, has measured the gap between what contracts are expected to deliver and what they actually deliver for more than a decade. Its research puts average <strong>value erosion at 8.6%</strong>, often 15% or more in complex industries, down only slightly from 9.2% when it was first measured in 2014{c(1)}. Construction is one of those complex industries.</p>
<p>When erosion turns into a dispute, the numbers get larger. Arcadis’s 2024 Construction Disputes Report found that the average dispute in North America was worth about <strong>$43 million</strong> and took about <strong>14.4 months</strong> to resolve. The most common cause was <strong>errors and omissions in the contract document</strong>, followed by parties failing to understand or comply with their contractual obligations{c(2)}.</p>
{pull('The most common cause of construction disputes is not the site. It is the contract document.')}
'''),
        ('where-risk-hides', 'Where the risk hides in a construction contract', f'''
<p>The clauses that cause trouble are rarely hidden. They are simply long, numerous and similar enough that a tired reviewer reads what they expect to read. In construction and supply contracts, the recurring high-risk patterns include{c(3)}:</p>
<ul>
<li><strong>Unlimited liability</strong>: “shall not be limited” where the template said “shall be limited to”.</li>
<li><strong>Pay-when-paid</strong>: the subcontractor is paid only when the main contractor is, passing the client’s payment risk down the chain.</li>
<li><strong>Long payment terms</strong>: 90 or 120 days instead of 30, which quietly finances the other party.</li>
<li><strong>Auto-renewal with long notice periods</strong>: a contract that renews itself unless cancelled 120 days before expiry, reviewed 90 days before.</li>
<li><strong>Retention and escalation terms</strong> that differ from the commercial assumption in the estimate.</li>
</ul>
<p>Notice that the risk is in the <strong>wording and word order</strong>, not in the presence of a keyword. “Limited” appears in both the safe and the dangerous version of a liability clause.</p>
'''),
        ('what-the-model-does', 'Teaching a model to read the wording', f'''
<p>The project started as a rules engine: flag clauses whose risk category is already High, and flag auto-renewing contracts expiring within 90 days. That works, but it relies on someone having already rated every clause, which is the expensive part{c(3)}.</p>
<p>Version 2 rates clauses from their text. It learns from a library of <strong>1,300 historical contracts and 6,539 clauses</strong>, each rated Low, Medium or High by one of six legal reviewers, and is tested on 800 later clauses it never saw. Seven methods were compared, from a keyword checklist to neural networks:</p>
{bars('Macro-F1 on 800 unseen clauses (higher is better)', [
    ('Keyword rules (baseline)', 0.379, '0.38', False), ('Naive Bayes', 0.599, '0.60', False),
    ('Linear SVM', 0.845, '0.85', False), ('Logistic regression', 0.858, '0.86', False),
    ('BiLSTM', 0.912, '0.91', False), ('MLP neural network', 0.917, '0.92', False),
    ('1D-CNN (in the app)', 0.942, '0.94', True)],
    'Synthetic clauses patterned on Indian construction contracts [3].', max_value=1)}
<p>The convolutional network won because it detects short phrases in order, exactly where the risk lives. It caught <strong>95% of High-risk clauses with 85% precision</strong>. Because a missed High clause costs far more than an extra review, High recall was tracked separately and the decision threshold was checked with a recall-weighted measure. At contract level, the model put 52 of 200 contracts on the priority list, including all 40 that contained a reviewer-rated High clause.</p>
'''),
        ('human-disagreement', 'Part of the error is human', f'''
<p>One finding matters more than the headline score. When the models were cross-checked against individual reviewers, agreement ranged from <strong>85% to 89%</strong>, and one reviewer rated borderline clauses High more often than the others{c(3)}. Legal risk rating is a judgement, and judges differ.</p>
<p>That changes how to read any accuracy figure. A model cannot be more consistent than the labels it learns from, and some of what looks like model error is reviewers disagreeing with each other. In practice this argues for calibrating reviewers against each other on a shared sample before training, and for using the model as a <strong>screening and ordering aid</strong>, not a verdict.</p>
{callout('Explainability', 'The app explains each rating by blanking one word at a time and measuring how much the probability of “High” changes. A reviewer sees which words drove the rating, and can disagree with it in seconds.')}
'''),
        ('what-to-do', 'Putting clause screening to work', checklist([
            '<strong>Decide what “high risk” means</strong> in writing, with examples, before anyone rates a clause.',
            '<strong>Calibrate reviewers on a shared sample</strong> and measure their agreement; that sets the ceiling for any model.',
            '<strong>Track recall on high-risk clauses separately.</strong> A missed unlimited-liability clause is not the same as a false alarm.',
            '<strong>Pull notice periods and payment terms into a register</strong> with dates, so renewals and deadlines are diarised, not remembered.',
            '<strong>Test on your own reviewed clauses</strong> before relying on any model; synthetic or vendor accuracy does not transfer.',
            '<strong>Keep a person in the loop.</strong> Use the model to order the review queue and highlight wording, not to approve contracts.',
        ])),
    ],
    applied=dict(title='Contract Lifecycle Intelligence',
                 text=['A review worklist of high-risk clauses and upcoming auto-renewals, plus a Clause Risk Reader that rates new clauses from their wording, highlights the words that drove the rating and extracts payment days, notice periods and retention. Built on synthetic contracts patterned on Indian construction contracts.'],
                 href='https://atuliwale.github.io/Portfolio/projects/05-contract-lifecycle-intelligence/ml.html', label='Open the Clause Risk Reader'),
    sources=[
        'World Commerce & Contracting. <a href="https://www.worldcc.com/resource/Poor-Contract-Management-Continues-To-Costs-Companies-9-Of-Their-Bottom-Line.html">Poor contract management continues to cost companies 9% of their bottom line</a>.',
        'Arcadis (2024). <a href="https://www.arcadis.com/en-us/insights/blog/united-states/benjamin-eiss/2024/disputes-in-the-digital-age-findings-of-the-2024-construction-disputes-report">Disputes in the digital age: findings of the 2024 Construction Disputes Report</a>.',
        f'Iwale, A. (2026). <a href="{GH}05-contract-lifecycle-intelligence">Contract Lifecycle Intelligence</a>, including the clause-risk NLP upgrade. GitHub.',
    ],
    next=['insight-llms-construction-documents', 'insight-construction-payments'],
)

PAYMENTS = dict(
    slug='insight-construction-payments', topic='Receivables & payables', topics='commercial',
    title='Getting paid in construction: payment delays, the MSME rules and evidence you can act on',
    dek='Cash, not profit, is what sinks contractors, and construction has some of the slowest payment cycles of any industry. What the data and Indian law say about late payment, and why a collections worklist should keep confirmed risk and suspicion apart.',
    meta='Construction payment delays, India’s MSMED Act rules on paying small suppliers within 45 days, and how to build receivables and payables worklists that separate confirmed risk from patterns.',
    blurb='US construction payment cycles average about 90 days; Indian law caps MSME supplier terms at 45. How to build AR/AP worklists that separate evidence from suspicion.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('~90 days', 'average payment cycle in US construction, per Rabbet’s 2024 payments report', 1),
          ('45 days', 'the longest a buyer may take to pay an Indian micro or small supplier (MSMED Act, s.15)', 2),
          ('3×', 'the RBI bank rate: compound interest owed on late payments to those suppliers (s.16)', 2)],
    takeaways=[
        'Rabbet’s 2024 report estimates the average US construction payment cycle at about <strong>90 days</strong> and the cost of slow payment at <strong>$280bn</strong> a year.',
        'In India, buyers must pay micro and small suppliers within the agreed term and <strong>never later than 45 days</strong>; late payment attracts compound interest at <strong>three times the RBI bank rate</strong>, whatever the contract says.',
        'Receivables and payables are two sides of the same cash problem, but they should never be netted in a review list.',
        'A worklist should keep <strong>confirmed settlement risk</strong> separate from <strong>patterns worth a look</strong>. Blending them into one score hides what is actually known.',
        'Predicting who will pay late needs point-in-time data and a time-based test; a snapshot of today’s statuses is not a forecast.',
    ],
    sections=[
        ('the-cash-problem', 'The cash problem', f'''
<p>A contractor pays for labour, materials and plant weeks or months before being paid for the work. The gap is financed from cash reserves, overdrafts or suppliers’ patience. When payment is slow, profitable firms can still fail.</p>
<p>Rabbet’s 2024 Construction Payments Report, a survey of US construction firms by a construction-finance software company, estimated the average payment cycle at about <strong>90 days</strong> and put the industry-wide cost of slow payment at about <strong>$280 billion</strong> in 2024{c(1)}. As a vendor survey, its exact figures deserve caution; the direction matches what anyone who has run a project’s cash flow will recognise.</p>
{pull('Profitable contractors still fail when cash arrives three months after the work.')}
'''),
        ('the-law-in-india', 'What Indian law says about paying small suppliers', f'''
<p>India’s Micro, Small and Medium Enterprises Development (MSMED) Act, 2006 sets hard limits on how long a buyer may take to pay a registered micro or small enterprise{c(2)}:</p>
<ul>
<li><strong>Section 15:</strong> pay within the agreed period, and in any case within <strong>45 days</strong> of accepting the goods or services. Where there is no agreed period, the limit is 15 days.</li>
<li><strong>Section 16:</strong> if payment is late, the buyer owes <strong>compound interest with monthly rests at three times the bank rate</strong> notified by the Reserve Bank of India. This rate applies notwithstanding any agreement to the contrary.</li>
</ul>
<p>For a main contractor, many subcontractors and material suppliers fall within this Act. That turns the payables ledger into a compliance register: an invoice from a registered small supplier that is 60 days old is not just slow, it is accruing statutory interest.</p>
{callout('Practical implication', 'Flag every vendor’s MSME registration status in the vendor master. Without it, no report can tell which late payables carry statutory interest.')}
'''),
        ('evidence-not-scores', 'Evidence, not a blended score', f'''
<p>The tempting design for a collections tool is one “risk score” per invoice. My Accounts Receivable &amp; Payable project deliberately avoids that, because the invoices in a review list do not all carry the same kind of evidence{c(3)}:</p>
{bars('Unpaid invoices by worklist (1,000 invoices, 110 unpaid)', [
    ('Confirmed settlement risk: receivables', 12, '12', True), ('Confirmed settlement risk: payables', 10, '10', True),
    ('Repeat-pattern review: receivables', 88, '88', False)],
    'Synthetic data patterned on ERP structures [3]. The two worklists do not overlap.')}
<ul>
<li><strong>Confirmed settlement risk</strong> is an invoice already labelled as a settlement problem: unpaid and overdue or disputed.</li>
<li><strong>Repeat-pattern review</strong> is an unpaid invoice from a party that has at least two unsettled invoices. It is worth a look, but it is a pattern, not a finding.</li>
</ul>
<p>Keeping these apart means a collections team knows which calls are about a confirmed problem and which are about a customer’s behaviour. Receivables and payables are shown in separate views and never netted, because a customer who owes you money and a vendor you owe are different conversations, even when they are the same company.</p>
'''),
        ('toward-prediction', 'From review to prediction', f'''
<p>The project is honest about what it is: an evidence viewer on a snapshot, not a predictive model. Its agreement with the labelled data is 100% by construction, because the confirmed category comes from the labels themselves{c(3)}. Predicting which invoices <em>will</em> be paid late is a different problem, and it needs different data:</p>
<ol>
<li><strong>Point-in-time history.</strong> For each invoice, what was known on the day it was raised: the customer’s payment record up to that date, not including later invoices.</li>
<li><strong>Features that exist on day one:</strong> amount, terms, project stage, whether the work is certified, dispute history, client type.</li>
<li><strong>A time-based test.</strong> Train on invoices raised earlier, test on invoices raised later, and compare with a simple baseline such as “customer paid late last time”.</li>
</ol>
'''),
        ('what-to-do', 'Controls for cash', checklist([
            '<strong>Record MSME status in the vendor master</strong> and report payables older than 45 days for registered suppliers.',
            '<strong>Separate confirmed issues from patterns</strong> in every collections and payables list, and label which is which.',
            '<strong>Never net receivables against payables</strong> in a review view, even for the same counterparty.',
            '<strong>Chase certification, not just invoices.</strong> Many receivables are late because the underlying work has not been certified.',
            '<strong>Keep dated history</strong> of every status change, so you can later build and test a genuine late-payment forecast.',
        ])),
    ],
    applied=dict(title='Accounts Receivable & Payable',
                 text=['An offline invoice-evidence app with separate receivables and payables views, two worklists (confirmed settlement risk and repeat-pattern review), source evidence for every invoice and category-specific exports. Built on synthetic ERP data.'],
                 href=GH + '07-accounts-receivable-payable', label='See the code and README'),
    sources=[
        'Rabbet (2024). <a href="https://rabbet.com/reports/construction-payments-2024">2024 Construction Payments Report</a>.',
        'Micro, Small and Medium Enterprises Development Act, 2006, sections 15–16. Summary in <a href="https://www.scconline.com/blog/post/2022/12/14/when-is-the-interest-rate-payable-under-section-16-of-the-msmed-act-2006-applicable/">SCC Online: when is interest payable under section 16 of the MSMED Act</a>.',
        f'Iwale, A. (2026). <a href="{GH}07-accounts-receivable-payable">Accounts Receivable &amp; Payable</a>. GitHub.',
    ],
    next=['insight-payroll-fraud', 'insight-inventory-records'],
)

INVENTORY = dict(
    slug='insight-inventory-records', topic='Inventory', topics='data commercial',
    title='Inventory records you can trust: adjustments, recorders and stale stock',
    dek='The number on the screen is rarely the number on the shelf. Research on inventory records found most of them wrong, and construction stores have more ways to go wrong than a shop. What to check, and what a clean result does and doesn’t prove.',
    meta='Research on inventory record inaccuracy, why construction stores are prone to it, and practical checks on stock adjustments, recorder concentration and stale stock.',
    blurb='A study of 370,000 inventory records found 65% inaccurate. Checks for adjustment concentration, stale stock and why “zero found” isn’t “clean”.',
    date=DATE, date_label=DATE_LABEL,
    keys=[('65%', 'of nearly 370,000 inventory records were inaccurate in a 37-store study', 1),
          ('2', 'recorders account for all 120 large negative adjustments, on three items, in my synthetic warehouse data', 2),
          ('114', 'item-warehouse positions with no movement for 90+ days in the same data', 2)],
    takeaways=[
        'In a study of nearly 370,000 records across 37 stores, DeHoratius and Raman found <strong>65%</strong> of inventory records inaccurate.',
        'Inaccuracy varied far more between product categories than between stores, and regular auditing reduced it.',
        'Construction stores add issues to work fronts, returns, inter-site transfers and unit mismatches, so they have more ways to drift.',
        '<strong>Negative adjustments</strong> are where losses are written off. Who records them, and how concentrated they are, is a key control signal.',
        'A check that finds nothing is not proof of clean stock. Without opening balances and on-hand counts, some checks cannot be run at all.',
    ],
    sections=[
        ('records-are-wrong', 'Most inventory records are wrong', f'''
<p>The best-known study of inventory record accuracy comes from retail. Nicole DeHoratius and Ananth Raman examined nearly <strong>370,000 inventory records from 37 stores</strong> of one retailer and found <strong>65% of them inaccurate</strong>: the system quantity did not match what was physically there{c(1)}.</p>
<p>Two further findings are directly useful. First, much more of the variation in accuracy lay <strong>between product categories</strong> (26.4% of the variance) than between stores (2.7%). Some kinds of items are simply harder to keep accurate. Second, <strong>auditing practices reduced inaccuracy</strong>, while complexity in the store and the distribution structure increased it{c(1)}.</p>
{pull('The number on the screen is rarely the number on the shelf.')}
'''),
        ('why-construction-is-harder', 'Why construction stores drift faster', f'''
<p>A construction site store is more complex than a shop in almost every way the research flags:</p>
<ul>
<li><strong>Issues to work fronts</strong> are often recorded after the fact, in bulk, or not at all during a pour or a deadline.</li>
<li><strong>Returns and offcuts</strong> come back in different quantities and units from what went out.</li>
<li><strong>Inter-site transfers</strong> leave one ledger before they arrive in another.</li>
<li><strong>Units differ</strong> between purchase, stock and issue: tonnes and bars, bags and cubic metres, rolls and metres.</li>
<li><strong>Adjustments</strong> are the catch-all that makes the books match the count, and the easiest place to hide a loss.</li>
</ul>
'''),
        ('what-to-check', 'What my inventory project checks', f'''
<p>My Inventory &amp; Warehouse Management project reviews 1,200 synthetic stock transactions across 80 items and 12 warehouses{c(2)}. Its central check is on <strong>adjustment concentration</strong>: large negative adjustments (50 units or more) where the same item and recorder pair repeats, and where that pair accounts for at least 40% of the item’s total negative adjustments.</p>
{table(['Check', 'Result', 'Status'], [
    ['Concentrated large negative adjustments', '120 transactions, 3 items, 2 recorders', 'Confirmed against labels'],
    ['Stock with no movement for 90+ days', '114 item-warehouse positions', 'Unscored review'],
    ['Possible duplicate transactions', '0', 'Unscored review'],
    ['Possible reversals within seven days', '0', 'Unscored review'],
    ['Below reorder level', 'Not evaluated', 'No on-hand counts supplied']],
    'Synthetic data patterned on ERP structures [2].')}
<p>The pattern it surfaces is exactly the one an auditor looks for: two recorders, each responsible for roughly half of all the large write-offs on three items. That does not prove misconduct; it says where to look first.</p>
{callout('Honest limit', 'In this synthetic data, the size of the adjustment alone reproduces every labelled case, so the concentration conditions add nothing measurable here. On real data they would matter more, but that has to be tested, not assumed.')}
'''),
        ('zero-is-not-clean', 'Why “zero found” is not “clean”', f'''
<p>Two of the checks found nothing, and one could not run. That is as informative as the positive findings:</p>
<ul>
<li><strong>Zero duplicates or reversals</strong> means none matched these particular definitions, not that the records are clean.</li>
<li><strong>Below-reorder</strong> could not be evaluated because the data had no on-hand counts or reorder points. The app asks the user to enter them rather than inventing a threshold.</li>
<li><strong>Running-balance checks</strong> were omitted entirely because there were no opening balances. Computing balances from zero would have produced negative stock that isn’t real.</li>
</ul>
<p>Reporting what could not be checked is a control in itself: it shows management exactly where the data needs to improve.</p>
'''),
        ('what-to-do', 'Controls for store records', checklist([
            '<strong>Cycle-count by category risk,</strong> not uniformly: the research shows accuracy varies most between kinds of item.',
            '<strong>Require a reason code and a second approver</strong> for adjustments above a threshold.',
            '<strong>Report adjustment concentration</strong> by item and recorder every month.',
            '<strong>Record issues at the time of issue,</strong> with the work front or cost code, not in end-of-week batches.',
            '<strong>Standardise units</strong> between purchase, stock and issue, with conversion factors held in the item master.',
            '<strong>Capture opening balances and periodic on-hand counts,</strong> so balance and reorder checks become possible.',
        ])),
    ],
    applied=dict(title='Inventory & Warehouse Management',
                 text=['An offline review app that separates confirmed adjustment-concentration findings from unscored stock checks, with source evidence for every transaction and a user-entered on-hand review instead of invented thresholds. Built on synthetic ERP data.'],
                 href=GH + '08-inventory-warehouse-management', label='See the code and README'),
    sources=[
        'DeHoratius, N. and Raman, A. (2008). <a href="https://pubsonline.informs.org/doi/10.1287/mnsc.1070.0789">Inventory record inaccuracy: an empirical analysis</a>. Management Science, 54(4), 627–641.',
        f'Iwale, A. (2026). <a href="{GH}08-inventory-warehouse-management">Inventory &amp; Warehouse Management</a>. GitHub.',
    ],
    next=['insight-predictive-maintenance', 'insight-rework-bad-data'],
)

POSTS = [CONTRACTS, PAYMENTS, INVENTORY]
