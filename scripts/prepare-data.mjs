import fs from 'node:fs/promises';
import {modules} from '../src/modules/catalog.js';
const root=new URL('../',import.meta.url),summary={};
for(const m of modules){
 const file=new URL('public/data/modules/'+m.id+'.json',root),d=JSON.parse(await fs.readFile(file,'utf8'));
 const frozen=JSON.parse(await fs.readFile(new URL('models/'+m.id+'.json',root),'utf8'));
 d.model=frozen.model;d.analysis=frozen.analysis;
 for(const r of d.rows){let i=0;while(d.model.nodes[i].left!==-1){const n=d.model.nodes[i];i=r[d.model.features[n.feature]]<=n.threshold?n.left:n.right;}r.risk_score=Number(d.model.nodes[i].probability.toFixed(6));r.evaluation_split=r[m.target]===null?'Excluded / unlabelled':r.record_date<'2024-06-01'&&r.label_available_date<'2024-08-01'?'Train':r.record_date>='2024-08-01'?'Test':'Excluded / unlabelled';}
 if(d.rows.length!==5000)throw Error(m.id+' row count mismatch');
 await fs.writeFile(file,JSON.stringify(d));
 summary[m.id]={rows:d.rows.length,model:d.model.kind,version:d.version};
}
await fs.writeFile(new URL('public/data/modules/validation.json',root),JSON.stringify({version:'AEC-DEMO-2026.1',modules:summary,note:'Run npm test for data validation. Canonical records are seeded; these apps use the checked-in trained models.'},null,2));
console.log('Prepared 40,000 records and eight exported models.');
