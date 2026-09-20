"""Build a standalone, local HTML report and readable result summary from run outputs."""
import html
import json
from pathlib import Path
from .data import load_dataset,records
from .analytics import control_tower

def main():
    out=Path('outputs')
    totals,orders,suppliers=control_tower(load_dataset('data'))
    d=json.loads((out/'delivery_metrics.json').read_text())
    c=json.loads((out/'cost_metrics.json').read_text())
    report=f'''# Executed synthetic-data results — seed 42

These are actual outputs of the committed pipeline, not client results. Re-run before
comparing changes. The seed and row counts are recorded in run_manifest.json.

| Evaluation | Selected model | Test result | Dummy baseline |
|---|---|---|---|
| Late-delivery ranking | {d['selected_model']} | AP {d['test']['average_precision']:.3f}; ROC-AUC {d['test']['roc_auc']:.3f} | AP {d['baseline_test']['average_precision']:.3f} |
| Delivery probability error | {d['selected_model']} | Brier {d['test']['brier']:.3f} | Brier {d['baseline_test']['brier']:.3f} |
| Final-cost ratio | {c['selected_model']} | MAE {c['test_mae_ratio']:.3f} | MAE {c['baseline_test_mae_ratio']:.3f} |

Delivery test n={d['test']['n']}; cost test n={c['split_counts']['test']}.
Cost interval observed coverage: {c['empirical_interval_coverage']:.1%}, nominal 90%.
Cost interval half-width: {c['interval_halfwidth_ratio']:.3f} × original budget.

## Interpretation, including weaknesses

The delivery model improves ranking over the dummy baseline, but its probability error
must be compared separately. Lower Brier is better. In the seed-42 run the chosen model's
Brier is worse than the dummy under the simulated later-period shift. Do not treat its
probabilities as deployment-ready. A high-recall threshold creates a large follow-up queue;
review workload and test-period utility need operational validation.

The cost model's lower ratio MAE is evidence of learning the synthetic process, not real
commercial forecasting accuracy. Wide intervals remain important; do not cherry-pick the
coverage number without their width. Neither project establishes prevented delays or savings.

## Procurement analysis

- Orders: {totals['orders']:,}
- Gross-completed orders: {totals['completed_orders']:,}
- On-time rate among completed orders: {totals['on_time_completed_rate']:.1%}
- Overdue open orders: {totals['overdue_open_orders']:,}
- Invoiced value: INR {totals['invoiced_value']:,.2f}
- Overdue invoice balance at {totals['as_of']}: INR {totals['overdue_invoice_balance']:,.2f}

See the JSON files for all metrics, slices, calibration bins, assumptions and review queues.
All three financial sums reconcile to their clean synthetic source tables in automated tests.
'''
    seed=json.loads((out/'run_manifest.json').read_text())['seed']
    report=report.replace('seed 42',f'seed {seed}')
    (out/'RESULTS.md').write_text(report)
    payload=json.dumps(records(orders)).replace('<','\\u003c')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AEC procurement control tower — synthetic portfolio</title>
<style>body{font:16px/1.55 system-ui;margin:0;background:#f5f1e9;color:#2d4653}main{max-width:1200px;margin:auto;padding:36px 24px}h1{font-size:clamp(28px,4vw,44px);line-height:1.15}h2{font-size:22px}.note{padding:16px;border-left:4px solid #3f7285;background:#e7eef1}.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin:24px 0}.metric{background:white;padding:20px;border:1px solid #758892;border-radius:12px}.metric strong{display:block;font-size:25px}.scroll{overflow:auto}table{border-collapse:collapse;width:100%;background:#fff}th,td{padding:10px 14px;text-align:left;border-bottom:1px solid #b6a78e;white-space:nowrap}select,input,button{font:inherit;padding:10px;margin:8px 12px 8px 0;border:1px solid #758892;border-radius:6px}button{background:#3f7285;color:white;cursor:pointer}a{color:#315e70}:focus-visible{outline:3px solid #3f7285;outline-offset:3px}caption{text-align:left;padding:10px 0}footer{margin-top:30px}#status{min-height:26px}</style>
<main><p>ATUL IWALE / DATA ANALYSIS</p><h1>Procure-to-Pay Control Tower</h1>
<p class="note">Entirely synthetic data • INR • As of 31 December 2025 • Local report, no ERP connection.<br>Gross receipt completion is not quality acceptance. Open orders are excluded from on-time-rate denominator.</p>
<label for="supplier">Supplier</label><select id="supplier"><option value="">All suppliers</option></select>
<label for="search">Order or project</label><input id="search" type="search" placeholder="e.g. O000120 or P010">
<button id="reset">Reset filters</button><div id="metrics" class="metrics"></div>
<h2>Orders and exceptions</h2><p id="status" role="status"></p><div class="scroll"><table><caption>First 200 matching orders; totals include all filtered orders.</caption><thead><tr><th>Order</th><th>Project</th><th>Supplier</th><th>Order value</th><th>Received / ordered</th><th>Delivery</th><th>Overdue invoice balance</th></tr></thead><tbody id="rows"></tbody></table></div>
<footer>Methods: aggregate receipts and payments before joining to orders. Negative balances are not interpreted as savings. Downloaded JSONL sources and SQL accompany this report in the repository.</footer></main>
<script>const data=PAYLOAD;
const supplier=document.getElementById('supplier'),search=document.getElementById('search');
[...new Set(data.map(r=>r.supplier_id))].sort().forEach(id=>{const o=document.createElement('option');o.value=id;o.textContent=id;supplier.append(o)});
const number=n=>n.toLocaleString('en-IN',{maximumFractionDigits:0});
function draw(){const q=search.value.trim().toLowerCase();const rows=data.filter(r=>(!supplier.value||r.supplier_id===supplier.value)&&(!q||(r.order_id+' '+r.project_id).toLowerCase().includes(q)));
const complete=rows.filter(r=>r.complete);const metrics=[['Orders',rows.length],['Ordered · INR',rows.reduce((a,r)=>a+r.amount,0)],['Overdue invoices · INR',rows.reduce((a,r)=>a+r.overdue,0)],['Overdue open',rows.filter(r=>r.overdue_open).length]];
document.getElementById('metrics').replaceChildren(...metrics.map(([label,value])=>{const d=document.createElement('div');d.className='metric';d.textContent=label;const s=document.createElement('strong');s.textContent=number(value);d.append(s);return d}));
document.getElementById('status').textContent=rows.length+' matches. On-time among completed: '+(complete.length?((1-complete.filter(r=>r.late_completed).length/complete.length)*100).toFixed(1)+'%':'not available');
document.getElementById('rows').replaceChildren(...rows.slice(0,200).map(r=>{const tr=document.createElement('tr');[r.order_id,r.project_id,r.supplier_id,number(r.amount),number(r.received_qty)+' / '+number(r.quantity),r.overdue_open?'Overdue open':r.complete?(r.late_completed?'Completed late':'Completed on time'):'Open',number(r.overdue)].forEach(v=>{const td=document.createElement('td');td.textContent=v;tr.append(td)});return tr}));}
supplier.addEventListener('change',draw);search.addEventListener('input',draw);document.getElementById('reset').addEventListener('click',()=>{supplier.value='';search.value='';draw()});draw();</script></html>'''
    (out/'control_tower.html').write_text(page.replace('PAYLOAD',payload))
    print('Wrote outputs/RESULTS.md and outputs/control_tower.html')

if __name__=='__main__': main()
