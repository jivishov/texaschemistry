// 2. Back: record every frame forward, then PageUp from the end to the start.
// At each landing the frame state (visible blocks, managed classes, timer, every animation's get()) must equal the forward record.
const L=require('./lib');
(async()=>{
  const {browser,page,errors}=await L.open({theme:process.argv[2]||'light'});
  const fwd={},fails=[];let prev=null,n=0;
  while(true){await L.wait(page,230);const fs=await L.frameState(page);
    if(prev&&prev.s===fs.s&&prev.f===fs.f)break;fwd[fs.s+'.'+fs.f]=fs;prev=fs;n++;await page.keyboard.press('PageDown')}
  let m=0;prev=null;
  while(true){await L.wait(page,230);const fs=await L.frameState(page),key=fs.s+'.'+fs.f;
    if(prev&&prev.s===fs.s&&prev.f===fs.f)break;
    const want=JSON.stringify(fwd[key]),got=JSON.stringify(fs);
    if(want!==got)fails.push(`s${fs.s+1}f${fs.f}: back ${got} vs forward ${want}`);
    if(prev){const lastOfPrev=await page.evaluate(s=>Deck.slides[s].frames.length-1,fs.s);
      if(!((fs.s===prev.s&&fs.f===prev.f-1)||(fs.s===prev.s-1&&fs.f===lastOfPrev)))fails.push(`PageUp from s${prev.s+1}f${prev.f} landed on s${fs.s+1}f${fs.f}`)}
    prev=fs;m++;await page.keyboard.press('PageUp')}
  if(m!==n)fails.push(`forward visited ${n} states, back visited ${m}`);
  if(errors.length)fails.push('console errors: '+errors.join(' | '));
  L.save('back.json',{forward:n,back:m,fails,fwd});
  console.log(`back: ${n} forward, ${m} back, ${fails.length?'FAIL':'PASS'}`);fails.forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
