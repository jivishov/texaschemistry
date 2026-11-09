// Zoom sheet: one zoomed state per unit type per slide (from zoom-<theme>.json), 6 columns, split under 4000 px.  node zoomsheet.js [light|dark]
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
if(!process.env.OUT)throw new Error('set OUT (the suite output folder); suite.py sets it');
const O=path.resolve(process.env.OUT),NAME=process.env.DECKNAME||path.basename(process.env.DECK||'deck');
(async()=>{const theme=process.argv[2]||'light',Z=JSON.parse(fs.readFileSync(O+'/zoom-'+theme+'.json')),dir=O+'/zoom-'+theme,files=Z.sheet;
  const COLS=6,CELL=212,HEAD=50,per=Math.floor((4000-HEAD-32)/(CELL+8))*COLS,groups=[];for(let i=0;i<files.length;i+=per)groups.push(files.slice(i,i+per));
  fs.readdirSync(O).filter(f=>f.startsWith('zoomsheet-'+theme)).forEach(f=>fs.unlinkSync(O+'/'+f));
  const b=await chromium.launch(),p=await b.newPage({viewport:{width:1990,height:1000}}),out=[];
  for(let n=0;n<groups.length;n++){const cells=groups[n].map(f=>{const r=Z.rec.find(x=>x.file===f);return `<figure><img src="file://${dir}/${f}"><figcaption><b>s${r.s}f${r.f}</b> ${r.kind} ${r.i}/${r.n} · ${Math.round(r.fill*100)}% ${(r.label||'').replace(/</g,'&lt;')}</figcaption></figure>`}).join('');
    fs.writeFileSync(O+'/zoomsheet.html',`<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:16px;background:${theme==='dark'?'#222':'#ccc'};font:14px system-ui}h1{font-size:18px;margin:0 0 10px;color:${theme==='dark'?'#eee':'#111'}}
      .g{display:grid;grid-template-columns:repeat(6,322px);gap:8px}figure{margin:0;background:#fff;padding:3px}img{width:316px;height:178px;display:block;border:1px solid #999}figcaption{padding:2px;color:#222;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}</style>
      <h1>${NAME} · zoom sheet, ${theme} theme · one zoomed state per unit type per slide · part ${n+1} of ${groups.length}</h1><div class="g">${cells}</div>`);
    await p.goto('file://'+O+'/zoomsheet.html');await p.waitForTimeout(900);const name='zoomsheet-'+theme+'-'+(n+1)+'.png';await p.screenshot({path:O+'/'+name,fullPage:true});
    out.push(name+' ('+groups[n].length+' shots, '+await p.evaluate(()=>document.documentElement.scrollHeight)+' px tall)')}
  await b.close();console.log('zoom sheet '+theme+': '+out.join(', '));
})();
