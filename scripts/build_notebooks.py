"""Author review-friendly notebooks. Execute with scripts/execute_notebooks.py."""
from pathlib import Path
import hashlib
import textwrap
import nbformat as nbf

ROOT=Path(__file__).resolve().parents[1]

def md(text): return nbf.v4.new_markdown_cell(textwrap.dedent(text).strip())
def code(text): return nbf.v4.new_code_cell(textwrap.dedent(text).strip())

SETUP=code('''
from pathlib import Path
import os, sys, subprocess, tempfile

# Pin the computational source/data so later edits to main do not change this walkthrough.
SOURCE_REV = "363f7edcd6c2357bc167257fce4e36b771b216d6"
try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

candidates = [Path.cwd(), *Path.cwd().parents]
ROOT = next((p for p in candidates if (p / "aec/features.py").exists()), None)
if ROOT is None:
    ROOT = Path(tempfile.mkdtemp(prefix="aec-portfolio-")) / "Portfolio"
    subprocess.run(["git", "clone", "--quiet", "https://github.com/AtulIwale/Portfolio.git", str(ROOT)], check=True)
    subprocess.run(["git", "-C", str(ROOT), "checkout", "--quiet", SOURCE_REV], check=True)
if IN_COLAB:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "-r", str(ROOT / "requirements.txt"), "matplotlib==3.10.8"], check=True)
sys.path.insert(0, str(ROOT)) if str(ROOT) not in sys.path else None
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "2")
os.environ.setdefault("OMP_NUM_THREADS", "2")
print("Source:", SOURCE_REV if IN_COLAB else "local checkout")
print("Data: synthetic only; no client information or credentials required.")
''')

COMMON=code('''
import json, hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
from aec.data import load_dataset

tables = load_dataset(ROOT / "data")
manifest = json.loads((ROOT / "data/manifest.json").read_text())
for name, spec in manifest["tables"].items():
    assert hashlib.sha256((ROOT / f"data/{name}.jsonl").read_bytes()).hexdigest() == spec["sha256"], name
plt.rcParams.update({"figure.figsize": (10, 4.8), "figure.dpi": 120,
    "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": "#2D4653", "text.color": "#2D4653", "axes.titleweight": "bold",
    "axes.prop_cycle": plt.cycler(color=["#3F7285", "#B6A78E", "#2D4653", "#899BA5"])})
FIGURES = ROOT / "outputs/notebook-figures"
FIGURES.mkdir(parents=True, exist_ok=True)
def finish(fig, name):
    fig.tight_layout()
    fig.savefig(FIGURES / f"{name}.png", dpi=140, bbox_inches="tight", facecolor="white")
    plt.show()
print(f"Verified {len(tables)} tables / {sum(len(t) for t in tables.values()):,} synthetic rows against manifest hashes.")
''')

def intro(title,question,slug):
    return [md(f'''# {title}

**Atul Iwale · AEC Intelligence Portfolio · executed synthetic-data walkthrough**

> **Decision:** {question}

[Case study](https://github.com/AtulIwale/Portfolio/tree/main/projects/{slug}) ·
[Data assumptions](https://github.com/AtulIwale/Portfolio/blob/main/docs/DATA_CARD.md) ·
[Portfolio](https://github.com/AtulIwale/Portfolio)

Read the narrative, tables and saved charts on GitHub; no installation is required to read.
To reproduce, use **Runtime → Run all** in a fresh Colab session. The first cell downloads
the public repository and installs dependencies only in Colab. Locally, install
`requirements-notebooks.txt` and open this notebook from the repository.

All data is fictional. Results demonstrate an analytical approach, not proven client impact.
'''),md('''## 1. Reproducible setup

The notebook verifies the dataset hashes and imports reusable project functions. The
important decisions and calculations remain visible below. Saved outputs were produced
by executing all cells in a fresh Python process with IPython rich output capture.
Local Jupyter kernel sockets were unavailable; the hosted Colab service was not used for validation.
'''),SETUP.copy(),COMMON.copy()]

