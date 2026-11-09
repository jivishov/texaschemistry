// Reduced motion (3D fixed three-quarter view, no live loop, instant stages) and the narrow-screen fallback (scrolling page under 760 px).
const L=require('./lib');
(async()=>{
  const out=[];const ok=(n,p,i)=>out.push({n,pass:!!p,i:i||''});
  // deck-specific ids: EXTRAS_CFG, the registry's extras_cfg for the deck (suite.py sets it)
  if(!process.env.EXTRAS_CFG)throw new Error('set EXTRAS_CFG (registry extras_cfg); suite.py sets it');
  const C=JSON.parse(process.env.EXTRAS_CFG);
  let {browser,page,errors}=await L.open({reduced:true,hash:C.hash});
  await L.wait(page,600);
  const a=await page.evaluate(c=>document.querySelector(c).toDataURL(),C.canvas);await L.wait(page,900);
  const b=await page.evaluate(c=>document.querySelector(c).toDataURL(),C.canvas);
  ok('reduced motion: the turning 3D model holds a fixed view',a===b);
  await page.screenshot({path:L.OUT+'/reduced-s2f2.png'});
  await page.keyboard.press('PageDown');await L.wait(page,60);
  ok('reduced motion: a revealed block has no fade animation',await page.evaluate(b=>getComputedStyle(document.querySelector('[id="'+b+'"],[data-b="'+b+'"]')).animationName==='none',C.block));
  ok('reduced motion: no console errors',!errors.length,errors.join(' | '));
  await browser.close();
  ({browser,page,errors}=await L.open({}));
  await page.setViewportSize({width:420,height:860});await L.wait(page,800);
  const f=await page.evaluate(()=>({flow:Deck.state().flow,scroll:document.documentElement.scrollHeight,shown:[...document.querySelectorAll('.slide')].filter(s=>getComputedStyle(s).display!=='none').length,
    wide:document.documentElement.scrollWidth>innerWidth+1}));
  ok('under 760 px: scrolling page of all slides',f.flow&&f.shown===C.slides&&f.scroll>860,JSON.stringify(f));
  ok('under 760 px: no horizontal scroll',!f.wide);
  await page.screenshot({path:L.OUT+'/fallback-420.png',fullPage:false});
  await page.setViewportSize({width:1920,height:1080});await L.wait(page,600);
  const g=await page.evaluate(()=>({flow:Deck.state().flow,shown:[...document.querySelectorAll('.slide')].filter(s=>getComputedStyle(s).display!=='none').length}));
  ok('back to projector mode at 1920 px: one slide shown',!g.flow&&g.shown===1,JSON.stringify(g));
  ok('fallback: no console errors',!errors.length,errors.join(' | '));
  await browser.close();
  L.save('extras.json',out);out.forEach(r=>console.log(`  ${r.pass?'PASS':'FAIL'}  ${r.n}${r.i?'  ('+r.i+')':''}`));
  const n=out.filter(r=>!r.pass).length;console.log('extras: '+(n?'FAIL':'PASS'));process.exitCode=n?1:0;
})();
