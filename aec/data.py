"""Seeded, relational synthetic ERP events. No client data or vendor manual content."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

AS_OF = pd.Timestamp('2025-12-31')

def records(frame):
    return json.loads(frame.to_json(orient='records', date_format='iso'))

def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')

def generate(seed=42, n_orders=3600, n_packages=750):
    rng = np.random.default_rng(seed)
    categories = ['Concrete', 'Steel', 'MEP', 'Finishes', 'Earthworks']
    suppliers = pd.DataFrame([{'supplier_id':f'S{i:03d}', 'name':f'Synthetic Supplier {i:03d}'} for i in range(1,61)])
    projects = pd.DataFrame([{'project_id':f'P{i:03d}', 'name':f'Synthetic Project {i:03d}',
        'sector':categories[i % 5], 'company_id':f'C{1+i%3}', 'currency':'INR'} for i in range(1,31)])
    # Hidden supplier effects belong to the simulation only, never to model features.
    reliability = rng.normal(0, 5, 60)
    orders, reqs, grns, invoices, payments = [], [], [], [], []
    for i, day in enumerate(sorted(rng.integers(0, 1461, n_orders))):
        oid, rid = f'O{i:06d}', f'RQ{i:06d}'
        date = pd.Timestamp('2022-01-01') + pd.Timedelta(days=int(day))
        supplier = int(rng.integers(0,60))
        category = str(rng.choice(categories))
        lead = int(rng.integers(10,65))
        qty = int(rng.integers(20,800))
        rate = round(float(rng.lognormal(5.4,0.65)),2)
        project = str(rng.choice(projects.project_id))
        currency = 'INR'
        # Unobserved shocks + supplier effects + later regime shift prevent perfect classification.
        delay = int(round(reliability[supplier] + (category=='MEP')*4 +
            (date.month in [6,7,8])*4 + (date.year==2025)*3 + rng.normal(-5,8)))
        duration = max(3,lead+delay)
        complete = date+pd.Timedelta(days=duration)
        required = date+pd.Timedelta(days=lead)
        req_date = date-pd.Timedelta(days=int(rng.integers(2,25)))
        reqs.append(dict(requisition_id=rid,project_id=project,date=str(req_date.date()),
            required_by=str(required.date()),resource_category=category,quantity=qty))
        orders.append(dict(order_id=oid,requisition_id=rid,project_id=project,supplier_id=f'S{supplier+1:03d}',
            order_date=str(date.date()),required_by=str(required.date()),category=category,quantity=qty,
            unit_rate=rate,amount=round(qty*rate,2),currency=currency))
        fractions = [0.4,0.6] if rng.random()<0.35 else [1.0]
        for j, fraction in enumerate(fractions):
            delivered = max(date+pd.Timedelta(days=1),complete-pd.Timedelta(days=4 if len(fractions)==2 and j==0 else 0))
            if delivered > AS_OF:
                continue
            received = round(qty*fraction,2)
            rejected = round(received*float(rng.uniform(.01,.12)),2) if rng.random()<.09 else 0
            gid = f'G{i:06d}-{j}'
            grns.append(dict(grn_id=gid,order_id=oid,received_date=str(delivered.date()),quantity=received,
                rejected_quantity=rejected))
            invoice_date = delivered+pd.Timedelta(days=int(rng.integers(2,16)))
            if invoice_date > AS_OF:
                continue
            iid=f'I{i:06d}-{j}'
            amount=round(received*rate,2)
            due=invoice_date+pd.Timedelta(days=30)
            invoices.append(dict(invoice_id=iid,grn_id=gid,order_id=oid,invoice_date=str(invoice_date.date()),
                due_date=str(due.date()),amount=amount,currency=currency))
            paid=due+pd.Timedelta(days=int(rng.integers(-10,36)))
            # Separate instalments test analytical join-grain handling.
            shares=[.5,.5] if rng.random()<.2 else [1.0]
            for k,share in enumerate(shares):
                paid_at=paid+pd.Timedelta(days=7*k)
                if paid_at<=AS_OF:
                    payments.append(dict(payment_id=f'PAY{i:06d}-{j}-{k}',invoice_id=iid,
                        paid_date=str(paid_at.date()),amount=round(amount*share,2),currency=currency))
    packages, snapshots, outcomes, variations = [], [], [], []
    for i,day in enumerate(sorted(rng.integers(0,2190,n_packages))):
        pid=f'WP{i:05d}'
        start=pd.Timestamp('2019-01-01')+pd.Timedelta(days=int(day))
        duration=int(rng.integers(240,500))
        budget=round(float(rng.lognormal(15,0.6)),2)
        complexity=float(rng.uniform(0,1))
        pressure=float(rng.uniform(0,1))
        final_ratio=float(np.clip(.82+.28*complexity+.18*pressure+rng.normal(0,.1),.7,1.8))
        complete=start+pd.Timedelta(days=duration)
        sector=str(rng.choice(categories))
        packages.append(dict(package_id=pid,project_id=f'CP{i:05d}',start_date=str(start.date()),
            sector=sector,original_budget=budget,currency='INR'))
        variation_count=int(rng.poisson(1+5*complexity))
        vrows=[]
        for j in range(variation_count):
            d=start+pd.Timedelta(days=int(rng.integers(20,duration)))
            row=dict(variation_id=f'V{i:05d}-{j}',package_id=pid,date=str(d.date()),
                amount=round(budget*float(rng.uniform(.003,.025)),2),
                status=str(rng.choice(['Approved','Pending','Rejected'],p=[.6,.3,.1])))
            if d<=AS_OF:
                variations.append(row)
            vrows.append(row)
        for stage in [.25,.5,.75]:
            d=start+pd.Timedelta(days=int(duration*stage))
            if d>AS_OF:
                continue
            known=[v for v in vrows if pd.Timestamp(v['date'])<=d]
            actual=round(budget*stage*(.85+.25*complexity+.13*pressure+rng.normal(0,.05)),2)
            snapshots.append(dict(snapshot_id=f'{pid}-{stage}',package_id=pid,snapshot_date=str(d.date()),
                progress_assumption=stage,actual_cost=actual,committed_remaining=round(budget*(1-stage)*.65,2),
                approved_variations=sum(v['amount'] for v in known if v['status']=='Approved'),
                pending_variations=sum(v['amount'] for v in known if v['status']=='Pending'),
                variation_count=len(known)))
        if complete<=AS_OF:
            outcomes.append(dict(package_id=pid,completion_date=str(complete.date()),final_cost=round(budget*final_ratio,2)))
    frames=dict(projects=projects,suppliers=suppliers,requisitions=pd.DataFrame(reqs),orders=pd.DataFrame(orders),
        grns=pd.DataFrame(grns),invoices=pd.DataFrame(invoices),payments=pd.DataFrame(payments),
        packages=pd.DataFrame(packages),snapshots=pd.DataFrame(snapshots),outcomes=pd.DataFrame(outcomes),
        variations=pd.DataFrame(variations))
    # Deliberately damaged copy, isolated from clean training and reporting tables.
    dirty=frames['orders'].head(100).copy()
    dirty.loc[0,'supplier_id']='UNKNOWN'
    dirty.loc[1,'amount']=-500
    dirty.loc[2,'required_by']='2020-01-01'
    dirty=pd.concat([dirty,dirty.iloc[[3]]],ignore_index=True)
    frames['orders_dirty']=dirty
    return frames

def save_dataset(frames, folder, seed):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    manifest={'seed':seed,'as_of':str(AS_OF.date()),'synthetic':True,'currency':'INR', 'tables':{}}
    for name,frame in frames.items():
        path=folder/f'{name}.jsonl'
        frame.to_json(path,orient='records',lines=True,double_precision=6)
        manifest['tables'][name]={'rows':len(frame),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'columns':list(frame.columns)}
    write_json(folder/'manifest.json',manifest)
    return manifest

def load_dataset(folder):
    return {p.stem:pd.read_json(p,lines=True,convert_dates=False) for p in Path(folder).glob('*.jsonl')}