def save(name,cells):
    nb=nbf.v4.new_notebook(cells=cells,metadata={"kernelspec":{"display_name":"Python 3", "language":"python","name":"python3"},
        "language_info":{"name":"python","version":"3.12"},"colab":{"name":name,"provenance":[]}})
    for i,c in enumerate(nb.cells):
        c.id=hashlib.sha256(f'{name}-{i}-{c.source}'.encode()).hexdigest()[:12]
    path=ROOT/'notebooks'/name; path.parent.mkdir(parents=True,exist_ok=True)
    nbf.write(nb,path)

def analyst():
    cells=intro('Procure-to-Pay & Supplier Performance','Where should buyers and finance investigate delivery and payment exceptions?','03-control-tower')
    cells += [md('''## 2. Understand the records before joining them

An order can have multiple receipts; an invoice can have multiple payment instalments.
I first establish the grain of each table. Joining every detail row and then summing order
values would repeat the same commitment. The report must retain **one row per order**.

Only INR is present. Taxes, retention, credit notes and cancellations are not simulated.
'''),code('''
keys = {"orders":"order_id", "grns":"grn_id", "invoices":"invoice_id", "payments":"payment_id"}
display(pd.DataFrame([{"table":n,"rows":len(tables[n]),"unique_primary_keys":tables[n][k].nunique(),
    "missing_cells":int(tables[n].isna().sum().sum())} for n,k in keys.items()]))
display(tables["orders"].head(5))
'''),md('''## 3. Audit quality without contaminating the clean analysis

The clean generator is intentionally complete, so “zero missing values” is not evidence
that real ERP data is clean. A separate damaged fixture tests unknown suppliers, negative
values, impossible dates and duplicate references. Flagging a record does not authorise
silently repairing it.
'''),code('''
from aec.analytics import audit_orders, control_tower, CONTROL_TOWER_SQL
findings = pd.DataFrame(audit_orders(tables["orders_dirty"], tables["suppliers"]))
display(findings)
assert audit_orders(tables["orders"], tables["suppliers"]) == []
print("Dirty fixture findings:", len(findings), "| clean data kept separate")
'''),md('''## 4. Demonstrate the join problem and the correction

The first calculation below is deliberately wrong: it sums order value after expanding
receipt detail. The correct SQL aggregates receipts and payment instalments before the
order-level join. This is a financial-control decision, not just a coding preference.
'''),code('''
naive = tables["orders"].merge(tables["grns"], on="order_id", how="left")
correct_value = tables["orders"].amount.sum()
display(pd.DataFrame({"calculation":["Incorrect: sum after detail join","Correct: unique orders"],
    "INR":[naive.amount.sum(),correct_value]}).round(2))
print(f"Illustrative join inflation: {(naive.amount.sum()/correct_value-1):.1%}")
print(CONTROL_TOWER_SQL)
'''),code('''
summary, detail, suppliers = control_tower(tables)
checks = pd.DataFrame({"source":["Orders","Invoices","Payments"],
    "register_total":[tables["orders"].amount.sum(),tables["invoices"].amount.sum(),tables["payments"].amount.sum()],
    "report_total":[detail.amount.sum(),detail.invoiced.sum(),detail.paid.sum()]})
checks["difference"] = checks.report_total-checks.register_total
assert np.allclose(checks.difference, 0, atol=.01)
display(checks.round(2))
'''),md('''## 5. Explore time and supplier performance

The monthly view uses **order issue month**, not receipt month. The supplier chart shows
the twelve suppliers with the most completed orders, selected by volume rather than
worst-looking rates. Each rate excludes incomplete orders; the open-order analysis follows.
These comparisons are descriptive, not supplier performance assessments in the real world.
'''),code('''
monthly = detail.assign(month=pd.to_datetime(detail.order_date).dt.to_period("M").dt.to_timestamp()).groupby("month").amount.sum()
top = suppliers.nlargest(12,"completed").sort_values("late_completed_rate")
fig, axes = plt.subplots(1,2,figsize=(13,5))
axes[0].plot(monthly.index, monthly.values/1e6, marker=".")
axes[0].set(title="Ordered value over time",ylabel="INR million",xlabel="Order month")
axes[0].tick_params(axis="x",rotation=35)
axes[1].barh(top.supplier_id,top.late_completed_rate*100)
axes[1].set(title="Late delivery: 12 highest-volume suppliers",xlabel="Late / completed orders (%)",xlim=(0,100))
finish(fig,"03-procurement-overview")
display(top[["supplier_id","completed","late_completed","overdue_open"]])
'''),md('''## 6. Turn findings into review queues

Overdue invoices and overdue-open orders need different owners. Outstanding value is not
automatically loss, and a missing receipt can reflect export timing. I show separate queues
instead of combining unlike problems into a vague risk score.
'''),code('''
display(pd.Series(summary,name="Value").to_frame())
display(detail.loc[detail.overdue_open,["order_id","project_id","supplier_id","required_by","received_qty","quantity"]])
display(detail.nlargest(10,"overdue")[["order_id","supplier_id","invoiced","paid","overdue"]])
fig,ax=plt.subplots()
by_project=detail.groupby("project_id").overdue.sum().nlargest(10).sort_values()
ax.barh(by_project.index,by_project.values/1e6)
ax.set(title="Where overdue invoice balances are concentrated",xlabel="INR million — top 10 projects")
finish(fig,"03-overdue-exposure")
'''),md('''## 7. Recommendation and limitations

- Buyers investigate overdue-open orders, confirming whether they are still required.
- AP verifies payment holds and missing receipts before chasing all overdue balances alike.
- The analyst reconciles totals on every refresh and records the extract cutoff.
- Material rejection rates should be compared within compatible units. This simplified
  dataset has no defensible cross-material UOM conversion, so I do not use its overall
  quantity rejection percentage to rank real suppliers.

**What this demonstrates:** SQL grain control, quality checks, KPI definitions and actionable
reporting. **What it does not demonstrate:** actual savings, root-cause causality or a live ERP
dashboard. Missing currency/tax/retention/cancellation rules would be discovery requirements.

**Interview discussion:** Why does a detail join inflate totals? Why report open orders beside
completed-order delivery rates? Which exceptions need a business owner rather than automatic correction?
''')]
    save('03_procure_to_pay.ipynb',cells)

