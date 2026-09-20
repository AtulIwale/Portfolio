"""python -m aec.run: reproducible end-to-end portfolio evidence."""
import argparse
from pathlib import Path
from .data import generate,save_dataset,write_json,records
from .features import delivery_features,cost_features
from .models import evaluate_delivery,evaluate_cost
from .analytics import control_tower,audit_orders,scenario,CONTROL_TOWER_SQL
from .evidence import evaluate_retrieval

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--orders',type=int,default=3600)
    parser.add_argument('--packages',type=int,default=750)
    parser.add_argument('--output',default='outputs')
    args=parser.parse_args(); out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    tables=generate(args.seed,args.orders,args.packages)
    manifest=save_dataset(tables,Path('data'),args.seed)
    print('Generated',sum(len(f) for f in tables.values()),'rows',flush=True)
    summary,detail,suppliers=control_tower(tables)
    write_json(out/'control_tower.json',summary)
    write_json(out/'supplier_scorecard.json',records(suppliers))
    write_json(out/'reconciliation_findings.json',audit_orders(tables['orders_dirty'],tables['suppliers']))
    delivery_report,delivery_scores=evaluate_delivery(delivery_features(tables))
    write_json(out/'delivery_metrics.json',delivery_report)
    write_json(out/'delivery_review_queue.json',records(delivery_scores.head(30)))
    print('Delivery evaluation complete',flush=True)
    cost=cost_features(tables); cost_report,cost_scores=evaluate_cost(cost)
    write_json(out/'cost_metrics.json',cost_report)
    write_json(out/'cost_review_queue.json',records(cost_scores.head(30)))
    sample=cost.sort_values('snapshot_date').iloc[-1]
    scenarios={}
    for name,escalation,receipt_delay in [('base',.06,2),('cost_stress',.18,2),('receipt_delay',.06,4)]:
        scenarios[name]=scenario(sample.to_dict(),sample.original_budget,seed=args.seed,
            escalation=escalation,receipt_delay=receipt_delay)
    write_json(out/'cash_scenarios.json',{'package_id':sample.package_id,'assumptions':{
        k:float(sample[k]) for k in ['original_budget','progress_assumption','actual_cost','pending_variations']},'scenarios':scenarios})
    write_json(out/'retrieval_evaluation.json',evaluate_retrieval())
    write_json(out/'run_manifest.json',{'seed':args.seed,'data_manifest':'../data/manifest.json',
        'synthetic_only':True,'model_selection':'validation only; no test tuning','rows':sum(len(f) for f in tables.values())})
    print('Complete. Inspect outputs/ metrics, scenarios, review queues and evidence evaluation.',flush=True)

if __name__=='__main__': main()
