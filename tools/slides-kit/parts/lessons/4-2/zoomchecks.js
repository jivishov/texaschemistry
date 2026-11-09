// Lesson 4.2: the teacher's explicit zoom checks, moved word for word from audits/zoom.js.
// zoom.js runs two generic checks for every deck (every zoomed check shows its options; every prompt on a routine slide is a
// unit). So "every prompt on slides 20 to 24 is a unit" is not repeated here, and the check entry keeps only its own part: the
// count of zoomed checks (the old entry also asserted that every zoomed check shows its options, now the generic check).
// rec: one row per zoomed state {s, f, i, n, kind, label, id, mode, fill, …}; has(s,f,pred) and cnt(s,f,pred) look rows up.
module.exports=(rec,{has,cnt})=>[
    ['slide 2: each product of labelRead is a unit (shelf), and the open label card (focus)',cnt(2,0,r=>r.kind==='part')===3&&has(2,1,r=>r.kind==='part'&&/^label/.test(r.label))],
    ['slides 6 and 7: the whole ionTable and the lit group of each stage are units',[1,2,3,4,5,6].every(f=>has(6,f,r=>r.kind==='animation')&&has(6,f,r=>r.kind==='part'&&/^group/.test(r.label)))&&has(7,0,r=>r.label==='four metals')],
    ['slides 8, 9, 16, 17: chargeBlocks at its current stage is a unit on every frame that shows it',[0,1,2,3,4,5,6,7,8,9,10].every(f=>has(8,f,r=>r.kind==='animation'&&r.id==='s08-sim'))&&[3,4,5,6,7,8].every(f=>has(16,f,r=>r.id==='s16-cb'))],
    ['slide 10: crisscross is a unit',[0,1,2,3,4,5,6,7].every(f=>has(10,f,r=>r.id==='s10-sim'))],
    ['slides 11 and 12: nameBuilder formula and the tiles or the joined name are units',has(11,0,r=>r.label==='name tiles')&&has(11,1,r=>r.label==='the joined name')&&has(11,0,r=>r.label==='formula')&&has(12,2,r=>r.label==='the joined name')],
    ['slides 12 and 17: each step line of stockDetective is a unit',has(12,9,r=>r.label==='step 1')&&has(12,9,r=>r.label==='step 3')&&has(17,5,r=>r.label==='step 3')],
    ['slide 15: polyIons (the current ion) is a unit on every frame',[0,1,2,3,4,5,6,7,8,9].every(f=>has(15,f,r=>r.id==='s15-sim'))],
    ['slide 16: parenBus is a unit',[0,1,2].every(f=>has(16,f,r=>r.id==='s16-pb'))],
    ['every check card with its options',rec.filter(r=>r.kind==='check').length>=9],
    ['each answer-table row (slides 13, 14, 18) and each spot-the-error row (slide 19) is a unit',cnt(13,5,r=>r.kind==='row')===4&&cnt(14,4,r=>r.kind==='row')===3&&cnt(18,7,r=>r.kind==='row')===6&&cnt(19,6,r=>r.kind==='row')===6],
    ['each word card on slide 5 is a unit',cnt(5,1,r=>r.kind==='wcard')===8],
    ['the memory cards (slides 7 and 15) and the pattern card (slide 15) are units',has(7,4,r=>r.kind==='memory card')&&has(15,7,r=>r.label==='memory card')&&has(15,6,r=>r.label==='pattern')]];
