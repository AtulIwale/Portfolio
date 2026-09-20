"""Baseline comparison, validation selection, held-out metrics and uncertainty."""
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import (roc_auc_score, average_precision_score, brier_score_loss,
    precision_score, recall_score, f1_score, mean_absolute_error, root_mean_squared_error)
from .features import DELIVERY_NUM,DELIVERY_CAT,COST_NUM,COST_CAT,split_mature

def pipeline(model,nums,cats):
    numeric=Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())])
    categorical=Pipeline([('impute',SimpleImputer(strategy='most_frequent')),
        ('encode',OneHotEncoder(handle_unknown='ignore',sparse_output=False))])
    return Pipeline([('prepare',ColumnTransformer([('numeric',numeric,nums),('category',categorical,cats)])),('model',model)])

def classification_metrics(y,p,threshold):
    labels=p>=threshold
    return {'roc_auc':float(roc_auc_score(y,p)) if len(set(y))>1 else None,
        'average_precision':float(average_precision_score(y,p)), 'brier':float(brier_score_loss(y,p)),
        'precision':float(precision_score(y,labels,zero_division=0)),
        'recall':float(recall_score(y,labels,zero_division=0)),
        'f1':float(f1_score(y,labels,zero_division=0)),'threshold':float(threshold),'n':len(y)}

def evaluate_delivery(f):
    train,val,test=split_mature(f,'order_date','late')
    nums,cats=DELIVERY_NUM,DELIVERY_CAT; cols=nums+cats
    candidates={'dummy':DummyClassifier(strategy='prior'),'logistic':LogisticRegression(max_iter=1000)}
    for leaves in [7,15]:
        candidates[f'boosting_{leaves}']=HistGradientBoostingClassifier(max_leaf_nodes=leaves,max_iter=100,
            l2_regularization=2,early_stopping=False,random_state=42)
    fitted,validation={},{}
    for name,model in candidates.items():
        pipe=pipeline(model,nums,cats).fit(train[cols],train.late)
        fitted[name]=pipe
        validation[name]=classification_metrics(val.late,pipe.predict_proba(val[cols])[:,1],.5)
    chosen=max(validation,key=lambda k:validation[k]['average_precision'])
    model=fitted[chosen]; vp=model.predict_proba(val[cols])[:,1]
    # Fixed scenario loss: missed late order = 5 units; unnecessary follow-up = 1 unit.
    thresholds=np.arange(.1,.91,.05)
    loss=[5*np.sum((vp<t)&(val.late==1))+np.sum((vp>=t)&(val.late==0)) for t in thresholds]
    threshold=float(thresholds[np.argmin(loss)])
    p=model.predict_proba(test[cols])[:,1]
    report={'selected_model':chosen,'split_counts':dict(train=len(train),validation=len(val),test=len(test)),
        'validation':validation,'test':classification_metrics(test.late,p,threshold),
        'baseline_test':classification_metrics(test.late,fitted['dummy'].predict_proba(test[cols])[:,1],threshold),
        'followup_loss_assumption':{'missed_late':5,'unnecessary_followup':1},
        'threshold_validation_loss':int(min(loss)),
        'slices':{},'calibration_bins':[], 'synthetic_only':True}
    for category in sorted(test.category.unique()):
        mask=(test.category==category).to_numpy()
        report['slices'][category]=classification_metrics(test.late[mask],p[mask],threshold)
    for lo in np.arange(0,1,.2):
        mask=(p>=lo)&(p<(lo+.2) if lo<.8 else p<=1)
        if mask.any():
            report['calibration_bins'].append({'lower':float(lo),'n':int(mask.sum()),
                'predicted':float(p[mask].mean()),'observed':float(test.late.to_numpy()[mask].mean())})
    imp=permutation_importance(model,test[cols],test.late,n_repeats=3,random_state=42,scoring='average_precision')
    report['permutation_importance']={c:float(x) for c,x in zip(cols,imp.importances_mean)}
    report['drift_ks']={c:float(ks_2samp(train[c].dropna(),test[c].dropna()).statistic) for c in nums}
    # Fixed-model bootstrap describes conditional test uncertainty, not training uncertainty.
    rng=np.random.default_rng(42); boot=[]
    for _ in range(200):
        ix=rng.integers(0,len(p),len(p))
        boot.append(average_precision_score(test.late.to_numpy()[ix],p[ix]))
    report['test_ap_bootstrap_95']=np.quantile(boot,[.025,.975]).tolist()
    out=test[['order_id','supplier_id','project_id','amount','late']].copy()
    out['late_probability']=p; out['review']=p>=threshold
    return report,out.sort_values('late_probability',ascending=False)

def evaluate_cost(f):
    train,val,test=split_mature(f,'snapshot_date','final_ratio')
    cols=COST_NUM+COST_CAT
    models={'dummy':DummyRegressor(strategy='median'),'ridge':Ridge(alpha=10),
        'boosting':HistGradientBoostingRegressor(max_iter=100,max_leaf_nodes=7,l2_regularization=3,
                                               early_stopping=False,random_state=42)}
    fitted={k:pipeline(v,COST_NUM,COST_CAT).fit(train[cols],train.final_ratio) for k,v in models.items()}
    # Separate chronological validation halves: model selection then interval calibration.
    val=val.sort_values('snapshot_date'); select=val.iloc[:len(val)//2]; cal=val.iloc[len(val)//2:]
    scores={k:float(mean_absolute_error(select.final_ratio,v.predict(select[cols]))) for k,v in fitted.items()}
    chosen=min(scores,key=scores.get); model=fitted[chosen]
    residual=np.abs(cal.final_ratio-model.predict(cal[cols]))
    q=float(np.quantile(residual,min(1,np.ceil((len(cal)+1)*.9)/len(cal)),method='higher'))
    pred=model.predict(test[cols]); low=pred-q; high=pred+q
    report={'selected_model':chosen,'validation_mae_ratio':scores,'interval_calibration_n':len(cal),
        'split_counts':dict(train=len(train),validation=len(val),test=len(test)),
        'test_mae_ratio':float(mean_absolute_error(test.final_ratio,pred)),
        'test_rmse_ratio':float(root_mean_squared_error(test.final_ratio,pred)),
        'test_mae_inr':float(mean_absolute_error(test.final_cost,pred*test.original_budget)),
        'baseline_test_mae_ratio':float(mean_absolute_error(test.final_ratio,fitted['dummy'].predict(test[cols]))),
        'nominal_interval_coverage':.9,'empirical_interval_coverage':float(np.mean((test.final_ratio>=low)&(test.final_ratio<=high))),
        'interval_halfwidth_ratio':q,'synthetic_only':True,
        'interval_warning':'Temporal drift violates exchangeability; coverage is measured, not guaranteed.',
        'overrun_threshold':1.05,'overrun_flag_f1':float(f1_score(test.final_ratio>1.05,pred>1.05,zero_division=0))}
    imp=permutation_importance(model,test[cols],test.final_ratio,n_repeats=3,random_state=42,scoring='neg_mean_absolute_error')
    report['permutation_importance']={c:float(v) for c,v in zip(cols,imp.importances_mean)}
    out=test[['package_id','original_budget','final_cost']].copy()
    out['predicted_final_cost']=pred*test.original_budget
    out['lower']=np.maximum(low,0)*test.original_budget; out['upper']=high*test.original_budget
    out['investigate_overrun']=pred>1.05
    return report,out
