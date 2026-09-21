import fs from 'node:fs';
import {modules,datasetVersion} from '../src/modules/catalog.js';
const out=new URL('../public/data/modules/',import.meta.url);fs.mkdirSync(out,{recursive:true});
let seed=20260921;const rand=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296;};
const int=(a,b)=>a+Math.floor(rand()*(b-a+1)),pick=a=>a[int(0,a.length-1)],round=x=>Math.round(x*100)/100;
const pad=(n,k=5)=>String(n).padStart(k,'0'),iso=d=>new Date(d).toISOString().slice(0,10),add=(d,n)=>iso(new Date(d).getTime()+n*86400000);
const projects=Array.from({length:20},(_,i)=>({project_id:'PRJ-'+pad(i+1,3),project_name:'Demonstration '+pick(['Housing','Infrastructure','Commercial','Mixed-use'])+' '+(i+1),region:pick(['West','South','North','East'])}));
const partners=Array.from({length:250},(_,i)=>({partner_id:'ORG-'+pad(i+1,3),partner_name:'Fictional enterprise '+(i+1),prior_delay_rate:round(rand()*.65)}));
const employees=Array.from({length:500},(_,i)=>({employee_id:'EMP-'+pad(i+1,3),employee_name:'Synthetic employee '+(i+1),role:pick(modules[6].types),monthly_salary:int(18,100)*1000,project_id:projects[i%20].project_id}));
const items=Array.from({length:100},(_,i)=>({item_id:'ITM-'+pad(i+1,3),item_name:pick(['Rebar','Cement','Aggregate','Pipe','Formwork','Cable'])+' grade '+(i+1),uom:pick(['kg','m','each']),unit_value:int(50,2000)}));
const all={};
for(const m of modules){
 const rows=[],details=[],events=[],balances=new Map();
 for(let i=0;i<5000;i++){
  const month=Math.floor(i/500),date=`2024-${pad(month+1,2)}-${pad(1+i%28,2)}`,id=m.prefix+'-'+pad(i+1),partner=partners[i%250];
  const r={record_id:id,record_date:date,project_id:projects[i%20].project_id,type:pick(m.types),status:pick(m.statuses)};
  let probability=.2,eligible=true;
  if(m.id==='tender-contracts'){
   Object.assign(r,{partner_id:partner.partner_id,boq_revision:int(1,4),bid_count:int(1,6),scope_changes:int(0,5),approval_levels:int(2,4),planned_days:int(20,60),package_value:int(50,800)*10000,payment_days:pick([30,45,60]),retention_pct:pick([.025,.05,.1]),contract_id:null,variation_amount:0,variation_status:pick(['None','Pending','Approved'])});
   probability=.07+.065*r.scope_changes+.04*(r.approval_levels-2)+.03*(r.bid_count>4)+.16*(r.planned_days<30);
   eligible=['Awarded','Contract active','Contract closed'].includes(r.status);if(eligible){r.contract_id='CON-'+pad(i+1);r.variation_amount=r.variation_status==='None'?0:round(r.package_value*rand()*.15);}
   for(let b=0;b<r.bid_count;b++)details.push({detail_id:id+'-B'+(b+1),record_id:id,bidder_id:partners[(i+b)%250].partner_id,bid_amount:round(r.package_value*(.8+rand()*.4)),technical_score:int(45,100),boq_revision:r.boq_revision,currency:'INR'});
  }
  if(m.id==='procurement-subcontracting'){
   r.status=rand()<.65?'Completed':pick(m.statuses);
   const qty=int(10,500),rate=int(100,5000),amount=qty*rate;
   Object.assign(r,{partner_id:partner.partner_id,requisition_id:'REQ-'+pad(i+1),item_id:r.type.includes('PO')?items[i%100].item_id:null,trade:r.type.includes('subcontract')||r.type.includes('work order')?pick(['Civil','MEP','Finishes']):null,quantity:qty,unit_rate:rate,order_amount:amount,budget_available:amount+int(0,100000),approval_levels:amount>500000?4:3,approval_role:amount>500000?'Director':'Commercial manager',lead_days:int(10,60),prior_delay_rate:partner.prior_delay_rate,urgency:int(1,3),retention_pct:r.type.includes('PO')?0:.05,advance_pct:pick([0,.1,.2])});
   probability=.06+.55*r.prior_delay_rate+.10*(r.urgency-1)+.12*(r.lead_days<20)+.06*(r.approval_levels===4);
   eligible=['Approved','Part delivered','Completed'].includes(r.status);
   r.accepted_qty=r.status==='Completed'?qty:r.status==='Part delivered'?int(1,qty-1):0;r.certified_amount=r.trade?round(r.accepted_qty*rate):0;
   r.promised_date=add(date,r.lead_days);r.completion_date=null;
   details.push({detail_id:id+'-L1',record_id:id,line_type:r.trade?'Measured work':'Supply / service',quantity:qty,unit_rate:rate,line_amount:amount,accepted_qty:r.accepted_qty,acceptance_evidence:r.accepted_qty?(r.trade?'CERT-':'GRN-')+pad(i+1):null});
  }
  if(m.id==='inventory-warehouse'){
   const item=items[i%100],store='WH-'+pad(i%5+1,2),key=item.item_id+store,opening=balances.get(key)??1000;
   r.status=r.type.startsWith('Adjustment')?'Count verified':pick(['Posted','Quarantined']);
   let qty=int(1,80),signed=['Issue','Adjustment out'].includes(r.type)?-qty:qty;if(opening+signed<0){r.type='Receipt';signed=qty;}
   if(r.status==='Quarantined'){r.type='Receipt';signed=0;}
   Object.assign(r,{item_id:item.item_id,uom:item.uom,store_id:store,locator:store+'-BIN-'+pad(i%20+1,2),lot_id:'LOT-'+pad(i+1),opening_qty:opening,movement_qty:qty,signed_qty:signed,closing_qty:opening+signed,item_value:item.unit_value,movement_value:qty*item.unit_value,quarantine_qty:r.status==='Quarantined'?qty:0,approval_status:r.type.startsWith('Adjustment')?'Approved':'Not required',days_since_count:int(1,120),manual_entry:int(0,1),purchase_order_id:null});
   balances.set(key,r.closing_qty);probability=.04+.002*r.days_since_count+.15*r.manual_entry+.09*(qty>60);
   details.push({detail_id:id+'-LOC',record_id:id,item_id:r.item_id,store_id:store,locator:r.locator,lot_id:r.lot_id,expiry_date:add(date,365),stock_uom:r.uom});
  }
  if(m.id==='real-estate-sales'){
   Object.assign(r,{customer_id:'CUS-'+pad(i+1),unit_id:'UNIT-'+pad(i+1),list_price:int(30,250)*100000,discount_pct:round(rand()*.12),response_days:int(0,12),prior_contact_count:int(0,10),financing_required:int(0,1)});r.agreed_price=round(r.list_price*(1-r.discount_pct));r.discount_approval=r.discount_pct>.07?'Sales head':'Sales manager';
   probability=.08+.04*r.response_days+.1*r.financing_required-.014*r.prior_contact_count;
   eligible=true;
   r.booking_id=['Booked','Agreement signed','Handed over'].includes(r.status)?'BOOK-'+pad(i+1):null;
   r.collected_amount=r.booking_id?round(r.agreed_price*pick([.1,.25,.5,1])):0;
   if(r.booking_id){let total=0;for(let j=0;j<4;j++){const amount=j===3?round(r.agreed_price-total):round(r.agreed_price*.25);total=round(total+amount);details.push({detail_id:id+'-I'+(j+1),record_id:id,installment_no:j+1,due_date:add(date,30*j),scheduled_amount:amount,collected_amount:round(Math.min(amount,Math.max(0,r.collected_amount-(total-amount))))});}}
  }
  if(m.id==='construction-assets'){
   const a=i%500;r.type=a%3===0?'Fixed':'Movable';r.project_id=projects[a%20].project_id;
   r.status=(a%17===0&&month>=6)?'Retired':pick(['Available','Deployed','Under maintenance']);
   const cost=100000+(a%80)*50000,life=120,age=12+a%60+month,dep=r.status==='Retired'?0:round(cost*.9/life);
   Object.assign(r,{asset_id:'AST-'+pad(a+1,3),custodian_id:employees[a].employee_id,acquisition_cost:cost,residual_value:cost*.1,useful_life_months:life,age_months:age,operating_hours:r.status==='Deployed'?int(60,240):0,available_hours:r.status==='Retired'?0:240,days_since_service:int(1,180),prior_breakdowns:int(0,5),depreciation:dep,opening_book_value:round(cost-Math.min(age-1,life)*cost*.9/life),retirement_date:r.status==='Retired'?'2024-07-01':null});
   // Retirement freezes the carrying amount from the preceding period.
   if(r.status==='Retired')r.opening_book_value=round(cost-(12+a%60+5)*cost*.9/life);
   r.closing_book_value=round(Math.max(r.residual_value,r.opening_book_value-dep));r.utilization_rate=round(r.available_hours?r.operating_hours/r.available_hours:0);
   probability=.025+.0015*r.days_since_service+.04*r.prior_breakdowns+.12*r.utilization_rate;eligible=r.status!=='Retired';
   details.push({detail_id:id+'-SVC',record_id:id,asset_id:r.asset_id,last_service_date:add(date,-r.days_since_service),service_type:pick(['Preventive','Inspection','Corrective']),next_service_date:add(date,30),maintenance_due_hours:250});
  }
  if(m.id==='receivables-payables'){
   r.status=rand()<.65?'Settled':pick(m.statuses);
   r.type=i%2?'AP':'AR';Object.assign(r,{entity_id:partner.partner_id,invoice_no:'INV-'+pad(i+1),source_id:null,net_amount:int(10,300)*10000,tax_rate:.18,payment_days:pick([15,30,45,60]),prior_late_rate:partner.prior_delay_rate,match_variance:round(rand()*.08),approval_levels:int(2,4),ledger_period:date.slice(0,7)});
   r.tax_amount=round(r.net_amount*r.tax_rate);r.gross_amount=round(r.net_amount+r.tax_amount);r.due_date=add(date,r.payment_days);r.settled_amount=r.status==='Settled'?r.gross_amount:r.status==='Part settled'?round(r.gross_amount*rand()*.8):0;r.outstanding=['Draft','Disputed'].includes(r.status)?0:round(r.gross_amount-r.settled_amount);r.unposted_amount=['Draft','Disputed'].includes(r.status)?r.gross_amount:0;if(r.status==='Posted')r.status='Overdue';
   r.days_overdue=r.outstanding?Math.max(0,Math.floor((new Date('2025-03-01')-new Date(r.due_date))/86400000)):0;
   probability=.06+.6*r.prior_late_rate+.16*(r.match_variance>.04)+.05*(r.approval_levels>2);eligible=!['Draft','Disputed'].includes(r.status);
   if(r.settled_amount)details.push({detail_id:id+'-ALLOC',record_id:id,allocation_amount:r.settled_amount,allocation_type:r.type==='AP'?'Payment':'Receipt',allocation_date:'2025-02-28'});
  }
  if(m.id==='construction-hr'){
   const e=employees[i%500];r.type=e.role;r.project_id=e.project_id;r.record_date=`2024-${pad(month+1,2)}-28`;
   Object.assign(r,{employee_id:e.employee_id,payroll_group:e.role==='Office staff'?'Monthly staff':'Monthly site',scheduled_days:26,paid_leave_days:int(0,3),absent_days:int(0,3),overtime_hours:int(0,40),overtime_approved:int(0,1),manual_entry:int(0,1),missing_punches:int(0,6),shift_changes:int(0,4),approver:'HR reviewer',monthly_salary:e.monthly_salary});r.worked_days=r.scheduled_days-r.paid_leave_days-r.absent_days;
   probability=.03+.07*r.missing_punches+.12*r.manual_entry+.04*r.shift_changes;
   details.push({detail_id:id+'-HANDOFF',record_id:id,employee_id:e.employee_id,month:date.slice(0,7),eligible_for_payroll:r.status==='Approved'?1:0,approved_overtime:r.overtime_approved?r.overtime_hours:0});
  }
  if(m.id==='construction-payroll'){
   const hr=all['construction-hr'].rows[i];r.project_id=hr.project_id;r.type=hr.payroll_group;r.record_date=hr.record_date;r.status=hr.status==='Approved'?pick(['Calculated','Under review','Approved','Paid']):'Held for attendance';
   Object.assign(r,{employee_id:hr.employee_id,attendance_id:hr.record_id,attendance_status:hr.status,monthly_salary:hr.monthly_salary,scheduled_days:hr.scheduled_days,paid_days:hr.worked_days+hr.paid_leave_days,overtime_hours:hr.overtime_approved?hr.overtime_hours:0,overtime_rate:round(hr.monthly_salary/208*1.5),allowance:int(0,5)*1000,manual_adjustments:int(0,4),input_exceptions:hr.missing_punches,demonstration_deduction_rate:.08});
   r.basic_pay=round(r.monthly_salary*r.paid_days/r.scheduled_days);r.overtime_pay=round(r.overtime_hours*r.overtime_rate);r.gross_pay=round(r.basic_pay+r.overtime_pay+r.allowance);r.deductions=round(r.gross_pay*r.demonstration_deduction_rate);r.net_pay=round(r.gross_pay-r.deductions);r.paid_amount=r.status==='Paid'?r.net_pay:0;
   probability=.02+.085*r.manual_adjustments+.04*r.input_exceptions+.0015*r.overtime_hours;
   details.push({detail_id:id+'-PAY',record_id:id,attendance_id:r.attendance_id,release_eligible:hr.status==='Approved'?1:0,payment_amount:r.paid_amount,payment_date:r.paid_amount?'2025-02-28':null});
  }
  r[m.target]=eligible?(rand()<Math.min(.85,probability)?1:0):null;r.label_available_date=eligible?add(r.record_date,60):null;
  if(m.id==='procurement-subcontracting'&&eligible){r[m.target]=r.status==='Completed'?r[m.target]:1;r.completion_date=r.status==='Completed'?add(r.promised_date,r[m.target]?int(1,30):-int(0,5)):null;r.label_available_date=add(r.promised_date,31);}
  if(m.id==='tender-contracts'&&eligible){r.actual_award_date=add(date,r.planned_days+(r[m.target]?int(1,25):-int(0,5)));r.label_available_date=r.actual_award_date;}else if(m.id==='tender-contracts')r.actual_award_date=null;
  if(m.id==='real-estate-sales'){r[m.target]=r.status==='Cancelled'?1:['Booked','Agreement signed','Handed over'].includes(r.status)?0:r[m.target];r.outcome_at_60_days=r[m.target]?'Lost / cancelled':'Retained';}
  if(m.id==='receivables-payables'&&eligible){r[m.target]=1;r.settlement_date=r.status==='Settled'?'2025-02-28':null;}else if(m.id==='receivables-payables')r.settlement_date=null;
  // Invoice historical outcome is generated at the original due date, separate from the reporting snapshot.
  if(m.id==='receivables-payables'&&r.status==='Settled'){r[m.target]=rand()<probability?1:0;r.settlement_date=add(r.due_date,r[m.target]?int(1,40):-int(0,5));const d=details.at(-1);if(d?.record_id===id)d.allocation_date=r.settlement_date;}
  events.push({event_id:id+'-E1',record_id:id,event_date:r.record_date,actor_role:m.owner,channel:pick(['ERP form','Spreadsheet import','Paper transcribed','WhatsApp transcribed']),event_type:'Record captured',approval_state:r.status});rows.push(r);
 }
 // Inventory chronology must be monotone for each item/store ledger.
 if(m.id==='inventory-warehouse'){balances.clear();for(const r of rows.sort((a,b)=>a.record_date.localeCompare(b.record_date)||a.record_id.localeCompare(b.record_id))){const key=r.item_id+r.store_id;r.opening_qty=balances.get(key)??1000;r.closing_qty=r.opening_qty+r.signed_qty;balances.set(key,r.closing_qty);}}
 all[m.id]={version:datasetVersion,module:m,asOf:'2025-03-01',seed:20260921,currency:'INR',provenance:'Synthetic demonstration data. Field concepts paraphrased from the user-supplied Xpedeon reference. Workflows, thresholds, statuses and statistical relationships are demonstration assumptions, not a vendor specification or implementation claim.',rows,details,events,projects,partners,employees:['construction-hr','construction-payroll','construction-assets'].includes(m.id)?employees:[],items:m.id==='inventory-warehouse'||m.id==='procurement-subcontracting'?items:[]};
}
// Cross-module evidence uses eligible source documents only.
const completed=all['procurement-subcontracting'].rows.filter(r=>r.status==='Completed'),sales=all['real-estate-sales'].rows.filter(r=>r.booking_id),contracts=all['tender-contracts'].rows.filter(r=>r.contract_id);
all['inventory-warehouse'].rows.filter(r=>r.type==='Receipt').forEach(r=>{const source=completed.find(s=>s.item_id===r.item_id&&s.completion_date<=r.record_date);r.purchase_order_id=source?.record_id??null;});
all['receivables-payables'].rows.forEach((r,i)=>{const pool=r.type==='AP'?completed:(i%4===0?sales:contracts);const eligible=pool.filter(s=>(s.completion_date||s.actual_award_date||s.record_date)<=r.record_date);r.source_id=eligible.length?eligible[i%eligible.length].record_id:null;});
// Historical invoice labels are observed no earlier than both the due-date horizon and actual settlement.
all['receivables-payables'].rows.forEach(r=>{if(r.label_available_date)r.label_available_date=r.settlement_date&&r.settlement_date>add(r.due_date,1)?r.settlement_date:add(r.due_date,1);});
for(const [id,data] of Object.entries(all))fs.writeFileSync(new URL(id+'.json',out),JSON.stringify(data));
fs.writeFileSync(new URL('catalog.json',out),JSON.stringify(modules));
console.log('Generated',Object.keys(all).length,'modules with',Object.values(all).reduce((s,x)=>s+x.rows.length,0),'primary records');
