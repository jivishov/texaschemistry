// Symbol and charge stay tight: for every <sup>/<sub> on every slide, the gap to the text before it is at most 2 canvas px.
const L=require('./lib');
(async()=>{
  const {browser,page}=await L.open({});
  const ns=await page.evaluate(()=>Deck.slides.length),bad=[];let n=0;
  for(let s=0;s<ns;s++){
    await page.evaluate(s=>Deck.go(s,-1),s);await L.wait(page,120);
    const r=await page.evaluate(()=>{const S=document.querySelector('.slide.current'),k=S.getBoundingClientRect().width/1600,out=[];let n=0;
      S.querySelectorAll('sup,sub').forEach(e=>{if(e.closest('svg,.notes'))return;let p=e.previousSibling;
        if(!p||p.nodeType!==3||!/\S$/.test(p.nodeValue))return;n++;
        const rg=document.createRange();rg.setStart(p,p.nodeValue.length-1);rg.setEnd(p,p.nodeValue.length);const a=rg.getBoundingClientRect(),b=e.getBoundingClientRect();
        if(!a.width&&!b.width)return;const gap=(b.left-a.right)/k;if(gap>2)out.push({text:p.nodeValue.trim().slice(-6)+e.textContent,gap:Math.round(gap)})});
      return {n,out}});
    n+=r.n;r.out.forEach(o=>bad.push(`slide ${s+1}: "${o.text}" gap ${o.gap}px`));
  }
  L.save('supgap.json',{checked:n,bad});
  console.log(`supgap: ${n} symbol+charge pairs checked, ${bad.length?'FAIL':'PASS'}`);bad.forEach(b=>console.log('  - '+b));
  await browser.close();process.exitCode=bad.length?1:0;
})();
