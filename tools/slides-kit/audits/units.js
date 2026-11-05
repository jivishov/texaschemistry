// List the zoom units on every frame of slides SLIDES (registry extra_slides, "first,last"; 4.2: 6,12), with the visible cards/captions that are not units.
// SLIDES=6,12 node units.js <deck> [out.json]
const {chromium}=require('playwright'),fs=require('fs');
if(!/^\d+,\d+$/.test(process.env.SLIDES||''))throw new Error('set SLIDES=first,last (registry extra_slides); suite.py sets it');
const [S0,S1]=process.env.SLIDES.split(',').map(n=>+n-1);
(async()=>{const [deck,out]=process.argv.slice(2);const b=await chromium.launch(),p=await (await b.newContext({viewport:{width:1920,height:1080},reducedMotion:'reduce'})).newPage();
  await p.goto('file://'+deck);await p.waitForFunction(()=>window.Deck&&Deck.slides.length>0);await p.waitForTimeout(400);
  const res=[];
  for(let s=S0;s<=S1;s++){const nf=await p.evaluate(s=>Deck.slides[s].frames.length,s);
    for(let f=0;f<nf;f++){await p.evaluate(([s,f])=>Deck.go(s,f),[s,f]);await p.waitForTimeout(120);
      const r=await p.evaluate(()=>{const U=Deck.zoomUnits(),S=document.querySelector('.slide.current');
        const vis=e=>{if(!e.getClientRects().length)return false;const c=getComputedStyle(e);if(c.visibility!=='visible'||+c.opacity<.05)return false;const q=e.getBoundingClientRect();return q.width>8&&q.height>8};
        const txt=e=>e.textContent.replace(/\s+/g,' ').trim().slice(0,40);
        // candidate visible cards / captions outside animations: elements with direct visible text or card classes
        // every visible band caption or card outside the animation, outermost only (a rule row zooms one line at a time)
        const C=[...S.querySelectorAll('.caprow,.rulerow>p,.card,.checkrow,.memrow')].filter(e=>!e.closest('.sim,.notes,.timer')&&vis(e)&&txt(e));
        const cards=C.filter(e=>!C.some(o=>o!==e&&o.contains(e)));
        const miss=[],dup=[];const ids=U.map(u=>u.id);
        cards.filter(e=>e.id).forEach(e=>{const n=ids.filter(i=>i===e.id).length;if(n===0)miss.push(e.id);if(n>1)dup.push(e.id)});
        const anon=cards.filter(e=>!e.id).length,anonU=U.filter(u=>!u.id).length;if(anon!==anonU)miss.push(`${anon} lines without id vs ${anonU} units`);
        return {units:U.map(u=>({id:u.id,kind:u.kind,label:u.label})),cards:cards.map(e=>e.id||txt(e).slice(0,20)),miss,dup}});
      res.push({s:s+1,f,...r})}}
  if(out)fs.writeFileSync(out,JSON.stringify(res,null,1));
  res.forEach(x=>console.log(`s${x.s}f${x.f}: ${x.units.map(u=>u.kind+(u.label?'('+u.label+')':'')+(u.id?'#'+String(u.id).slice(0,18):'')).join(' | ')}${x.miss.length||x.dup.length?'   MISSING '+x.miss.join(',')+' DUP '+x.dup.join(','):''}`));
  const bad=res.filter(x=>x.miss.length||x.dup.length);console.log(`${res.length} frames, ${res.reduce((a,x)=>a+x.cards.length,0)} visible cards and captions, ${bad.length} frames with a card missing or twice: ${bad.length?'FAIL':'PASS'}`);
  process.exitCode=bad.length?1:0;await b.close()})();