def simulation():
    cells=intro('Cash Flow & Estimate-at-Completion Scenarios','How sensitive are completion cost and funding needs to cost pressure and receipt timing?','04-cash-eac')
    cells += [md('''## 2. Separate observations from assumptions

This is a scenario simulator, not a fitted forecasting model. Physical progress, remaining
scope and customer receipt terms are explicit fictional extensions. They are not claimed
to be available from the documented registers. Actual cost is assumed already paid.

I choose the latest 50% snapshot without using its final-cost label. A fixed snapshot makes
scenario comparisons reproducible; it does not represent a typical project.
'''),code('''
from aec.features import cost_features
from aec.analytics import scenario
f = cost_features(tables)
row = f.sort_values("snapshot_date").iloc[-1]
inputs = row[["package_id","snapshot_date","original_budget","progress_assumption","actual_cost","pending_variations"]]
display(inputs.to_frame("Scenario input"))
'''),md('''## 3. Make the cash and cost logic explicit

Remaining base cost = original budget × (1 − assumed progress).
EAC = incurred cost + simulated remaining cost + accepted pending variations.

A shared escalation shock affects all remaining months. Pending variations are accepted
as one package-level event with assumed probability 60%. Payment/receipt timing changes
funding needs; it does not directly change completion cost. Existing commitments are not
added again on top of remaining cost.

Five thousand draws use seed 42. P10/P50/P90 are **scenario quantiles**, not validated forecast
confidence intervals. These distributions and correlations need business-owner challenge.
'''),code('''
settings={"Base":(.06,2),"Cost stress":(.18,2),"Receipt delay":(.06,4)}
results={name:scenario(row.to_dict(),row.original_budget,draws=5000,seed=42,
    escalation=e,receipt_delay=lag) for name,(e,lag) in settings.items()}
comparison=pd.DataFrame([{"scenario":name,"EAC P10":r["eac_p10_p50_p90"][0],
    "EAC P50":r["eac_p10_p50_p90"][1],"EAC P90":r["eac_p10_p50_p90"][2],
    "Funding P50":r["peak_funding_p10_p50_p90"][1]} for name,r in results.items()]).set_index("scenario")
display(comparison.round(0))
'''),code('''
fig,axes=plt.subplots(1,2,figsize=(12,4.8))
for i,(name,r) in enumerate(results.items()):
    lo,mid,hi=np.array(r["eac_p10_p50_p90"])/1e6
    axes[0].errorbar(mid,i,xerr=[[mid-lo],[hi-mid]],fmt="o",capsize=7,color="#3F7285")
    axes[1].plot(range(1,13),np.array(r["monthly_net_cash_p50"])/1e6,marker=".",label=name)
axes[0].set(yticks=range(3),yticklabels=list(results),xlabel="EAC — INR million",title="P10–P90 scenario range; dot = P50")
axes[1].axhline(0,color="#899BA5",linewidth=1)
axes[1].set(title="Timing changes the net cash profile",xlabel="Future month",ylabel="Median net cash — INR million",xticks=range(1,13))
axes[1].legend()
finish(fig,"04-scenarios")
'''),md('''## 4. Sensitivity: which assumption should be challenged first?

Vary one assumption at a time while preserving the same random seed. This isolates
scenario effects; it is not causal inference. Receipt lag should leave EAC unchanged,
while funding changes. I test that invariant below.
'''),code('''
stress=[]
for lag in range(0,7):
    r=scenario(row.to_dict(),row.original_budget,seed=42,receipt_delay=lag)
    stress.append({"receipt_lag":lag,"funding_p50":r["peak_funding_p10_p50_p90"][1],"eac_p50":r["eac_p10_p50_p90"][1]})
sensitivity=pd.DataFrame(stress)
assert sensitivity.eac_p50.nunique()==1
assert results["Cost stress"]["eac_p10_p50_p90"][1]>results["Base"]["eac_p10_p50_p90"][1]
fig,ax=plt.subplots()
ax.plot(sensitivity.receipt_lag,sensitivity.funding_p50/1e6,marker="o")
ax.set(title="Funding sensitivity to customer receipt delay",xlabel="Receipt lag (months)",ylabel="Median peak funding — INR million",xticks=range(7))
finish(fig,"04-funding-sensitivity")
display(sensitivity.round(2))
'''),md('''## 5. Simulation stability is not model validity

More draws should stabilise a chosen model's quantiles, but cannot validate its assumptions.
Compare P50/P90 across seeds below. This checks Monte Carlo variability only. There is no
empirical cash-flow backtest in this dataset.
'''),code('''
stability=[]
for seed in [11,42,73]:
    r=scenario(row.to_dict(),row.original_budget,draws=5000,seed=seed)
    stability.append({"seed":seed,"EAC P50":r["eac_p10_p50_p90"][1],"EAC P90":r["eac_p10_p50_p90"][2]})
display(pd.DataFrame(stability).round(2))
'''),md('''## 6. Decision and next steps

Use the funding sensitivity to discuss collection terms, payment commitments and available
liquidity; use the cost stress to request a revised quantity/rate forecast. Do not replace the
commercial team's forecast with these assumptions.

Before production: obtain authorised remaining quantities, resource rates, actual payment
schedules, retention/tax treatment and opening cash. Estimate distributions from appropriate
history, backtest and have finance review extreme scenarios. No funding savings are claimed.

**Interview discussion:** Why is this Data Science without training an ML model? Why is P90
not a guarantee? Why can late receipts increase funding need without increasing EAC?
''')]
    save('04_cash_flow_eac.ipynb',cells)

