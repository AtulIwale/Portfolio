import fs from 'node:fs/promises';
import {build} from 'esbuild';
import React from 'react';
import {renderToString} from 'react-dom/server';
import App from '../src/App.js';
import {modules} from '../src/modules/catalog.js';
await fs.access('public/data/modules/procurement-subcontracting.json').catch(()=>{throw Error('Run npm run data before building.');});
await fs.rm('dist',{recursive:true,force:true});await fs.cp('public','dist',{recursive:true});
await build({entryPoints:['src/client.js'],bundle:true,format:'esm',outfile:'dist/app.js',minify:true,define:{'process.env.NODE_ENV':'"production"'}});
const paths=['/','/index.html','/process-projects.html','/ai-app.html',...modules.flatMap(m=>['/modules/'+m.id+'.html','/ai-app/module-'+m.id+'.html'])];
for(const route of paths){const target='dist'+(route==='/'?'/index.html':route);await fs.mkdir(new URL('.',new URL(target,'file://'+process.cwd()+'/')),{recursive:true});const html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AEC module projects — Atul Iwale</title><link rel="stylesheet" href="/assets/base.css"><link rel="stylesheet" href="/assets/modules.css"><script type="module" src="/app.js"></script></head><body><div id="root">'+renderToString(React.createElement(App,{initialPath:route}))+'</div></body></html>';await fs.writeFile(target,html);}
console.log('Built module projects, eight apps and dataset downloads.');
