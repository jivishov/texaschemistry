// 1. Walk: 1920x1080, F5 (no reload), then PageDown to the end; screenshot every press.
// Per press: no console error, cue present, nothing past the slide or out of its container by > 1 px, frame or slide advanced.
const L=require('./lib');
const EMAX=process.env.EMPTY_MAX?+process.env.EMPTY_MAX:1/3; // teacher round: at most one third of the slide body empty
(async()=>{
  const theme=process.argv[2]||'light',dir=L.ensure(L.OUT+'/shots-'+theme);
  require('fs').readdirSync(dir).forEach(f=>require('fs').unlinkSync(dir+'/'+f));
  const {browser,page,errors}=await L.open({theme});
  await page.evaluate(()=>{window.__noReload=1});
  await page.keyboard.press('F5');await L.wait(page,500);
  const reloaded=!(await page.evaluate(()=>window.__noReload===1));
  const rec=[],fails=[];let i=0,prev=null,lastFile=null;
  if(reloaded)fails.push('F5 reloaded the page');
  while(true){
    await L.wait(page,1100);
    const st=await L.state(page),fs=await L.frameState(page),ov=await L.overflow(page),em=await L.emptiness(page);
    const file=`${String(i).padStart(3,'0')}-s${st.s+1}f${st.f}.png`;lastFile=file;
    await page.screenshot({path:dir+'/'+file});
    const row={press:i,s:st.s+1,f:st.f,empty:em,cue:st.cue,sims:st.sims,on:fs.on,cls:fs.cls,overflow:ov,errors:errors.splice(0),file};
    if(!/^(Next ▶ .+|End of the deck)$/.test(st.cue))fails.push(`press ${i}: cue missing ("${st.cue}")`);
    if(ov.length)fails.push(`press ${i} (s${st.s+1}f${st.f}): ${ov.length} overflow: `+ov.map(o=>o.el+' '+o.why+' '+o.px+'px').join('; '));
    if(em>EMAX)fails.push(`press ${i} (s${st.s+1}f${st.f}): ${Math.round(em*100)}% of the slide body is empty (gate ${Math.round(EMAX*100)}%)`);
    if(row.errors.length)fails.push(`press ${i}: console errors: `+row.errors.join(' | '));
    if(prev&&prev.s===st.s&&prev.f===st.f)break;
    if(prev&&!((st.s===prev.s&&st.f===prev.f+1)||(st.s===prev.s+1&&st.f===0)))fails.push(`press ${i}: did not advance by one frame (from s${prev.s+1}f${prev.f} to s${st.s+1}f${st.f})`);
    rec.push(row);prev=st;i++;
    await page.keyboard.press('PageDown');
  }
  require('fs').unlinkSync(dir+'/'+lastFile); // the extra shot taken after the last press
  L.save('walk-'+theme+'.json',{theme,presses:rec.length,fails,rec});
  console.log(`walk ${theme}: ${rec.length} states, max empty ${Math.round(Math.max(...rec.map(r=>r.empty))*100)}% (s${rec.reduce((a,r)=>r.empty>a.empty?r:a,rec[0]).s}f${rec.reduce((a,r)=>r.empty>a.empty?r:a,rec[0]).f}), ${fails.length?'FAIL':'PASS'}`);fails.forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
