import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {JSDOM} from 'jsdom';
import {build} from 'esbuild';
import {modules} from '../src/modules/catalog.js';
const datasets=Object.fromEntries(modules.map(m=>[m.id,JSON.parse(fs.readFileSync('public/data/modules/'+m.id+'.json','utf8'))]));
test('Each module app hydrates, filters, opens evidence and calculates a what-if score',async()=>{
 const bundle=await build({entryPoints:['src/client.js'],bundle:true,format:'iife',write:false,define:{'process.env.NODE_ENV':'"production"'}});
 for(const m of modules){const dom=new JSDOM(fs.readFileSync('dist/ai-app/module-'+m.id+'.html','utf8'),{url:'https://portfolio.test/ai-app/module-'+m.id,runScripts:'outside-only',pretendToBeVisual:true});const w=dom.window,errors=[];
  w.console.error=(...args)=>errors.push(args.join(' '));w.addEventListener('error',e=>errors.push(e.message));w.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync('public'+url,'utf8'))});w.matchMedia=()=>({matches:true,addEventListener(){},removeEventListener(){}});w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=function(){};w.ResizeObserver=class{observe(){}disconnect(){}};w.IntersectionObserver=class{observe(){}disconnect(){}};
  w.eval(bundle.outputFiles[0].text);const wait=()=>new Promise(r=>setTimeout(r,80));await wait();await wait();assert.equal(w.document.querySelectorAll('.module-record-button').length,15,m.id);
  const filters=w.document.querySelector('.module-filters');
  assert.equal(filters.children.length,4,'Filters must contain only four controls: '+m.id);
  assert(!filters.querySelector('.module-kpis,.module-table-scroll,.module-pagination,.module-question'),'Results must sit below the filters, not inside their grid');
  assert.equal(w.document.querySelector('.module-kpis').parentElement,filters.parentElement,'Summary and filters share the full-width workspace');
  const sel=w.document.querySelector('.module-filters select');sel.value=datasets[m.id].rows[0].status;sel.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();assert(w.document.querySelector('.module-kpis').textContent.includes(String(datasets[m.id].rows.filter(r=>r.status===sel.value).length).replace(/(\d)(?=(\d{3})+$)/g,'$1,')));
  w.document.querySelector('.module-record-button').click();await wait();assert(w.document.querySelector('.module-review'));assert(w.document.querySelector('.module-evidence').textContent.includes('Record captured'));assert(w.document.querySelector('.module-score').textContent.includes('model score'));
  const input=w.document.querySelector('.module-input input');Object.getOwnPropertyDescriptor(w.HTMLInputElement.prototype,'value').set.call(input,'0');input.dispatchEvent(new w.Event('input',{bubbles:true}));await wait();assert(!w.document.querySelector('.module-score').textContent.includes('NaN'));
  const q=w.document.querySelector('.module-question input');Object.getOwnPropertyDescriptor(w.HTMLInputElement.prototype,'value').set.call(q,'highest risk');q.dispatchEvent(new w.Event('input',{bubbles:true}));await wait();w.document.querySelector('.module-question').dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));await wait();assert(w.document.querySelector('.module-answer').textContent.includes('Highest model scores'));
  assert.equal(errors.length,0,errors.join('\n'));dom.window.close();
 }
});
