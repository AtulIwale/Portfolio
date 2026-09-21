import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve('dist'),port=Number(process.env.PORT||4173),types={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json','.xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'};
http.createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');let p=decodeURIComponent(url.pathname);if(p==='/')p='/index.html';if(!path.extname(p))p+='.html';const file=path.resolve(root,'.'+p);if(!file.startsWith(root+path.sep))throw Error('Invalid path');const content=await fs.readFile(file);res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream'});res.end(content);}catch{res.writeHead(404);res.end('Not found');}}).listen(port,'127.0.0.1',()=>console.log('Open http://localhost:'+port));
