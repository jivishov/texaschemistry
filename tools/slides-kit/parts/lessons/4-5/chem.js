// Chemistry checks on the Lesson 4.5 animations as placed in the deck (meta() of each placed instance at the deck's own stages, by
// slide id and stage, as 4.2's chem.js does), the shape floor of every placed canvas, the check frames' subjects, and the deck's text
// facts (lessons/4-5.md and brief 04). Every meta() assertion of scratch-check.js is repeated here on the placed instances.
const L=require('../../../audits/lib'); // DECK and OUT from the environment (suite.py)
const REG=require('../../../registry.json').decks.find(d=>d.unit===4&&d.lesson===5);
(async()=>{
  const {browser,page,errors}=await L.open({});const res=[];const ok=(n,p,i)=>res.push({n,pass:!!p,i:i===undefined?'':JSON.stringify(i)});
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  /* every frame of a slide: {f, stage, meta, visible} of one placed animation */
  const run=(sid,sim)=>page.evaluate(([sid,sim])=>{const s=Deck.slides.findIndex(S=>S.id===sid),S=Deck.slides[s],x=Deck.sims[sim],out=[];
    S.frames.forEach((fr,f)=>{Deck.go(s,f);const h=document.getElementById(sim),cs=getComputedStyle(h);
      out.push({f,stage:x.get(),meta:x.meta(),visible:cs.visibility==='visible'&&h.offsetParent!==null&&h.clientHeight>0})});return out},[sid,sim]);
  const at=(R,stage)=>{const r=R.filter(x=>x.stage===stage);return r.length?r[r.length-1].meta:null};
  const staged=(R,list)=>list.every(s=>R.some(x=>x.stage===s));
  /* the shape floor on the deck's own host: every atom or ion sphere drawn on a visible frame is 60 px or more (meta().drawn.atom) */
  const shapes=(name,R)=>{const bad=R.filter(x=>x.visible&&x.meta.drawn&&x.meta.drawn.atom!==null&&x.meta.drawn.atom<60).map(x=>`f${x.f} ${x.stage} ${x.meta.drawn.atom}px`);
    const mins=R.filter(x=>x.visible&&x.meta.drawn&&x.meta.drawn.atom!==null).map(x=>x.meta.drawn.atom);
    ok(`${name}: every atom or ion sphere 60 px or more on every frame that shows it (smallest ${mins.length?Math.min(...mins)+' px':'none drawn'})`,!bad.length,bad)};
  /* the stage on screen at a slide's check frame (RULES 5: the check's subject) */
  const checkStage=(sid,sim)=>page.evaluate(([sid,sim])=>{const s=Deck.slides.findIndex(S=>S.id===sid),S=Deck.slides[s];
    const f=S.frames.findIndex(fr=>fr.show.includes(sid+'-check'));Deck.go(s,f);const h=document.getElementById(sim);
    return {f,stage:Deck.sims[sim].get(),visible:getComputedStyle(h).visibility==='visible'&&h.offsetParent!==null}},[sid,sim]);
  const subject=async(sid,sim,stage,why)=>{const c=await checkStage(sid,sim);ok(`slide ${+sid.slice(1)} check frame shows ${sim} at "${stage}" (${why})`,c.visible&&c.stage===stage,c)};

  /* 1. brickBag (slide 2) */
  let R=await run('s02','s02-sim');
  ok('slide 2 brickBag: stages models, shake, pour, words',staged(R,['models','shake','pour','words']),R.map(x=>x.stage));
  R.forEach(x=>ok(`slide 2 brickBag f${x.f} ${x.stage}: 3 models, 11 bricks, all snapped`,x.meta.models===3&&x.meta.bricks===11&&x.meta.snapped===11&&x.meta.counter==='Bricks snapped: 11 of 11',x.meta));
  ok('slide 2 brickBag words: the two labels',eq(at(R,'words').labels,['a snap between bricks = a bond within','models side by side = an attraction between']),at(R,'words').labels);
  ok('slide 2 brickBag pour: on the table, out of the bag',at(R,'pour').onTable&&!at(R,'pour').inBag);

  /* 2. meltScale (slide 3) */
  R=await run('s03','s03-sim');let m;
  ok('slide 3 meltScale: stages snow, salt, sand, melt, numbers',staged(R,['snow','salt','sand','melt','numbers']),R.map(x=>x.stage));
  ok('slide 3 meltScale: the solids appear one per press',eq(at(R,'snow').shown,['snow'])&&eq(at(R,'salt').shown,['snow','salt'])&&eq(at(R,'sand').shown,['snow','salt','sand']));
  R.forEach(x=>ok(`slide 3 meltScale f${x.f} ${x.stage} (${x.meta.layout} layout): smallest atom or ion sphere ${x.meta.minSphere===null?'none drawn':x.meta.minSphere+' px'}`,x.meta.layout==='tall'?x.meta.minSphere>=60:x.meta.minSphere===null,{layout:x.meta.layout,minSphere:x.meta.minSphere}));
  ok('slide 3 meltScale: the particle panels show while the lines are on screen (tall layout on frames 0 to 6)',R.slice(0,7).every(x=>x.meta.layout==='tall'),R.map(x=>x.meta.layout));
  m=at(R,'melt');ok('slide 3 meltScale melt: snow 0.0, salt 801, sand near 1700; snow molecules whole; salt and sand stay',eq(m.values,{snow:0.0,salt:801,sand:'near 1700'})&&m.snowMoleculesIntact&&m.snowMoved&&!m.saltMoved&&!m.sandMoved,m);
  /* step 04b (the teacher's review): every drawing inside its panel; two water molecules and one hydrogen bond; a neutral 2 x 4 salt grid;
     at the melt the names say which solids stay solid */
  R.filter(x=>x.meta.layout==='tall').forEach(x=>ok(`slide 3 meltScale f${x.f} ${x.stage}: every drawing inside its panel (clearance ${JSON.stringify(x.meta.clearance)})`,Object.values(x.meta.clearance).every(v=>v>=4),x.meta.clearance));
  m=at(R,'snow');ok('slide 3 meltScale snow: two water molecules joined by one hydrogen bond, H···O 1.94 times O–H',m.snowMolecules===2&&m.snowHbonds===1&&m.hbondRatio===1.94,m);
  m=at(R,'salt');ok('slide 3 meltScale salt: 2 x 4 grid, four Na⁺ and four Cl⁻',eq(m.saltIons,{rows:2,cols:4,cations:4,anions:4}),m.saltIons);
  m=at(R,'melt');ok('slide 3 meltScale melt: "snow: melts", "salt: stays solid", "sand: stays solid"; the hydrogen bond let go',eq(m.states,['snow: melts','salt: stays solid','sand: stays solid'])&&m.snowHbonds===0&&!at(R,'sand').states,m.states);
  m=at(R,'numbers');ok('slide 3 meltScale numbers: "Melting point" and chips "snow 0.0 °C", "salt 801 °C", "sand near 1700 °C"',m.label==='Melting point'&&eq(m.chips,['snow 0.0 °C','salt 801 °C','sand near 1700 °C']),m.chips);

  /* 3. threeSolids (slide 6) */
  R=await run('s06','s06-sim');
  m=at(R,'chlorine');ok('slide 6 threeSolids chlorine: Cl₂ molecules, one stick within each, no dashed line yet',m.molecules>=4&&m.sticksWithin===m.molecules&&m.dashedBetween===0,m);
  m=at(R,'within');ok('slide 6 threeSolids within: "bond within"',m.withinGlow&&m.labels.includes('bond within'),m.labels);
  m=at(R,'between');ok('slide 6 threeSolids between: dashed lines, "attraction between (much weaker)"',m.dashedBetween>0&&m.labels.includes('attraction between (much weaker)'),m);
  m=at(R,'salt');ok('slide 6 threeSolids salt: Na⁺ 102 and Cl⁻ 181 pm at 282 pm, "ionic bonds through the whole crystal, no molecules"',eq(m.naclRadii,[102,181])&&m.naclSpacing===282&&m.labels.includes('ionic bonds through the whole crystal, no molecules'),m);
  m=at(R,'copper');ok('slide 6 threeSolids copper: delocalized electrons, "metallic bonds through the whole metal"',m.copper==='delocalized electrons'&&m.panels===3&&m.labels.includes('metallic bonds through the whole metal'),m);
  shapes('slide 6 threeSolids',R);await subject('s06','s06-sim','between','Cl₂ molecules with the attractions between');

  /* 4. attractions and bpPlot (slides 7, 8, 9) */
  R=await run('s07','s07-sim');
  ok('slide 7 attractions: the dispersion family (cloud, flicker, neighbor, attract)',staged(R,['cloud','flicker','neighbor','attract']));
  ['flicker','neighbor','attract'].forEach(s=>{m=at(R,s);ok(`slide 7 attractions ${s}: nonpolar, δ signs for an instant only`,m.family==='dispersion'&&m.polar===false&&m.deltaLabels==='instant',m)});
  ok('slide 7 attractions cloud: no δ signs yet',at(R,'cloud').deltaLabels===null);
  ok('slide 7 attractions (step 04b): a key names the gray + circles "nucleus" and the − dots "electron" on every dispersion frame',['cloud','flicker','neighbor','attract'].every(s=>eq(at(R,s).key,['nucleus','electron'])));
  ok('slide 7 attractions attract: the dashed line, "dispersion forces"',at(R,'attract').line&&at(R,'attract').label==='dispersion forces');
  const V={F2:['F₂',18,-188.1,'dispersion forces'],Cl2:['Cl₂',34,-34.0,'dispersion forces'],Br2:['Br₂',70,58.8,'dispersion forces'],I2:['I₂',106,184.4,'dispersion forces'],
    CH4:['CH₄',10,-161.5,'dispersion forces'],NH3:['NH₃',10,-33.3,'hydrogen bonding'],H2O:['H₂O',10,100.0,'hydrogen bonding'],HCl:['HCl',18,-85.1,'dipole-dipole forces']};
  const plot=(R,want,n)=>Object.entries(want).forEach(([s,ks])=>{const mm=at(R,s);if(!mm){ok(`slide ${n} bpPlot ${s}: staged`,false);return}
    const bright=mm.points.filter(q=>!q.faint),got=bright.map(q=>q.f);
    ok(`slide ${n} bpPlot ${s}: points ${ks.map(k=>V[k][0]).join(', ')||'none'}, each with its electrons, boiling point and strongest attraction`,eq(got,ks.map(k=>V[k][0]))&&bright.every(q=>{const k=Object.keys(V).find(k=>V[k][0]===q.f);return k&&q.e===V[k][1]&&q.bp===V[k][2]&&q.force===V[k][3]}),bright)});
  R=await run('s07','s07-plot');
  plot(R,{axes:[],F2:['F2'],Cl2:['F2','Cl2'],Br2:['F2','Cl2','Br2'],I2:['F2','Cl2','Br2','I2'],trend:['F2','Cl2','Br2','I2']},7);
  ok('slide 7 bpPlot: axes 0 to 110 electrons, −200 to 200 °C; the trend line at trend',eq(at(R,'axes').xRange,[0,110])&&eq(at(R,'axes').yRange,[-200,200])&&at(R,'trend').trend);
  await subject('s07','s07-plot','trend','Cl₂ and Br₂ on the halogen trend');
  R=await run('s08','s08-sim');
  ok('slide 8 attractions: the dipole family (F2, HCl, turn, face, compare)',staged(R,['F2','HCl','turn','face','compare']));
  m=at(R,'F2');ok('slide 8 attractions F2: no δ signs, dashed gray only',m.family==='dipole'&&m.F2&&m.F2.dplus===null&&m.F2.dminus===null&&m.F2.line==='dashed gray'&&m.HCl===null,m);
  m=at(R,'HCl');ok('slide 8 attractions HCl: δ+ on H, δ− on Cl',eq(m.HCl,{dplus:'H',dminus:'Cl'}),m.HCl);
  ok('slide 8 attractions turn: head to tail',at(R,'turn').headToTail===true);
  m=at(R,'face');ok('slide 8 attractions face: δ+ to δ− line, "dipole-dipole forces"',m.line==='δ+ to δ−'&&m.label==='dipole-dipole forces',m);
  m=at(R,'compare');ok('slide 8 attractions compare: 18 and 18 electrons; F₂ −188.1, HCl −85.1 °C',eq(m.electrons,{F2:18,HCl:18})&&eq(m.bp,{F2:-188.1,HCl:-85.1}),m);
  shapes('slide 8 attractions',R);await subject('s08','s08-sim','compare','HCl with its δ signs');
  R=await run('s09','s09-plot');
  plot(R,{trio:['CH4','NH3','H2O'],reveal:['CH4','NH3','H2O']},9);
  ok('slide 9 bpPlot trio: no labels yet; reveal: labelled',at(R,'trio').points.filter(q=>!q.faint).every(q=>!q.labelled)&&at(R,'reveal').points.filter(q=>!q.faint).every(q=>q.labelled));
  R=await run('s09','s09-sim');
  ok('slide 9 attractions: the hydrogen family (hbond, ammonia, methane, four)',staged(R,['hbond','ammonia','methane','four']));
  m=at(R,'hbond');ok('slide 9 attractions hbond: H on O to a lone pair on O, longer than the O–H bond, the label',eq(m.water,{donor:'H on O',acceptor:'lone pair on O'})&&m.hbond&&m.hbondLonger&&m.label==='hydrogen bond: about 5 to 10% of a covalent bond',m);
  m=at(R,'ammonia');ok('slide 9 attractions ammonia: H on N to a lone pair on N',eq(m.ammonia,{donor:'H on N',acceptor:'lone pair on N'}),m);
  m=at(R,'methane');ok('slide 9 attractions methane: none, "H on C: no hydrogen bond"',m.methane==='none'&&m.label==='H on C: no hydrogen bond',m);
  m=at(R,'four');ok('slide 9 attractions four: four hydrogen bonds, four neighbors',m.waterMax===4&&m.hbonds===4&&m.neighbors===4,m);
  shapes('slide 9 attractions',R);await subject('s09','s09-sim','four','water with its four hydrogen bonds');

  /* 5. forceDecider (slide 10): triplet 1 */
  R=await run('s10','s10-sim');
  m=at(R,'empty');ok('slide 10 forceDecider empty: nothing filled, no drawing',m.molecule===null&&m.drawing===false&&Object.values(m.answers).every(v=>v===null),m);
  const FD={'NH3/strongest':['NH3',{polar:'yes',H:'yes',lone:'yes',strongest:'hydrogen bonding'}],'CO2/strongest':['CO2',{polar:'no',H:'no',lone:'not needed',strongest:'dispersion forces'}],
    'HBr/polar':['HBr',{polar:'yes',H:null,lone:null,strongest:null}],'HBr/H':['HBr',{polar:'yes',H:'no',lone:'not needed',strongest:null}],'HBr/strongest':['HBr',{polar:'yes',H:'no',lone:'not needed',strongest:'dipole-dipole forces'}]};
  Object.entries(FD).forEach(([s,[mol,ans]])=>{m=at(R,s);ok(`slide 10 forceDecider ${s}: ${mol}, ${Object.values(ans).filter(Boolean).join(' · ')}`,m&&m.molecule===mol&&eq(m.answers,ans),m)});
  ok('slide 10 forceDecider: every stage from empty to HBr/strongest in order',eq(R.map(x=>x.stage),['empty','NH3/polar','NH3/H','NH3/lone','NH3/strongest','CO2/polar','CO2/H','CO2/strongest','HBr/EN','HBr/EN','HBr/polar','HBr/H','HBr/strongest']),R.map(x=>x.stage));
  m=at(R,'HBr/EN');ok('slide 10 you do: "Electronegativity (pull on electrons)", Br 2.96, H 2.20, difference 0.76 (Pauling, shared data)',m.en&&m.en.label==='Electronegativity (pull on electrons)'&&m.en.Br===2.96&&m.en.H===2.20&&m.en.difference===0.76&&await page.evaluate(()=>(Deck.EN.Br-Deck.EN.H).toFixed(2)==='0.76'),m.en);
  ok('slide 10 you do answers: polar; H on Br, not N, O or F; dipole-dipole forces',at(R,'HBr/strongest').answers.polar==='yes'&&at(R,'HBr/strongest').answers.H==='no'&&at(R,'HBr/strongest').answers.strongest==='dipole-dipole forces');

  /* 6. heating (slide 11) */
  R=await run('s11','s11-sim');
  ok('slide 11 heating: stages CH4/solid, melt, liquid, boil, gas, H2O/boil, energy, H2O/gas',staged(R,['CH4/solid','CH4/melt','CH4/liquid','CH4/boil','CH4/gas','H2O/boil','energy','H2O/gas']));
  R.forEach(x=>ok(`slide 11 heating f${x.f} ${x.stage}: ${x.meta.bondsIntact} of ${x.meta.bondsTotal} covalent bonds intact, ${x.meta.molecules} molecules`,x.meta.molecules===(x.meta.substance==='CH4'?4:6)&&x.meta.bondsIntact===x.meta.bondsTotal&&x.meta.bondsTotal===(x.meta.substance==='CH4'?16:12),x.meta));
  const HT={'CH4/solid':'−182.5 °C (melting point)','CH4/melt':'−182.5 °C, melting','CH4/liquid':'liquid','CH4/boil':'−161.5 °C, boiling','CH4/gas':'−161.5 °C (boiling point)','H2O/boil':'100.0 °C, boiling','H2O/gas':'100.0 °C (boiling point)'};
  Object.entries(HT).forEach(([s,v])=>{m=at(R,s);ok(`slide 11 heating ${s}: "${v}"`,m.temperature===v,m.temperature)});
  ok('slide 11 heating: attractions drawn 4, 2, 2, 1, 0 for CH₄; 1 and 0 for water boiling and gas',['CH4/solid','CH4/melt','CH4/liquid','CH4/boil','CH4/gas','H2O/boil','H2O/gas'].map(s=>at(R,s).attractionsDrawn).join()==='4,2,2,1,0,1,0');
  m=at(R,'energy');ok('slide 11 heating energy: 40.7 kJ and about 928 kJ, "more than 20 times as much"',eq(m.energies,{boil:40.7,bonds:928})&&m.energyBars&&m.caption==='more than 20 times as much',m);
  ok('slide 11 heating energy (step 04b): the bars alone, no molecules or container under them; both back on the check frame',!m.moleculesShown&&!m.containerShown&&at(R,'H2O/gas').moleculesShown&&at(R,'H2O/boil').moleculesShown,m);
  for(const sub of ['CH4','H2O']){const S=at(R,sub+'/gas').spread;
    ok(`slide 11 heating ${sub}: the gas spreads over the container (${Math.round(S.gasBoxShare*100)}% of it)`,S.gasBoxShare>=.8,S);
    ok(`slide 11 heating ${sub} (brief D1): solid block ${Math.round(S.solidBlockShare*100)}% of the container (target 40% or less)`,S.solidBlockShare<=.4,S);
    ok(`slide 11 heating ${sub} (brief D1): area per molecule grows ${S.areaRatio} times (target 2.5 or more)`,S.areaRatio>=2.5,S)}
  shapes('slide 11 heating',R);await subject('s11','s11-sim','H2O/gas','steam: water molecules far apart, bonds intact');

  /* 7. iceLattice (slide 12) */
  R=await run('s12','s12-sim');
  m=at(R,'molecules');ok('slide 12 iceLattice: 13 molecules, 26 O–H bonds, 16 hydrogen bonds',m.molecules===13&&m.bondsOH===26&&m.hbonds===16,m);
  ok('slide 12 iceLattice: hydrogen bonds drawn from hbonds on',!at(R,'molecules').hbondsDrawn&&at(R,'hbonds').hbondsDrawn);
  m=at(R,'neighbors');ok('slide 12 iceLattice neighbors: 4 at 276 pm, "four neighbors, 276 pm away"',m.neighborsOfChosen===4&&m.distancePm===276&&m.label==='four neighbors, 276 pm away',m);
  m=at(R,'rings');ok('slide 12 iceLattice rings: down the axis, "open six-sided rings"',m.view==='down the axis'&&m.label==='open six-sided rings',m);
  m=at(R,'float');ok('slide 12 iceLattice float: 0.9167 and 0.99984 g/cm³, 100.0 → 109.1 cm³, 8.3% above',eq(m.densities,{ice:0.9167,water:0.99984})&&eq(m.volumes,{water:100.0,ice:109.1})&&m.aboveSurfacePct===8.3,m);
  shapes('slide 12 iceLattice',R);await subject('s12','s12-sim','float','the ice block and the two volume bars');

  /* 8. conductTester (slides 15, 16, 17) */
  const CTW={'NaCl-s':['solid NaCl','Na⁺ and Cl⁻','no',false],'NaCl-l':['molten NaCl, 801 °C','Na⁺ and Cl⁻','yes',true],'NaCl-aq':['salt water','Na⁺ and Cl⁻','yes',true],Cu:['copper','delocalized electrons','yes',true],
    sugar:['sugar water','none',null,false],water:['distilled water','very few ions',null,false],'KCl-l':['molten KCl','K⁺ and Cl⁻','yes',true],'CaCl2-s':['solid CaCl₂','Ca²⁺ and Cl⁻','no',false]};
  R=await run('s15','s15-sim');
  ok('slide 15 conductTester: tester, then solid and molten NaCl (predict, close, zoom), salt water, copper, sugar water, distilled water',
    eq([...new Set(R.map(x=>x.stage))],['tester','NaCl-s/predict','NaCl-s/close','NaCl-s/zoom','NaCl-l/predict','NaCl-l/close','NaCl-l/zoom','NaCl-aq/zoom','Cu/zoom','sugar/close','water/close']),[...new Set(R.map(x=>x.stage))]);
  ok('slide 15 conductTester tester: no sample, bulb dark; the "?" circle where the magnified view will be',at(R,'tester').sample===null&&!at(R,'tester').lit&&at(R,'tester').placeholder);
  ok('slide 15 conductTester (step 04b): the readout shows results only, never the question "Lights or stays dark?"',R.filter(x=>/predict$/.test(x.stage)).every(x=>x.meta.readout===null)&&at(R,'NaCl-s/close').readout==='The bulb stays dark.'&&at(R,'NaCl-l/close').readout==='The bulb lights.'&&at(R,'NaCl-l/zoom').readout==='Na⁺ and Cl⁻ free to move',R.map(x=>[x.stage,x.meta.readout]));
  const ct=(R,n,list)=>list.forEach(k=>{const [name,ch,free,lit]=CTW[k];const xs=R.filter(x=>x.stage.startsWith(k+'/')).map(x=>x.meta);
    ok(`slide ${n} conductTester ${k}: "${name}", ${ch}, free to move ${free}, ${lit?'lights':'stays dark'} once the switch closes`,xs.length&&xs.every(q=>q.name===name&&q.chargedParticles===ch&&q.freeToMove===free&&(q.switchClosed?q.lit===lit:!q.lit)),xs[xs.length-1])});
  ct(R,15,['NaCl-s','NaCl-l','NaCl-aq','Cu','sugar','water']);
  shapes('slide 15 conductTester',R);await subject('s15','s15-sim','NaCl-l/zoom','molten NaCl with its moving ions');
  R=await run('s16','s16-sim');ct(R,16,['KCl-l','CaCl2-s']);shapes('slide 16 conductTester',R);
  ok('slide 16 conductTester: KCl-l predict, close; CaCl₂ predict, close; the you-do answer frame back at KCl-l/zoom',staged(R,['KCl-l/predict','KCl-l/close','CaCl2-s/predict','CaCl2-s/close','KCl-l/zoom'])&&R[R.length-1].stage==='KCl-l/zoom');
  {const iy=R.findIndex(x=>x.stage==='tester'),ic=R.findIndex(x=>x.stage==='CaCl2-s/close');
   ok('slide 16 conductTester you do (step 04b): the tester reset (no sample, switch open, no result) after the we-do result, until the answer',iy>ic&&ic>=0&&R[iy].meta.sample===null&&!R[iy].meta.lit&&!R[iy].meta.switchClosed&&R[iy].meta.readout===null&&R.slice(iy,-1).every(x=>x.stage==='tester'),R.map(x=>x.stage))}
  ok('slide 16 conductTester (step 04b): while the class predicts, the "?" circle holds the magnified view\'s place; no readout',R.filter(x=>/predict$/.test(x.stage)).every(x=>x.meta.placeholder&&x.meta.readout===null));
  R=await run('s17','s17-sim');
  const DSW={NaCl:['ionic','yes'],sucrose:['molecular','yes'],CaCO3:['ionic','barely'],I2:['molecular','slightly'],SiO2:['covalent network','no'],Cu:['metallic','no']};
  Object.entries(DSW).forEach(([k,[ty,ds]])=>{m=at(R,'dis/'+k);ok(`slide 17 dissolve ${k}: ${ty}, dissolves ${ds}`,m&&m.sample===k&&m.type===ty&&m.dissolves===ds,m)});
  ok('slide 17 dissolve NaCl: "ions spread out: an electrolyte"; sucrose: "whole molecules spread out"',at(R,'dis/NaCl').label==='ions spread out: an electrolyte'&&at(R,'dis/sucrose').label==='whole molecules spread out');
  shapes('slide 17 dissolve',R);await subject('s17','s17-sim','dis/CaCO3','calcium carbonate, ionic, barely dissolves');

  /* 9. hammerBlow (slide 18) */
  R=await run('s18','s18-sim');
  m=at(R,'before');ok('slide 18 hammerBlow before: no shift, no like-charge pairs',m.copper.offsetSpacings===0&&m.nacl.offsetSpacings===0&&m.nacl.likeChargePairs===0&&!m.nacl.split,m);
  ok('slide 18 hammerBlow blow: the hammer strikes',at(R,'blow').hammer===true);
  m=at(R,'shift');ok('slide 18 hammerBlow (step 04b): the hammer swings in from the left at the top layer, and that layer moves right, the way the blow points',at(R,'blow').hammerFrom==='left'&&at(R,'blow').hammerMoves==='right'&&at(R,'blow').struck==='top layer'&&m.topLayerMoves===m.hammerMoves,m);
  m=at(R,'shift');ok('slide 18 hammerBlow shift: one spacing; like charges side by side in NaCl',m.copper.offsetSpacings===1&&m.nacl.offsetSpacings===1&&m.nacl.likeChargePairs>0&&!m.nacl.split,m);
  m=at(R,'result');ok('slide 18 hammerBlow result: copper one piece "malleable"; NaCl split "brittle"',m.copper.onePiece&&m.copper.label==='malleable'&&m.nacl.split&&m.nacl.label==='brittle',m);
  ok('slide 18 hammerBlow: Na⁺ 102, Cl⁻ 181, Cu 128 pm; 282 pm',eq(m.radii,{Na:102,Cl:181,Cu:128})&&m.spacingPm===282);
  shapes('slide 18 hammerBlow',R);await subject('s18','s18-sim','result','the split salt block beside the bent copper');

  /* 10. networkVsMolecules (slide 19) */
  R=await run('s19','s19-sim');
  m=at(R,'co2');ok('slide 19 co2: six CO₂ molecules, dispersion lines, −78.5 °C',m.co2.molecules===6&&m.co2.attractionsDrawn>0&&m.thermometer==='−78.5 °C',m);
  m=at(R,'sublime');ok('slide 19 sublime: whole molecules fly off, no lines, "sublimes at −78.5 °C: no liquid"',m.co2.flown&&m.co2.intactAfterSublime&&m.co2.attractionsDrawn===0&&m.co2.sublimesAt===-78.5&&m.label==='sublimes at −78.5 °C: no liquid',m);
  m=at(R,'quartz');ok('slide 19 quartz: one network, no molecules, every Si bonded to four O',m.sio2.network&&m.sio2.molecules===0&&m.sio2.siFourO&&m.label==='quartz, SiO₂: one network, no molecules',m.sio2);
  m=at(R,'heat');ok('slide 19 heat: above 1000 °C, "to melt it, covalent bonds must break: near 1700 °C"',m.thermometer==='above 1000 °C'&&m.sio2.meltsNear===1700&&m.label==='to melt it, covalent bonds must break: near 1700 °C',m);
  m=at(R,'diamond');ok('slide 19 diamond: a carbon network, "diamond: the hardest natural substance"',m.diamond.element==='C'&&m.diamond.network&&m.label==='diamond: the hardest natural substance',m);
  shapes('slide 19 networkVsMolecules',R);await subject('s19','s19-sim','quartz','the quartz network');

  /* text facts */
  const T=await page.evaluate(()=>{const txt=e=>{const c=e.cloneNode(true);c.querySelectorAll('br').forEach(x=>x.replaceWith(' '));return c.textContent.replace(/\s+/g,' ').trim()}; /* a line break reads as a space */
    const t=id=>{const e=document.querySelector('[id="'+id+'"],[data-b="'+id+'"]');return e?txt(e):null};
    const rowText=sel=>[...document.querySelectorAll(sel)].map(r=>[...r.cells].map(c=>txt(c)));
    return {warm:[1,2,3].map(i=>t('s14-a'+i)),you16:[t('s16-a1'),t('s16-a2')],kinds:rowText('#s20-tbl tbody tr'),rate:[...document.querySelectorAll('#s26 .rev')].map(e=>e.textContent),
      pred:[1,2,3].map(i=>{const c=document.getElementById('s25-p'+i);return {ans:c.querySelector('.opt').textContent.replace(/\s+/g,' ').trim(),reason:c.querySelector('.reason').textContent}}),
      predQ:[1,2,3].map(i=>document.querySelector('#s04-q'+i+' .q').textContent),pred25Q:[1,2,3].map(i=>document.querySelector('#s25-p'+i+' .q').textContent),
      words:[...document.querySelectorAll('#s05 .wcard .t')].map(e=>e.textContent.replace(/\s+/g,' ').trim()),
      caps:Object.fromEntries(['s03','s06','s15','s17','s18','s19'].map(s=>[s,(document.getElementById(s+'-cap')||{}).textContent||null])),
      checks:[...document.querySelectorAll('.slide')].filter(s=>s.querySelector('.card.check[id$="-check"],.checkrow')).map(s=>+s.id.slice(1)),
      fbs:[...document.querySelectorAll('.card.check[id$="-check"],.checkrow')].map(c=>({id:c.id,n:c.querySelectorAll('.opt[data-fb]').length,right:[...c.querySelectorAll('.opt')].filter(o=>o.dataset.ok==='1').map(o=>o.id.slice(-1).toUpperCase()),ans:c.querySelector('.ans').textContent.trim().slice(0,2)})),
      periods:Deck.slides.map(S=>+S.period),n:Deck.slides.length,ellipsis:document.body.innerText.includes('…')||[...document.querySelectorAll('.notes')].some(n=>n.textContent.includes('…'))}});
  ok('slide 14 warm-up answers: dispersion forces; N, O or F; each H₂O molecule, with its two O–H bonds',eq(T.warm,['dispersion forces','N, O or F','each H2O molecule, with its two O–H bonds']),T.warm);
  ok('slide 16 you-do answers: 2 samples (KCl in water, molten KCl); K⁺ and Cl⁻ ions that can move',eq(T.you16,['2 samples: KCl in water and molten KCl.','K+ and Cl− ions that can move.']),T.you16);
  ok('slide 20 the four rows of the Review table',eq(T.kinds,[['Molecular, I2','attractions between molecules; low melting point','no','soft'],['Ionic, NaCl','ionic bonds; high melting point','when molten or dissolved','hard, brittle'],
    ['Metallic, Cu','metallic bonds; melting point usually high','yes, solid and liquid','malleable'],['Covalent network, SiO2','covalent bonds; very high melting point','no (except graphite)','very hard (except graphite)']]),T.kinds);
  ok('slide 26 review lines: slides 6 and 7; 8 to 10; 11 and 12; 15 to 17; 18 and 19',eq(T.rate,['Review: slides 6 and 7','Review: slides 8 to 10','Review: slides 11 and 12','Review: slides 15 to 17','Review: slides 18 and 19']),T.rate);
  ok('slide 25 the three answers: A H₂O molecules; B does not conduct; B an attraction between molecules, with their reasons',eq(T.pred.map(p=>p.ans),['AH2O molecules','Bdoes not conduct','Ban attraction between molecules'])&&
    eq(T.pred.map(p=>p.reason),['Boiling separates whole molecules. Each keeps its O–H bonds.','Its ions are locked in the crystal. Molten or dissolved salt conducts.','It pulls an H on one molecule to a lone pair on the next. About 5 to 10% of a covalent bond.']),T.pred);
  ok('slide 25 repeats the three questions of slide 4',eq(T.predQ,T.pred25Q),T.predQ);
  ok('slide 5 the eight terms with their Spanish cognates (reading glossary)',eq(T.words,['intermolecular force (fuerza intermolecular)','dispersion forces (fuerzas de dispersión)','dipole-dipole forces (fuerzas dipolo-dipolo)','hydrogen bonding (enlace de hidrógeno)',
    'electrolyte (electrolito)','malleable (maleable)','brittle (frágil)','covalent network solid (sólido de red covalente)']),T.words);
  ok('caption "Atom colors show the element, not the charge." on slides 3, 6, 15, 17, 18, 19',Object.values(T.caps).every(c=>c==='Atom colors show the element, not the charge.'),T.caps);
  ok('ten checks on slides 6, 7, 8, 9, 11, 12, 15, 17, 18, 19 (registry: '+REG.checks+')',T.checks.join()==='6,7,8,9,11,12,15,17,18,19'&&T.checks.length===REG.checks,T.checks);
  ok('every check: three options with a feedback line each, one right option (A), the reason starts with "A."',T.fbs.length===10&&T.fbs.every(c=>c.n===3&&eq(c.right,['A'])&&c.ans==='A.'),T.fbs);
  const p1=T.periods.map((p,i)=>p===1?i+1:0).filter(Boolean),p2=T.periods.map((p,i)=>p===2?i+1:0).filter(Boolean);
  ok(`periods: slides 1 to ${p1[p1.length-1]} and ${p2[0]} to ${p2[p2.length-1]} (registry ${JSON.stringify(REG.periods)})`,T.n===27&&eq([[p1[0],p1[p1.length-1]],[p2[0],p2[p2.length-1]]],REG.periods)&&p1.length+p2.length===27,{p1,p2});
  ok('no ellipsis character in slides or notes',!T.ellipsis);
  ok('no console errors',!errors.length,errors);
  L.save('chem45-deck.json',res);res.forEach(r=>console.log(`  ${r.pass?'PASS':'FAIL'}  ${r.n}${r.pass?'':'  '+r.i}`));
  const n=res.filter(r=>!r.pass).length;console.log(`chem45 (deck): ${n?'FAIL ('+n+')':'PASS'} ${res.length} checks`);await browser.close();process.exitCode=n?1:0;
})();
