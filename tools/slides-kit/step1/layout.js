// Layout audit (teacher round, A3 and A4): on every frame, no option list wraps 2 + 1 (one row, stacked, or 2 x 2 for four),
// at most one third of the slide body is empty, and no visible text is clipped or ellipsized (slide and footer).
const L=require('./lib');
const EMAX=process.env.EMPTY_MAX?+process.env.EMPTY_MAX:1/3;
(async()=>{
  const {browser,page,errors}=await L.open({reduced:true});
  const nf=await page.evaluate(()=>Deck.slides.map(S=>S.frames.length));
  const rec=[],fails=[];let lists=0;
  for(let s=0;s<nf.length;s++)for(let f=0;f<nf[s];f++){
    await page.evaluate(([s,f])=>Deck.go(s,f),[s,f]);await L.wait(page,100);
    const o=await page.evaluate(()=>[...document.querySelectorAll('.slide.current .opts')].filter(x=>x.getClientRects().length&&getComputedStyle(x).visibility==='visible').map(x=>{
      const r=[...x.children].map(c=>c.getBoundingClientRect()),tops=[...new Set(r.map(q=>Math.round(q.top/4)))],lefts=[...new Set(r.map(q=>Math.round(q.left/4)))];
      const per=tops.map(t=>r.filter(q=>Math.round(q.top/4)===t).length);
      return {id:x.closest('[id]').id,n:r.length,rows:tops.length,per,shape:tops.length===1?'row':tops.length===r.length&&lefts.length===1?'stacked':r.length===4&&per.join()==='2,2'?'2x2':'wrap '+per.join('+')}}));
    const em=await L.emptiness(page),cl=await L.clipped(page);lists+=o.length;
    /* canvas text drawn past the edge of its animation would be cut off too */
    const ct=await page.evaluate(()=>Deck.slides[Deck.cur.s].sims.filter(x=>x.outText>0).map(x=>x.id+' '+x.outText));
    ct.forEach(c=>fails.push(`s${s+1}f${f}: canvas text cut at the edge in ${c}`));
    cl.forEach(c=>fails.push(`s${s+1}f${f}: clipped text in ${c.el} (${c.sw}x${c.sh} in ${c.cw}x${c.ch})`));
    o.forEach(x=>{if(x.shape.startsWith('wrap'))fails.push(`s${s+1}f${f} ${x.id}: options ${x.shape}`)});
    if(em>EMAX)fails.push(`s${s+1}f${f}: ${Math.round(em*100)}% of the slide body is empty (gate ${Math.round(EMAX*100)}%)`);
    rec.push({s:s+1,f,empty:em,opts:o});
  }
  if(errors.length)fails.push('console errors: '+errors.join(' | '));
  const sh={};rec.forEach(r=>r.opts.forEach(x=>{sh[x.shape]=(sh[x.shape]||0)+1}));
  const worst=rec.reduce((a,r)=>r.empty>a.empty?r:a,rec[0]);
  L.save('layout.json',{frames:rec.length,fails,rec});
  console.log(`layout: ${rec.length} frames, ${lists} visible option lists (${Object.entries(sh).map(([k,v])=>k+' '+v).join(', ')}), max empty ${Math.round(worst.empty*100)}% (s${worst.s}f${worst.f}), gate ${Math.round(EMAX*100)}%, clipped or ellipsized text: ${fails.filter(f=>/clipped text/.test(f)).length}, ${fails.length?'FAIL':'PASS'}`);fails.forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
