// Chemistry checks on the Lesson 4.2 animations as placed in the deck (meta() of each placed instance), plus the deck's text facts.
process.env.DECK=process.env.DECK||'/home/user/texaschemistry/unit4/slides-4-2.html';
const L=require('./lib');
(async()=>{
  const {browser,page,errors}=await L.open({});const res=[];const ok=(n,p,i)=>res.push({n,pass:!!p,i:i===undefined?'':JSON.stringify(i)});
  const meta=(sid,sim,stage)=>page.evaluate(([sid,sim,stage])=>{const s=Deck.slides.findIndex(S=>S.id===sid),f=Deck.slides[s].frames.findIndex(fr=>fr.stage.some(x=>x.sim===sim&&x.s===stage));
    if(f<0)return {missing:stage};Deck.go(s,f);return Deck.sims[sim].meta()},[sid,sim,stage]);
  let m=await meta('s02','s02-sim','focus0');ok('slide 2 labelRead: toothpaste, sodium fluoride',m.name==='sodium fluoride',m);
  m=await meta('s02','s02-sim','focus2');ok('slide 2 labelRead: lawn food, ammonium sulfate',m.name==='ammonium sulfate',m);
  m=await meta('s06','s06-sim','g15');ok('slide 6 ionTable: group charges',JSON.stringify(m.badges)===JSON.stringify({'group 1':'1+','group 2':'2+','group 13':'3+','group 17':'1−','group 16':'2−','group 15':'3−'}),m.badges);
  ok('slide 6 ionTable: -ide names and no squeezed symbols',m.names.length===7&&m.omittedSymbols===0,{names:m.names,cell:m.cellPx});
  m=await meta('s07','s07-sim','tm');ok('slide 7 ionTable: the four transition metals',m.tm.join('|')==='Fe²⁺  Fe³⁺|Cu⁺  Cu²⁺|Ag⁺|Zn²⁺',m.tm);
  m=await meta('s08','s08-sim','Ca-Cl/name');ok('slide 8 chargeBlocks: CaCl₂, calcium chloride, balanced',m.formula==='CaCl₂'&&m.name==='calcium chloride'&&m.balanced,m);
  m=await meta('s08','s08-sim','Ca-Cl/ions');ok('slide 8 chargeBlocks: one Ca²⁺ and one Cl⁻ do not balance',!m.balanced,m);
  m=await meta('s08','s08-sim','Al-O/formula');ok('slide 8 chargeBlocks: Al₂O₃ with 6+ and 6−',m.formula==='Al₂O₃'&&m.totals.join()==='6,6',m);
  m=await meta('s09','s09-sim','Mg-O/reduce');ok('slide 9 chargeBlocks: Mg₂O₂ reduces to MgO',m.formula==='MgO'&&m.tiles.join()==='1,1',m);
  m=await meta('s09','s09-sim','K-S/formula');ok('slide 9: K₂S',m.formula==='K₂S',m);
  m=await meta('s09','s09-sim','Ca-N/formula');ok('slide 9: Ca₃N₂',m.formula==='Ca₃N₂',m);
  m=await meta('s10','s10-sim','Al-O/check');ok('slide 10 crisscross Al₂O₃ check',m.check&&m.check.join('|')==='2 × 3+ = 6+|3 × 2− = 6−',m);
  m=await meta('s10','s10-sim','Mg-O/reduce');ok('slide 10 crisscross Mg₂O₂ → MgO',m.crossed==='Mg₂O₂'&&m.reduced==='MgO',m);
  m=await meta('s11','s11-sim','K2S/join');ok('slide 11 nameBuilder: potassium sulfide',m.name==='potassium sulfide',m);
  m=await meta('s11','s11-sim','CaBr2/join');ok('slide 11 answer frame: calcium bromide',m.name==='calcium bromide',m);
  for(const [c,n] of [['FeCl3','iron(III) chloride'],['FeCl2','iron(II) chloride'],['AgCl','silver chloride'],['ZnO','zinc oxide']]){m=await meta('s12','s12-nb',c+'/join');ok(`slide 12 nameBuilder ${c}: ${n}`,m.name===n,m)}
  m=await meta('s12','s12-sd','CuO/name');ok('slide 12 stockDetective CuO: copper(II) oxide',m.name==='copper(II) oxide'&&m.metalCharge===2,m);
  m=await meta('s12','s12-sd','Cu2O/name');ok('slide 12 stockDetective Cu₂O: copper(I) oxide',m.name==='copper(I) oxide'&&m.metalCharge===1,m);
  for(const [k,f] of [['NH4','NH₄⁺'],['OH','OH⁻'],['NO3','NO₃⁻'],['CO3','CO₃²⁻'],['SO4','SO₄²⁻'],['PO4','PO₄³⁻']]){m=await meta('s15','s15-sim',k);ok(`slide 15 polyIons ${k}: ${f}`,m.formula===f,m.formula)}
  m=await meta('s16','s16-pb','two');ok('slide 16 parenBus: Ca(OH)₂',m.formula==='Ca(OH)₂'&&m.parentheses,m);
  m=await meta('s16','s16-cb','NH4-SO4/formula');ok('slide 16 chargeBlocks: (NH₄)₂SO₄',m.formula==='(NH₄)₂SO₄',m);
  m=await meta('s16','s16-cb','Na-NO3/formula');ok('slide 16 chargeBlocks: NaNO₃, no parentheses',m.formula==='NaNO₃',m);
  m=await meta('s17','s17-cb','Al-SO4/formula');ok('slide 17 chargeBlocks: Al₂(SO₄)₃',m.formula==='Al₂(SO₄)₃'&&m.totals.join()==='6,6',m);
  m=await meta('s17','s17-sd','Cu2S/name');ok('slide 17 stockDetective: Cu₂S is copper(I) sulfide',m.name==='copper(I) sulfide'&&m.metalCharge===1,m);
  // text facts on the slides
  const txt=await page.evaluate(()=>{const t=id=>(document.querySelector('[id="'+id+'"],[data-b="'+id+'"]')||{}).textContent;return {
    a18:[1,2,3,4,5,6].map(i=>t('s18-a'+i)),a19:[1,2,3,4,5,6].map(i=>t('s19-a'+i)),mem:document.querySelector('#s15-c2 .mem').textContent,
    s9:[t('s09-a1'),t('s09-a2')],a13:[1,2,3,4].map(i=>t('s13-a'+i)),cap:t('s15-cap'),checks:[...document.querySelectorAll('.slide')].filter(s=>s.querySelector('.card.check[id$="-check"],.checkrow')).map(s=>+s.id.slice(1))}});
  ok('slide 18 answers',txt.a18.join('|')==='NaF|CaCO3|(NH4)2SO4|magnesium bromide|iron(II) oxide|zinc hydroxide',txt.a18);
  ok('slide 19 fixes',txt.a19.join('|')==='Na2SO4|MgO|Ca(OH)2|copper(I) oxide|iron(III) chloride|sodium nitrate',txt.a19);
  ok('slide 9 try two: K₂S and Ca₃N₂',txt.s9.join('|')==='K2S|Ca3N2',txt.s9);
  ok('slide 13 retrieval answers',txt.a13.join('|')==='aluminum chloride|potassium oxide|CaS|iron(II) oxide',txt.a13);
  ok('slide 15 memory card sentence and CPK caption',txt.mem.trim()==='Nick the Camel ate Supper in Phoenix.'&&txt.cap==='Atom colors show the element, not the charge.',txt);
  ok('nine checks on slides 6, 7, 8, 10, 11, 12, 15, 16, 17',txt.checks.join()==='6,7,8,10,11,12,15,16,17',txt.checks);
  ok('no console errors',!errors.length,errors);
  L.save('chem42-deck.json',res);res.forEach(r=>console.log(`  ${r.pass?'PASS':'FAIL'}  ${r.n}${r.pass?'':'  '+r.i}`));
  const n=res.filter(r=>!r.pass).length;console.log(`chem42 (deck): ${n?'FAIL ('+n+')':'PASS'} ${res.length} checks`);await browser.close();process.exitCode=n?1:0;
})();
