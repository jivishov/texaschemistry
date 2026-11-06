// Step 7 cross-check: the unit blueprint's numbers against the built decks, and every "slide N" mention in each deck.
// Rule (coordinator): a matrix slide must exist and carry the objective in its footer reference, or hold a check for that objective.
// Configuration (suite.py sets it from registry.json): XCHECK, a JSON list of decks
//   [{lesson:'4.1', deck:<deck path>, blueprint:<unit blueprint path>, section:'41', next:'42', objectives:['4.1.1',…], mentions:{…}, walk:<walk-light.json>}]
// and OUT, the folder that receives xcheck.json.
// Each deck also carries form (registry blueprint.form; "unit4" when absent), teks_rows (blueprint.teks_rows), checks and periods.
//   form "unit4": the blueprint prints "Slide checks: N, … The deck has N slides: period 1 uses slides 1 to A, period 2 slides B to C."
//     and the objective rows <tr><td>4.1.1</td><td>…</td><td>SLIDES</td>; the assertions below are the Unit 4 ones, unchanged.
//   form "unit5": inside the lesson's section (section to next) the "Slides and missions" deck line
//     "Deck: N slides. Checkpoints A to B, predictions revisited C, CER exit ticket D, self-rating E." and the objectives table rows
//     <tr><td>5.1.k</td><td>…</td><td>…</td><td>SLIDES</td></tr>; in section "matrix" the row whose first cell carries each TEKS code
//     of teks_rows ({"C.8(A)": ["5.1.1", "5.1.2"], …}) and the cell "Deck 5.1, slides …". The check count and the period split
//     are asserted against the registry (checks, periods) and the deck: the Unit 5 blueprint does not print them.
//   Both forms: the rate slide's review lines, every "slide N" mention (registry mentions) and the footer cues from the walk.
// Dry run (form "unit5" only): node audits/xcheck.js --dry (or XCHECK_DRY=1) prints what the parser reads from the blueprint, with
//   no deck, no browser and no OUT; exit 1 if a deck line, objective row or matrix row is not found.
const fs=require('fs'),path=require('path'),{chromium}=require('playwright');
const DRY=process.argv.includes('--dry')||process.env.XCHECK_DRY==='1';
if(!process.env.XCHECK||!process.env.OUT&&!DRY)throw new Error('set XCHECK (the decks to cross-check) and OUT; suite.py sets both');
const DECKS=JSON.parse(process.env.XCHECK),OUT=DRY?null:path.resolve(process.env.OUT);
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
const form=d=>d.form||'unit4';
const ranged=t=>{try{return range(t)}catch(e){return null}};
// the Unit 5 form, read from the blueprint alone (no deck): the deck line, the objectives table, the matrix rows of teks_rows
function parse5(d){
  const BP=bp(d.blueprint),SEC=BP.slice(BP.indexOf('id="'+d.section+'"'),BP.indexOf('id="'+d.next+'"'));
  const m=SEC.match(/Deck: (\d+) slides(?:, [^.<]*)?\. Checkpoints (\d+) to (\d+), predictions revisited (\d+), CER exit ticket (\d+), self-rating (\d+)\./);
  const line=m&&{text:m[0],n:+m[1],a:+m[2],b:+m[3],c:+m[4],d:+m[5],e:+m[6]};
  const obj={};for(const r of SEC.matchAll(/<tr><td>(\d+\.\d+\.\d+)<\/td><td>.*?<\/td><td>.*?<\/td><td>([^<]*)<\/td><\/tr>/g))obj[r[1]]=r[2].trim();
  const MS=BP.slice(BP.indexOf('id="matrix"')),MX=MS.slice(0,MS.indexOf('</section>'));
  const cells=row=>[...row.matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)].map(c=>c[1].replace(/<[^>]+>/g,'').replace(/\s+/g,' ').trim());
  const dk=new RegExp('Deck '+d.lesson.replace(/\./g,'\\.')+', slides? (\\d+(?: to \\d+)?(?:, \\d+(?: to \\d+)?)*)');
  const rows={};
  for(const code of Object.keys(d.teks_rows||{})){
    const hit=[...MX.matchAll(/<tr>([\s\S]*?)<\/tr>/g)].map(r=>cells(r[1])).filter(c=>c.length&&c[0].includes(code)).map(c=>({c,m:c.join(' | ').match(dk)})).filter(x=>x.m);
    rows[code]={n:hit.length,list:hit.length?hit[0].m[1]:null,first:hit.length?hit[0].c[0]:'',objCell:hit.length?hit[0].c[1]||'':''};
  }
  return {line,obj,rows};
}
if(DRY){let bad=0;
  for(const d of DECKS){
    if(form(d)!=='unit5'){console.log(`xcheck --dry: ${d.lesson}: form ${form(d)} has no dry run (only form unit5)`);continue}
    const P=parse5(d),L=P.line;
    console.log(`xcheck --dry: ${d.lesson}, ${d.blueprint}, form unit5, section ${d.section} (to ${d.next}), no deck`);
    console.log(`  deck line: ${L?'"'+L.text+'"':'NOT FOUND'}`);
    if(L)console.log(`  section ${d.section}: deck ${L.n}, checkpoints ${L.a} to ${L.b}, predictions ${L.c}, exit ${L.d}, rating ${L.e}`);
    console.log(`  objectives: ${d.objectives.map(o=>`${o} ${o in P.obj?'"'+P.obj[o]+'"':'NOT FOUND'}`).join(', ')}`);
    console.log(`  matrix: ${Object.keys(d.teks_rows||{}).map(c=>`${c} ${P.rows[c].list?'"'+P.rows[c].list+'"':'NOT FOUND'}${P.rows[c].n>1?' ('+P.rows[c].n+' rows)':''}`).join(', ')}`);
    for(const [c,obs] of Object.entries(d.teks_rows||{})){const R=P.rows[c];if(!R.list)continue;
      const list=[...new Set(ranged(R.list)||[])].sort((x,y)=>x-y),un=[...new Set(obs.flatMap(o=>ranged(P.obj[o]||'')||[]))].sort((x,y)=>x-y);
      console.log(`    ${c}: row "${R.first}", objectives cell "${R.objCell}"; slides ${list.join(', ')}; union of ${obs.join(', ')}: ${un.join(', ')} (${list.join()===un.join()?'equal':'NOT equal'})`)}
    bad+=(L?0:1)+d.objectives.filter(o=>!(o in P.obj)).length+Object.values(P.rows).filter(R=>R.n!==1).length;
  }
  console.log(`xcheck --dry: ${bad?bad+' item(s) not found':'every item found'}; no assertion run against a deck`);process.exitCode=bad?1:0;
}else(async()=>{
  const b=await chromium.launch();
  const sec=(BP,id,next)=>BP.slice(BP.indexOf('id="'+id+'"'),BP.indexOf('id="'+next+'"'));
  // the matrix rows of the objectives the registry lists for these decks
  const U4=DECKS.filter(d=>form(d)==='unit4');   /* the Unit 4 form; a Unit 5 deck fills matrix from its objectives table below */
  const OBJ=U4.flatMap(d=>d.objectives),matrix={};
  for(const f of new Set(U4.map(d=>d.blueprint)))for(const m of bp(f).matchAll(/<tr><td>(\d+\.\d+\.\d+)<\/td><td>[^<]*<\/td><td>([^<]*)<\/td>/g))if(OBJ.includes(m[1]))matrix[m[1]]=m[2];
  if(U4.length)ok(`matrix: ${OBJ.length} rows ${OBJ[0]} to ${OBJ[OBJ.length-1]} found`,OBJ.every(o=>o in matrix),matrix);
  for(const {lesson:L,deck,blueprint,section:sid,next:nid,objectives,walk,form:FM,teks_rows:TR,checks:RC,periods:RP} of DECKS){const BP=bp(blueprint);
    const p=await b.newPage({viewport:{width:1920,height:1080}});await p.goto('file://'+path.resolve(deck));await p.waitForTimeout(500);
    const S=await p.evaluate(()=>Deck.slides.map((S,i)=>{const cl=S.el.cloneNode(true);cl.querySelectorAll('.notes,script').forEach(n=>n.remove());
      return {n:i+1,id:S.id,title:S.title,period:+S.period,ref:S.ref,checks:S.el.querySelectorAll('.card.check[id$="-check"],.checkrow').length,
      notes:[...S.frames.map((f,k)=>({w:'f'+k,t:f.note||''})),{w:'notes',t:S.notes?S.notes.textContent:''},{w:'text',t:cl.textContent.replace(/\s+/g,' ')}]}}));
    await p.close();
    if(FM==='unit5'){const P=parse5({lesson:L,blueprint,section:sid,next:nid,teks_rows:TR}),D=P.line,t=k=>S[k-1]?S[k-1].title:'missing';
      // the deck line of "Slides and missions"
      ok(`${L} blueprint deck line found`,!!D,D?D.text:`"Deck: N slides. Checkpoints A to B, predictions revisited C, CER exit ticket D, self-rating E." not in section ${sid}`);
      if(D){ok(`${L} "Deck: ${D.n} slides": deck has ${S.length}`,S.length===D.n);
        const cp=S.slice(D.a-1,D.b);
        ok(`${L} "Checkpoints ${D.a} to ${D.b}": the checkpoint routine slide, then three checkpoint slides (titles start with "Checkpoint")`,
          D.b-D.a===3&&cp.length===4&&cp.every(s=>/^Checkpoint/.test(s.title))&&/routine/i.test(cp[0].title),cp.map(s=>s.n+' '+s.title).join(', ')||'no slides');
        ok(`${L} "predictions revisited ${D.c}, CER exit ticket ${D.d}": both are the slide "Predictions and exit ticket"`,D.c===D.d&&t(D.c)==='Predictions and exit ticket',`${D.c} ${t(D.c)}${D.c!==D.d?', '+D.d+' '+t(D.d):''}`);
        ok(`${L} "self-rating ${D.e}": the slide "Rate your learning"`,t(D.e)==='Rate your learning',`${D.e} ${t(D.e)}`)}
      // the check count and the period split: registry and deck (the Unit 5 blueprint does not print them)
      const ck=S.filter(s=>s.checks).map(s=>s.n);ok(`${L} registry "checks": ${RC}: slides with a check are ${ck.join(', ')}`,ck.length===RC);
      const p1e=RP[0][1],p2s=RP[1][0],p2e=RP[1][1],last1=Math.max(...S.filter(s=>s.period===1).map(s=>s.n)),first2=Math.min(...S.filter(s=>s.period===2).map(s=>s.n));
      ok(`${L} registry "periods" period 1 slides ${RP[0][0]} to ${p1e}: last period-1 slide is ${last1}, all of 1..${p1e} are period 1`,RP[0][0]===1&&last1===p1e&&S.slice(0,p1e).every(s=>s.period===1));
      ok(`${L} registry "periods" period 2 slides ${p2s} to ${p2e}: first period-2 slide is ${first2}, all of ${p2s}..${p2e} are period 2`,first2===p2s&&p2e===S.length&&S.slice(p2s-1).every(s=>s.period===2));
      // the objectives table: each listed slide exists and carries the objective in its footer reference (the Unit 4 rule)
      for(const ob of objectives){const list=ob in P.obj?ranged(P.obj[ob]):null;
        ok(`${L} objectives table row ${ob} found`,!!list,ob in P.obj?`slides "${P.obj[ob]}"`:'no row');
        if(!list)continue;matrix[ob]=P.obj[ob];
        list.forEach(k=>{const s=S[k-1];const why=!s?'missing':covers(s.ref,ob)?`footer "${s.ref}"`:'';
          ok(`${ob} → slide ${k}${s?' ('+s.title+')':''}: exists and carries ${ob}`,!!why&&why!=='missing',why||(s?`footer "${s.ref}", ${s.checks?'a check on the slide but its footer does not name '+ob:'no check'}`:'slide missing'))})}
      // the matrix rows: each listed slide carries one of the row's objectives; the row lists exactly the union of their slides
      for(const [code,obs] of Object.entries(TR||{})){const R=P.rows[code],list=R&&R.list?ranged(R.list):null;
        ok(`${L} matrix row ${code}: one row carries "Deck ${L}, slides …" and its objectives cell names ${obs.join(', ')}`,!!list&&R.n===1&&obs.every(o=>covers(R.objCell,o)),
          R&&R.n?`${R.n} row${R.n>1?'s':''}; "${R.first}": "${R.objCell}", slides "${R.list}"`:`no row whose first cell carries ${code} and names Deck ${L}`);
        if(!list)continue;
        list.forEach(k=>{const s=S[k-1],hit=s?obs.find(o=>covers(s.ref,o)):null;
          ok(`${L} ${code} → slide ${k}${s?' ('+s.title+')':''}: exists and carries one of ${obs.join(', ')}`,!!hit,s?`footer "${s.ref}"`:'slide missing')});
        const A=[...new Set(list)].sort((x,y)=>x-y),U=[...new Set(obs.flatMap(o=>ranged(P.obj[o]||'')||[]))].sort((x,y)=>x-y);
        ok(`${L} ${code} "slides ${R.list}" equal the union of the slides of ${obs.join(', ')}`,A.join()===U.join(),`row ${A.join(', ')}; union ${U.join(', ')}`)}
    }else{
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
    }
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