def delivery():
    cells=intro('Procurement Delivery Risk','Which newly issued orders should receive early buyer follow-up?','05-delivery-risk')
    cells += [md('''## 2. Define the prediction moment and label

The model scores an order **when it is issued**. A late outcome means full gross receipt
after required-by date. Rejected quantities are separate; delivery completion does not mean
quality acceptance. Open/partial orders have unknown outcomes and must not become negatives.

I start with censoring and label frequency because a model can look successful by ignoring
difficult open orders. Required-by dates may also reflect negotiation or unrealistic planning.
'''),code('''
from aec.features import delivery_features, split_mature, DELIVERY_NUM, DELIVERY_CAT
from aec.models import pipeline, classification_metrics, evaluate_delivery
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score

f=delivery_features(tables)
display(pd.Series({"all_orders":len(f),"labelled_completed":int(f.complete.sum()),
    "unlabelled_open":int((~f.complete).sum()),"late_fraction_completed":f.late.mean()}).to_frame("Value"))
display(f[["order_id","order_date","required_by","completion_date","late","supplier_prior_completed"]].head())
'''),md('''## 3. Features: learn from information already available

Quantity, value, lead days, month and material category are known at issue time. Supplier
history uses only orders completed **before** this order's date, smoothed with a Beta(1,1)
prior. No current-order receipt, payment or final-delay field is a predictor. Numeric imputation,
scaling and category encoding are fitted inside the training pipeline.

Historical features update as earlier orders finish, including during the test period; the
model itself stays frozen. This represents sequential scoring, not one bulk forecast at test start.
'''),code('''
cols=DELIVERY_NUM+DELIVERY_CAT
assert not {"late","completion_date","received_qty"}.intersection(cols)
sample=f.iloc[700]
history=f[(f.supplier_id==sample.supplier_id)&(f.completion_date<sample.order_date)&f.complete]
assert len(history)==sample.supplier_prior_completed
display(pd.DataFrame({"feature":cols,"available_at_issue":[True]*len(cols)}))
print("One audited history count:",len(history),"completed prior orders")
'''),md('''## 4. Split by time and by when the label becomes known

Training requires issue and completion before January 2023. Validation requires issue from
January 2023 and completion before July 2024. Later orders form the held-out test set.
Boundary-spanning outcomes are purged. Random splitting would hide the later regime shift.
'''),code('''
train,val,test=split_mature(f,"order_date","late")
parts={"Train":train,"Validation":val,"Test":test}
display(pd.DataFrame([{"split":name,"rows":len(part),"issue_start":part.order_date.min(),
    "issue_end":part.order_date.max(),"late_rate":part.late.mean()} for name,part in parts.items()]))
fig,ax=plt.subplots()
ax.bar(list(parts),[p.late.mean()*100 for p in parts.values()])
ax.set(title="Late-delivery prevalence shifts over time",ylabel="Late / labelled completed orders (%)",ylim=(0,100))
finish(fig,"05-label-shift")
'''),md('''## 5. Compare a simple baseline before increasing complexity

I compare a constant-prior baseline, logistic regression and two shallow boosting settings.
Validation **average precision** selects the candidate because prioritising late orders is the
task. This is a small candidate comparison, not an exhaustive tuning exercise. Test results
must not change the selected model.
'''),code('''
candidates={"dummy":DummyClassifier(strategy="prior"),"logistic":LogisticRegression(max_iter=1000)}
for leaves in [7,15]:
    candidates[f"boosting_{leaves}"]=HistGradientBoostingClassifier(max_leaf_nodes=leaves,max_iter=100,
        l2_regularization=2,early_stopping=False,random_state=42)
fitted={}; comparison=[]
for name,estimator in candidates.items():
    fitted[name]=pipeline(estimator,DELIVERY_NUM,DELIVERY_CAT).fit(train[cols],train.late)
    probability=fitted[name].predict_proba(val[cols])[:,1]
    comparison.append({"model":name,"validation_AP":average_precision_score(val.late,probability)})
comparison=pd.DataFrame(comparison).sort_values("validation_AP",ascending=False)
selected=comparison.iloc[0].model
display(comparison)
print("Selected on validation only:",selected)
'''),md('''## 6. Translate scores into a review threshold

The demonstration assigns cost 5 to a missed late order and cost 1 to unnecessary follow-up.
These are scenario loss units, not measured money. The validation set selects the threshold;
the same threshold is then frozen for test evaluation. Review capacity could justify a different
policy and must be agreed with buyers.
'''),code('''
vp=fitted[selected].predict_proba(val[cols])[:,1]
thresholds=np.arange(.1,.91,.05)
losses=[5*np.sum((vp<t)&(val.late==1))+np.sum((vp>=t)&(val.late==0)) for t in thresholds]
threshold=float(thresholds[np.argmin(losses)])
p=fitted[selected].predict_proba(test[cols])[:,1]
display(pd.DataFrame({"selected":classification_metrics(test.late,p,threshold),
    "dummy":classification_metrics(test.late,fitted["dummy"].predict_proba(test[cols])[:,1],threshold)}))
print(f"Frozen threshold: {threshold:.2f}; test review workload: {np.mean(p>=threshold):.1%}")
fig,ax=plt.subplots()
ax.plot(thresholds,losses,marker="."); ax.axvline(threshold,linestyle="--",color="#B6A78E")
ax.set(title="Threshold chosen using validation loss",xlabel="Probability threshold",ylabel="Assumed review-loss units")
finish(fig,"05-threshold")
'''),md('''## 7. Check calibration, explanations and weak spots

The shared audit function recomputes the same locked experiment and adds category slices,
calibration bins, a fixed-model bootstrap and permutation importance. A high ranking score
does not imply accurate probabilities. Permutation importance is global association, not a
causal explanation for an individual supplier.
'''),code('''
report,queue=evaluate_delivery(f)
assert report["selected_model"]==selected
assert np.isclose(report["test"]["average_precision"],average_precision_score(test.late,p))
bins=pd.DataFrame(report["calibration_bins"])
importance=pd.Series(report["permutation_importance"]).sort_values()
fig,axes=plt.subplots(1,2,figsize=(13,5))
axes[0].plot([0,1],[0,1],linestyle="--",color="#B6A78E",label="Perfect calibration")
axes[0].plot(bins.predicted,bins.observed,marker="o",label="Observed test bins")
axes[0].set(xlabel="Mean predicted probability",ylabel="Observed late rate",title="Ranking is not calibration",xlim=(0,1),ylim=(0,1));axes[0].legend()
axes[1].barh(importance.index,importance.values);axes[1].set(title="Global permutation importance",xlabel="Drop in test average precision")
finish(fig,"05-calibration-importance")
display(pd.DataFrame(report["slices"]).T[["n","average_precision","precision","recall"]])
display(queue.head(8))
display(Markdown(f"**Brier (lower is better):** model {report['test']['brier']:.3f}; dummy {report['baseline_test']['brier']:.3f}. **AP bootstrap 95%:** {report['test_ap_bootstrap_95'][0]:.3f}–{report['test_ap_bootstrap_95'][1]:.3f}."))
'''),md('''## 8. What I would recommend

In the committed seed-42 run, logistic regression wins validation selection. Test ranking
improves on the dummy, but Brier probability error is worse under the simulated shift. I would
not deploy these probabilities. The high-recall threshold also creates substantial buyer work.

Next: validate labels, compare to operational rules, assess capacity, reserve new calibration
data and run shadow review on authorised real observations. Test-period findings are diagnostic;
they are not used here to tune a better-looking answer on the same holdout.

**Limits:** synthetic signal recovery, completed-order selection bias, few candidate models,
correlated supplier observations and bootstrap intervals conditional on one fitted model.
No prevented delays or cost savings are claimed.

**Interview discussion:** Why can ranking improve while probability accuracy worsens? What
information was unavailable at order issue? How would a buyer's daily capacity change the threshold?
''')]
    save('05_delivery_risk.ipynb',cells)

