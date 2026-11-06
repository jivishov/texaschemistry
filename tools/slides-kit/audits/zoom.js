// Zoom cycle audit (teacher round, A1): every frame of every slide, the Blank key steps through every visible unit.
// Per unit: the cue reads "Zoom i of n · Blank ▶ next|exit · Back ▶ exit", the unit fills at least 60% of the slide width or height,
// a zoomed check shows all its options; the press after the last unit unzooms; Back unzooms at once without moving.
// Screenshots of every zoomed state, and a zoom sheet: one zoomed state per unit type per slide.  node zoom.js [light|dark]
// Geometry (step 10): every zoomed unit is measured live on screen (Deck.state().zoomLive, from getBoundingClientRect): centred in the
// slide, wholly inside it (so above the footer), filling at least 60% of its width or height. The main pass loads at 1366 x 768
// and changes to 1920 x 1080 before zooming (F5 full screen). The matrix pass (motion on, as in the teacher's Chrome) runs every
// viewport 1366 x 768, 1536 x 864, 1920 x 1080, 1024 x 768 at device scale factors 1, 1.25 and 1.5, each loaded at another size
// and changed before zooming; per slide the last frame's whole cycle with a resize while zoomed (and back), and on every slide
// with an animation: the cycle on frame 0, Next while zoomed through every frame, a zoom during the zoom-out, a zoom right
// after Back, and a zoom after the slide list opened and closed.  MATRIX=0 skips the matrix pass.
const L=require('./lib'),fs=require('fs');
const TOL=6; // slide px: centring tolerance
function geoFails(where,st){
  const r=st.zoomLive;if(!r)return [`${where}: not zoomed`];const out=[];
  const dx=r.x+r.w/2-r.sw/2,dy=r.y+r.h/2-r.sh/2,fill=Math.max(r.w/r.sw,r.h/r.sh);
  if(Math.abs(dx)>TOL||Math.abs(dy)>TOL)out.push(`${where}: off centre by (${dx.toFixed(0)}, ${dy.toFixed(0)}) slide px`);
  if(r.x<-1||r.y<-1||r.x+r.w>r.sw+1||r.y+r.h>r.sh+1)out.push(`${where}: leaves the slide (x ${r.x.toFixed(0)}..${(r.x+r.w).toFixed(0)} of ${r.sw.toFixed(0)}, y ${r.y.toFixed(0)}..${(r.y+r.h).toFixed(0)} of ${r.sh.toFixed(0)}, footer below)`);
  if(fill<.6)out.push(`${where}: fills ${Math.round(fill*100)}% (< 60%)`);
  return out}
const checkOpts=page=>page.evaluate(()=>{const z=document.querySelector('.zoomed')||document.querySelector('.zflow');const sr=document.querySelector('.slide.current').getBoundingClientRect();
  const o=[...z.querySelectorAll('.opt')];return {n:o.length,ok:o.length>0&&o.every(e=>{const q=e.getBoundingClientRect();return getComputedStyle(e).visibility==='visible'&&q.left>=sr.left-1&&q.right<=sr.right+1&&q.top>=sr.top-1&&q.bottom<=sr.bottom+1})}});
