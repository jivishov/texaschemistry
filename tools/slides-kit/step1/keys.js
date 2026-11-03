// 4. Clicker keys (Logitech R800: PageDown, PageUp, F5/Escape, period) and the laptop keys.
const L=require('./lib');
(async()=>{
  const {browser,page,errors}=await L.open({});
  // deck-specific ids (defaults: Lesson 4.1); KEYS_CFG overrides them for another deck
  const C=Object.assign({cr:'s07',sim:'cr-sim',card:'cr-rule',tm:'s19',ex:'s03',hk:'s02',notes:['s09',6]},process.env.KEYS_CFG?JSON.parse(process.env.KEYS_CFG):{});
  const ix=id=>page.evaluate(id=>Deck.slides.findIndex(S=>S.id===id),id);const CR=await ix(C.cr),TM=await ix(C.tm),EX=await ix(C.ex),HK=await ix(C.hk);
  const res=[];const ok=(name,pass,info)=>res.push({name,pass:!!pass,info:info===undefined?'':info});
  const st=()=>L.state(page),go=(s,f)=>page.evaluate(([s,f])=>Deck.go(s,f),[s,f]),key=async(k,ms=450)=>{await page.keyboard.press(k);await L.wait(page,ms)};
  const dir=L.ensure(L.OUT+'/keys');

  // F5: no reload, full screen requested
  await page.evaluate(()=>{window.__mark=1});await key('F5',500);
  ok('F5 does not reload',await page.evaluate(()=>window.__mark===1));

  // Next / Back across slide edges
  await go(0,-1);await L.wait(page,300);let a=await st();await key('PageDown',300);let b=await st();
  ok('PageDown on last frame enters next slide at frame 0',b.s===a.s+1&&b.f===0,`s${b.s+1}f${b.f}`);
  await key('PageUp',300);b=await st();ok('PageUp at frame 0 enters previous slide at its last frame',b.s===a.s&&b.f===a.nf-1,`s${b.s+1}f${b.f}`);

  // repeat ignored (Playwright sends repeat:true for a second keydown without keyup), and a synthetic repeat
  await go(CR,0);await L.wait(page,300);a=await st();
  await page.keyboard.down('PageDown');await L.wait(page,250);await page.keyboard.down('PageDown');await L.wait(page,250);await page.keyboard.down('PageDown');await page.keyboard.up('PageDown');await L.wait(page,300);
  b=await st();ok('held PageDown (repeat) advances once',b.f===a.f+1,`f${a.f} -> f${b.f}`);
  a=b;await page.evaluate(()=>window.dispatchEvent(new KeyboardEvent('keydown',{key:'PageDown',repeat:true,bubbles:true})));await L.wait(page,300);
  b=await st();ok('synthetic keydown with repeat:true is ignored',b.f===a.f);
  // debounce 180 ms
  a=await st();await page.keyboard.press('PageDown');await L.wait(page,60);await page.keyboard.press('PageDown');await L.wait(page,300);
  b=await st();ok('two presses within 180 ms advance once (debounce)',b.f===a.f+1,`f${a.f} -> f${b.f}`);

  // focused <select> does not swallow keys; textarea does
  await go(CR,0);await L.wait(page,250);
  await page.evaluate(()=>{const s=document.createElement('select');s.id='tsel';s.innerHTML='<option>1</option><option>2</option><option>3</option>';document.querySelector('.slide.current .col').appendChild(s);s.focus()});
  a=await st();await key('PageDown',300);b=await st();const sv=await page.evaluate(()=>document.getElementById('tsel').value);
  ok('focused <select>: PageDown still advances',b.f===a.f+1&&sv==='1',`f${a.f} -> f${b.f}, select value ${sv}`);
  await key('ArrowDown',300);const c=await st();ok('focused <select>: ArrowDown still advances',c.f===b.f+1);
  await page.evaluate(()=>{const s=document.getElementById('tsel');s.focus();s.dispatchEvent(new MouseEvent('click',{bubbles:true}))});await L.wait(page,100);
  ok('a click on a control is followed by blur()',await page.evaluate(()=>document.activeElement===document.body||document.activeElement===document.documentElement));
  await page.evaluate(()=>{document.getElementById('tsel').remove();const t=document.createElement('textarea');t.id='tta';document.querySelector('.slide.current .col').appendChild(t);t.focus()});
  a=await st();await key('PageDown',300);b=await st();ok('focused <textarea> keeps its keys',b.f===a.f);
  await page.evaluate(()=>{document.getElementById('tta').remove();document.activeElement.blur()});

  // '.' cycles the zoom through the frame's units (animation first); canvases re-render at the zoomed resolution (teacher round, A1)
  await go(CR,2);await L.wait(page,1200);
  const w0=await page.evaluate(sim=>document.querySelector('#'+sim+' canvas').width,C.sim);
  const U2=await page.evaluate(()=>Deck.zoomUnits());
  await key('.',700);a=await st();
  const w1=await page.evaluate(sim=>document.querySelector('#'+sim+' canvas').width,C.sim);
  ok("'.' zooms unit 1, the animation on a stage frame",a.zoom===C.sim&&a.zoomScale>1&&a.zoomIndex===0&&a.zoomCount===U2.length,`zoom ${a.zoom} x${a.zoomScale.toFixed(2)}, unit ${a.zoomIndex+1} of ${a.zoomCount}`);
  const bFit=await page.evaluate(sim=>{const b=Deck.sims[sim].bounds(),S=document.querySelector('.slide.current');return Math.max(1,Math.min(4,(1600-48)/b.w,(S.offsetHeight-48)/b.h))},C.sim);
  ok('zoom fits the drawn content (bounds of the current stage), not the whole box',Math.abs(a.zoomScale-bFit)<.02,`zoom x${a.zoomScale.toFixed(2)} vs bounds fit x${bFit.toFixed(2)}`);
  ok('zoomed canvas re-renders at the zoomed resolution',Math.abs(w1/w0-a.zoomScale)<.03||w1/w0>3.2,`canvas width ${w0} -> ${w1}, ratio ${(w1/w0).toFixed(3)} vs zoom ${a.zoomScale.toFixed(3)}`);
  ok('the cue while zoomed reads "Zoom 1 of n · Blank ▶ next · Back ▶ exit"',a.cue===`Zoom 1 of ${U2.length} · Blank ▶ next · Back ▶ exit`,a.cue);
  await page.screenshot({path:dir+'/zoom-sim.png'});
  await page.keyboard.press('.');await L.wait(page,120);await page.keyboard.press('.');await L.wait(page,500);a=await st();
  ok("while zoomed, two fast presses step the cycle twice and never blank",!a.blank&&a.zoomIndex===Math.min(2,U2.length-1)||(!a.blank&&U2.length<3&&a.zoom===null),`unit ${a.zoomIndex+1} of ${a.zoomCount}, blank ${a.blank}`);
  for(let i=a.zoomIndex+1;i<U2.length;i++)await key('.',250);a=await st();
  ok('the last unit cue says Blank ▶ exit',/^Zoom (\d+) of \1 · Blank ▶ exit · Back ▶ exit$/.test(a.cue),a.cue);
  await key('.',400);a=await st();ok("the press after the last unit unzooms",a.zoom===null&&a.f===2&&/^Next ▶ /.test(a.cue),a.cue);
  await go(CR,3);await L.wait(page,600);const U3=await page.evaluate(()=>Deck.zoomUnits());
  ok("the cycle at this frame reaches the card it shows",U3.some(u=>u.id===C.card),U3.map(u=>u.id).join(' '));
  await key('.',700);for(let i=0;i<U3.findIndex(u=>u.id===C.card);i++)await key('.',300);a=await st();ok("'.' steps to that card",a.zoom===C.card,a.zoom);
  await page.screenshot({path:dir+'/zoom-rule.png'});
  await key('PageUp',500);a=await st();ok('Back while zoomed exits the zoom at once and stays on the frame',a.zoom===null&&a.f===3,`zoom ${a.zoom} f${a.f}`);
  await key('.',700);await key('.',300);await key('PageDown',700);a=await st();ok('Next restarts the cycle: a zoom on a card is cleared',a.zoom===null&&a.f===4);
  // zoom kept when the next frame drives the same animation
  await go(CR,0);await L.wait(page,600);await key('.',700);await key('PageDown',1700);a=await st();
  ok('zoom on the animation stays while the next frame drives it',a.zoom===C.sim&&a.f===1,`zoom ${a.zoom} f${a.f}`);
  await key('PageDown',1200);a=await st();ok('zoom on the animation stays through a stage-only frame',a.zoom===C.sim&&a.f===2,`zoom ${a.zoom} f${a.f}`);
  await page.screenshot({path:dir+'/zoom-sim-turn.png'});
  await key('Escape',500);

  // '.' '.' within 400 ms on an unzoomed slide: blank; any key clears it without acting
  await go(EX,2);await L.wait(page,500);a=await st();
  await page.keyboard.press('.');await L.wait(page,120);await page.keyboard.press('.');await L.wait(page,300);b=await st();
  ok("'.' '.' within 400 ms blanks the screen (and undoes the first zoom)",b.blank&&b.zoom===null);
  await page.screenshot({path:dir+'/blank.png'});
  await key('PageDown',300);b=await st();ok('any key clears the blank screen without advancing',!b.blank&&b.f===a.f&&b.s===a.s);
  await key('b',700);b=await st();ok("'b' acts like '.'",b.zoom!==null);await key('Escape',400);

  // Escape unwinds blank -> zoom -> notes (a blank screen is reached only from an unzoomed slide)
  await go(EX,3);await L.wait(page,400);await key('n',300);
  await page.keyboard.press('.');await L.wait(page,100);await page.keyboard.press('.');await L.wait(page,300);
  a=await st();ok('setup: notes + blank',a.notes&&a.blank,JSON.stringify({n:a.notes,b:a.blank}));
  await page.screenshot({path:dir+'/blank-over-notes.png'});
  await key('Escape',400);a=await st();ok('Escape 1 closes the blank screen only',!a.blank&&a.notes);
  await key('.',700);a=await st();ok('setup: notes + zoom',a.notes&&a.zoom);
  await page.screenshot({path:dir+'/zoom-with-notes.png'});
  await key('Escape',500);a=await st();ok('Escape 2 closes the zoom only',!a.zoom&&a.notes);
  await page.screenshot({path:dir+'/notes.png'});
  await key('Escape',300);a=await st();ok('Escape 3 closes the notes',!a.notes);

  // slide list on click: the counter and the section label open the overview; a click on a slide jumps (A5)
  await page.click('#count');await L.wait(page,300);a=await st();ok('a click on the slide counter opens the slide list',a.overview);
  const ovn=await page.evaluate(()=>[...document.querySelectorAll('#overview button')].map(b=>b.textContent));
  ok('the slide list shows every slide number and title',ovn.length===a.ns&&ovn.every((t,i)=>t.startsWith(String(i+1))),ovn.length+' entries');
  await page.screenshot({path:dir+'/slide-list.png'});
  await page.click('#overview button >> nth=4');await L.wait(page,400);a=await st();ok('a click on a slide jumps to it',!a.overview&&a.s===4&&a.f===0,`s${a.s+1}f${a.f}`);
  await page.click('#sec');await L.wait(page,300);a=await st();ok('a click on the section label opens the slide list',a.overview);await key('Escape',300);

  // timer: starts on its frame, Back then Next restarts it
  await go(TM,1);await L.wait(page,2300);a=await st();
  ok('timer runs on its frame',a.timer&&a.timer.sec===180&&/^2:5\d$/.test(a.timer.text),a.timer&&a.timer.text);
  await key('PageUp',300);b=await st();ok('timer stops when leaving its frame',!b.timer);
  await key('PageDown',400);b=await st();ok('Back then Next restarts the timer',b.timer&&b.timer.text==='3:00',b.timer&&b.timer.text);
  await page.screenshot({path:dir+'/timer.png'});

  // a timed frame on a slide without a .timer slot is an authoring error the runtime reports (the walk fails on it)
  await page.evaluate(i=>{Deck.slides[i].frames[1].timer=10;Deck.go(i,1)},HK);await L.wait(page,300);
  const te=errors.findIndex(e=>/no \.timer slot/.test(e));ok('a timed frame without a .timer slot is reported',te>=0);if(te>=0)errors.splice(te,1);
  await page.evaluate(i=>{Deck.slides[i].frames[1].timer=0;Deck.go(i,0)},HK);

  // laptop keys: Home, End, O overview, T theme, Z zoom
  await key('End',300);a=await st();ok('End goes to the last frame of the last slide',a.s===a.ns-1&&a.f===a.nf-1);
  await key('Home',300);a=await st();ok('Home goes to slide 1 frame 0',a.s===0&&a.f===0);
  await key('o',300);a=await st();ok('O opens the overview',a.overview);
  await key('PageDown',150);await key('PageDown',150);await page.screenshot({path:dir+'/overview.png'});await key('Enter',400);a=await st();
  ok('overview: PageDown moves, Enter goes',!a.overview&&a.s===2&&a.f===0,`s${a.s+1}`);
  await key('z',700);a=await st();ok('Z toggles zoom',a.zoom!==null);await key('z',500);
  await key('t',400);a=await st();ok('T switches to dark',a.theme==='dark');
  await page.screenshot({path:dir+'/theme-dark.png'});await key('t',300);a=await st();ok('T switches back to light',a.theme==='light');

  // overflow detector self-test: an injected oversize block must be reported
  await go(CR,3);await L.wait(page,400);
  await page.evaluate(card=>{const p=document.createElement('p');p.id='ovtest';p.textContent='overflow test';p.style.cssText='width:2400px';document.getElementById(card).appendChild(p)},C.card);
  const ov=await L.overflow(page);ok('overflow detector catches an injected oversize block',ov.some(o=>o.el.includes('ovtest')),ov.length+' findings');
  await page.evaluate(()=>document.getElementById('ovtest').remove());

  await page.evaluate(([id,f])=>Deck.go(Deck.slides.findIndex(S=>S.id===id),f),C.notes);await L.wait(page,600);await key('n',400);await page.screenshot({path:dir+'/notes-'+C.notes[0]+'.png'});await key('n',300);
  ok('no console errors',errors.length===0,errors.join(' | '));
  L.save('keys.json',res);
  res.forEach(r=>console.log(`  ${r.pass?'PASS':'FAIL'}  ${r.name}${r.info?'  ('+r.info+')':''}`));
  const n=res.filter(r=>!r.pass).length;console.log(`keys: ${n?'FAIL ('+n+')':'PASS'} ${res.length} checks`);
  await browser.close();process.exitCode=n?1:0;
})();
