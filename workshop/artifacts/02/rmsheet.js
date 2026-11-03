// Reduced-motion end states: one shot per scratch slide at its animation's last stage (reducedMotion 'reduce'), both themes,
// composed into one sheet per theme like contact.js.  node rmsheet.js <deck> <outdir>
const {chromium}=require('playwright'),fs=require('fs');
(async()=>{const [deck,out]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});const b=await chromium.launch();
for(const theme of ['light','dark']){const p=await (await b.newContext({viewport:{width:1600,height:900},reducedMotion:'reduce'})).newPage();
  await p.goto('file://'+deck+'?theme='+theme);await p.waitForFunction(()=>window.Deck&&Deck.slides.length);await p.waitForTimeout(400);
  const ns=await p.evaluate(()=>Deck.slides.length),cells=[];
  for(let s=0;s<ns;s++){const r=await p.evaluate(s=>{const S=Deck.slides[s],x=S.sims[0],last=x.stages.filter(st=>S.frames.some(fr=>fr.stage.some(q=>q.s===st))).pop();
      const f=S.frames.map((fr,i)=>fr.stage.some(q=>q.s===last)?i:-1).filter(i=>i>=0).pop();Deck.go(s,f);return {id:S.id,f,last,anim:x.host.dataset.sim,rm:Deck.reduced()}},s);
    await p.waitForTimeout(300);const file=`${out}/rm-${theme}-${r.id}.png`;await p.screenshot({path:file});cells.push({...r,file})}
  const html=`<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:16px;background:${theme==='dark'?'#222':'#ccc'};font:14px system-ui}h1{font-size:18px;margin:0 0 10px;color:${theme==='dark'?'#eee':'#111'}}
    .g{display:grid;grid-template-columns:repeat(4,482px);gap:8px}figure{margin:0;background:#fff;padding:3px}img{width:476px;height:268px;display:block;border:1px solid #999}figcaption{padding:2px;color:#222}</style>
    <h1>scratch45.html · reduced motion (prefers-reduced-motion: reduce) · each animation at its last stage · ${theme} theme</h1><div class="g">${cells.map(c=>`<figure><img src="file://${c.file}"><figcaption><b>${c.id}</b> ${c.anim} · last stage ${c.last} (frame ${c.f}) · reduced ${c.rm}</figcaption></figure>`).join('')}</div>`;
  fs.writeFileSync(out+'/rm.html',html);const q=await b.newPage({viewport:{width:1990,height:900}});await q.goto('file://'+out+'/rm.html');await q.waitForTimeout(800);
  await q.screenshot({path:`${out}/rmsheet-${theme}.png`,fullPage:true});await q.close();await p.context().close();console.log('rm sheet',theme,cells.map(c=>c.id+':'+c.last).join(' '))}
await b.close()})();
