// Timing: per-frame minutes in the notes sum to the coordinator's per-slide budgets, and each period to at most 47 min.
// A timed frame must allow at least its timer.
const L=require('./lib');
const BUDGET=process.env.BUDGET?JSON.parse(require('fs').readFileSync(process.env.BUDGET,'utf8')):{s01:.5,s02:4,s03:4,s04:2.5,s05:3,s06:5,s07:4,s08:4,s09:5,s10:5,s11:3,s12:4,s13:3,
  s14:3,s15:4,s16:4,s17:3,s18:5,s19:5,s20:1,s21:4.5,s22:4.5,s23:4.5,s24:7,s25:1.5};
(async()=>{
  const {browser,page}=await L.open({});
  const rows=await page.evaluate(()=>Deck.slides.map(S=>({id:S.id,title:S.title,period:S.period,mins:Math.round(S.frames.reduce((a,f)=>a+(f.t||0),0)*100)/100,
    timers:S.frames.filter(f=>f.timer).map(f=>({timer:f.timer,t:f.t})),noT:S.frames.filter(f=>!f.t).length})));
  const fails=[],per={};
  rows.forEach(r=>{per[r.period]=(per[r.period]||0)+r.mins;
    if(BUDGET[r.id]!==undefined&&Math.abs(BUDGET[r.id]-r.mins)>.001)fails.push(`${r.id} ${r.title}: ${r.mins} min, budget ${BUDGET[r.id]}`);
    if(r.noT)fails.push(`${r.id}: ${r.noT} frame(s) without minutes`);
    r.timers.forEach(x=>{if(x.timer/60>x.t+1e-9)fails.push(`${r.id}: timer ${x.timer} s on a ${x.t} min frame`)})});
  Object.entries(per).forEach(([p,m])=>{per[p]=Math.round(m*100)/100;if(m>47+1e-9)fails.push(`period ${p}: ${per[p]} min > 47`)});
  Object.keys(BUDGET).forEach(id=>{if(!rows.some(r=>r.id===id))fails.push(`${id}: in the budget but not in the deck`)});
  L.save('timing.json',{rows,per,fails});
  rows.forEach(r=>console.log(`  ${r.id} P${r.period} ${r.mins} min  ${r.title}${r.timers.length?'  timers '+r.timers.map(x=>x.timer+'s').join(','):''}`));
  console.log(`timing: period 1 ${per['1']} min, period 2 ${per['2']} min, ${fails.length?'FAIL':'PASS'}`);fails.forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
