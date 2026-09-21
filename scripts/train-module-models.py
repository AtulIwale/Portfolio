"""Reproducible synthetic-data experiments; no real-world performance claims."""
import json, pathlib, statistics, hashlib
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, brier_score_loss, confusion_matrix
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/'public/data/modules'
summary={}
for path in DATA.glob('*.json'):
 if path.name in ('catalog.json','validation.json'):continue
 d=json.loads(path.read_text());m=d['module'];rows=d['rows'];features=m['features'];target=m['target']
 train=[r for r in rows if r[target] is not None and r['record_date']<'2024-06-01' and r['label_available_date']<'2024-08-01']
 test=[r for r in rows if r[target] is not None and r['record_date']>='2024-08-01']
 X=lambda rr:np.array([[r[f] for f in features] for r in rr]);y=lambda rr:np.array([r[target] for r in rr])
 model=DecisionTreeClassifier(max_depth=4,min_samples_leaf=60,random_state=21).fit(X(train),y(train))
 p=model.predict_proba(X(test))[:,list(model.classes_).index(1)]; pred=p>=.5
 tree=model.tree_;nodes=[]
 for i in range(tree.node_count):
  values=tree.value[i][0];risk=float(values[list(model.classes_).index(1)]/sum(values))
  nodes.append(dict(feature=int(tree.feature[i]),threshold=float(tree.threshold[i]),left=int(tree.children_left[i]),right=int(tree.children_right[i]),probability=round(risk,8),samples=int(tree.n_node_samples[i])))
 train_ids={r['record_id'] for r in train};test_ids={r['record_id'] for r in test}
 for r,score in zip(rows,model.predict_proba(X(rows))[:,list(model.classes_).index(1)]):r['risk_score']=round(float(score),6);r['evaluation_split']='Train' if r['record_id'] in train_ids else 'Test' if r['record_id'] in test_ids else 'Excluded / unlabelled'
 baseline=float(y(train).mean());truth=y(test);matrix=confusion_matrix(truth,pred,labels=[0,1]).tolist()
 metrics={'trainRows':len(train),'testRows':len(test),'excludedRows':len(rows)-len(train)-len(test),'trainCutoff':'2024-06-01','testStart':'2024-08-01','labelCutoff':'2024-08-01','auc':round(float(roc_auc_score(truth,p)),4) if len(set(truth))>1 else None,'accuracy':round(float(accuracy_score(truth,pred)),4),'precision':round(float(precision_score(truth,pred,zero_division=0)),4),'recall':round(float(recall_score(truth,pred,zero_division=0)),4),'brier':round(float(brier_score_loss(truth,p)),4),'baselineBrier':round(float(brier_score_loss(truth,np.full(len(test),baseline))),4),'baselineAccuracy':round(float(accuracy_score(truth,np.full(len(test),baseline>=.5))),4),'testEventRate':round(float(truth.mean()),4),'confusionMatrix':matrix}
 d['model']={'kind':'Decision tree classifier','maxDepth':4,'minLeaf':60,'features':features,'target':target,'threshold':.5,'nodes':nodes,'featureImportance':dict(zip(features,map(float,model.feature_importances_))),'metrics':metrics,'limitations':'Temporal holdout on synthetic data only. January–May training; June–July excluded; August–October test. Training labels must be known before August. Repeated entities may occur in both periods: this tests future records for known populations, not unseen suppliers or employees. Scores are uncalibrated tree frequencies, not established real-world probabilities. Model features are captured at record creation; outcomes, status, payment and completion fields are excluded. No automated approvals or personnel decisions.'}
 group=lambda field:[{'name':v,'count':sum(r[field]==v for r in rows),'value':round(sum(r[m['amountField']] for r in rows if r[field]==v),2)} for v in sorted(set(r[field] for r in rows))]
 values=[r[m['amountField']] for r in rows]
 d['analysis']={'rows':len(rows),'details':len(d['details']),'events':len(d['events']),'total':round(sum(values),2),'median':round(statistics.median(values),2),'p90':round(float(np.percentile(values,90)),2),'byStatus':group('status'),'byType':group('type'),'months':[{'name':f'2024-{i:02d}','count':sum(r['record_date'].startswith(f'2024-{i:02d}') for r in rows),'value':round(sum(r[m['amountField']] for r in rows if r['record_date'].startswith(f'2024-{i:02d}')),2)} for i in range(1,11)],'labelled':sum(r[target] is not None for r in rows),'eventsObserved':sum(r[target]==1 for r in rows),'currency':'INR'}
 # Model parity and fundamental domain arithmetic checks are part of generation.
 for r in rows:
  k=0
  while nodes[k]['left']!=-1:
   node=nodes[k];k=node['left'] if r[features[node['feature']]]<=node['threshold'] else node['right']
  assert abs(nodes[k]['probability']-r['risk_score'])<1e-6
  if m['id']=='procurement-subcontracting':assert r['order_amount']==r['quantity']*r['unit_rate'] and 0<=r['accepted_qty']<=r['quantity']
  if m['id']=='inventory-warehouse':assert r['closing_qty']==r['opening_qty']+r['signed_qty'] and r['closing_qty']>=0
  if m['id']=='construction-hr':assert r['scheduled_days']==r['worked_days']+r['paid_leave_days']+r['absent_days']
  if m['id']=='construction-payroll':assert abs(r['gross_pay']-r['deductions']-r['net_pay'])<.011 and (r['status']!='Paid' or r['attendance_status']=='Approved')
  if m['id']=='receivables-payables':assert abs(r['gross_amount']-r['settled_amount']-r['outstanding']-r['unposted_amount'])<.011
  if m['id']=='construction-assets':assert r['closing_book_value']>=r['residual_value'] and (r['status']!='Retired' or r['operating_hours']==0)
 assert len({r['record_id'] for r in rows})==5000
 record_ids={r['record_id'] for r in rows}
 assert all(x['record_id'] in record_ids for x in d['details']+d['events'])
 path.write_text(json.dumps(d,separators=(',',':')))
 (ROOT/'models').mkdir(exist_ok=True)
 (ROOT/'models'/path.name).write_text(json.dumps({'model':d['model'],'analysis':d['analysis']},indent=2))
 summary[m['id']]={'analysis':d['analysis'],'model':{k:v for k,v in d['model'].items() if k!='nodes'},'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 print(m['id'],len(train),len(test),'AUC',metrics['auc'])
hr=json.loads((DATA/'construction-hr.json').read_text())['rows'];py=json.loads((DATA/'construction-payroll.json').read_text())['rows']
assert all(a['record_id']==b['attendance_id'] and a['employee_id']==b['employee_id'] and a['status']==b['attendance_status'] for a,b in zip(hr,py))
(ROOT/'src/modules/metrics.json').write_text(json.dumps(summary))
(DATA/'validation.json').write_text(json.dumps({'version':'AEC-DEMO-2026.1','primaryRows':40000,'modules':8,'checks':['Unique primary IDs','Detail/event foreign keys','Inventory nonnegative ledger arithmetic','Order extensions and acceptance bounds','HR attendance-day reconciliation','Payroll net and approved-attendance eligibility','AR/AP posted and unposted reconciliation','Asset residual-value and retirement controls','Shared HR/payroll IDs','Exported decision-tree scoring parity'],'results':'Passed','files':{k:v['sha256'] for k,v in summary.items()}},indent=2))
