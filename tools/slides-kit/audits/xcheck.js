// Step 7 cross-check: the unit blueprint's numbers against the built decks, and every "slide N" mention in each deck.
// Rule (coordinator): a matrix slide must exist and carry the objective in its footer reference, or hold a check for that objective.
// Configuration (suite.py sets it from registry.json): XCHECK, a JSON list of decks
//   [{lesson:'4.1', deck:<deck path>, blueprint:<unit blueprint path>, section:'41', next:'42', objectives:['4.1.1',…], mentions:{…}, walk:<walk-light.json>}]
// and OUT, the folder that receives xcheck.json.
const fs=require('fs'),path=require('path'),{chromium}=require('playwright');
if(!process.env.XCHECK||!process.env.OUT)throw new Error('set XCHECK (the decks to cross-check) and OUT; suite.py sets both');
const DECKS=JSON.parse(process.env.XCHECK),OUT=path.resolve(process.env.OUT);
const BPS={},bp=f=>BPS[f]||(BPS[f]=fs.readFileSync(f,'utf8'));
const res=[];const ok=(n,p,i)=>{res.push({n,pass:!!p,i:i===undefined?'':(typeof i==='string'?i:JSON.stringify(i))})};
const range=t=>t.split(',').flatMap(p=>{const m=p.trim().match(/^(\d+)(?: to (\d+))?$/);if(!m)throw new Error('bad range '+t);const a=+m[1],b=m[2]?+m[2]:a;return Array.from({length:b-a+1},(_,k)=>a+k)});
// does a footer reference name objective o? "§4.2.2", "Objective 4.2.2", "§4.2.2 and §4.2.3", ranges "§4.1.1 to §4.1.3", "Objectives 4.2.2 to 4.2.4"
const covers=(ref,o)=>{const n=o.split('.').map(Number);const ids=[...ref.matchAll(/(\d+)\.(\d+)\.(\d+)/g)].map(m=>[+m[1],+m[2],+m[3]]);
  if(ids.some(x=>x.join('.')===o))return true;
  const r=ref.match(/(\d+\.\d+\.\d+)\s+to\s+§?(\d+\.\d+\.\d+)/);if(r){const a=r[1].split('.').map(Number),b=r[2].split('.').map(Number);return a[0]===n[0]&&a[1]===n[1]&&n[2]>=a[2]&&n[2]<=b[2]}
  return false};
