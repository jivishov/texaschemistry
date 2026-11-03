// 7. Readability: student-facing text of each slide (all blocks, all frames; not notes, cue or section label).
// Flesch-Kincaid grade and average sentence length per slide; flags grade > 8, average > 14 words,
// any single sentence over 14 words, and sentences that start with "This lesson", "It is important", "In order to".
const L=require('./lib');
function syl(w){w=w.toLowerCase().replace(/[^a-z]/g,'');if(!w)return 0;if(w.length<=3)return 1;
  w=w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/,'').replace(/^y/,'');const m=w.match(/[aeiouy]{1,2}/g);return Math.max(1,m?m.length:1)}
(async()=>{
  const {browser,page}=await L.open({});
  const units=await page.evaluate(()=>Deck.slides.map(S=>{
    const BLOCK='p,li,td,th,h2,text,.k,.term,.mean,.tag,.line,.cell,.rh,.ans,.q,.small';
    const groups=new Map();const w=document.createTreeWalker(S.el,NodeFilter.SHOW_TEXT);let n;
    while((n=w.nextNode())){const e=n.parentElement;if(e.closest('.notes,script,style,.timer'))continue;const b=e.closest(BLOCK)||e;
      groups.set(b,(groups.get(b)||'')+' '+n.nodeValue)}
    // nested blocks: keep the innermost text with its own block
    return {title:S.title,units:[...groups.values()].map(t=>t.replace(/\s+/g,' ').trim()).filter(Boolean)};
  }));
  // word budget: student-facing prose visible at one time (per frame), outside tables and labels.
  // Not counted: tables, the four-part argument table (.cer), the glossary strip (.words), legend, chips and labels,
  // sentence frames and word banks (fragments, as ruled by the coordinator); teacher round: chips, and the done cards of an
  // accumulating column (already read on an earlier frame, kept on screen as a reminder) — the budget counts the active card.
  const budget=[];
  for(let s=0;s<units.length;s++){const nf=await page.evaluate(s=>Deck.slides[s].frames.length,s);let max=0,at=0;
    for(let f=0;f<nf;f++){await page.evaluate(([s,f])=>Deck.go(s,f),[s,f]);
      const n=await page.evaluate(()=>{const S=document.querySelector('.slide.current');let t='';
        const w=document.createTreeWalker(S,NodeFilter.SHOW_TEXT);let x;
        while((x=w.nextNode())){const e=x.parentElement;if(e.closest('.notes,script,style,.timer,h2,td,th,.tag,.rh,.k,.rail,.opt>b,.bank,.frames,svg,.es,.cer,.words,.legend,.lbl,.rev,.scale,.r800,.kicker,.bt,.chips,.acc>.adone'))continue;
          const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none')continue;t+=' '+x.nodeValue}
        return t.split(/\s+/).filter(x=>/[A-Za-z]/.test(x)).length});
      if(n>max){max=n;at=f}}
    budget.push({max,at})}
  const DQ=await page.evaluate(()=>[...new Set([...document.querySelectorAll('.dq p:not(.tag)')].map(p=>p.textContent.replace(/\s+/g,' ').trim()))]);
  const BAN=/^(This lesson|It is important|In order to)\b/i,slides=[],fails=[];
  units.forEach((u,i)=>{
    const sents=[];u.units.forEach(t=>t.split(/(?<=[.?!][”"’)]?)\s+(?=[A-Z“"(0-9+−])/).forEach(s=>{if(s.trim())sents.push(s.trim())}));
    let words=0,syls=0;const long=[],banned=[];
    sents.forEach(s=>{const ws=s.split(/\s+/).filter(x=>/[A-Za-z]/.test(x));words+=ws.length;ws.forEach(x=>{syls+=syl(x)});
      if(ws.length>14&&!DQ.includes(s))long.push(s);if(BAN.test(s))banned.push(s)});
    const S=sents.filter(s=>/[A-Za-z]/.test(s)).length||1,W=words||1;
    const fk=0.39*(W/S)+11.8*(syls/W)-15.59,asl=W/S;
    // prose only: full sentences (end punctuation, 4+ words), the register the rule cards and prompts use
    const prose=sents.filter(s=>/[.?!][”"’)]?$/.test(s)&&s.split(/\s+/).filter(x=>/[A-Za-z]/.test(x)).length>=4);
    let pw=0,ps=0;prose.forEach(s=>{const ws=s.split(/\s+/).filter(x=>/[A-Za-z]/.test(x));pw+=ws.length;ws.forEach(x=>{ps+=syl(x)})});
    const pfk=prose.length?0.39*(pw/prose.length)+11.8*(ps/(pw||1))-15.59:null;
    const row={slide:i+1,title:u.title,maxVisibleProseWords:budget[i].max,atFrame:budget[i].at,sentences:S,words,avgWords:+asl.toFixed(1),fk:+fk.toFixed(1),prose:prose.length,proseAvgWords:prose.length?+(pw/prose.length).toFixed(1):null,proseFk:pfk==null?null:+pfk.toFixed(1),long,banned};slides.push(row);
    if(pfk!=null&&pfk>8)fails.push(`slide ${i+1}: prose FK grade ${row.proseFk} > 8`);
    if(budget[i].max>35)fails.push(`slide ${i+1}: ${budget[i].max} words of prose visible at frame ${budget[i].at} (budget 35)`);
    if(fk>8)fails.push(`slide ${i+1}: FK grade ${row.fk} > 8`);if(asl>14)fails.push(`slide ${i+1}: ${row.avgWords} words per sentence > 14`);
    long.forEach(s=>fails.push(`slide ${i+1}: sentence over 14 words: "${s}"`));banned.forEach(s=>fails.push(`slide ${i+1}: banned opening: "${s}"`));
  });
  const regs=await page.evaluate(()=>[...document.querySelectorAll('.slide .reg')].map(e=>{const c=e.cloneNode(true);c.querySelectorAll('.tag').forEach(t=>t.remove());const w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT);let n,t=[];while((n=w.nextNode()))t.push(n.nodeValue);return {slide:[...document.querySelectorAll('.slide')].indexOf(e.closest('.slide'))+1,id:e.id||e.className,text:t.join(' ').replace(/\s+([.,?!])/g,'$1').replace(/\s+/g,' ').trim()}}));
  const reg=regs.map(r=>{const se=r.text.split(/(?<=[.?!][”"’)]?)\s+/).filter(x=>/[A-Za-z]/.test(x));let W=0,Y=0;se.forEach(x=>{const ws=x.split(/\s+/).filter(t=>/[A-Za-z]/.test(t));W+=ws.length;ws.forEach(t=>{Y+=syl(t)})});
    const fk=0.39*(W/se.length)+11.8*(Y/W)-15.59;return {...r,fk:+fk.toFixed(1),inTarget:fk>=5&&fk<=8}});
  reg.forEach(r=>{if(r.fk>8)fails.push(`slide ${r.slide} ${r.id}: register grade ${r.fk} > 8`)});
  reg.forEach(r=>console.log(`  register (rule/prompt/sample) slide ${r.slide} ${r.id}: grade ${r.fk}${r.inTarget?'':' (outside 5 to 8)'}: "${r.text}"`));
  L.save('readability.json',{slides,fails,units,register:reg});
  slides.forEach(r=>console.log(`  slide ${r.slide} ${r.title}: FK ${r.fk} (${r.avgWords} words/unit, ${r.sentences} units, ${r.words} words); prose only: FK ${r.proseFk}, ${r.proseAvgWords} words/sentence, ${r.prose} sentences; max ${r.maxVisibleProseWords} prose words visible (frame ${r.atFrame})`));
  console.log(`readability: ${fails.length?'FAIL':'PASS'}`);fails.forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
