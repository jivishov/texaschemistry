// Lesson 5.1 bench check (step 02): opens the scratch deck (build.py 5 1 --scratch), visits every stage of the eleven animations
// and asserts every meta() fact of plan section 4, the painter's smallest label (36 px or more), the smallest primary shape (60 px or
// more: spheres, coins, cells, eggs, cards, badges), the live flag on the three live stages (tally, zoom, line) from meta() and from
// the test-time instrumentation, and the reduced-motion still frame of every live or turning stage.
// Run with the environment suite.py sets: DECK=<scratch deck> OUT=<folder> node parts/lessons/5-1/scratch-check.js
const L=require('../../../audits/lib'),{instrument}=require('../../../audits/layout');
const near=(a,b,r)=>Math.abs(a/b-1)<=(r||.005);
(async()=>{
  const res=[];const ok=(n,p,i)=>res.push({n,pass:!!p,i:i===undefined?'':JSON.stringify(i)});
  const {browser,page,errors}=await L.open({reduced:true,init:instrument});
  const list=await page.evaluate(()=>Deck.slides.map((S,i)=>{const h=S.el.querySelector('.sim[data-sim]');return {i,id:S.id,sim:h.dataset.sim,host:h.id,stage:S.frames[0].stage[0].s}}));
  const seen={};
  const at=async(sim,stage)=>{const x=list.find(r=>r.sim===sim&&r.stage===stage);if(!x)return {missing:true};seen[sim+':'+stage]=1;
    return page.evaluate(([i,id])=>{Deck.go(i,0);const m=Deck.sims[id];return {meta:m.meta(),minFont:m.minFont,live:!!m.host.__live,units:(m.units&&m.units()||[]).length}},[x.i,x.host])};
  const LIVE=new Set(['coinScale:tally','howMany:zoom','secondsLine:line']);
  /* every stage: label floor, shape floor, live flag, at least one zoom sub-unit */
  for(const r of list){const v=await at(r.sim,r.stage),m=v.meta,key=r.sim+':'+r.stage,live=LIVE.has(key);
    ok(`${key}: labels at 36 px or more (painter minFont ${v.minFont})`,v.minFont>=36);
    ok(`${key}: primary shapes at 60 px or more (${m.minShape==null?'none drawn on this stage: the line, its ticks and markers only':'smallest '+m.minShape})`,m.minShape==null?r.sim==='secondsLine':m.minShape>=60);
    if(live||'live' in m&&!['siliconSphere','naclCrystal'].includes(r.sim))ok(`${key}: live flag ${live} (meta and instrumentation)`,!!m.live===live&&v.live===live,{meta:m.live,inst:v.live});
    ok(`${key}: zoom sub-units`,v.units>=1,v.units)}
  let m;
  /* 1. coinScale */
  m=(await at('coinScale','jar')).meta;ok('coinScale jar: hook family, nickels',m.family==='hook'&&m.coin==='nickel'&&m.massPerCoin===5);
  m=(await at('coinScale','guess')).meta;ok('coinScale guess: the "?" badge and the prompt',m.guess);
  m=(await at('coinScale','tally')).meta;ok('coinScale tally: live, 8 coins counted one a second',m.live&&m.tallyCoins===8);
  m=(await at('coinScale','scale')).meta;ok('coinScale scale: 2,000.0 g of coins, 5.000 g per nickel',m.total===2000&&m.texts.includes('2,000.0 g')&&m.texts.includes('5.000 g'),m.texts);
  m=(await at('coinScale','reveal')).meta;ok('coinScale reveal: 2,000.0 g ÷ 5.000 g = 400 nickels',m.count===400&&m.count*m.massPerCoin===m.total&&m.texts.includes('400 nickels'),m);
  m=(await at('coinScale','bag')).meta;ok('coinScale bag: bank family, no reading yet, not zeroed',m.family==='bank'&&m.reading===null&&!m.zeroed,m);
  m=(await at('coinScale','zero')).meta;ok('coinScale zero: the empty bag, 0.0 g, zeroed',m.total===0&&m.reading==='0.0 g'&&m.zeroed,m);
  m=(await at('coinScale','read')).meta;ok('coinScale read: scale reading 1,250.0 g',m.reading==='1,250.0 g'&&m.total===1250&&m.zeroed,m);
  m=(await at('coinScale','divide')).meta;ok('coinScale divide: 1,250.0 g × 1 nickel / 5.000 g, the g struck twice',m.bridge==='1,250.0 g × 1 nickel / 5.000 g'&&m.struck.length===2,m);
  m=(await at('coinScale','count')).meta;ok('coinScale count: 250 nickels, check 250 × 5.000 g = 1,250.0 g',m.count===250&&m.count*5===1250&&m.check==='250 × 5.000 g = 1,250.0 g',m);
  m=(await at('coinScale','roll')).meta;ok('coinScale roll: 200.0 g on the scale, the answer (40) not drawn',m.reading==='200.0 g'&&m.roll.mass===200&&m.roll.answer===m.roll.mass/5&&!m.roll.answerDrawn&&m.count===null,m);
  /* 2. centJar */
  m=(await at('centJar','jar')).meta;ok('centJar jar: before 1982 3.11 g, after 1982 2.500 g, the jar 1,017.1 g',m.old===3.11&&m.new===2.5&&m.jar===1017.1,m);
  m=(await at('centJar','wrong')).meta;ok('centJar wrong: ÷ 2.500 g about 407 too many; ÷ 3.11 g about 327 too few',m.wrong[0].cents===407&&m.wrong[0].verdict==='too many'&&m.wrong[1].cents===327&&m.wrong[1].verdict==='too few'&&Math.round(m.jar/m.new)===407&&Math.round(m.jar/m.old)===327,m.wrong);
  m=(await at('centJar','sample')).meta;ok('centJar sample: 100 cents, 267.69 g',m.sample===267.69&&m.sampleN===100,m);
  m=(await at('centJar','average')).meta;ok('centJar average: 267.69 g ÷ 100 = 2.6769 g',m.average===2.6769&&near(m.sample/m.sampleN,m.average,1e-9),m);
  m=(await at('centJar','count')).meta;ok('centJar count: 1,017.1 g ÷ 2.6769 g = about 380 cents; 2.6769 between 2.500 and 3.11',m.count===380&&Math.round(m.jar/m.average)===380&&m.countText==='about 380 cents'&&m.between,m);
  m=(await at('centJar','isotopes')).meta;ok('centJar isotopes: "isotopes", the table cell, no isotope masses',m.isotopes&&m.isotopes.label==='isotopes'&&!m.isotopes.isotopeMassesShown&&m.isotopes.mass==='63.546',m.isotopes);
  /* 3. countingUnits */
  m=(await at('countingUnits','dozen')).meta;ok('countingUnits dozen: 12',m.dozen===12);
  m=(await at('countingUnits','ream')).meta;ok('countingUnits ream: 500',m.ream===500&&m.dozen===12);
  m=(await at('countingUnits','mole')).meta;ok('countingUnits mole: 6.022 × 10²³, symbol mol',m.mole==='6.022 × 10²³'&&m.symbol==='mol',m);
  m=(await at('countingUnits','exact')).meta;ok('countingUnits exact: exactly 6.02214076 × 10²³, rounded 6.022 × 10²³, since May 20, 2019',m.exact==='6.02214076 × 10²³'&&m.rounded==='6.022 × 10²³'&&m.since==='May 20, 2019',m);
  m=(await at('countingUnits','constant')).meta;ok('countingUnits constant: N_A = 6.022 × 10²³ mol⁻¹',/= 6\.022 × 10²³ mol⁻¹$/.test(m.constant||''),m.constant);
  /* 4. howMany */
  m=(await at('howMany','thousand')).meta;ok('howMany thousand: 1,000 per step, the ladder starts at 10³',m.perStep===1000&&m.ladder.join()==='10³',m.ladder);
  m=(await at('howMany','zoom')).meta;ok('howMany zoom: live, seven steps of × 1,000 to 10²¹',m.live&&m.steps===7&&m.top==='10²¹'&&m.exps.join()==='3,6,9,12,15,18,21',m);
  m=(await at('howMany','mole')).meta;ok('howMany mole: × 602 more, 6.022 × 10²³; 10²¹ × 602 = 6.02 × 10²³',m.last===602&&m.check&&m.mole==='6.022 × 10²³'&&m.ladder.length===8&&m.ladder[7]==='× 602',m);
  m=(await at('howMany','spoon')).meta;ok('howMany spoon: one mole of water, about 18 g',m.water===18);
  /* 5. moleKinds */
  m=(await at('moleKinds','al')).meta;ok('moleKinds al: 1 mol of Al atoms, 26.982 g',m.masses.Al===26.982&&m.masses.Cu===null);
  m=(await at('moleKinds','cu')).meta;ok('moleKinds cu: 1 mol of Cu atoms, 63.546 g; the beam tips toward copper',m.masses.Cu===63.546&&m.heavier==='Cu');
  m=(await at('moleKinds','compare')).meta;ok('moleKinds compare: both 6.022 × 10²³ atoms, different masses',m.equal&&m.counts.Al===m.counts.Cu&&m.counts.Al==='6.022 × 10²³ atoms'.replace(' atoms','')&&m.masses.Al!==m.masses.Cu,m);
  m=(await at('moleKinds','oxygen')).meta;ok('moleKinds oxygen: O₂ holds twice the atoms',m.o2Ratio===2);
  m=(await at('moleKinds','four')).meta;ok('moleKinds four: atoms, molecules, formula units, ions; Shannon radii 102 and 181 pm',m.names.join('|')==='atoms|molecules|formula units|ions'&&m.radii.Na_ion===102&&m.radii.Cl_ion===181,m);
  /* 6. secondsLine */
  m=(await at('secondsLine','line')).meta;ok('secondsLine line: live counter, marks in order on the log line',m.live&&m.order,m);
  m=(await at('secondsLine','year')).meta;ok('secondsLine year: 1 year = 3.156 × 10⁷ s',m.yearS===3.156e7);
  m=(await at('secondsLine','earth')).meta;ok('secondsLine earth: 4.5 billion years',m.earthYears===4.5e9);
  m=(await at('secondsLine','universe')).meta;ok('secondsLine universe: 13.8 billion years',m.universeYears===1.38e10);
  m=(await at('secondsLine','mole')).meta;ok('secondsLine mole: 6.022 × 10²³ s = 1.908 × 10¹⁶ years, shown "about 1.9 × 10¹⁶ years"',m.yearsCheck&&m.moleYears===1.908e16&&m.moleShown==='about 1.9 × 10¹⁶ years',m);
  m=(await at('secondsLine','times')).meta;ok('secondsLine times: about 1.4 million times the age of the universe (1.38 × 10⁶); Earth: about 4 million',m.timesCheck&&m.times===1.38e6&&m.timesShown==='about 1.4 million times'&&Math.round(m.earthTimes)===4,m);
  m=(await at('secondsLine','spoon')).meta;ok('secondsLine spoon: 1 mol of water, about 18 g',m.water===18);
  /* 7. moleHistory */
  const H=[['avogadro','1811','Avogadro'],['loschmidt','1865','Loschmidt'],['ostwald','1890s','Ostwald'],['perrin','1909','Perrin'],['si','1971','SI'],['exact','2019','exact']];
  for(let i=0;i<H.length;i++){m=(await at('moleHistory',H[i][0])).meta;ok(`moleHistory ${H[i][0]}: ${i+1} ticks, the last ${H[i][1]} ${H[i][2]}`,m.ticks.length===i+1&&m.ticks[i].year===H[i][1]&&m.ticks[i].name===H[i][2],m.ticks)}
  m=(await at('moleHistory','perrin')).meta;ok('moleHistory perrin: measured, named after Avogadro, Nobel Prize 1926',m.lines.join(' ').includes('Nobel Prize, 1926')&&m.lines.join(' ').includes('Named it after Avogadro'),m.lines);
  m=(await at('moleHistory','si')).meta;ok('moleHistory si: SI base unit, the old definition (12 g of carbon-12)',m.lines.join(' ').includes('SI base unit')&&m.lines.join(' ').includes('12 g')&&m.oldDefinition==='12 g of carbon-12',m.lines);
  m=(await at('moleHistory','exact')).meta;ok('moleHistory exact: voted November 16, 2018; exact since May 20, 2019; 6.02214076 × 10²³',m.vote==='November 16, 2018'&&m.since==='May 20, 2019'&&m.lines.join(' ').includes('6.02214076 × 10²³'),m.lines);
  /* 8. siliconSphere */
  m=(await at('siliconSphere','crystal')).meta;ok('siliconSphere crystal: 2 × 2 × 2 cubes of diamond-cubic silicon (95 atoms), turning (live)',m.atoms===95&&m.edges===54&&m.live,m);
  m=(await at('siliconSphere','cube')).meta;ok('siliconSphere cube: edge 543.102 pm, 8 atoms per cube (8 × 1/8 + 6 × 1/2 + 4), 18 atoms lit',m.edge===543.102&&m.perCube===8&&m.cornerFaceInside===8&&m.litAtoms===18,m);
  m=(await at('siliconSphere','divide')).meta;ok('siliconSphere divide: mass of one mole ÷ mass of one atom = 6.022 × 10²³',m.result==='6.022 × 10²³');
  /* 9. moleMap */
  const X={Cu:['2.00 mol','1.20 × 10²⁴ Cu atoms',2.00*6.022e23,1.20e24,'Cu atoms'],Fe:['9.03 × 10²³ Fe atoms','1.50 mol',9.03e23/6.022e23,1.50,'Fe atoms'],
    CO2m:['0.250 mol','1.51 × 10²³ molecules',0.250*6.022e23,1.51e23,'molecules'],H2Om:['1.81 × 10²⁴ molecules','3.01 mol',1.81e24/6.022e23,3.01,'molecules']};
  for(const [k,[g0,r0,calc,shown,part]] of Object.entries(X)){m=(await at('moleMap',k+'/setup')).meta;ok(`moleMap ${k}/setup: given ${g0}`,m.given===g0&&m.result===null,m);
    m=(await at('moleMap',k+'/cancel')).meta;ok(`moleMap ${k}/cancel: the canceled unit struck, the remaining unit circled`,m.canceled&&m.remains&&m.canceled!==m.remains,m);
    m=(await at('moleMap',k+'/result')).meta;ok(`moleMap ${k}/result: ${r0}, the particle named (${part})`,m.result===r0&&near(calc,shown)&&m.particle===part&&!!m.check,m)}
  m=(await at('moleMap','map')).meta;ok('moleMap map: moles and particles, the bridge 6.022 × 10²³ per mole',m.bridge==='6.022 × 10²³ per mole'&&m.stations.join()==='moles,particles',m);
  m=(await at('moleMap','half')).meta;ok('moleMap half: 3.011 × 10²³ molecules = 0.5000 mol',near(m.particles/6.022e23,m.moles,1e-9)&&m.moles===.5,m);
  m=(await at('moleMap','energy/one')).meta;ok('moleMap energy: 496 kJ/mol ÷ 6.022 × 10²³ = 8.24 × 10⁻¹⁹ J for one atom',m.perMole===496&&m.perAtom==='8.24 × 10⁻¹⁹ J'&&near(496e3/6.022e23,m.perAtomValue),m);
  m=(await at('moleMap','energy/why')).meta;ok('moleMap energy/why: per mole, numbers of a handy size',m.why==='Per mole: numbers of a handy size');
  /* 10. naclCrystal */
  m=(await at('naclCrystal','crystal')).meta;ok('naclCrystal crystal: 27 ions, Na⁺ 102 pm and Cl⁻ 181 pm, 564 pm cell, turning (live)',m.ions===27&&m.radii.Na===102&&m.radii.Cl===181&&m.cell===564&&m.live,m);
  m=(await at('naclCrystal','unit')).meta;ok('naclCrystal unit: the lit pair is one cation and one anion',m.lit.join()==='Cl⁻,Na⁺',m.lit);
  m=(await at('naclCrystal','count')).meta;ok('naclCrystal count: 4.50 mol × 6.022 × 10²³ = 2.71 × 10²⁴ formula units',m.count==='2.71 × 10²⁴'&&m.particle==='formula units'&&near(m.numbers.count[0]*6.022e23,m.numbers.count[1]),m);
  m=(await at('naclCrystal','wrong')).meta;ok('naclCrystal wrong: 2.50 mol, 1.51 × 10²⁴, "molecules" struck for "formula units"',m.wrong==='1.51 × 10²⁴'&&m.wrongParticle==='molecules'&&near(m.numbers.wrong[0]*6.022e23,m.numbers.wrong[1]),m);
  /* 11. atomCounter */
  m=(await at('atomCounter','H2O/one')).meta;ok('atomCounter H2O/one: H₂O, 2 H atoms and 1 O atom',m.formula==='H₂O'&&m.subscripts.H===2&&m.subscripts.O===1);
  m=(await at('atomCounter','H2O/mol')).meta;ok('atomCounter H2O/mol: 1 mol H₂O → 2 mol H, 1 mol O',m.molIn===1&&m.molOut.H===2&&m.molOut.O===1);
  m=(await at('atomCounter','CO2/mol')).meta;ok('atomCounter CO2/mol: 2.00 mol CO₂ × 2 = 4.00 mol O',m.formula==='CO₂'&&m.molOut.O===m.molIn*m.subscripts.O&&m.molOut.O===4);
  m=(await at('atomCounter','CO2/atoms')).meta;ok('atomCounter CO2/atoms: 4.00 mol × 6.022 × 10²³ = 2.41 × 10²⁴ O atoms',m.atomsOut==='2.41 × 10²⁴'&&near(4*6.022e23,2.41e24));
  m=(await at('atomCounter','NaCl/mol')).meta;ok('atomCounter NaCl/mol: 1 mol NaCl → 1 mol Na⁺, 1 mol Cl⁻',m.ions&&m.molOut['Na⁺']===1&&m.molOut['Cl⁻']===1);
  m=(await at('atomCounter','NH3/mol')).meta;ok('atomCounter NH3/mol: 0.500 mol NH₃ × 3 = 1.50 mol H',m.formula==='NH₃'&&m.molOut.H===m.molIn*m.subscripts.H&&m.molOut.H===1.5);
  /* reduced motion: every live or turning stage holds one still frame */
  for(const key of ['coinScale:tally','howMany:zoom','secondsLine:line','siliconSphere:crystal','siliconSphere:cube','naclCrystal:crystal','naclCrystal:unit']){const [sim,stage]=key.split(':'),x=list.find(r=>r.sim===sim&&r.stage===stage);
    await page.evaluate(i=>Deck.go(i,0),x.i);await L.wait(page,300);const a=await page.evaluate(id=>document.querySelector('#'+id+' canvas').toDataURL(),x.host);await L.wait(page,900);
    const b=await page.evaluate(id=>document.querySelector('#'+id+' canvas').toDataURL(),x.host);ok(`${key}: one still frame under reduced motion`,a===b)}
  /* with motion on, the live stages move */
  const mo=await L.open({browser,reduced:false});
  for(const key of LIVE){const [sim,stage]=key.split(':'),x=list.find(r=>r.sim===sim&&r.stage===stage);await mo.page.evaluate(i=>Deck.go(i,0),x.i);await L.wait(mo.page,1200);
    const a=await mo.page.evaluate(id=>document.querySelector('#'+id+' canvas').toDataURL(),x.host);await L.wait(mo.page,1000);const b=await mo.page.evaluate(id=>document.querySelector('#'+id+' canvas').toDataURL(),x.host);
    ok(`${key}: moves with motion on`,a!==b)}
  ok('every stage of section 4 has a scratch slide (78)',list.length===78&&Object.keys(seen).length===78,{slides:list.length,seen:Object.keys(seen).length});
  ok('no console errors',!errors.length&&!mo.errors.length,errors.concat(mo.errors));
  L.save('scratch-check-51.json',res);res.forEach(r=>console.log(`  ${r.pass?'PASS':'FAIL'}  ${r.n}${r.pass?'':'  '+r.i}`));
  const n=res.filter(r=>!r.pass).length;console.log(`scratch-check 5.1: ${n?'FAIL ('+n+')':'PASS'} ${res.length} assertions`);await browser.close();process.exitCode=n?1:0;
})();
