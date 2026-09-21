import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {modules} from '../src/modules/catalog.js';
import {scoreRecord} from '../src/modules/ModulePages.js';
test('All generated module records reconcile with exported models and temporal splits',()=>{
 const all={};for(const m of modules){const d=JSON.parse(fs.readFileSync('public/data/modules/'+m.id+'.json'));all[m.id]=d;assert.equal(d.rows.length,5000);assert.equal(new Set(d.rows.map(r=>r.record_id)).size,5000);assert.equal(Math.round(d.rows.reduce((s,r)=>s+r[m.amountField],0)*100)/100,d.analysis.total);for(const r of d.rows){assert(Math.abs(scoreRecord(d.model,r).score-r.risk_score)<1e-6);if(r.evaluation_split==='Train')assert(r.record_date<'2024-06-01'&&r.label_available_date<'2024-08-01');if(r.evaluation_split==='Test')assert(r.record_date>='2024-08-01');}}
 const hr=new Map(all['construction-hr'].rows.map(r=>[r.record_id,r]));for(const r of all['construction-payroll'].rows){const input=hr.get(r.attendance_id);assert.equal(input.employee_id,r.employee_id);assert.equal(r.paid_days,input.worked_days+input.paid_leave_days);if(r.status==='Paid')assert.equal(input.status,'Approved');assert(Math.abs(r.gross_pay-r.deductions-r.net_pay)<.011);}
});
test('Every module has project and app output plus its workbook',()=>{for(const m of modules){for(const p of ['dist/modules/'+m.id+'.html','dist/ai-app/module-'+m.id+'.html','dist/data/modules/'+m.id+'.xlsx'])assert(fs.statSync(p).size>0,p);const html=fs.readFileSync('dist/modules/'+m.id+'.html','utf8');for(const file of ['business-analysis.md','implementation.md','data-analysis.md','machine-learning-ai.md'])assert(html.includes('https://github.com/AtulIwale/Portfolio/blob/main/modules/'+m.id+'/'+file));}});