async function matrixRun(browser,theme,vw,vh,dsf,pre,dir){
  const {page,errors}=await L.open({browser,theme,viewport:{width:pre[0],height:pre[1]},dsf});
  const fails=[],tag=`${vw}x${vh}@${dsf}`;let n=0,shots=0;
  await page.setViewportSize({width:vw,height:vh});await L.wait(page,350);
  const info=await page.evaluate(()=>Deck.slides.map(S=>({nf:S.frames.length,sims:S.sims.length})));
  const Z=420;
  // measure at rest: a loaded machine can run the .35 s zoom transition late, which is not a geometry fault (it is reported past 3 s)
  const rest=()=>page.waitForFunction(()=>!document.getAnimations().some(a=>a.transitionProperty==='transform'&&a.playState==='running'),null,{timeout:3000}).then(()=>true,()=>false);
  const look=async(where,kind)=>{const still=!(await rest());const st=await L.state(page);n++;const f=geoFails(where,st);if(still)f.push(`${where}: the zoom transition still runs after 3 s`);
    if(kind==='check'){const c=await checkOpts(page);if(!c.ok)f.push(`${where}: zoomed check does not show its ${c.n} options`)}
    if(f.length){fails.push(...f.map(x=>tag+' '+x));if(shots++<12)await page.screenshot({path:`${dir}/${tag}-${where.replace(/[^\w.-]+/g,'_')}.png`})}return st};
  const cycle=async(s,f,resizeAt)=>{const units=await page.evaluate(()=>Deck.zoomUnits());if(!units.length)return;
    for(let i=0;i<units.length;i++){await page.keyboard.press('.');await L.wait(page,Z);const st=await look(`s${s+1}f${f} u${i+1}/${units.length} ${units[i].kind}`,units[i].kind);
      if(st.zoomIndex!==i)fails.push(`${tag} s${s+1}f${f} u${i+1}: cycle at ${st.zoomIndex+1}`);
      if(i===resizeAt){const o=vw===1920?[1366,768]:[1920,1080];await page.setViewportSize({width:o[0],height:o[1]});await L.wait(page,Z);
        let q=await look(`s${s+1}f${f} u${i+1} after a resize to ${o[0]}x${o[1]} while zoomed`,units[i].kind);if(q.zoomIndex!==i)fails.push(`${tag} s${s+1}f${f}: the resize while zoomed moved the cycle to ${q.zoomIndex+1}`);
        await page.setViewportSize({width:vw,height:vh});await L.wait(page,Z);q=await look(`s${s+1}f${f} u${i+1} after the resize back`,units[i].kind)}}
    await page.keyboard.press('.');await L.wait(page,Z);const st=await L.state(page);if(st.zoom)fails.push(`${tag} s${s+1}f${f}: the press after the last unit did not unzoom`)};
  for(let s=0;s<info.length;s++){const {nf,sims}=info[s];
    await page.evaluate(([s,f])=>Deck.go(s,f),[s,nf-1]);await L.wait(page,300);await cycle(s,nf-1,0);
    if(!sims)continue;
    await page.evaluate(s=>Deck.go(s,0),s);await L.wait(page,300);await cycle(s,0,-1);
    // a press right after the exit (the zoom-out still in flight)
    const nu=(await page.evaluate(()=>Deck.zoomUnits())).length;await page.keyboard.press('.');await L.wait(page,Z);
    for(let i=1;i<nu;i++){await page.keyboard.press('.');await L.wait(page,140)}
    await page.keyboard.press('.');await L.wait(page,90);await page.keyboard.press('.');await L.wait(page,Z);await look(`s${s+1}f0 zoom pressed during the zoom-out`);
    await page.keyboard.press('PageUp');await L.wait(page,250);
    // Next while zoomed on the animation: the zoom stays on it, laid out afresh on each frame
    await page.keyboard.press('.');await L.wait(page,Z);
    for(let f=1;f<nf;f++){await page.keyboard.press('PageDown');await L.wait(page,650);const st=await L.state(page);if(st.s!==s)break;if(st.zoom&&st.zoomMode==='transform')await look(`s${s+1}f${f} Next while zoomed`);else if(st.zoom)await look(`s${s+1}f${f} Next while zoomed (frame zoom)`);else break}
    await page.keyboard.press('Escape');await L.wait(page,250);
    // a zoom right after Back, and after the slide list
    await page.evaluate(([s,f])=>Deck.go(s,f),[s,Math.min(1,nf-1)]);await L.wait(page,250);await page.keyboard.press('PageDown');await L.wait(page,250);
    await page.keyboard.press('PageUp');await L.wait(page,60);await page.keyboard.press('.');await L.wait(page,Z);await look(`s${s+1} zoom right after Back`);
    await page.keyboard.press('Escape');await L.wait(page,250);
    await page.keyboard.press('o');await L.wait(page,250);await page.keyboard.press('Escape');await L.wait(page,250);await page.keyboard.press('.');await L.wait(page,Z);await look(`s${s+1} zoom after the slide list`);
    await page.keyboard.press('Escape');await L.wait(page,250);
  }
  if(errors.length)fails.push(`${tag}: console errors: `+errors.splice(0).join(' | '));
  await page.context().close();
  return {view:`${vw}x${vh}`,dsf,loaded:`${pre[0]}x${pre[1]}`,states:n,fails};
}
(async()=>{
  const theme=process.argv[2]||'light',dir=L.ensure(L.OUT+'/zoom-'+theme);fs.readdirSync(dir).forEach(f=>fs.unlinkSync(dir+'/'+f));
  const {browser,page,errors}=await L.open({theme,reduced:true,viewport:{width:1366,height:768}});
  await page.setViewportSize({width:1920,height:1080});await L.wait(page,350); // F5 full screen after the deck loaded
  const nf=await page.evaluate(()=>Deck.slides.map(S=>S.frames.length));
  const rec=[],fails=[];let shot=0,backTests=0;
  for(let s=0;s<nf.length;s++)for(let f=0;f<nf[s];f++){
    await page.evaluate(([s,f])=>Deck.go(s,f),[s,f]);await L.wait(page,140);
    const units=await page.evaluate(()=>Deck.zoomUnits());
    if(!units.length){fails.push(`s${s+1}f${f}: no zoom unit`);continue}
    await page.keyboard.press('.');await L.wait(page,460);
    for(let i=0;i<units.length;i++){
      if(i>0){await page.keyboard.press('.');await L.wait(page,120)}
      const st=await L.state(page),u=units[i];
      const r=st.zoomLive,fill=r?Math.max(r.w/r.sw,r.h/r.sh):0;
      const chk=u.kind==='check'?await checkOpts(page):null;
      geoFails(`s${s+1}f${f} unit ${i+1} (${u.kind} ${u.id} ${u.label})`,st).filter(x=>!/fills/.test(x)).forEach(x=>fails.push(x));
      const file=`${String(shot++).padStart(4,'0')}-s${s+1}f${f}-u${i+1}-${u.kind}.png`;await page.screenshot({path:dir+'/'+file});
      const row={s:s+1,f,i:i+1,n:units.length,kind:u.kind,label:u.label,id:u.id,mode:st.zoomMode,fill:+fill.toFixed(3),scale:+st.zoomScale.toFixed(2),cue:st.cue,check:chk,file};rec.push(row);
      if(st.zoomIndex!==i||st.zoomCount!==units.length)fails.push(`s${s+1}f${f} unit ${i+1}: cycle at ${st.zoomIndex+1} of ${st.zoomCount}, expected ${i+1} of ${units.length}`);
      if(!/^Zoom \d+ of \d+ · Blank ▶ (next|exit) · Back ▶ exit$/.test(st.cue))fails.push(`s${s+1}f${f} unit ${i+1}: cue "${st.cue}"`);
      if(fill<.6)fails.push(`s${s+1}f${f} unit ${i+1} (${u.kind} ${u.id} ${u.label}): fills ${Math.round(fill*100)}% (< 60%) at x${st.zoomScale.toFixed(2)}`);
      if(chk&&!chk.ok)fails.push(`s${s+1}f${f} unit ${i+1}: zoomed check does not show its ${chk.n} options`);
      const wantRe=!['animation','part','column','table'].includes(u.kind); // text units re-flow; animations, their parts and the summary table (columns of icons and cells) transform
      if(st.zoomMode!==(wantRe?'reflow':'transform'))fails.push(`s${s+1}f${f} unit ${i+1} (${u.kind}): zoom mode ${st.zoomMode}, expected ${wantRe?'reflow':'transform'}`);
      if(st.zoomMode==='reflow'&&(st.zoomScale>2.2001||r.x<59||r.y<59||r.x+r.w>r.sw-59||r.y+r.h>r.sh-59))fails.push(`s${s+1}f${f} unit ${i+1}: re-flowed text at x${st.zoomScale.toFixed(2)} outside the 60 px margins`);
      const cl=st.zoomMode==='reflow'?await page.evaluate(()=>{const z=document.querySelector('.zflow');return [...z.querySelectorAll('*')].filter(e=>{const c=getComputedStyle(e);return (/hidden|clip/.test(c.overflowX+c.overflowY)||c.textOverflow==='ellipsis')&&(e.scrollWidth>e.clientWidth+1||e.scrollHeight>e.clientHeight+1)}).length}):0;
      if(cl)fails.push(`s${s+1}f${f} unit ${i+1}: clipped text in the re-flowed clone`);
      if(st.blank)fails.push(`s${s+1}f${f} unit ${i+1}: the screen blanked while zoomed`);
    }
    await page.keyboard.press('.');await L.wait(page,120);let st=await L.state(page);
    if(st.zoom!==null||st.s!==s||st.f!==f)fails.push(`s${s+1}f${f}: the press after the last unit did not unzoom (zoom ${st.zoom}, s${st.s+1}f${st.f})`);
    if(units.length>1&&f===nf[s]-1){backTests++; // Back exits the zoom at once and stays on the frame
      await page.keyboard.press('.');await L.wait(page,460);await page.keyboard.press('.');await L.wait(page,120);await page.keyboard.press('PageUp');await L.wait(page,200);st=await L.state(page);
      if(st.zoom!==null||st.s!==s||st.f!==f)fails.push(`s${s+1}f${f}: Back did not exit the zoom at once (zoom ${st.zoom}, s${st.s+1}f${st.f})`)}
    if(errors.length)fails.push(`s${s+1}f${f}: console errors: `+errors.splice(0).join(' | '));
  }
  // explicit checks: two generic ones for every deck (scratch decks too), then the lesson's own list asked by the teacher
  // (ZOOM_CHECKS: the lesson's zoomchecks.js, set by suite.py from the registry's zoom_checks; absent for a scratch deck)
  const has=(s,f,pred)=>rec.some(r=>r.s===s&&r.f===f&&pred(r)),cnt=(s,f,pred)=>rec.filter(r=>r.s===s&&r.f===f&&pred(r)).length;
  const routine=await page.evaluate(()=>Deck.slides.map((S,i)=>S.el.classList.contains('t-routine')&&[...S.el.querySelectorAll('.prompt,.dq')].some(e=>!e.closest('.notes'))?i+1:0).filter(Boolean));
  const B=[['every zoomed check shows its options',rec.filter(r=>r.kind==='check').every(r=>r.check&&r.check.ok)],
    [`every prompt on a routine slide is a unit (routine slides with a prompt: ${routine.join(', ')||'none'})`,routine.every(s=>rec.some(r=>r.s===s&&r.kind==='prompt'))]]
    .concat(process.env.ZOOM_CHECKS?require(require('path').resolve(process.env.ZOOM_CHECKS))(rec,{has,cnt}):[]);
  B.forEach(([n,ok])=>{if(!ok)fails.push('FAIL '+n)});
  // matrix pass: viewports x device scale factors, motion on, each loaded at another size and changed before zooming
  const matrix=[];
  if(process.env.MATRIX!=='0'){const {chromium}=require('playwright'),mb=await chromium.launch(),mdir=L.ensure(L.OUT+'/zoom-'+theme+'-matrix');fs.readdirSync(mdir).forEach(f=>fs.unlinkSync(mdir+'/'+f));
    const V=[[1366,768],[1536,864],[1920,1080],[1024,768]],jobs=[];V.forEach((v,i)=>[1,1.25,1.5].forEach(d=>jobs.push([v,d,V[(i+1)%V.length]])));
    const q=jobs.slice();await Promise.all([0,1,2,3].map(async()=>{while(q.length){const [v,d,pre]=q.shift();matrix.push(await matrixRun(mb,theme,v[0],v[1],d,pre,mdir))}}));await mb.close();
    matrix.sort((a,b)=>a.view.localeCompare(b.view)||a.dsf-b.dsf);matrix.forEach(m=>fails.push(...m.fails))}
  // zoom sheet: one zoomed state per unit type per slide
  const pick=[],seen=new Set();rec.forEach(r=>{const k=r.s+':'+r.kind;if(!seen.has(k)){seen.add(k);pick.push(r)}});
  L.save('zoom-'+theme+'.json',{theme,units:rec.length,fails,matrix,explicit:B.map(([n,ok])=>({n,ok})),sheet:pick.map(r=>r.file),rec});
  const kinds={};rec.forEach(r=>{kinds[r.kind]=(kinds[r.kind]||0)+1});
  console.log(`zoom ${theme}: ${rec.length} zoomed states over ${nf.reduce((a,b)=>a+b,0)} frames (re-flow ${rec.filter(r=>r.mode==='reflow').length}, transform ${rec.filter(r=>r.mode==='transform').length}), ${Object.entries(kinds).map(([k,v])=>k+' '+v).join(', ')}; min fill ${Math.round(Math.min(...rec.map(r=>r.fill))*100)}%; Back tests ${backTests}; ${fails.length?'FAIL':'PASS'}`);
  B.forEach(([n,ok])=>console.log(`  ${ok?'PASS':'FAIL'}  ${n}`));
  matrix.forEach(m=>console.log(`  ${m.fails.length?'FAIL':'PASS'}  matrix ${m.view} at x${m.dsf} (loaded at ${m.loaded}): ${m.states} zoomed states measured, ${m.fails.length} fails`));fails.filter(f=>!f.startsWith('FAIL ')).slice(0,40).forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
