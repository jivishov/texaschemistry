// Mouse grading audit (teacher round, A2): on every check, click each option: the right one turns green with its reason,
// a wrong one turns red with its own feedback line (on screen, 34 px or more); another click re-marks. Then Next shows the
// correct answer state with no mouse marks left. On Predict now, a click only highlights the option, without grading.
const L=require('./lib');
(async()=>{
  const {browser,page,errors}=await L.open({reduced:true});
  const nf=await page.evaluate(()=>Deck.slides.map(S=>S.frames.length));
  const res=[],fails=[];const ok=(n,p,i)=>{res.push({n,pass:!!p,i:i===undefined?'':JSON.stringify(i)});if(!p)fails.push(n+(i===undefined?'':'  '+JSON.stringify(i)))};
  const done=new Set();let checks=0,picks=0;
  for(let s=0;s<nf.length;s++)for(let f=0;f<nf[s];f++){
    await page.evaluate(([s,f])=>Deck.go(s,f),[s,f]);await L.wait(page,120);
    const cards=await page.evaluate(()=>{const S=document.querySelector('.slide.current'),vis=e=>e&&e.getClientRects().length&&getComputedStyle(e).visibility==='visible';
      return [...S.querySelectorAll('.check,.checkrow')].filter(c=>vis(c)&&[...c.querySelectorAll('.opt')].some(vis)).map(c=>({id:c.id,mode:c.dataset.mode||'grade',ansShown:vis(c.querySelector('.ans')),
        opts:[...c.querySelectorAll('.opt')].filter(vis).map(o=>({id:o.id,ok:o.dataset.ok==='1',fb:o.dataset.fb==null?null:o.dataset.fb.replace(/<[^>]+>/g,'')}))}))});
    for(const c of cards){if(done.has(c.id)||c.ansShown||c.mode==='none')continue;done.add(c.id);
      if(c.mode==='pick'){picks++;
        for(let i=0;i<c.opts.length;i++){await page.locator(`#${c.id} .opt >> nth=${i}`).click();await L.wait(page,80);
          const m=await page.evaluate(id=>{const C=document.getElementById(id);return {picked:[...C.querySelectorAll('.opt.picked')].map(o=>[...C.querySelectorAll('.opt')].indexOf(o)),graded:C.querySelectorAll('.opt.okmk,.opt.wrong').length,fb:C.querySelector('.fb.on')?1:0}},c.id);
          ok(`s${s+1}f${f} ${c.id} option ${'ABC'[i]}: highlighted only, no grading`,m.picked.join()===String(i)&&!m.graded&&!m.fb,m)}
        continue}
      checks++;
      for(let i=0;i<c.opts.length;i++){const o=c.opts[i];await page.locator(`#${c.id} .opt >> nth=${i}`).click();await L.wait(page,80);
        const m=await page.evaluate(([id,i])=>{const C=document.getElementById(id),os=[...C.querySelectorAll('.opt')],o=os[i],fb=C.querySelector('.fb');const cs=fb&&getComputedStyle(fb),S=document.querySelector('.slide.current').getBoundingClientRect(),r=fb&&fb.getBoundingClientRect();
          const k=S.width/1600;return {mark:o.classList.contains('okmk')?'right':o.classList.contains('wrong')?'wrong':'none',others:os.filter((x,j)=>j!==i&&(x.classList.contains('okmk')||x.classList.contains('wrong'))).length,
            fb:fb?fb.textContent.trim():'',fbVis:!!fb&&cs.visibility==='visible',px:fb?parseFloat(cs.fontSize):0,color:fb?fb.className:'',onSlide:!!r&&r.width>0&&r.left>=S.left-1&&r.right<=S.right+1&&r.top>=S.top-1&&r.bottom<=S.bottom+1,
            ansHidden:!C.querySelector('.ans')||getComputedStyle(C.querySelector('.ans')).visibility!=='visible'}},[c.id,i]);
        ok(`s${s+1}f${f} ${c.id} click ${'ABC'[i]} (${o.ok?'right':'wrong'}): ${o.ok?'green mark and reason':'red mark and its feedback'}, visible at ${m.px} px`,
          m.mark===(o.ok?'right':'wrong')&&!m.others&&m.fbVis&&m.onSlide&&m.px>=34&&m.fb&&m.fb===o.fb&&m.color.includes(o.ok?'ok':'bad'),m)}
      await page.keyboard.press('PageDown');await L.wait(page,200);
      const a=await page.evaluate(id=>{const C=document.getElementById(id),vis=e=>e&&getComputedStyle(e).visibility==='visible';return {ans:vis(C.querySelector('.ans')),right:[...C.querySelectorAll('.opt.right')].map(o=>o.id),marks:C.querySelectorAll('.opt.okmk,.opt.wrong,.opt.picked').length,fb:C.querySelector('.fb.on')?1:0}},c.id);
      const right=c.opts.find(o=>o.ok);
      ok(`s${s+1} ${c.id} Next: the answer shows, ${right?right.id:'?'} is marked right, no mouse marks left`,a.ans&&right&&a.right.join()===right.id&&!a.marks&&!a.fb,a);
      await page.evaluate(([s,f])=>Deck.go(s,f),[s,f]);await L.wait(page,80)}
  }
  ok('every graded option has a feedback line and exactly one right option per check',await page.evaluate(()=>[...document.querySelectorAll('.slide .check:not([data-mode]),.slide .checkrow')].every(c=>{const o=[...c.querySelectorAll('.opt')];return o.every(x=>x.dataset.fb)&&o.filter(x=>x.dataset.ok==='1').length===1})));
  ok('no console errors',!errors.length,errors);
  L.save('click.json',{checks,picks,res,fails});
  console.log(`click: ${checks} graded checks, ${picks} Predict-now questions, ${res.length} assertions, ${fails.length?'FAIL':'PASS'}`);fails.forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