// expected targets of every "slide N" mention in notes and text (deck, slide id, number) -> title of the slide meant (registry "mentions")
const MENTIONS=Object.fromEntries(DECKS.map(d=>[d.lesson,d.mentions]));
(async()=>{
  const b=await chromium.launch();
  const sec=(BP,id,next)=>BP.slice(BP.indexOf('id="'+id+'"'),BP.indexOf('id="'+next+'"'));
  // the matrix rows of the objectives the registry lists for these decks
  const OBJ=DECKS.flatMap(d=>d.objectives),matrix={};
  for(const f of new Set(DECKS.map(d=>d.blueprint)))for(const m of bp(f).matchAll(/<tr><td>(\d+\.\d+\.\d+)<\/td><td>[^<]*<\/td><td>([^<]*)<\/td>/g))if(OBJ.includes(m[1]))matrix[m[1]]=m[2];
  ok(`matrix: ${OBJ.length} rows ${OBJ[0]} to ${OBJ[OBJ.length-1]} found`,OBJ.every(o=>o in matrix),matrix);
  for(const {lesson:L,deck,blueprint,section:sid,next:nid,objectives,walk} of DECKS){const BP=bp(blueprint);
    const p=await b.newPage({viewport:{width:1920,height:1080}});await p.goto('file://'+path.resolve(deck));await p.waitForTimeout(500);
    const S=await p.evaluate(()=>Deck.slides.map((S,i)=>{const cl=S.el.cloneNode(true);cl.querySelectorAll('.notes,script').forEach(n=>n.remove());
      return {n:i+1,id:S.id,title:S.title,period:+S.period,ref:S.ref,checks:S.el.querySelectorAll('.card.check[id$="-check"],.checkrow').length,
      notes:[...S.frames.map((f,k)=>({w:'f'+k,t:f.note||''})),{w:'notes',t:S.notes?S.notes.textContent:''},{w:'text',t:cl.textContent.replace(/\s+/g,' ')}]}}));
    await p.close();
    // deck sentence
    const m=sec(BP,sid,nid).match(/Slide checks: (\d+),[^.]*\. The deck has (\d+) slides: period 1 uses slides 1 to (\d+), period 2 slides (\d+) to (\d+)\./);
    ok(`${L} blueprint sentence found`,!!m,m&&m[0]);
    const [ , chk,n,p1e,p2s,p2e]=m.map(Number),last1=Math.max(...S.filter(s=>s.period===1).map(s=>s.n)),first2=Math.min(...S.filter(s=>s.period===2).map(s=>s.n));
    ok(`${L} "The deck has ${n} slides": deck has ${S.length}`,S.length===n);
    ok(`${L} "period 1 uses slides 1 to ${p1e}": last period-1 slide is ${last1}, all of 1..${p1e} are period 1`,last1===p1e&&S.slice(0,p1e).every(s=>s.period===1));
    ok(`${L} "period 2 slides ${p2s} to ${p2e}": first period-2 slide is ${first2}, all of ${p2s}..${p2e} are period 2`,first2===p2s&&p2e===S.length&&S.slice(p2s-1).every(s=>s.period===2));
    const ck=S.filter(s=>s.checks).map(s=>s.n);ok(`${L} "Slide checks: ${chk}": slides with a check are ${ck.join(', ')}`,ck.length===chk);
    // matrix rows
    for(const ob of objectives){const list=range(matrix[ob]);
      list.forEach(k=>{const s=S[k-1];const why=!s?'missing':covers(s.ref,ob)?`footer "${s.ref}"`:'';
        ok(`${ob} → slide ${k}${s?' ('+s.title+')':''}: exists and carries ${ob}`,!!why&&why!=='missing',why||(s?`footer "${s.ref}", ${s.checks?'a check on the slide but its footer does not name '+ob:'no check'}`:'slide missing'))})}
    // the rate slide's review lines: each slide exists, carries the objective, and lies in the matrix row
    const rate=S.find(s=>/Rate your learning/.test(s.title)),rt=rate.notes.find(x=>x.w==='text').t;
    for(const mm of rt.matchAll(new RegExp('('+objectives.map(o=>o.replace(/\./g,'\\.')).join('|')+')[^R]*?Review: (slides? [0-9 ,andto]+?)(?= \\d\\.\\d|\\s*$)','g'))){
      const ob=mm[1],nums=range(mm[2].replace(/^slides? /,'').replace(' and ',', ')),mx=range(matrix[ob]);
      ok(`${L} rate slide ${rate.n}: ${ob} "Review: ${mm[2].replace(/^slides? /,'')}" are slides that carry ${ob} and are in the matrix row (${matrix[ob]})`,
        nums.every(k=>S[k-1]&&covers(S[k-1].ref,ob)&&mx.includes(k)),nums.length<mx.length?`matrix also lists ${mx.filter(k=>!nums.includes(k)).join(', ')}`:'same set')}
    // every "slide N" mention
    const re=/\b[Ss]lides?\s+(\d+(?:\s*(?:to|and|,)\s*\d+)*)/g;let seen=0;
    S.forEach(s=>{if(s===rate)return;const done=new Set();s.notes.forEach(x=>{for(const mm of x.t.matchAll(re)){const nums=range(mm[1].replace(/ and /g,', '));
      nums.forEach(k=>{const key=s.id+':'+k;if(done.has(key))return;done.add(key);seen++;const exp=MENTIONS[L][key];
        ok(`${L} ${s.id} mentions slide ${k} ("…${x.t.slice(Math.max(0,mm.index-40),mm.index+mm[0].length).trim()}")`,exp&&S[k-1]&&S[k-1].title===exp,exp?`target: ${S[k-1]?S[k-1].title:'missing'}`:'no expected target listed')})}})});
    ok(`${L} every listed mention was found`,Object.keys(MENTIONS[L]).every(k=>res.some(r=>r.n.startsWith(L+' '+k.split(':')[0]+' mentions slide '+k.split(':')[1]+' '))),`${seen} mentions`);
    // footer cues "slide N: Title" from the walk
    const w=JSON.parse(fs.readFileSync(walk));let nc=0,bad=[];
    w.rec.forEach(r=>{const c=r.cue.match(/slide (\d+): (.+)$/);if(c){nc++;const t=S[+c[1]-1];if(!(t&&t.title.startsWith(c[2].replace(/…$/,''))&&+c[1]===r.s+1))bad.push(r.cue)}});
    ok(`${L} footer cues "slide N: title": ${nc} cues, each names the next slide by its number and title`,!bad.length&&nc===S.length-1,bad.join(' | '))}
  await b.close();
  res.forEach(r=>console.log(`  ${r.pass?'PASS':'FAIL'}  ${r.n}${r.i?'  ('+r.i+')':''}`));const f=res.filter(r=>!r.pass).length;
  fs.writeFileSync(path.join(OUT,'xcheck.json'),JSON.stringify(res,null,1));console.log(`xcheck: ${res.length-f} of ${res.length} pass${f?', '+f+' FAIL':''}`);process.exitCode=f?1:0;
})();
