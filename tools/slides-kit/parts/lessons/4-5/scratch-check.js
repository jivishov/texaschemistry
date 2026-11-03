// Lesson 4.5, period-1 animations on the scratch deck (workshop step 02): drives every stage of every instance with Deck.go and
// asserts the meta() values of brief 02 against lessons/4-5.md. A lesson script, not an audit; step 04 turns it into chem.js.
//   DECK=<scratch deck> OUT=<folder> node parts/lessons/4-5/scratch-check.js
const L=require('../../../audits/lib');
(async()=>{
  const {browser,page,errors}=await L.open({});const res=[];const ok=(n,p,i)=>res.push({n,pass:!!p,i:i===undefined?'':JSON.stringify(i)});
  /* every frame of a scratch slide: {stage, meta} of its animation */
  const run=sid=>page.evaluate(sid=>{const s=Deck.slides.findIndex(S=>S.id===sid),S=Deck.slides[s],out=[];
    S.frames.forEach((fr,f)=>{Deck.go(s,f);const x=S.sims[0];out.push({f,stage:x.get(),meta:x.meta()})});return out},sid);
  const at=(rows,stage)=>{const r=rows.filter(x=>x.stage===stage);return r.length?r[r.length-1].meta:null};
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);

  /* 1. brickBag: 3 models, every brick snapped at every stage */
  let R=await run('x-bb');
  ok('brickBag: four stages driven (models, shake, pour, words)',eq(R.map(x=>x.stage),['models','shake','pour','words']),R.map(x=>x.stage));
  R.forEach(x=>ok(`brickBag ${x.stage}: 3 models, ${x.meta.bricks} bricks, all snapped`,x.meta.models===3&&x.meta.bricks===11&&x.meta.snapped===x.meta.bricks,x.meta));
  ok('brickBag: the counter reads "Bricks snapped: 11 of 11"',R.every(x=>x.meta.counter==='Bricks snapped: 11 of 11'),R[0].meta.counter);
  ok('brickBag words: the two labels',eq(at(R,'words').labels,['a snap between bricks = a bond within','models side by side = an attraction between']),at(R,'words').labels);
  ok('brickBag pour: the models are on the table, out of the bag',at(R,'pour').onTable&&!at(R,'pour').inBag);

  /* 2. meltScale: the three melting points; after melt the snow's molecules are whole and salt and sand did not move */
  R=await run('x-ms');let m=at(R,'melt');
  ok('meltScale melt: values snow 0.0, salt 801, sand near 1700',eq(m.values,{snow:0.0,salt:801,sand:'near 1700'}),m.values);
  ok('meltScale melt: snow molecules intact, salt and sand not moved',m.snowMoleculesIntact===true&&m.snowMoved===true&&m.saltMoved===false&&m.sandMoved===false,m);
  m=at(R,'numbers');ok('meltScale numbers: label line "Melting point" and chips "snow 0.0 °C", "salt 801 °C", "sand near 1700 °C"',m.label==='Melting point'&&eq(m.chips,['snow 0.0 °C','salt 801 °C','sand near 1700 °C']),m);
  ok('meltScale three: no chips before the numbers stage',at(R,'three').chips.length===0);
  ok('meltScale: scale −200 to 1800 °C',eq(m.scale,[-200,1800]));

  /* 3. threeSolids */
  R=await run('x-ts');
  m=at(R,'chlorine');ok('threeSolids chlorine: molecules drawn, one stick within each, no dashed line yet',m.molecules>=4&&m.sticksWithin===m.molecules&&m.dashedBetween===0,m);
  m=at(R,'within');ok('threeSolids within: the sticks glow, label "bond within"',m.withinGlow&&m.labels.includes('bond within'),m);
  m=at(R,'between');ok('threeSolids between: dashed lines between molecules, label "attraction between (much weaker)"',m.dashedBetween>0&&m.labels.includes('attraction between (much weaker)'),m);
  m=at(R,'salt');ok('threeSolids salt: NaCl radii 102 and 181 pm, spacing 282 pm, label',eq(m.naclRadii,[102,181])&&m.naclSpacing===282&&m.saltIons>=12&&m.labels.includes('ionic bonds through the whole crystal, no molecules'),m);
  m=at(R,'copper');ok('threeSolids copper: delocalized electrons, three panels, label',m.copper==='delocalized electrons'&&m.panels===3&&m.labels.includes('metallic bonds through the whole metal'),m);
  ok('threeSolids: sticks within equal molecules at every stage',R.every(x=>x.meta.sticksWithin===x.meta.molecules),R.map(x=>[x.meta.molecules,x.meta.sticksWithin]));

  /* 4. attractions: three instances, one per family */
  R=await run('x-ad');
  ['flicker','neighbor','attract'].forEach(s=>{m=at(R,s);ok(`attractions ${s}: nonpolar, δ labels only for an instant`,m.family==='dispersion'&&m.polar===false&&m.deltaLabels==='instant',m)});
  ok('attractions cloud: no δ labels yet',at(R,'cloud').deltaLabels===null);
  ok('attractions neighbor: the neighbor shifts the same way',at(R,'neighbor').neighborShift===true);
  ok('attractions attract: the dashed line and the label "dispersion forces"',at(R,'attract').line&&at(R,'attract').label==='dispersion forces');
  R=await run('x-aq');
  m=at(R,'F2');ok('attractions F2: no δ labels, dashed gray only',m.family==='dipole'&&m.F2&&m.F2.dplus===null&&m.F2.dminus===null&&m.F2.line==='dashed gray'&&m.HCl===null,m);
  m=at(R,'HCl');ok('attractions HCl: δ+ on H, δ− on Cl',eq(m.HCl,{dplus:'H',dminus:'Cl'}),m.HCl);
  m=at(R,'turn');ok('attractions turn: head to tail',m.headToTail===true);
  m=at(R,'face');ok('attractions face: δ+ to δ− line, label "dipole-dipole forces"',m.line==='δ+ to δ−'&&m.label==='dipole-dipole forces',m);
  m=at(R,'compare');ok('attractions compare: electrons F2 18, HCl 18; boiling points F2 −188.1, HCl −85.1',eq(m.electrons,{F2:18,HCl:18})&&eq(m.bp,{F2:-188.1,HCl:-85.1})&&eq(m.HCl,{dplus:'H',dminus:'Cl'}),m);
  R=await run('x-ah');
  m=at(R,'water');ok('attractions water: two water molecules, no hydrogen bond drawn yet',m.family==='hydrogen'&&m.hbond===false,m);
  m=at(R,'hbond');ok('attractions hbond: donor H on O, acceptor lone pair on O; drawn longer than the O–H bond',eq(m.water,{donor:'H on O',acceptor:'lone pair on O'})&&m.hbond&&m.hbondLonger&&m.label==='hydrogen bond: about 5 to 10% of a covalent bond',m);
  m=at(R,'ammonia');ok('attractions ammonia: donor H on N, acceptor lone pair on N',eq(m.ammonia,{donor:'H on N',acceptor:'lone pair on N'}),m);
  m=at(R,'methane');ok('attractions methane: no hydrogen bond, label "H on C: no hydrogen bond"',m.methane==='none'&&m.label==='H on C: no hydrogen bond',m);
  m=at(R,'four');ok('attractions four: up to four hydrogen bonds, four neighbors',m.waterMax===4&&m.hbonds===4&&m.neighbors===4,m);

  /* 5. bpPlot: points visible at each stage, values and strongest attraction */
  R=await run('x-bp');
  const V={F2:['F₂',18,-188.1,'dispersion forces'],Cl2:['Cl₂',34,-34.0,'dispersion forces'],Br2:['Br₂',70,58.8,'dispersion forces'],I2:['I₂',106,184.4,'dispersion forces'],
    CH4:['CH₄',10,-161.5,'dispersion forces'],NH3:['NH₃',10,-33.3,'hydrogen bonding'],H2O:['H₂O',10,100.0,'hydrogen bonding'],HCl:['HCl',18,-85.1,'dipole-dipole forces']};
  const want={axes:[],F2:['F2'],Cl2:['F2','Cl2'],Br2:['F2','Cl2','Br2'],I2:['F2','Cl2','Br2','I2'],trend:['F2','Cl2','Br2','I2'],trio:['CH4','NH3','H2O'],reveal:['CH4','NH3','H2O'],HCl:['F2','HCl']};
  Object.entries(want).forEach(([s,ks])=>{m=at(R,s);const bright=m.points.filter(q=>!q.faint),got=bright.map(q=>q.f);
    ok(`bpPlot ${s}: points ${ks.map(k=>V[k][0]).join(', ')||'none'}`,eq(got,ks.map(k=>V[k][0])),got);
    ok(`bpPlot ${s}: each point's electrons, boiling point and strongest attraction`,bright.every(q=>{const k=Object.keys(V).find(k=>V[k][0]===q.f);return k&&q.e===V[k][1]&&q.bp===V[k][2]&&q.force===V[k][3]}),bright)});
  ok('bpPlot trio: the 10-electron points have no labels yet; reveal adds them',at(R,'trio').points.filter(q=>!q.faint).every(q=>!q.labelled)&&at(R,'reveal').points.filter(q=>!q.faint).every(q=>q.labelled));
  ok('bpPlot trio: the halogens stay faint behind',at(R,'trio').points.filter(q=>['F₂','Cl₂','Br₂','I₂'].includes(q.f)).every(q=>q.faint));
  ok('bpPlot trend: the dashed trend line only at trend',R.filter(x=>x.meta.trend).map(x=>x.stage).join()==='trend');
  ok('bpPlot: no "all eight" stage',!R.some(x=>/all/i.test(x.stage)));
  ok('bpPlot: axes 0 to 110 electrons, −200 to 200 °C',eq(at(R,'axes').xRange,[0,110])&&eq(at(R,'axes').yRange,[-200,200])&&at(R,'axes').xAxis==='Electrons per molecule');

  /* 6. forceDecider: the answers of triplet 1 */
  R=await run('x-fd');
  const FD={'NH3/polar':['NH3',{polar:'yes',H:null,lone:null,strongest:null}],'NH3/H':['NH3',{polar:'yes',H:'yes',lone:null,strongest:null}],'NH3/lone':['NH3',{polar:'yes',H:'yes',lone:'yes',strongest:null}],
    'NH3/strongest':['NH3',{polar:'yes',H:'yes',lone:'yes',strongest:'hydrogen bonding'}],'CO2/polar':['CO2',{polar:'no',H:null,lone:null,strongest:null}],
    'CO2/H':['CO2',{polar:'no',H:'no',lone:'not needed',strongest:null}],'CO2/strongest':['CO2',{polar:'no',H:'no',lone:'not needed',strongest:'dispersion forces'}],
    'HBr/EN':['HBr',{polar:null,H:null,lone:null,strongest:null}],'HBr/polar':['HBr',{polar:'yes',H:null,lone:null,strongest:null}],
    'HBr/H':['HBr',{polar:'yes',H:'no',lone:'not needed',strongest:null}],'HBr/strongest':['HBr',{polar:'yes',H:'no',lone:'not needed',strongest:'dipole-dipole forces'}]};
  Object.entries(FD).forEach(([s,[mol,ans]])=>{m=at(R,s);ok(`forceDecider ${s}: ${mol}, answers ${Object.values(ans).filter(Boolean).join(' · ')||'none yet'}`,m&&m.molecule===mol&&eq(m.answers,ans),m)});
  m=at(R,'HBr/EN');ok('forceDecider HBr/EN: "Electronegativity (pull on electrons)", Br 2.96, H 2.20, difference 0.76',m.en&&m.en.label==='Electronegativity (pull on electrons)'&&m.en.Br===2.96&&m.en.H===2.20&&m.en.difference===0.76,m.en);
  ok('forceDecider: box titles',eq(at(R,'NH3/polar').boxes,['Polar?','H on N, O or F?','Lone pair on N, O or F?','Strongest attraction']));
  /* the difference shown is the shared Pauling data */
  ok('forceDecider: 2.96 − 2.20 = 0.76 from the shared electronegativity table',await page.evaluate(()=>Deck.EN.Br===2.96&&Deck.EN.H===2.20&&(Deck.EN.Br-Deck.EN.H).toFixed(2)==='0.76'));

  ok('no console errors',!errors.length,errors);
  L.save('scratch-check.json',res);res.forEach(r=>console.log(`  ${r.pass?'PASS':'FAIL'}  ${r.n}${r.pass?'':'  '+r.i}`));
  const n=res.filter(r=>!r.pass).length;console.log(`scratch-check 4.5: ${n?'FAIL ('+n+')':'PASS'} ${res.length} checks`);await browser.close();process.exitCode=n?1:0;
})();
