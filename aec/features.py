"""Prediction-time feature construction and outcome-mature, purged splits."""
import numpy as np
import pandas as pd

DELIVERY_NUM=['quantity','amount','lead_days','order_month','supplier_prior_late_rate','supplier_prior_completed']
DELIVERY_CAT=['category']
COST_NUM=['original_budget','progress_assumption','actual_ratio','commitment_ratio','approved_ratio','pending_ratio','variation_count']
COST_CAT=['sector']

def delivery_features(tables):
    orders=tables['orders'].copy()
    g=tables['grns'].groupby('order_id').agg(received_qty=('quantity','sum'),completion_date=('received_date','max'))
    f=orders.merge(g,on='order_id',how='left',validate='one_to_one')
    f['order_date']=pd.to_datetime(f.order_date); f['required_by']=pd.to_datetime(f.required_by)
    f['completion_date']=pd.to_datetime(f.completion_date)
    f['complete']=f.received_qty.fillna(0)>=f.quantity-.001
    f.loc[~f.complete,'completion_date']=pd.NaT
    f['late']=np.where(f.complete,(f.completion_date>f.required_by).astype(int),np.nan)
    f['lead_days']=(f.required_by-f.order_date).dt.days
    f['order_month']=f.order_date.dt.month
    rates,counts=[],[]
    for row in f.itertuples():
        history=f[(f.supplier_id==row.supplier_id)&(f.completion_date<row.order_date)&f.complete]
        counts.append(len(history))
        rates.append((history.late.sum()+1)/(len(history)+2))
    f['supplier_prior_late_rate']=rates; f['supplier_prior_completed']=counts
    return f

def cost_features(tables):
    f=tables['snapshots'].merge(tables['packages'],on='package_id',validate='many_to_one')
    # One decision point per package. No repeated-package leakage across splits.
    f=f[f.progress_assumption==.5].copy()
    f=f.merge(tables['outcomes'],on='package_id',how='left',validate='one_to_one')
    for col in ['snapshot_date','completion_date']:
        f[col]=pd.to_datetime(f[col])
    for source,name in [('actual_cost','actual_ratio'),('committed_remaining','commitment_ratio'),
                        ('approved_variations','approved_ratio'),('pending_variations','pending_ratio')]:
        f[name]=f[source]/f.original_budget
    f['final_ratio']=f.final_cost/f.original_budget
    return f

def split_mature(f,date_col,label_col,first='2023-01-01',second='2024-07-01'):
    a,b=pd.Timestamp(first),pd.Timestamp(second)
    train=f[(f[date_col]<a)&(f.completion_date<a)&f[label_col].notna()].copy()
    val=f[(f[date_col]>=a)&(f[date_col]<b)&(f.completion_date<b)&f[label_col].notna()].copy()
    test=f[(f[date_col]>=b)&f[label_col].notna()].copy()
    for name,part in [('train',train),('validation',val),('test',test)]:
        if len(part)<20:
            raise ValueError(f'{name} requires at least 20 mature outcomes; found {len(part)}')
    return train,val,test