def cost():
    cells=intro('Cost Overrun & Variation Risk','Which packages merit commercial review at 50% assumed progress?','06-cost-risk')
    cells += [md('''## 2. Define a decision point instead of predicting with hindsight

I use one 50% progress snapshot per package. Original budget normalises the final-cost
target so that a large package does not dominate every comparison. Original budget remains
a feature and INR error is also reported. Final cost and completion date are labels, never inputs.

Physical progress and outcome cost are fictional extensions. Their availability is not
established by the register documentation. The cost and procurement populations are separate.
'''),code('''
from aec.features import cost_features,split_mature,COST_NUM,COST_CAT
from aec.models import pipeline,evaluate_cost
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

f=cost_features(tables)
assert not f.package_id.duplicated().any()
assert f.progress_assumption.eq(.5).all()
display(f[["package_id","snapshot_date","original_budget","actual_ratio","pending_ratio","final_ratio"]].head())
print("Decision snapshots:",len(f),"| known final outcomes:",f.final_ratio.notna().sum())
'''),md('''## 3. Explore only training data before choosing a model

The same time boundaries require outcomes to be known before training/validation cutoffs.
There is one package per fictional commercial project, so projects do not cross partitions.
The scatter plot uses training records only; apparent relationships reflect the generator.
'''),code('''
train,val,test=split_mature(f,"snapshot_date","final_ratio")
assert not set(train.project_id)&set(test.project_id)
val=val.sort_values("snapshot_date")
select=val.iloc[:len(val)//2]; calibration=val.iloc[len(val)//2:]
display(pd.DataFrame([{"partition":n,"n":len(p),"start":p.snapshot_date.min(),"end":p.snapshot_date.max()}
    for n,p in [("Train",train),("Select",select),("Calibrate",calibration),("Test",test)]]))
fig,axes=plt.subplots(1,2,figsize=(12,4.8))
axes[0].hist(train.final_ratio,bins=22,color="#3F7285",edgecolor="white")
axes[0].axvline(1.05,color="#B6A78E",linestyle="--",label="5% review threshold")
axes[0].set(title="Training final-cost distribution",xlabel="Final cost / original budget",ylabel="Packages");axes[0].legend()
axes[1].scatter(train.actual_ratio,train.final_ratio,s=18,alpha=.5)
axes[1].set(title="Training relationship, not causality",xlabel="Cost incurred / original budget at 50%",ylabel="Final cost / original budget")
finish(fig,"06-training-exploration")
'''),md('''## 4. Compare baseline, regularised regression and boosting

All preprocessing is trained only on training rows. Median prediction provides the minimum
comparison; ridge limits coefficient size; shallow boosting tests nonlinear patterns. Select
by MAE on the first validation half. Reserve the second half for interval calibration.
'''),code('''
cols=COST_NUM+COST_CAT
assert not {"final_cost","final_ratio","completion_date"}.intersection(cols)
candidates={"dummy":DummyRegressor(strategy="median"),"ridge":Ridge(alpha=10),
    "boosting":HistGradientBoostingRegressor(max_iter=100,max_leaf_nodes=7,l2_regularization=3,
        early_stopping=False,random_state=42)}
fitted={name:pipeline(est,COST_NUM,COST_CAT).fit(train[cols],train.final_ratio) for name,est in candidates.items()}
scores={name:mean_absolute_error(select.final_ratio,model.predict(select[cols])) for name,model in fitted.items()}
selected=min(scores,key=scores.get)
display(pd.Series(scores,name="Selection MAE — budget ratio").sort_values().to_frame())
print("Selected before inspecting test:",selected)
'''),md('''## 5. Show uncertainty, not only one forecast

Absolute residuals from the separate calibration subset define a split-conformal interval.
The finite-sample 90% quantile rounds up. Temporal drift can violate exchangeability, so I
report actual test coverage **and width** rather than promising a 90% guarantee.
'''),code('''
model=fitted[selected]
residual=np.abs(calibration.final_ratio-model.predict(calibration[cols]))
level=min(1,np.ceil((len(calibration)+1)*.9)/len(calibration))
halfwidth=float(np.quantile(residual,level,method="higher"))
prediction=model.predict(test[cols])
coverage=np.mean((test.final_ratio>=prediction-halfwidth)&(test.final_ratio<=prediction+halfwidth))
display(pd.Series({"test_MAE_ratio":mean_absolute_error(test.final_ratio,prediction),
    "dummy_MAE_ratio":mean_absolute_error(test.final_ratio,fitted["dummy"].predict(test[cols])),
    "test_MAE_INR":mean_absolute_error(test.final_cost,prediction*test.original_budget),
    "nominal_coverage":.9,"observed_coverage":coverage,"interval_halfwidth_ratio":halfwidth}).to_frame("Value"))
fig,axes=plt.subplots(1,2,figsize=(12,4.8))
axes[0].scatter(test.final_ratio,prediction,alpha=.65,s=24)
lim=[min(test.final_ratio.min(),prediction.min())-.05,max(test.final_ratio.max(),prediction.max())+.05]
axes[0].plot(lim,lim,linestyle="--",color="#B6A78E")
axes[0].set(title="Held-out point predictions",xlabel="Observed final-cost ratio",ylabel="Predicted final-cost ratio")
ix=np.argsort(test.snapshot_date.to_numpy())[:20]
axes[1].errorbar(range(20),prediction[ix],yerr=halfwidth,fmt="o",capsize=3,label="Prediction and interval")
axes[1].scatter(range(20),test.final_ratio.to_numpy()[ix],marker="x",color="#2D4653",label="Observed outcome")
axes[1].set(title="First 20 test packages by snapshot date",xlabel="Package position (not all test cases)",ylabel="Final-cost ratio");axes[1].legend(fontsize=9)
finish(fig,"06-predictions-intervals")
'''),md('''## 6. Translate the forecast into investigation

A forecast above 105% of original budget creates a review flag. It is not a calibrated overrun
probability and does not approve a budget change. Check pending variations, quantity/rate
assumptions and remaining scope with a commercial owner.
'''),code('''
report,queue=evaluate_cost(f)
assert report["selected_model"]==selected
assert np.isclose(report["test_mae_ratio"],mean_absolute_error(test.final_ratio,prediction))
display(queue.head(8).round(2))
importance=pd.Series(report["permutation_importance"]).sort_values()
fig,ax=plt.subplots()
ax.barh(importance.index,importance.values)
ax.set(title="Which features support held-out accuracy?",xlabel="Increase in ratio MAE after permutation")
finish(fig,"06-importance")
print("Constant feature check:",train[COST_NUM].nunique()[lambda x:x==1].index.tolist())
'''),md('''## 7. Interpretation and limits

In the committed seed-42 run, ridge beats the median baseline on test MAE. The interval
coverage is high but the interval width is substantial. These are two different aspects of
usefulness: a wide interval can cover many outcomes without supporting a precise decision.

Assumed progress is constant because this model uses only the 50% milestone; it contributes
no discrimination here. Permutation importance is not proof of causal cost drivers, especially
with correlated cost features. Next iteration could remove constants without changing the
prediction-time contract, then validate on a newly held-out period.

Before production: reconcile actual cost records, verify physical progress and remaining
scope, broaden the project population and conduct prospective commercial review. No real
cost-overrun reduction or savings has been demonstrated.

**Interview discussion:** Why a budget ratio and an INR metric? Why separate selection from
calibration? Why does high coverage not make a forecast precise? Why is an overrun flag not a probability?
''')]
    save('06_cost_overrun.ipynb',cells)

if __name__=='__main__':
    analyst();simulation();delivery();cost()
    print('Authored four notebooks; execute and validate before committing.')
