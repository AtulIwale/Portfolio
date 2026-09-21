import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
// Run from a scratch build directory linked to the primary runtime dependencies.
const root=process.env.MODULE_SITE_ROOT||process.cwd();
const id=process.argv[2],out=process.env.MODULE_OUTPUT||path.join(root,'outputs','workbooks');
const d=JSON.parse(await fs.readFile(path.join(root,'public/data/modules',id+'.json'),'utf8')),m=d.module;
const datasetVersion=d.version;
const {implementationStages}=await import(path.join(root,'src/modules/catalog.js'));
await fs.mkdir(out,{recursive:true});await fs.mkdir(path.join(out,'previews',id),{recursive:true});
const wb=Workbook.create(),names=['Summary','Records','Details','Events','Masters','Dictionary','Requirements','Implementation','Model'];const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const fields=[...new Set(d.rows.flatMap(Object.keys))],fieldcol=f=>col(fields.indexOf(f));
const fmt='#,##0.00;[Red](#,##0.00);–',dateKey=k=>k.endsWith('_date')||k==='record_date';
function grid(name,headers,rows,{wide=false}={}){
 const s=sheets[name],end=col(headers.length-1),last=rows.length+1;
 s.showGridLines=false;s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(1);
 s.getRange(`A1:${end}${last}`).values=[headers,...rows];
 s.getRange(`A1:${end}${last}`).format.font={name:'Arial',color:'#2D4653'};
 s.getRange(`A1:${end}${last}`).format.rowHeight=34;
 s.getRange(`A2:${end}${last}`).format.wrapText=true;
 s.getRange(`A1:${end}${last}`).format.verticalAlignment='center';
 s.getRange(`A1:${end}1`).format={fill:'#2D4653',font:{name:'Arial',bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:42};
 s.getRange(`A1:${end}${last}`).format.columnWidth=wide?36:19;
 s.getRange(`A1:A${last}`).format.columnWidth=wide?26:20;
 if(wide){s.getRange(`A2:${end}${last}`).format.wrapText=true;s.getRange(`A2:${end}${last}`).format.rowHeight=82;}
 if(rows.length)s.tables.add(`A1:${end}${last}`,true,name+'Table');
 return s;
}
const typed=(r,keys)=>keys.map(k=>dateKey(k)&&r[k]?new Date(r[k]+'T00:00:00Z'):r[k]??null);
const rec=grid('Records',fields,d.rows.map(r=>typed(r,fields)));
fields.forEach((f,i)=>{const v=d.rows.find(r=>r[f]!==null)?.[f],r=rec.getRange(`${col(i)}2:${col(i)}5001`);if(dateKey(f))r.setNumberFormat('yyyy-mm-dd');else if(typeof v==='number')r.setNumberFormat(f.includes('pct')||f.includes('_rate')&&!['unit_rate','overtime_rate'].includes(f)||f==='risk_score'?'0.0%':Number.isInteger(v)&&!/(amount|price|value|salary|pay|cost)/.test(f)?'0':fmt);});
const cell=(f,r)=>fieldcol(f)+r;
const formulaSets={
 'tender-contracts':{},
 'procurement-subcontracting':{order_amount:r=>`ROUND(${cell('quantity',r)}*${cell('unit_rate',r)},2)`},
 'inventory-warehouse':{closing_qty:r=>`${cell('opening_qty',r)}+${cell('signed_qty',r)}`,movement_value:r=>`${cell('movement_qty',r)}*${cell('item_value',r)}`},
 'real-estate-sales':{agreed_price:r=>`ROUND(${cell('list_price',r)}*(1-${cell('discount_pct',r)}),2)`},
 'construction-assets':{closing_book_value:r=>`ROUND(MAX(${cell('residual_value',r)},${cell('opening_book_value',r)}-${cell('depreciation',r)}),2)`},
 'receivables-payables':{tax_amount:r=>`ROUND(${cell('net_amount',r)}*${cell('tax_rate',r)},2)`,gross_amount:r=>`${cell('net_amount',r)}+${cell('tax_amount',r)}`,outstanding:r=>`ROUND(${cell('gross_amount',r)}-${cell('settled_amount',r)}-${cell('unposted_amount',r)},2)`},
 'construction-hr':{worked_days:r=>`${cell('scheduled_days',r)}-${cell('paid_leave_days',r)}-${cell('absent_days',r)}`},
 'construction-payroll':{basic_pay:r=>`ROUND(${cell('monthly_salary',r)}*${cell('paid_days',r)}/${cell('scheduled_days',r)},2)`,overtime_pay:r=>`ROUND(${cell('overtime_hours',r)}*${cell('overtime_rate',r)},2)`,gross_pay:r=>`${cell('basic_pay',r)}+${cell('overtime_pay',r)}+${cell('allowance',r)}`,deductions:r=>`ROUND(${cell('gross_pay',r)}*${cell('demonstration_deduction_rate',r)},2)`,net_pay:r=>`${cell('gross_pay',r)}-${cell('deductions',r)}`}
};
for(const [f,fn] of Object.entries(formulaSets[id])){rec.getRange(fieldcol(f)+'2:'+fieldcol(f)+'5001').formulas=d.rows.map((_,i)=>['='+fn(i+2)]);}
for(const [name,key] of [['Details','details'],['Events','events']]){const f=[...new Set(d[key].flatMap(Object.keys))];const s=grid(name,f,d[key].map(r=>typed(r,f)));f.forEach((k,i)=>{if(dateKey(k))s.getRange(`${col(i)}2:${col(i)}${d[key].length+1}`).setNumberFormat('yyyy-mm-dd');else if(typeof d[key][0]?.[k]==='number')s.getRange(`${col(i)}2:${col(i)}${d[key].length+1}`).setNumberFormat(fmt)});}
const masters=[];for(const key of ['projects','partners','employees','items'])for(const r of d[key]){const keys=Object.keys(r);masters.push([key,r[keys[0]],r[keys[1]],JSON.stringify(r)]);}grid('Masters',['Master type','Master ID','Name','Attributes (JSON)'],masters);sheets.Masters.getRange('D1:D'+(masters.length+1)).format.columnWidth=85;
const meanings={record_id:'Stable primary key; used unchanged in Excel, JSON and app.',record_date:'Feature observation date. All model inputs are known at this snapshot.',status:'Workflow snapshot at reporting date; excluded from model features.',type:'Module-specific document or record category.',project_id:'Foreign key to the shared project master.',risk_score:'Exported training-tree leaf frequency. Uncalibrated; not a live Excel model.',evaluation_split:'Train: Jan–May with matured labels. Test: Aug–Oct. June–July/unlabelled excluded.',label_available_date:'Earliest date the simulated outcome can be known. Prevents temporal label leakage.',movement_value:'Absolute physical movement value including quarantined receipts; not net posted stock value.',outstanding:'Posted gross less settlement; draft/disputed balances are classified as unposted.',net_pay:'Calculated gross less demonstration deductions; held rows are not payable.',source_id:'Sample source-record reference; not a complete downstream allocation.',opening_book_value:'Per-asset monthly carrying-value snapshot, never sum across months.',prior_delay_rate:'Historical supplier delay rate available before the order date.',prior_late_rate:'Historical entity late-payment rate available before invoice date.'};
const dictionary=[];
for(const [sheet,rows] of [['Records',d.rows],['Details',d.details],['Events',d.events]])for(const f of [...new Set(rows.flatMap(Object.keys))]){const value=rows.find(r=>r[f]!=null)?.[f];dictionary.push([sheet,f,dateKey(f)?'Date':typeof value==='number'?'Number':'Text',m.features.includes(f)?'Model input':f===m.target?'Outcome (post observation)':f in formulaSets[id]?'Calculated':'Source / reference',meanings[f]||f===m.target&&m.targetLabel||f.replaceAll('_',' ')+'; synthetic demonstration field.',m.features.includes(f)?'Captured at record date':f===m.target?'1 = event, 0 = no event; blank = ineligible':'See module grain and source notes']);}
grid('Dictionary',['Sheet','Field','Type','Role','Meaning','Timing / null policy'],dictionary,{wide:true});
grid('Requirements',['Requirement','Key concepts','Business rule','Acceptance test'],m.requirements,{wide:true});
const impl=grid('Implementation',['Phase','Start week','End week','Role','Effort days','Daily rate INR','Cost INR','Exit gate'],implementationStages.map(([s,a,b,role,days,rate,gate])=>[s,a,b,role,days,rate,null,gate]));impl.getRange('A1:A6').format.columnWidth=28;impl.getRange('D1:D6').format.columnWidth=28;impl.getRange('H1:H6').format.columnWidth=65;impl.getRange('H2:H6').format.wrapText=true;impl.getRange('A2:H6').format.rowHeight=44;impl.getRange('G2:G6').formulas=implementationStages.map((_,i)=>['=E'+(i+2)+'*F'+(i+2)]);impl.getRange('F2:G11').setNumberFormat(fmt);impl.getRange('F8:G11').values=[['Base cost',null],['Contingency rate',.15],['Contingency',null],['Total budget',null]];impl.getRange('G8').formulas=[['=SUM(G2:G6)']];impl.getRange('G9').setNumberFormat('0%');impl.getRange('G10').formulas=[['=G8*G9']];impl.getRange('G11').formulas=[['=G8+G10']];impl.getRange('A14:H14').merge();impl.getRange('A14').values=[['Illustrative 12-week, two-site pilot. Rates exclude vendor licensing, hardware, statutory localization and taxes.']];impl.getRange('A14:H14').format.wrapText=true;impl.getRange('A14:H14').format.rowHeight=42;
const modelRows=[['Model',d.model.kind],['Target',m.targetLabel],['Inputs',m.features.join(', ')],['Depth / minimum leaf','4 / 60'],...Object.entries(d.model.metrics).map(([k,v])=>[k,typeof v==='object'?JSON.stringify(v):v]),['Limitations',d.model.limitations],['Inference','Use the exported model nodes in canonical JSON; Excel risk scores are frozen for this dataset version.'],['Reference',m.reference],['Provenance',d.provenance]];grid('Model',['Item','Value'],modelRows,{wide:true});sheets.Model.getRange('B1:B'+(modelRows.length+1)).format.columnWidth=100;sheets.Model.getRange('A2:B'+(modelRows.length+1)).format.rowHeight=35;sheets.Model.getRange('A'+(modelRows.length-3)+':B'+(modelRows.length+1)).format.rowHeight=110;
const s=sheets.Summary;s.showGridLines=false;s.getRange('A1:F32').format.font={name:'Arial',color:'#2D4653'};s.getRange('A1:F32').format.columnWidth=19;s.getRange('A1:F2').merge();s.getRange('A1').values=[[m.name]];s.getRange('A1:F2').format={fill:'#2D4653',font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:25};
const notes=[[4,datasetVersion+' | SYNTHETIC DATA | Currency: INR'],[6,m.grain+'.'],[8,'Reporting date: 1 March 2025. Records: January–October 2024.'],[10,'Download once; reuse the same IDs for requirements, implementation, analysis and ML.'],[24,m.reference],[27,'Demonstration assumptions: simplified taxes, deductions, approval thresholds and planning rates. No real personal data.'],[30,'Read Dictionary for timing and field roles. Model scores are frozen; changing data does not retrain the model.']];for(const [r,t] of notes){s.getRange(`A${r}:F${r+1}`).merge();s.getRange('A'+r).values=[[t]];s.getRange(`A${r}:F${r+1}`).format.wrapText=true;}
s.getRange('A13:D20').values=[['Metric','Value',null,null],['Primary records',null,null,null],[m.metric,null,null,null],['Median record value',null,null,null],['Labelled outcomes',null,null,null],['Observed events',null,null,null],['Supporting details',d.details.length,null,null],['Capture events',d.events.length,null,null]];s.getRange('A13:B13').format={fill:'#4F7E8F',font:{bold:true,color:'#FFFFFF'}};s.getRange('A13:A20').format.columnWidth=33;s.getRange('B13:B20').format.columnWidth=25;s.getRange('A14:A20').format.wrapText=true;s.getRange('A13:F20').format.rowHeight=32;s.getRange('B14').formulas=[['=COUNTA(Records!A2:A5001)']];s.getRange('B15').formulas=[['=SUM(Records!'+fieldcol(m.amountField)+'2:'+fieldcol(m.amountField)+'5001)']];s.getRange('B16').formulas=[['=MEDIAN(Records!'+fieldcol(m.amountField)+'2:'+fieldcol(m.amountField)+'5001)']];s.getRange('B17').formulas=[['=COUNT(Records!'+fieldcol(m.target)+'2:'+fieldcol(m.target)+'5001)']];s.getRange('B18').formulas=[['=SUM(Records!'+fieldcol(m.target)+'2:'+fieldcol(m.target)+'5001)']];s.getRange('B14:B20').setNumberFormat(fmt);s.getRange('B14').setNumberFormat('#,##0');s.getRange('B17:B20').setNumberFormat('#,##0');s.freezePanes.freezeRows(2);
await wb.recalculate();
const got=s.getRange('B14:B18').values.flat();const expected=[5000,d.analysis.total,d.analysis.median,d.analysis.labelled,d.analysis.eventsObserved];expected.forEach((v,i)=>{if(Math.abs(Number(got[i])-v)>.011)throw Error(id+' summary mismatch '+i+': '+got[i]+' / '+v)});
for(const f of Object.keys(formulaSets[id])){const vals=rec.getRange(fieldcol(f)+'2:'+fieldcol(f)+'5001').values.flat();vals.forEach((v,i)=>{if(Math.abs(Number(v)-d.rows[i][f])>.011)throw Error(id+' formula mismatch '+f+' row '+i)});}
for(const name of names){const error=sheets[name].getUsedRange().values.flat().find(v=>typeof v==='string'&&/^#(REF!|DIV\/0!|VALUE!|NAME\?|NUM!|N\/A)/.test(v));if(error)throw Error(name+': '+error);}
await fs.writeFile(path.join(out,id+'-verification.json'),JSON.stringify({summary:got,expected,formulasChecked:Object.keys(formulaSets[id]),inspect:await wb.inspect({kind:'region',sheetId:'Summary',range:'A13:B20',maxChars:2000})}));
for(const name of names){const range=name==='Summary'?'A1:F20':name==='Implementation'?'A1:H11':name==='Model'?'A1:B7':name==='Requirements'?'A1:D5':name==='Dictionary'?'A1:F5':'A1:F7';const preview=await wb.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(path.join(out,'previews',id,name+'.png'),new Uint8Array(await preview.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(out,id+'.xlsx'));
await fs.copyFile(path.join(out,id+'.xlsx'),path.join(root,'public/data/modules',id+'.xlsx'));
console.log(id+': saved, 5,000 records; formulas reconciled; '+names.length+' sheet previews rendered.');
