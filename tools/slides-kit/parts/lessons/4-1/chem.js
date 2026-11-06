// Chemistry checks on the animations as placed in the real deck (meta() of each placed instance).
const L=require('../../../audits/lib'); // DECK and OUT from the environment (suite.py)
(async()=>{
  const {browser,page,errors}=await L.open({});const res=[];const ok=(n,p,i)=>res.push({n,pass:!!p,i:i===undefined?'':JSON.stringify(i)});
  const meta=(sid,stage)=>page.evaluate(([sid,stage])=>{const s=Deck.slides.findIndex(S=>S.id===sid),f=Deck.slides[s].frames.findIndex(fr=>fr.stage.some(x=>x.s===stage));Deck.go(s,f);
    const fr=Deck.slides[s].frames[f],id=fr.stage.find(x=>x.s===stage).sim;return Deck.sims[id].meta()},[sid,stage]);
  let m=await meta('s02','even');ok('slide 2 tugOfWar: Cl 3.16 vs Cl 3.16, knot centered',m.ea===3.16&&m.eb===3.16&&m.knot===0,m);
  m=await meta('s02','uneven');ok('slide 2 tugOfWar: H 2.20 vs Cl 3.16, knot toward Cl',m.a==='H'&&m.winner==='Cl'&&m.knot>0,m);
  m=await meta('s02','blowout');ok('slide 2 tugOfWar: Na 0.93 vs Cl 3.16, all the way, ions',m.a==='Na'&&m.knot===1&&m.ion===1,m);
  m=await meta('s06','atoms');ok('slide 6 ionHop: 11 p 11 e, 17 p 17 e',m.counts.join()==='11 p · 11 e,17 p · 17 e',m.counts);
  ok('slide 6 ionHop: Na+ smaller than Na, Cl- larger than Cl',m.naIon<m.naAtom&&m.clIon>m.clAtom,m);
  m=await meta('s06','ions');ok('slide 6 ionHop: 11 p 10 e, 17 p 18 e',m.counts.join()==='11 p · 10 e,17 p · 18 e',m.counts);
  m=await meta('s07','turn');ok('slide 7 ionHop: center Na+ with six Cl- neighbors',m.neighbors===6&&m.neighborsAreAnions&&m.centerIsCation,m);
  m=await meta('s08','even');ok('slide 8 tugOfWar recap: even pull',m.knot===0&&m.ea===3.16,m);
  m=await meta('s08','H2');ok('slide 8 sharedPair H2: 0.00, no δ',m.diff==='0.00'&&m.deltaMinus===null,m);
  m=await meta('s08','Cl2');ok('slide 8 sharedPair Cl2: 0.00, no δ',m.diff==='0.00'&&m.deltaMinus===null,m);
  for(const [st,d,dm] of [['H2','0.00',null],['HCl','0.96','Cl'],['HO','1.24','O'],['HF','1.78','F']]){m=await meta('s09',st);ok(`slide 9 sharedPair ${st}: ${d}, δ− on ${dm||'neither'}`,m.diff===d&&m.deltaMinus===dm,m)}
  for(const [st,n,c] of [['sea',1,'+'],['Mg',2,'2+'],['Al',3,'3+']]){m=await meta('s10',st);ok(`slide 10 electronSea ${st}: ${n} per core, ${c}`,m.electronsPerCore===n&&m.coreCharge===c,m)}
  m=await meta('s10','drift');ok('slide 10 electronSea drift: electrons stream',m.stream,m);
  for(const [b,t] of [['Cl-Cl','3.16 − 3.16 = 0.00'],['H-Cl','3.16 − 2.20 = 0.96'],['Na-Cl','3.16 − 0.93 = 2.23']]){m=await meta('s15',b);ok(`slide 15 enMeter ${b}: ${t}`,m.sub===t,m.sub)}
  m=await meta('s15','lines');ok('slide 15 enMeter: guide lines 0.4 and 1.8',m.guideLines.join()==='0.4,1.8'&&m.guideLabel,m);
  for(const [p,c] of [['Na-Cl','metal + nonmetal'],['H-Cl','two nonmetals'],['Cu-Cu','one metal']]){m=await meta('s16',p);ok(`slide 16 ptMap ${p}: ${c}`,m.caption[1]===c,m)}
  m=await meta('s16','outline');ok('slide 16 ptMap: 118 cells, no symbol squeezed or left out',m.cells===118&&m.omittedSymbols===0,{cellPx:m.cellPx,omitted:m.omittedSymbols});
  for(const [b,t] of [['H-F','3.98 − 2.20 = 1.78'],['Mg-Cl','3.16 − 1.31 = 1.85'],['Fe-Cl','3.16 − 1.83 = 1.33']]){m=await meta('s17',b);ok(`slide 17 enMeter ${b}: ${t}`,m.sub===t,m.sub)}
  m=await meta('s18','KF-strength');ok('slide 18 cerBuilder KF: four parts',m.filled.length===4&&m.set==='KF',m);
  m=await meta('s18','HCl-claim');ok('slide 18 cerBuilder HCl: starts fresh',m.set==='HCl'&&m.filled.join()==='claim',m);
  ok('no console errors',!errors.length,errors);
  L.save('chem-deck.json',res);res.forEach(r=>console.log(`  ${r.pass?'PASS':'FAIL'}  ${r.n}${r.pass?'':'  '+r.i}`));
  const n=res.filter(r=>!r.pass).length;console.log(`chem (deck): ${n?'FAIL ('+n+')':'PASS'} ${res.length} checks`);await browser.close();process.exitCode=n?1:0;
})();
