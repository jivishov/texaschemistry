// 3. Font floor: at every frame of every slide, list visible student-facing text below 34 px on the 1600 x 900 canvas.
// sub/sup are judged by their own size (0.78em: 34.3 px on 44 px body). SVG text is measured at its rendered scale.
// Canvas text is reported by each animation's painter (minFont). Cue (28 px) and section label (26 px) live outside the slide.
const L=require('./lib');
(async()=>{
  const {browser,page,errors}=await L.open({theme:process.argv[2]||'light'});
  const ns=await page.evaluate(()=>Deck.slides.length),slides=[],fails=[];
  for(let s=0;s<ns;s++){
    const nf=await page.evaluate(s=>Deck.slides[s].frames.length,s);let min=Infinity,minBase=Infinity,canvasMin=Infinity;const low=new Map();
    for(let f=0;f<nf;f++){
      await page.evaluate(([s,f])=>Deck.go(s,f),[s,f]);await L.wait(page,f===nf-1?1000:150);
      const r=await page.evaluate(()=>{
        const S=document.querySelector('.slide.current'),k=S.getBoundingClientRect().width/1600,out=[];
        const w=document.createTreeWalker(S,NodeFilter.SHOW_TEXT);let n;
        while((n=w.nextNode())){const t=n.nodeValue.trim();if(!t)continue;const e=n.parentElement;if(e.closest('.notes,script,style'))continue;
          const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none'||e.closest('[hidden]'))continue;
          let px=parseFloat(cs.fontSize);
          if(e instanceof SVGElement){const m=e.getScreenCTM();px=px*Math.hypot(m.a,m.b)/k}
          const ss=e.closest('sub,sup');let base=px;
          if(ss){const p=ss.parentElement;base=parseFloat(getComputedStyle(p).fontSize);if(p instanceof SVGElement){const m=p.getScreenCTM();base=base*Math.hypot(m.a,m.b)/k}}
          out.push({t:t.slice(0,40),px:Math.round(px*10)/10,base:Math.round(base*10)/10,sub:!!ss})}
        const sims=[...S.querySelectorAll('.sim[data-sim]')].map(h=>({id:h.id,min:Deck.sims[h.id].minFont,floor:(h.dataset.sim==='ptMap'||h.dataset.sim==='ionTable')?34:36}));
        return {out,sims};
      });
      for(const o of r.out){const judged=o.px;if(!o.sub)min=Math.min(min,o.px);else minBase=Math.min(minBase,o.px);
        if(judged<34-0.05)low.set(o.t,judged)}
      r.sims.forEach(x=>{if(isFinite(x.min))canvasMin=Math.min(canvasMin,x.min);if(x.min<x.floor-0.05)low.set('canvas '+x.id,x.min)});
    }
    const row={slide:s+1,minTextPx:min,minSubSupBasePx:isFinite(minBase)?minBase:null,minCanvasLabelPx:isFinite(canvasMin)?canvasMin:null,below:[...low].map(([t,px])=>({t,px}))};
    slides.push(row);if(row.below.length)fails.push(`slide ${s+1}: `+row.below.map(b=>`"${b.t}" ${b.px}px`).join('; '));
  }
  if(errors.length)fails.push('console errors: '+errors.join(' | '));
  L.save('fonts.json',{slides,fails});
  slides.forEach(r=>console.log(`  slide ${r.slide}: min text ${r.minTextPx}px, sub/sup ${r.minSubSupBasePx??'-'}px, canvas labels ${r.minCanvasLabelPx??'-'}px, below floor: ${r.below.length}`));
  console.log(`fonts: ${fails.length?'FAIL':'PASS'}`);fails.forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
