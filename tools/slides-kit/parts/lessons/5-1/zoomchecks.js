// Lesson 5.1: the explicit zoom checks of brief 02 (V3), run by audits/zoom.js after its two generic checks (every zoomed check shows its
// options; every prompt on a routine slide is a unit). rec: one row per zoomed state {s, f, i, n, kind, label, id, mode, fill, …};
// has(s,f,pred) and cnt(s,f,pred) look rows up. Frame counts are those of gen_slides.py's TIMES.
const NF={2:6,6:8,7:11,8:9,9:10,10:10,11:11,12:8,13:9,16:8,17:9,18:8,19:9,20:12,21:5};
const HOST={2:'s02-sim',6:'s06-sim',7:'s07-sim',8:'s08-sim',9:'s09-sim',10:'s10-sim',11:'s11-sim',12:'s12-sim',13:'s13-sim',16:'s16-sim',17:'s17-sim',18:'s18-sim',19:'s19-sim',21:'s21-sim'};
const fr=s=>[...Array(NF[s]).keys()];
module.exports=(rec,{has,cnt})=>[
  ['every animation host is a unit with fill 0.6 or more on every frame that shows it',Object.entries(HOST).every(([s,id])=>fr(+s).every(f=>has(+s,f,r=>r.kind==='animation'&&r.id===id&&r.fill>=.6)))
    &&[0,1,2,3,4,5,6,7,8].every(f=>has(20,f,r=>r.kind==='animation'&&r.id==='s20-sim'&&r.fill>=.6))&&[9,10,11].every(f=>has(20,f,r=>r.kind==='animation'&&r.id==='s20-ac'&&r.fill>=.6))],
  ['every animation unit and sub-unit fills 0.6 or more',rec.filter(r=>r.kind==='animation'||r.kind==='part').every(r=>r.fill>=.6)],
  ['slide 5: each of the eight word cards is a unit',cnt(5,1,r=>r.kind==='wcard')===8&&cnt(5,2,r=>r.kind==='wcard')===8],
  ['slide 5: the color legend is a unit',has(5,2,r=>r.kind==='legend')],
  ['slide 14: each column of the summary table is a unit (the runtime zooms this table by column)',cnt(14,7,r=>r.kind==='column')===3],
  ['slide 15: each warm-up answer row is a unit (3)',cnt(15,4,r=>r.kind==='row')===3],
  ['slide 20: each you-do answer row is a unit (3)',cnt(20,11,r=>r.kind==='row')===3],
  ['slides 16, 17, 20, 21: each station and the bridge of moleMap are units',[[16,4],[17,3],[20,3],[20,6],[21,3]].every(([s,f])=>['moles','particles','the bridge'].every(l=>has(s,f,r=>r.kind==='part'&&r.label===l)))],
  ['slides 16, 17, 20: the factor, the result and the check line of moleMap are units',[[16,4],[17,3],[20,3],[20,6]].every(([s,f])=>['the factor','the result','the check'].every(l=>has(s,f,r=>r.kind==='part'&&r.label===l)))],
  ['slide 12: each history card is a unit on its frame',['1811 · Amedeo Avogadro','1865 · Josef Loschmidt','1890s · Wilhelm Ostwald','1909 · Jean Perrin','1971 · an SI base unit'].every((t,f)=>has(12,f,r=>r.kind==='part'&&r.label===t))&&has(12,6,r=>r.label==='2018 and 2019')&&has(12,0,r=>r.label==='the time ruler')],
  ['slide 9: the exponent ladder (from the thousand on) and the spoon are units',[2,3,4,5,6,7,8,9].every(f=>has(9,f,r=>r.label==='the ladder of exponents'))&&[6,7,8,9].every(f=>has(9,f,r=>r.label==='the spoon'))],
  ['the cards with a chip row are units (slides 6, 7, 10, 26)',has(6,3,r=>r.id==='s06-c2')&&has(7,0,r=>r.id==='s07-c0')&&has(10,3,r=>r.id==='s10-c2')&&has(26,0,r=>r.id==='s26-p1')],
  ['every rule card is a unit on its frame',[[6,5],[7,8],[8,6],[9,7],[10,7],[12,7],[13,6],[16,5],[17,6],[18,5],[19,6],[21,4]].every(([s,f])=>has(s,f,r=>r.kind==='rule'))&&cnt(11,8,r=>r.kind==='p')===3],
  ['every prompt of the routine slides is a unit (slides 4, 22 to 27)',[[4,0],[22,0],[23,0],[24,0],[25,0],[26,3],[27,0]].every(([s,f])=>s===27?has(s,f,r=>r.kind==='scale'):has(s,f,r=>r.kind==='prompt'))],
  ['the caption under the picture is a unit (slides 10 and 19)',has(10,6,r=>r.kind==='caption')&&has(19,0,r=>r.kind==='caption')],
  ['every check card with its options (11)',new Set(rec.filter(r=>r.kind==='check').map(r=>r.id)).size>=11]];
