// Lesson 4.1: the teacher's explicit zoom checks (rounds B5, B6, A1), moved word for word from audits/zoom.js.
// zoom.js runs two generic checks for every deck (every zoomed check shows its options; every prompt on a routine slide is a
// unit), so the two 4.1 entries that said the same ("A1 checks…", "B6 slides 20 to 24: the prompts are units") are not repeated here.
// rec: one row per zoomed state {s, f, i, n, kind, label, id, mode, fill, …}; has(s,f,pred) and cnt(s,f,pred) look rows up.
module.exports=(rec,{has,cnt})=>[['B5 slide 6: the animation is a unit on the electron transfer stages (f0 to f3)',[0,1,2,3].every(f=>has(6,f,r=>r.kind==='animation'&&r.fill>=.6))],
    ['B5 slide 7: the lattice is a unit on the grow and turn frames (f1, f2)',[1,2].every(f=>has(7,f,r=>r.kind==='animation'&&r.fill>=.6))],
    ['B5 slide 8: the H–H pair and the pairs after it are units (f1 to f5)',[1,2,3,4,5].every(f=>has(8,f,r=>r.kind==='animation'&&r.id==='s08-sim'&&r.fill>=.6))],
    ['B6 slide 18: each of the four argument boxes is its own unit',[1,2,3,4,5,6,7,8].every(f=>['Claim','Evidence','Reasoning','Strength'].every(t=>has(18,f,r=>r.kind==='part'&&r.label===t&&r.fill>=.6)))],
    ['A1 slide 2: the three mini-frames of the labels stage are units',has(2,5,r=>r.label==='nonpolar covalent')&&has(2,5,r=>r.label==='polar covalent')&&has(2,5,r=>r.label==='ionic')],
    ['A1 slide 16: the lit pair and the whole table are units',[3,4,5].every(f=>has(16,f,r=>r.kind==='part'&&/^pair/.test(r.label))&&has(16,f,r=>r.kind==='animation'))],
    ['A1 slide 16: the three rule cards are units, each one',rec.filter(r=>r.s===16&&r.f===6&&r.kind==='p').length===3],
    ['A1 slide 11: each column of the summary table is a unit',rec.filter(r=>r.s===11&&r.f===8&&r.kind==='column').length===3],
    ['A1 slides 14 and 19: each row of an answer table is a unit',rec.filter(r=>r.s===14&&r.f===4&&r.kind==='row').length===3&&rec.filter(r=>r.s===19&&r.f===4&&r.kind==='row').length===3]];
