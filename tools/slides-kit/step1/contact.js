// Contact sheets: every walk screenshot of one theme, 6 columns, split into images no taller than 4000 px (at slide boundaries).
const {chromium}=require('playwright');const fs=require('fs');const O=process.env.OUT||__dirname;
(async()=>{
  const theme=process.argv[2]||'light',dir=O+'/shots-'+theme,files=fs.readdirSync(dir).filter(f=>f.endsWith('.png')).sort((a,b)=>parseInt(a)-parseInt(b));
  const walk=JSON.parse(fs.readFileSync(O+'/walk-'+theme+'.json'));
  const COLS=6,CELL=212,HEAD=50,MAXH=4000,perImg=Math.floor((MAXH-HEAD-32)/(CELL+8))*COLS;
  const groups=[];let cur=[];
  files.forEach((f,i)=>{const s=+f.match(/-s(\d+)f/)[1];if(cur.length>=perImg){let k=cur.length;while(k>0&&+cur[k-1].f.match(/-s(\d+)f/)[1]===s)k--;if(k===0)k=cur.length;groups.push(cur.slice(0,k));cur=cur.slice(k)}cur.push({f,i})});
  if(cur.length)groups.push(cur);
  ['contact-'+theme+'.png'].concat(groups.map((_,n)=>'contact-'+theme+'-'+(n+1)+'.png')).forEach(n=>{try{fs.unlinkSync(O+'/'+n)}catch(e){}});
  const b=await chromium.launch(),p=await b.newPage({viewport:{width:1990,height:1000}});const out=[];
  for(let n=0;n<groups.length;n++){const g=groups[n];
    const cells=g.map(({f,i})=>{const r=walk.rec.find(x=>x.file===f)||{};return `<figure><img src="file://${dir}/${f}"><figcaption><b>${f.replace('.png','')}</b> ${(r.cue||'').replace(/</g,'&lt;')}</figcaption></figure>`}).join('');
    const html=`<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:16px;background:${theme==='dark'?'#222':'#ccc'};font:14px system-ui}
    h1{font-size:18px;margin:0 0 10px;color:${theme==='dark'?'#eee':'#111'}}.g{display:grid;grid-template-columns:repeat(6,322px);gap:8px}figure{margin:0;background:#fff;padding:3px}
    img{width:316px;height:178px;display:block;border:1px solid #999}figcaption{padding:2px;color:#222;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}</style>
    <h1>${process.env.DECKNAME||'slides-4-1.html'} · walk, ${theme} theme · part ${n+1} of ${groups.length} · presses ${g[0].i} to ${g[g.length-1].i} (file: press-slide-frame; caption: footer cue)</h1><div class="g">${cells}</div>`;
    fs.writeFileSync(O+'/contact.html',html);await p.goto('file://'+O+'/contact.html');await p.waitForTimeout(900);
    const name='contact-'+theme+'-'+(n+1)+'.png';await p.screenshot({path:O+'/'+name,fullPage:true});
    const h=await p.evaluate(()=>document.documentElement.scrollHeight);out.push(name+' ('+g.length+' shots, '+h+' px tall)')}
  await b.close();console.log('contact sheets '+theme+': '+out.join(', '));
})();
