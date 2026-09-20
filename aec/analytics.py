"""SQL analytics at explicit grains, reconciliation, and scenario uncertainty."""
import sqlite3
import numpy as np
import pandas as pd
from .data import AS_OF

CONTROL_TOWER_SQL = '''
WITH receipts AS (
 SELECT order_id, SUM(quantity) AS received_qty,
 SUM(rejected_quantity) AS rejected_qty, MAX(received_date) AS last_receipt
 FROM grns GROUP BY order_id
), invoice_payment AS (
 SELECT i.invoice_id, i.order_id, i.amount, i.due_date,
 COALESCE(SUM(p.amount),0) AS paid
 FROM invoices i LEFT JOIN payments p ON p.invoice_id=i.invoice_id
 GROUP BY i.invoice_id, i.order_id, i.amount, i.due_date
), billing AS (
 SELECT order_id, SUM(amount) AS invoiced, SUM(paid) AS paid,
 SUM(CASE WHEN due_date < :as_of THEN MAX(amount-paid,0) ELSE 0 END) AS overdue
 FROM invoice_payment GROUP BY order_id
)
SELECT o.order_id,o.project_id,o.supplier_id,o.category,o.amount,o.quantity,
 o.order_date,o.required_by,o.currency,
 COALESCE(r.received_qty,0) AS received_qty,
 COALESCE(r.rejected_qty,0) AS rejected_qty,r.last_receipt,
 COALESCE(b.invoiced,0) AS invoiced,COALESCE(b.paid,0) AS paid,
 COALESCE(b.overdue,0) AS overdue,
 MAX(o.amount-COALESCE(b.invoiced,0),0) AS uninvoiced_commitment
FROM orders o LEFT JOIN receipts r ON r.order_id=o.order_id
LEFT JOIN billing b ON b.order_id=o.order_id
ORDER BY o.order_id
'''

def control_tower(tables):
    with sqlite3.connect(':memory:') as db:
        for name in ['orders','grns','invoices','payments']:
            tables[name].to_sql(name,db,index=False)
        detail=pd.read_sql_query(CONTROL_TOWER_SQL,db,params={'as_of':str(AS_OF.date())})
    detail['complete']=detail.received_qty>=detail.quantity-.001
    detail['late_completed']=detail.complete & (pd.to_datetime(detail.last_receipt)>pd.to_datetime(detail.required_by))
    detail['overdue_open']=~detail.complete & (pd.to_datetime(detail.required_by)<AS_OF)
    complete=detail[detail.complete]
    summary={'as_of':str(AS_OF.date()),'currency':'INR','orders':len(detail),
        'order_value':float(detail.amount.sum()),'invoiced_value':float(detail.invoiced.sum()),
        'paid_value':float(detail.paid.sum()),'overdue_invoice_balance':float(detail.overdue.sum()),
        'uninvoiced_commitment':float(detail.uninvoiced_commitment.sum()),
        'completed_orders':len(complete),'on_time_completed_rate':float(1-complete.late_completed.mean()),
        'overdue_open_orders':int(detail.overdue_open.sum()),
        'rejection_rate_by_quantity':float(detail.rejected_qty.sum()/max(1,detail.received_qty.sum()))}
    suppliers=detail.groupby('supplier_id').agg(orders=('order_id','size'),order_value=('amount','sum'),
        completed=('complete','sum'),late_completed=('late_completed','sum'),overdue_open=('overdue_open','sum'),
        received_qty=('received_qty','sum'),rejected_qty=('rejected_qty','sum')).reset_index()
    suppliers['late_completed_rate']=suppliers.late_completed/suppliers.completed.replace(0,np.nan)
    return summary,detail,suppliers

def audit_orders(frame,suppliers):
    findings=[]
    for i,r in frame.iterrows():
        rules=[]
        if r.supplier_id not in set(suppliers.supplier_id): rules.append('UNKNOWN_SUPPLIER')
        if r.amount<0: rules.append('NEGATIVE_ORDER_VALUE')
        if pd.Timestamp(r.required_by)<pd.Timestamp(r.order_date): rules.append('REQUIRED_BEFORE_ORDER')
        if frame.order_id.duplicated(keep=False).iloc[i]: rules.append('DUPLICATE_ORDER_ID')
        for rule in rules:
            findings.append({'row_index':int(i),'order_id':r.order_id,'rule':rule,'action':'Review source record; do not auto-correct.'})
    return findings

def scenario(snapshot,budget,draws=5000,seed=42,escalation=.06,payment_delay=1,receipt_delay=2):
    """Synthetic cost/cash planning, not an observed cash-flow forecast.

    actual_cost is assumed paid before month 1; remaining costs are spread over six
    months. Remaining client receipts are an explicit fictional 1.1 x budget.
    """
    if draws<100 or not 0<=escalation<=1 or not 0<=payment_delay<=6 or not 0<=receipt_delay<=6:
        raise ValueError('Invalid scenario parameters')
    if budget<=0 or not 0<snapshot['progress_assumption']<1:
        raise ValueError('Positive budget and intermediate progress required')
    rng=np.random.default_rng(seed)
    remaining=max(0,budget*(1-snapshot['progress_assumption']))
    # Common shock creates correlated month-to-month escalation, not independent noise.
    multipliers=np.maximum(.5,1+rng.normal(escalation,.08,draws))
    pending=snapshot['pending_variations']*rng.binomial(1,.6,draws)
    cost=remaining*multipliers+pending
    eac=snapshot['actual_cost']+cost
    weights=np.array([.1,.2,.25,.2,.15,.1])
    outflow=np.zeros((draws,12)); inflow=np.zeros((draws,12))
    outflow[:,payment_delay:payment_delay+6]=cost[:,None]*weights
    # Receipts are scenario assumptions, deliberately not fabricated AR register evidence.
    inflow[:,receipt_delay:receipt_delay+6]=budget*(1-snapshot['progress_assumption'])*1.1*weights
    balance=np.cumsum(inflow-outflow,axis=1)
    funding=np.maximum(0,-balance.min(axis=1))
    return {'draws':draws,'seed':seed,'currency':'INR','escalation':escalation,
        'payment_delay_months':payment_delay,'receipt_delay_months':receipt_delay,
        'eac_p10_p50_p90':np.quantile(eac,[.1,.5,.9]).tolist(),
        'peak_funding_p10_p50_p90':np.quantile(funding,[.1,.5,.9]).tolist(),
        'monthly_net_cash_p50':np.median(inflow-outflow,axis=0).tolist(),
        'warning':'Synthetic scenario distribution, not empirically validated forecast confidence.'}
