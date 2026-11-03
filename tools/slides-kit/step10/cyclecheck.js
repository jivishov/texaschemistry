// Motion on: does the zoom cycle reach every unit right after a Next press? Slides 6..12 of 4.2. node cyclecheck.js <deck>
const {chromium}=require('playwright');
(async()=>{const [deck]=process.argv.slice(2);const b=await chromium.launch(),p=await (await b.newContext({viewport:{width:1920,height:1080}})).newPage();
  await p.goto('file://'+deck);await p.waitForFunction(()=>window.Deck&&Deck.slides.length>0);await p.waitForTimeout(400);
  const bad=[];let n=0;
  for(let s=5;s<=11;s++){const nf=await p.evaluate(s=>Deck.slides[s].frames.length,s);
    for(const mode of ['plain','kept'])for(let f=1;f<nf;f++){
      await p.evaluate(([s,f])=>Deck.go(s,f),[s,f-1]);await p.waitForTimeout(500);
      if(mode==='kept'){await p.keyboard.press('.');await p.waitForTimeout(450)}
      await p.keyboard.press('PageDown');await p.waitForTimeout(60);
      let st=await p.evaluate(()=>Deck.state());
      if(mode==='plain'||!st.zoom){await p.keyboard.press('.');await p.waitForTimeout(60);st=await p.evaluate(()=>Deck.state())}
      const got=st.zoomCount;await p.keyboard.press('Escape');await p.waitForTimeout(500);
      const want=(await p.evaluate(()=>Deck.zoomUnits())).length;n++;
      if(got!==want)bad.push(`s${s+1}f${f} ${mode}: cycle has ${got} units right after Next, ${want} at rest`)}}
  console.log(`${n} checks, ${bad.length} short cycles`);bad.forEach(x=>console.log('  '+x));await b.close()})();
