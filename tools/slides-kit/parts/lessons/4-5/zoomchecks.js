// Lesson 4.5: the deck's own zoom checks (brief 04, V3). zoom.js runs the generic checks for every deck (every zoomed check shows its
// options; every prompt on a routine slide is a unit, slides 21 to 26 here), so they are not repeated.
// rec: one row per zoomed state {s, f, i, n, kind, label, id, mode, fill, …}; has(s,f,pred) and cnt(s,f,pred) look rows up.
const R=(a,b)=>Array.from({length:b-a+1},(_,k)=>a+k);
// every animation host: a unit filling 60% or more on every frame that shows it (slide, the host's animation, frames)
const HOSTS=[[2,'brickBag',R(0,4)],[3,'meltScale',R(0,8)],[6,'threeSolids',R(0,8)],[7,'attractions',R(0,4)],[7,'bpPlot',R(5,13)],[8,'attractions',R(0,8)],
  [9,'bpPlot',R(0,2)],[9,'attractions',R(3,10)],[10,'forceDecider',R(0,12)],[11,'heating',R(0,10)],[12,'iceLattice',R(0,9)],[15,'conductTester',R(0,13)],
  [16,'conductTester',R(0,14)],[17,'conductTester',R(2,10)],[18,'hammerBlow',R(0,8)],[19,'networkVsMolecules',R(0,8)]];
// the rule card of each concept slide, on the frame that shows it (slides 15 and 18: the band's rule lines, one unit each)
const RULES=[[6,6],[7,11],[8,6],[9,8],[11,8],[12,7],[17,8],[19,6]];
const BOX=['Polar?','H on N, O or F?','Lone pair on N, O or F?','Strongest attraction'];
module.exports=(rec,{has,cnt})=>[
  ...HOSTS.map(([s,a,fs])=>[`slide ${s}: ${a} is a unit filling 60% or more on frames ${fs[0]} to ${fs[fs.length-1]}`,fs.every(f=>has(s,f,r=>r.kind==='animation'&&r.label===a&&r.fill>=.6))]),
  ['slides 7 and 9: only the visible host of the stack is a unit (one animation unit per frame)',[7,9].every(s=>R(0,10).every(f=>cnt(s,f,r=>r.kind==='animation')<=1))],
  ['slide 5: each word card is a unit (8), and the legend',cnt(5,1,r=>r.kind==='wcard')===8&&cnt(5,2,r=>r.kind==='wcard')===8&&has(5,2,r=>r.kind==='legend')],
  ['slide 10: each box of forceDecider is a unit while it fills (frames 1 to 12), and the molecule drawing',R(1,12).every(f=>BOX.every(t=>has(10,f,r=>r.kind==='part'&&r.label===t)))&&R(1,12).every(f=>has(10,f,r=>r.label==='the molecule'))],
  ['slide 10: the electronegativity chips are a unit on the HBr frames',R(8,12).every(f=>has(10,f,r=>r.label==='electronegativity'))],
  ['slide 13: each rung of the ladder is a unit (3)',cnt(13,4,r=>r.kind==='row')===3],
  ['slide 14: each warm-up answer row is a unit (3)',cnt(14,4,r=>r.kind==='row')===3],
  ['slide 16: the steps card and the you-do card with its answers are units',has(16,5,r=>r.label==='four steps')&&has(16,14,r=>r.label==='you do')],
  ['slide 17: the dissolving table is one unit while its rows build (as 4.2 slide 11; a row of three short cells fills under 60%)',[2,3,4,5,6,7].every(f=>has(17,f,r=>r.kind==='dissolving table'&&r.fill>=.6))],
  ['slide 18: the result line is a unit',has(18,4,r=>r.label==='result'&&r.fill>=.6)],
  ['slide 20: each row of the four kinds of solids is a unit (4)',cnt(20,3,r=>r.kind==='row')===4&&cnt(20,4,r=>r.kind==='row')===4],
  ...RULES.map(([s,f])=>[`slide ${s}: the rule card is a unit (frame ${f})`,has(s,f,r=>r.kind==='rule'&&r.fill>=.6)]),
  ['slides 15 and 18: each line of the band\'s rule is a unit (3 and 2)',cnt(15,11,r=>r.kind==='p')===3&&cnt(18,6,r=>r.kind==='p')===2],
  ['slide 18: the sizes chip row is a unit',has(18,0,r=>r.kind==='sizes')],
  ['the caption "Atom colors show the element, not the charge." is a unit on slides 3, 6, 15, 17, 18, 19',[[3,0],[6,0],[15,0],[17,0],[18,0],[19,0]].every(([s,f])=>has(s,f,r=>r.kind==='caption'))],
  ['ten check cards, each a unit with its options',rec.filter(r=>r.kind==='check').length>=10&&[6,7,8,9,11,12,15,17,18,19].every(s=>rec.some(r=>r.s===s&&r.kind==='check'))],
  ['the routine slides 21 to 26: every prompt is a unit (generic check), listed',[22,23,24].every(s=>has(s,0,r=>r.kind==='prompt'))&&has(25,3,r=>r.kind==='prompt')]];
