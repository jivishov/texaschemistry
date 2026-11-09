// Chemistry checks on the Lesson 5.1 animations as placed in the deck (meta() of each placed instance at the deck's own stages, by
// slide id, host and stage, as 4.2's chem.js does), the label and shape floors of every placed instance, the animation on screen with
// each check, and the deck's text facts (plan section 10, item 2).
const L=require('../../../audits/lib'); // DECK and OUT from the environment (suite.py)
const fs=require('fs'),path=require('path');
const near=(a,b,r)=>Math.abs(a/b-1)<=(r||.005);
(async()=>{
  const {browser,page,errors}=await L.open({});const res=[];const ok=(n,p,i)=>res.push({n,pass:!!p,i:i===undefined?'':JSON.stringify(i)});
  const meta=(sid,sim,stage)=>page.evaluate(([sid,sim,stage])=>{const s=Deck.slides.findIndex(S=>S.id===sid),f=s<0?-1:Deck.slides[s].frames.findIndex(fr=>fr.stage.some(x=>x.sim===sim&&x.s===stage));
    if(f<0)return {missing:stage};Deck.go(s,f);const m=Deck.sims[sim];return Object.assign(m.meta(),{minFont:m.minFont})},[sid,sim,stage]);
  const floors=(t,m)=>ok(`${t}: labels at 36 px or more, shapes at 60 px or more`,m.minFont>=36&&(m.minShape==null?/^slide 11 /.test(t):m.minShape>=60),{font:m.minFont,shape:m.minShape});
  let m;
  /* slide 2: coinScale, the jar of nickels */
  m=await meta('s02','s02-sim','tally');ok('slide 2 coinScale tally: live, 8 coins counted one a second',m.live&&m.tallyCoins===8,m);floors('slide 2 tally',m);
  m=await meta('s02','s02-sim','scale');ok('slide 2 coinScale scale: 2,000.0 g of coins, 5.000 g per nickel',m.total===2000&&m.massPerCoin===5,m);
  m=await meta('s02','s02-sim','reveal');ok('slide 2 coinScale reveal: 2,000.0 g ÷ 5.000 g = 400 nickels',m.count===400&&m.count*m.massPerCoin===m.total,m);floors('slide 2 reveal',m);
  /* slide 6: the bank */
  m=await meta('s06','s06-sim','zero');ok('slide 6 coinScale zero: the empty bag, 0.0 g, zeroed',m.total===0&&m.reading==='0.0 g'&&m.zeroed,m);
  m=await meta('s06','s06-sim','read');ok('slide 6 coinScale read: 1,250.0 g',m.reading==='1,250.0 g'&&m.total===1250,m);
  m=await meta('s06','s06-sim','divide');ok('slide 6 coinScale divide: 1,250.0 g × 1 nickel / 5.000 g, the grams struck',m.bridge==='1,250.0 g × 1 nickel / 5.000 g'&&m.struck.length===2,m);
  m=await meta('s06','s06-sim','count');ok('slide 6 coinScale count: 250 nickels; 250 × 5.000 g = 1,250.0 g',m.count===250&&m.count*m.massPerCoin===1250&&m.check==='250 × 5.000 g = 1,250.0 g',m);floors('slide 6 count',m);
  m=await meta('s06','s06-sim','roll');ok('slide 6 coinScale roll (the check): 200.0 g, the answer 40 not drawn',m.roll&&m.roll.mass===200&&m.roll.answer===40&&!m.roll.answerDrawn,m);
  /* slide 7: the jar of pennies */
  m=await meta('s07','s07-sim','jar');ok('slide 7 centJar: before 1982 3.11 g, after 1982 2.500 g, the jar 1,017.1 g',m.old===3.11&&m.new===2.5&&m.jar===1017.1,m);
  m=await meta('s07','s07-sim','wrong');ok('slide 7 centJar wrong: about 407 (too many), about 327 (too few)',m.wrong[0].cents===Math.round(1017.1/2.5)&&m.wrong[1].cents===Math.round(1017.1/3.11)&&m.wrong[0].verdict==='too many'&&m.wrong[1].verdict==='too few',m.wrong);
  m=await meta('s07','s07-sim','average');ok('slide 7 centJar: 267.69 g ÷ 100 = 2.6769 g',m.sample===267.69&&m.sampleN===100&&near(267.69/100,m.average,1e-9),m);
  m=await meta('s07','s07-sim','count');ok('slide 7 centJar: 1,017.1 g ÷ 2.6769 g = about 380 cents, between the two masses',m.count===380&&Math.round(1017.1/2.6769)===380&&m.between,m);floors('slide 7 count',m);
  m=await meta('s07','s07-sim','isotopes');ok('slide 7 centJar isotopes: the table\'s average mass, no isotope masses',m.isotopes&&m.isotopes.label==='isotopes'&&!m.isotopes.isotopeMassesShown,m.isotopes);
  /* slide 8: the counting units */
  m=await meta('s08','s08-sim','ream');ok('slide 8 countingUnits: a dozen is 12, a ream 500',m.dozen===12&&m.ream===500,m);
  m=await meta('s08','s08-sim','exact');ok('slide 8 countingUnits: exactly 6.02214076 × 10²³, rounded 6.022 × 10²³, since May 20, 2019',m.exact==='6.02214076 × 10²³'&&m.rounded==='6.022 × 10²³'&&m.since==='May 20, 2019',m);
  m=await meta('s08','s08-sim','constant');ok('slide 8 countingUnits: N_A = 6.022 × 10²³ mol⁻¹',/6\.022 × 10²³ mol⁻¹$/.test(m.constant||''),m.constant);floors('slide 8 constant',m);
  /* slide 9: how many is a mole */
  m=await meta('s09','s09-sim','zoom');ok('slide 9 howMany zoom: live, seven steps of × 1,000 to 10²¹',m.live&&m.steps===7&&m.perStep===1000&&m.top==='10²¹',m);
  m=await meta('s09','s09-sim','mole');ok('slide 9 howMany mole: × 602 more, 6.022 × 10²³',m.last===602&&m.check&&m.mole==='6.022 × 10²³',m);
  m=await meta('s09','s09-sim','spoon');ok('slide 9 howMany spoon: one mole of water about 18 g',m.water===18,m);floors('slide 9 spoon',m);
  /* slide 10: name the particle */
  m=await meta('s10','s10-sim','compare');ok('slide 10 moleKinds compare: 26.982 g and 63.546 g, the same 6.022 × 10²³ atoms',m.masses.Al===26.982&&m.masses.Cu===63.546&&m.equal&&m.counts.Al===m.counts.Cu,m);
  m=await meta('s10','s10-sim','oxygen');ok('slide 10 moleKinds oxygen: O₂ holds twice the atoms',m.o2Ratio===2,m);
  m=await meta('s10','s10-sim','four');ok('slide 10 moleKinds four: atoms, molecules, formula units, ions; Na⁺ 102 pm, Cl⁻ 181 pm',m.names.join('|')==='atoms|molecules|formula units|ions'&&m.radii.Na_ion===102&&m.radii.Cl_ion===181,m);floors('slide 10 four',m);
  /* slide 11: the size of a mole */
  m=await meta('s11','s11-sim','line');ok('slide 11 secondsLine line: live',m.live,m);
  m=await meta('s11','s11-sim','mole');ok('slide 11 secondsLine: 6.022 × 10²³ s ÷ 3.156 × 10⁷ s = 1.908 × 10¹⁶ years',m.yearsCheck&&m.yearS===3.156e7&&m.moleShown==='about 1.9 × 10¹⁶ years',m);
  m=await meta('s11','s11-sim','times');ok('slide 11 secondsLine times: about 1.4 million times 13.8 billion years; Earth 4.5 billion: about 4 million',m.timesCheck&&m.universeYears===1.38e10&&m.earthYears===4.5e9&&Math.round(m.earthTimes)===4,m);floors('slide 11 times',m);
  m=await meta('s11','s11-sim','spoon');ok('slide 11 secondsLine spoon: about 18 g',m.water===18,m);
  /* slide 12: who found the number */
  m=await meta('s12','s12-sim','exact');ok('slide 12 moleHistory: 1811, 1865, 1890s, 1909, 1971, 2019; voted November 16, 2018; exact since May 20, 2019',m.ticks.map(t=>t.year+' '+t.name).join('|')==='1811 Avogadro|1865 Loschmidt|1890s Ostwald|1909 Perrin|1971 SI|2019 exact'&&m.vote==='November 16, 2018'&&m.since==='May 20, 2019',m);floors('slide 12 exact',m);
  m=await meta('s12','s12-sim','si');ok('slide 12 moleHistory si: the old definition, 12 g of carbon-12',m.oldDefinition==='12 g of carbon-12'&&m.lines.join(' ').includes('12 g'),m.lines);
  /* slide 13: the silicon sphere */
  m=await meta('s13','s13-sim','crystal');ok('slide 13 siliconSphere crystal: 95 atoms in 2 × 2 × 2 diamond cubes, turning',m.atoms===95&&m.live,m);
  m=await meta('s13','s13-sim','cube');ok('slide 13 siliconSphere cube: edge 543.102 pm, 8 atoms per cube',m.edge===543.102&&m.perCube===8&&m.cornerFaceInside===8,m);floors('slide 13 cube',m);
  m=await meta('s13','s13-sim','divide');ok('slide 13 siliconSphere divide: 6.022 × 10²³',m.result==='6.022 × 10²³',m);
  /* slides 16, 17, 20, 21: the map */
  for(const [sid,host,k,res,calc,shown] of [['s16','s16-sim','Cu','1.20 × 10²⁴ Cu atoms',2.00*6.022e23,1.20e24],['s17','s17-sim','Fe','1.50 mol',9.03e23/6.022e23,1.50],
    ['s20','s20-sim','CO2m','1.51 × 10²³ molecules',0.250*6.022e23,1.51e23],['s20','s20-sim','H2Om','3.01 mol',1.81e24/6.022e23,3.01]]){
    m=await meta(sid,host,k+'/cancel');ok(`slide ${+sid.slice(1)} moleMap ${k}/cancel: one unit struck, the other circled`,m.canceled&&m.remains&&m.canceled!==m.remains,m);
    m=await meta(sid,host,k+'/result');ok(`slide ${+sid.slice(1)} moleMap ${k}/result: ${res}`,m.result===res&&near(calc,shown)&&!!m.particle,m);floors(`slide ${+sid.slice(1)} ${k}`,m)}
  m=await meta('s16','s16-sim','map');ok('slide 16 moleMap map: the bridge 6.022 × 10²³ per mole',m.bridge==='6.022 × 10²³ per mole',m);
  m=await meta('s17','s17-sim','half');ok('slide 17 moleMap half: 3.011 × 10²³ = 0.5000 mol',near(m.particles/6.022e23,m.moles,1e-9)&&m.moles===.5,m);
  m=await meta('s21','s21-sim','energy/one');ok('slide 21 moleMap energy: 496 kJ/mol ÷ 6.022 × 10²³ = 8.24 × 10⁻¹⁹ J per atom',m.perMole===496&&m.perAtom==='8.24 × 10⁻¹⁹ J'&&near(496e3/6.022e23,8.24e-19),m);floors('slide 21 energy',m);
  /* slide 18: formula units */
  m=await meta('s18','s18-sim','unit');ok('slide 18 naclCrystal unit: one Na⁺ and one Cl⁻ lit; Shannon radii; 564 pm cell; turning',m.lit.join()==='Cl⁻,Na⁺'&&m.radii.Na===102&&m.radii.Cl===181&&m.cell===564&&m.live,m);
  m=await meta('s18','s18-sim','count');ok('slide 18 naclCrystal count: 4.50 mol × 6.022 × 10²³ = 2.71 × 10²⁴ formula units',m.count==='2.71 × 10²⁴'&&m.particle==='formula units'&&near(4.50*6.022e23,2.71e24),m);
  m=await meta('s18','s18-sim','wrong');ok('slide 18 naclCrystal wrong: 2.50 mol → 1.51 × 10²⁴, "molecules" is the wrong particle',m.wrong==='1.51 × 10²⁴'&&m.wrongParticle==='molecules'&&near(2.50*6.022e23,1.51e24),m);floors('slide 18 wrong',m);
  /* slide 19 and 20: atoms in a formula */
  m=await meta('s19','s19-sim','H2O/mol');ok('slide 19 atomCounter H2O/mol: 1 mol H₂O → 2 mol H, 1 mol O',m.formula==='H₂O'&&m.molOut.H===2&&m.molOut.O===1,m);
  m=await meta('s19','s19-sim','CO2/mol');ok('slide 19 atomCounter CO2/mol: 2.00 mol × 2 = 4.00 mol O',m.molOut.O===m.molIn*m.subscripts.O&&m.molOut.O===4,m);
  m=await meta('s19','s19-sim','CO2/atoms');ok('slide 19 atomCounter CO2/atoms: 2.41 × 10²⁴ O atoms',m.atomsOut==='2.41 × 10²⁴'&&near(4*6.022e23,2.41e24),m);
  m=await meta('s19','s19-sim','NaCl/mol');ok('slide 19 atomCounter NaCl/mol: 1 mol Na⁺ and 1 mol Cl⁻',m.ions&&m.molOut['Na⁺']===1&&m.molOut['Cl⁻']===1,m);floors('slide 19 NaCl',m);
  m=await meta('s20','s20-ac','NH3/mol');ok('slide 20 atomCounter NH3/mol: 0.500 mol × 3 = 1.50 mol H',m.molOut.H===m.molIn*m.subscripts.H&&m.molOut.H===1.5,m);
  /* the animation on screen with each check shows the check's subject */
  const want={s06:['s06-sim','roll'],s07:['s07-sim','sample'],s08:['s08-sim','constant'],s09:['s09-sim','spoon'],s10:['s10-sim','compare'],s11:['s11-sim','times'],s13:['s13-sim','cube'],
    s16:['s16-sim','Cu/result'],s17:['s17-sim','half'],s18:['s18-sim','unit'],s19:['s19-sim','CO2/mol']};
  const at=await page.evaluate(w=>Object.fromEntries(Object.entries(w).map(([sid,[sim]])=>{const s=Deck.slides.findIndex(S=>S.id===sid),f=Deck.slides[s].frames.findIndex(fr=>fr.show.includes(sid+'-check'));Deck.go(s,f);return [sid,Deck.sims[sim].get()]})),want);
  Object.entries(want).forEach(([sid,[sim,st]])=>ok(`slide ${+sid.slice(1)}: the check frame shows ${sim} at "${st}"`,at[sid]===st,at[sid]));
  /* text facts */
  const T=await page.evaluate(()=>{const t=id=>{const e=document.querySelector('[id="'+id+'"],[data-b="'+id+'"]');return e?e.textContent.replace(/\s+/g,' ').trim():null};return {
    warm:[1,2,3].map(i=>t('s15-a'+i)),you:[1,2,3].map(i=>t('s20-a'+i)),
    s14:[...document.querySelectorAll('#s14 .g3 .cell')].map(c=>c.textContent.replace(/\s+/g,' ').trim()),s14h:[...document.querySelectorAll('#s14 .g3 .colh p')].map(c=>c.textContent.trim()),
    rate:[...document.querySelectorAll('#s27 .rev')].map(e=>e.textContent.trim()),
    pred:[1,2,3].map(i=>{const c=document.getElementById('s26-p'+i);return {right:c.querySelector('.opt.right span').textContent.replace(/\s+/g,' ').trim(),letter:c.querySelector('.opt.right b').textContent,reason:c.querySelector('.reason').textContent.replace(/\s+/g,' ').trim()}}),
    q4:[1,2,3].map(i=>[...document.querySelectorAll('#s04-q'+i+' .opt span')].map(s=>s.textContent.replace(/\s+/g,' ').trim())),
    es:[...document.querySelectorAll('#s05 .wcard')].map(w=>[w.querySelector('.t').firstChild.textContent.trim(),w.querySelector('.es').textContent.replace(/[()]/g,'').trim()]),
    legend:[...document.querySelectorAll('#s05-leg>span')].map(s=>s.textContent.replace(/\s+/g,' ').trim()),
    cap:[t('s10-cap'),t('s19-cap')],
    checks:[...document.querySelectorAll('.slide')].filter(s=>s.querySelector('.card.check[id$="-check"],.checkrow')).map(s=>+s.id.slice(1)),
    periods:Deck.slides.map(S=>+S.period),n:Deck.slides.length}});
  ok('slide 15 warm-up answers: 200, 6.022 × 10²³, the four particles',(w=>w[0]==='200(1,000.0g÷5.000g)'&&w[1].startsWith('6.022×1023(exactly6.02214076×1023')&&w[2]==='atoms,molecules,formulaunits,ions')(T.warm.map(x=>x.replace(/\s/g,''))),T.warm);
  ok('slide 20 you-do answers: 1.50 mol of H atoms; 7.23 × 10²⁴ H atoms; 0.042 mol',T.you[0]==='1.50 mol of H atoms'&&T.you[1].includes('12.0 mol')&&T.you[1].replace(/\s/g,'').includes('=7.23×1024Hatoms')&&T.you[2].startsWith('0.042 mol')&&near(.5*3,1.5)&&near(12*6.022e23,7.23e24)&&near(2.5e22/6.022e23,.042,.02),T.you);
  ok('slide 14 table: nickels, cents, atoms; 5.000 g; the average; moles of 6.022 × 10²³; the particles named',T.s14h.join('|')==='nickels|cents|atoms'&&T.s14.length===9&&T.s14[3].includes('5.000 g')&&T.s14[5].includes('6.022 × 1023')&&T.s14[8].includes('formula units'),T.s14);
  ok('slide 27 review lines: slides 6 and 7; 8 to 13 and 21; 16 to 18; 19 and 20',T.rate.join('|')==='Review: slides 6 and 7|Review: slides 8 to 13 and 21|Review: slides 16 to 18|Review: slides 19 and 20',T.rate);
  ok('slide 26 the three predictions: the same number of atoms (B), formula units (B), 2 mol (B), with their reasons',T.pred.map(p=>p.letter+' '+p.right).join('|')==='B the same number of atoms|B formula units|B 2 mol'&&T.pred[0].reason.includes('Al 26.982 g')&&T.pred[0].reason.includes('Cu 63.546 g')&&T.pred[2].reason.includes('subscript 2 multiplies'),T.pred);
  ok('slide 26 answers are the slide 4 options B',T.q4[0][1]==='the same number of atoms'&&T.q4[1][1]==='formula units'&&T.q4[2][1]==='2 mol',T.q4);
  const COG=[['mole','mol'],['Avogadro\'s number','número de Avogadro'],['Avogadro constant','constante de Avogadro'],['amount of substance','cantidad de sustancia'],['molecule','molécula'],['formula unit','unidad fórmula'],['chemical formula','fórmula química'],['subscript','subíndice']];
  ok('slide 5 the eight Spanish cognates of the lesson sheet',JSON.stringify(T.es)===JSON.stringify(COG),T.es);
  let gl={};try{const r=fs.readFileSync(path.join(path.dirname(L.DECK),'reading-5-1.html'),'utf8');for(const m2 of r.matchAll(/"([^"]+)":\{d:"[^"]*",es:"([^"]+)"\}/g))gl[m2[1]]=m2[2]}catch(e){}
  ok('slide 5 the cognates match the reading\'s glossary (unit5/reading-5-1.html)',COG.every(([t,e])=>gl[t]===e),COG.map(([t])=>t+': '+gl[t]));
  ok('slide 5 the Unit 5 legend: grams, moles, particles, cation, anion, atom',T.legend.join('|')==='ggrams (mass)|molmoles (amount)|#particles (number)|+cation|−anion|Oatom (CPK color = element)',T.legend);
  ok('slides 10 and 19: "Atom colors show the element, not the charge."',T.cap.every(c=>c==='Atom colors show the element, not the charge.'),T.cap);
  ok('eleven checks on slides 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 19',T.checks.join()==='6,7,8,9,10,11,13,16,17,18,19',T.checks);
  const reg=JSON.parse(fs.readFileSync(path.join(__dirname,'../../../registry.json'),'utf8')).decks.find(d=>d.unit===5&&d.lesson===1);
  ok(`registry: ${reg.checks} checks and periods ${JSON.stringify(reg.periods)} match the deck`,T.checks.length===reg.checks&&T.n===reg.periods[1][1]&&T.periods.every((p,i)=>p===(i+1<=reg.periods[0][1]?1:2)),{checks:T.checks.length,periods:T.periods.join('')});
  ok('no console errors',!errors.length,errors);
  L.save('chem51-deck.json',res);res.forEach(r=>console.log(`  ${r.pass?'PASS':'FAIL'}  ${r.n}${r.pass?'':'  '+r.i}`));
  const n=res.filter(r=>!r.pass).length;console.log(`chem51 (deck): ${n?'FAIL ('+n+')':'PASS'} ${res.length} checks`);await browser.close();process.exitCode=n?1:0;
})();
