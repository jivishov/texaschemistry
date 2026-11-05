# Report 04b: The teacher's fidelity review of the 4.5 deck

Step: 04b · Lesson: 4.5 · Commit: the commit `[implementer] 04b: teacher fidelity review fixes (fit, dashed lines, overlaps, tester, hammer, checks, texts)` on `workshop/unit4-5-6`, parent `84a0dd0` (its hash is in the pull-request comment `report 04b ready`)

## Source of this step
There is no brief 04b. `status.md` read `turn: teacher`, step 04a, waiting for the teacher's review of the deck, which would become fix brief 04b. The teacher sent the review straight to this session as 14 remarks in three batches, with screenshots, and closed with:

> "I need you to fix all given issues. Put them in any relevant round or as a separate one with appropriate message. Due to the low limit available for the orchestrator (in a different Claude account) I can't use it to instruct you without hitting its limit. Therefore, this is the independent critical fidelity review and refine work."

So this round is 04b, the step that `status.md` and review 04a reserved for the teacher's remarks. `briefs/` is not edited (IMPLEMENTER.md: never edit `briefs/`). The teacher's remarks stand in for the brief and are quoted item by item below. Remark Tb.n means batch b, remark n.

## Done
Files: `parts/lessons/4-5/sims.html`, `gen_slides.py`, `css.css`, `chem.js`, `scratch-check.js`, and the generated `slides.html`; the deck `unit4/slides-4-5.html` was rebuilt with `build.py 4 5`. No shared part changed. 4.1 and 4.2 were not rebuilt and are unchanged.

### Batch 1
**T1.1 "Check the text overflow"** (slide 6, the rule card over the caption).
- On the rule frame, the five earlier cards (chlorine, bond within, attraction between, salt, copper) now leave the column, so the rule card stands alone above the caption.
- The same kind of overlap (one block running over a sibling) was found on slides 13, 20 and 25. The walk's overflow detector does not catch it, so this round adds an overlap scan (Verification).

**T1.2 "Should the structures fit their frames?"** Yes. Every drawing on slide 3 now sits inside its panel, and `meta().clearance` measures the tightest side:

| panel | before (04a) | after (04b) | clearance |
|---|---|---|---|
| snow | three water molecules, 314 px tall in a 245 px panel | two water molecules, one hydrogen bond, H···O 1.94 times O–H (186 to 96 pm), centred by their full outline | 17 px (24 px melted) |
| salt | 3 × 3 grid, 278 px tall, five Cl⁻ and four Na⁺ | 2 × 4 grid, four Na⁺ and four Cl⁻ (neutral), still to scale, Na⁺ 61 px | 26 px |
| sand | Si–O sticks at 0.55 px/pm, 4 px from the frame | 0.50 px/pm | 12 px |

`chem.js` and `scratch-check.js` assert a clearance of at least 4 px on every tall-layout frame.

**T1.3 "Should non-water molecules also melt?"** No. At 0 °C only the snow melts; salt melts at 801 °C and sand near 1700 °C.
- At the melt stage the three names now read "snow: melts", "salt: stays solid", "sand: stays solid".
- The slide-3 notes add the same sentence.
- `meta().states` carries the three names; `chem.js` checks them.

**T1.4 "Add legend for the non-charged circles"** (slide 7, dispersion).
- The gray circles are the nuclei. Each now carries a "+" mark.
- A key at the top of the animation reads "⊕ nucleus" and "⊖ electron" on every dispersion frame (`meta().key`, checked).

**T1.5 "Show the dashed line for the H bond clearly."**
- One drawing rule now applies to every attraction line: round-capped dashes with a set visible length and gap, over a halo of the slide color, drawn over the molecules.
  - Before, the round caps ate the gaps: a hydrogen bond's 12 px gap showed as 3 px.
  - New sizes: hydrogen bond 9 px wide (18 px dashes, 12 px gaps); dispersion 6 px (16/12); dipole-dipole 7 px.
- A hydrogen bond now runs from the H's surface into the centre of the acceptor's lone pair, so it visibly ends in the lone pair. This covers slide 3 (snow), slide 9 (water, ammonia, the four neighbours) and slide 12 (below).

### Batch 2
**T2.1 "Two images overlaying with the chem structures faded. Is it expected?"** No.
- Slide 11, energy stage: the molecules and their container now leave fully. The two bars stand alone. `meta().moleculesShown` and `containerShown` are false there and true again on the check frame (checked).
- The same pattern was on slide 8: a faded F₂ pair (30%) sat behind the randomly turned HCl pair, which overlapped it. The faded F₂ is gone from the HCl, turn and face stages and returns, solid, at compare.

**T2.2 "The dashed lines are not clear."**
- Slide 11, heating: each attraction line is drawn over the molecules and placed in a real gap. It joins the closest pair of atoms of the two molecules whose gap is 28 px or longer and crosses no other atom; with no such gap, 18 px or longer; failing that, the two central atoms.
  - An earlier try drew the line centre to centre over the molecules. It crossed an H and read as a bridging bond, so it was dropped.
  - The 2 × 2 methane block keeps its 166 × 206 px packing, so brief 04a's thresholds still hold: block 40% or less, area per molecule 2.5 times or more.
- Slide 12, ice: the hydrogen bonds were short segments drawn behind the spheres. Now each is drawn after the spheres, from the H's surface to the O's surface, and is cut only where a nearer sphere covers it, so the lattice keeps its depth.

**T2.3 "Overlapping structures/cards/text."**
- **Slide 13:** the table's grid row could shrink below the table (`minmax(0, 1fr)`), so the line card covered the third rung.
  - The rows are now `minmax(min-content, 1fr) auto auto` (slides 13 and 20).
  - On the write frame the thread line gives way to the writing frame, which asks for the same idea, so the table, the frame, the word bank and the timer all fit.
- **Slide 12:** "O–" ended one line and "H bonds" began the next. Every bond written with an en dash between two element symbols (O–H, C–H, Cl–Cl, Br–Br, Si–O; 12 places) now stays on one line. It is wrapped in `<span class="nw">` in `gen_slides.py`, in text only, never in a tag or a script.
- **Slide 12, floating ice:** the label "8.3% above the surface" ran over the tank's wall and the water line. The tank is narrower now; the label sits beside it, with a bracket on the ice's exposed part and a leader line to the label.

**T2.4 "Starting slide 15, the main question and the side question 'Lights or stays dark?' repeat; their positions are off and too close."**
- The animation's readout now shows results only: "The bulb lights." / "The bulb stays dark." at close, and the particle line at zoom. It is empty at the predict stages, which ask the question on the slide's own band line.
  - The readout is centred under the magnified view's place, so it no longer sits at the far right edge.
  - It applies on slides 15, 16 and 17 (`meta().readout`; `chem.js` checks that no predict stage shows it).
- The band's single line is centred in the band, 10 px clear of the caption, away from the animation's labels.
- While the class predicts (tester and predict stages), a dashed circle with "?" marks where the magnified view will open.
  - Without it, removing the repeated question left slide 15 at 50% empty and slide 16 at 35%, over the 33% gate.
  - The circle carries the lesson's thread ("what can move inside?").

**T2.5 "The MCQ is too tight vertically; feedback neatly on the right side in a box."** Slides 15 and 18 now lay the check out in two columns:
- the question across the top;
- the options on the left (58%) at 36 px, 12 px apart;
- the answer, or the clicked option's feedback, in a box on the right (42%). The box shows its border only when it holds a line.

Slide 18's option A was shortened to fit one line: "Shifted layers put like charges together." The repulsion stays in its feedback line and in the answer "A. Like charges repel and push the layers apart."

### Batch 3
**T3.1 "Reset the circuit to avoid confusion that the circuit state is relevant to the question."** Slide 16's you-do frame now sets the tester back to the `tester` stage: empty beaker, switch open, no result. Before, it showed solid CaCl₂ with the bulb dark. `chem.js` checks the reset from the you-do frame until the answer frame, which returns to molten KCl, magnified.

**T3.2 "Ensure hammer contact direction is appropriate to cause such effect."**
- Slide 18: the hammer now swings in from the left, its head along the swing, and strikes the top layer's left side. The top layer then slides right, the way the blow points.
- The head stays at the contact point while the layer slides on (it never runs into the block) and rests there at the result.
- The names are headers over the blocks. At the result they read "copper: malleable" and "salt, NaCl: brittle".
- The band line reads "A hammer hits the top layer of each from the side."; the notes and the aria label say the same.
- `meta()` gives `hammerFrom: 'left'`, `hammerMoves: 'right'`, `struck: 'top layer'`, and `topLayerMoves: 'right'` at the shift (checked).

**T3.3 "Overlapping cards/text"** (slide 20, the closing card over the last row).
- Same grid fix as slide 13.
- The table is set at 34 px (the floor) with columns at 23/35/21/21%, and `<br>` in four cells, so every row takes at most two lines. Measured: each column's widest unbroken line fits its column.
- **Found by the scan:** the slide-25 timer covered the writing card's corner by 14 px (also there in 04a). It is now centred on the rail row (54 px digits, less padding), 5 px clear of the driving question and 6 px clear of the card.

**T3.4 "Check the fidelity of the questions and their answers in the checkpoints and exit ticket."** Every prompt, frame, word bank, criterion and sample on slides 22 to 25 was read against the lesson sheet and the reading. Changes:
- **Checkpoint 1:**
  - The prompt reads "… Methane boils at −161.5 °C, water at 100.0 °C. Explain the difference." (one word shorter, so the sample fits the 35-word budget).
  - The frame "Water boils far above methane because {gap}." became "… because of {gap}.", so the bank's noun phrases ("hydrogen bonding", "stronger attraction") complete it.
  - The sample "Water forms hydrogen bonds: H on O, lone pairs. …" read as a list. It now reads "Water forms hydrogen bonds: H on O to lone pairs. Methane has dispersion forces only, so it boils lower."
- **Checkpoint 2:** the bank item "no electrons move" was wrong as worded (electrons do move in the wires). It is now "ions, not electrons". The prompt and sample were correct and are unchanged.
- **Checkpoint 3:** correct; unchanged.
- **Prediction 3** (slide 25): the reason "A hydrogen bond is about 5 to 10% of a covalent bond." gave a strength, not why the answer is "an attraction between molecules". It now reads "It pulls an H on one molecule to a lone pair on the next. About 5 to 10% of a covalent bond."
- **Exit ticket:**
  - The 04a sample ended "Attractions are weaker than bonds." It did not finish the reasoning frame "… so {gap}." and used "set" where the claim frame says "decide". It now reads "The forces that come apart decide the melting point. Snow, 0 °C: only attractions between molecules let go. Salt, 801 °C: ionic bonds break. Sand, near 1700 °C: covalent bonds break. Attractions are weaker, so snow melts lowest." (35 counted words.)
  - The write card's tag reads "Write: the melting point". The driving question names three properties; the exit ticket takes the melting-point part, and the notes say that checkpoints 2 and 3 answered conductivity and hardness (open question 2).

### Other changes
- Review 04a F2 (nit): the `heating` header comment in `sims.html` now says four CH₄ (2 × 2) or six H₂O (2 × 3).

## Verification
Full suite on the final deck (md5 `25d4b747…`), both themes, `MATRIX=0`: **21 of 22 PASS**. The one FAIL is xcheck: its 16 failing lines are the same blueprint-number lines as in 04a, waiting for step 05; the diff of the two logs' FAIL lines is empty.

| Audit | Theme | Verdict | Line |
|---|---|---|---|
| walk | light | PASS | 210 states, max empty 32% (s18f4) (04a: 33%, s18f1) |
| walk | dark | PASS | 210 states, max empty 32% (s18f4) |
| back | light, dark | PASS | 210 forward, 210 back |
| fonts | light | PASS | |
| keys | | PASS | 48 checks |
| readability | | PASS | every slide at most 35 visible prose words, no sentence over 14 words; samples: checkpoint 1 grade 4.9, exit ticket 4.7 |
| print | | PASS | 27 slides, 210 frame lines, 12 PDF pages |
| render3d | | PASS | |
| extras | | PASS | |
| chem | | PASS | 172 checks (04a: 156; the 16 new ones cover this round) |
| timing | | PASS | period 1 45.5 min, period 2 47 min (unchanged) |
| supgap | | PASS | 56 symbol and charge pairs |
| zoom | light, dark | PASS | 1241 zoomed states over 210 frames, min fill 65%, Back tests 27 |
| click | | PASS | 10 graded checks, 3 Predict-now questions, 51 assertions |
| layout | | PASS | 26 option lists (stacked 23, row 3), max empty 32%, clipped text 0 |
| xcheck | | FAIL | 27 of 43; the 16 blueprint-number lines of 04a, unchanged |
| contact, zoomsheet | light, dark | PASS | sheets under `artifacts/04b/` |

- **Bench:** `build.py 4 5 --scratch` then `scratch-check.js`: `scratch-check 4.5: PASS 157 checks` (04a: 150), no console errors (`artifacts/04b/bench/`).
- **During the round:**
  - A first full run failed zoom on slide 18: the two new name labels filled 39% and 49% at the 4× cap. Their zoom units are now 260 px wide or more (fill 65%).
  - The deck was rebuilt and the whole suite re-run from the start on the final build. The table above is that run.

**Overlap scan** (`artifacts/04b/overlap/overlap.js`, written for this round). On every frame it checks two things:
- visible text against a visibly boxed element it does not belong to (a box has a border or a background; the animation host counts, except its `data-reserve` band, which the text band uses by design);
- boxed elements against each other.

Text boxes are trimmed by a fifth of their line height at top and bottom, so a subscript's line box touching the next line does not count.

| deck | theme | frames | overlaps |
|---|---|---|---|
| 04a (`c3886bd7…`) | light | 210 | 16, on four frames: slide 6 f6 (caption under the rule card), slide 13 f4 (third rung under the line card), slide 20 f4 (last row under the closing card), slide 25 f5 (timer over the writing card) |
| 04b (`25d4b747…`) | light | 210 | 0 |
| 04b | dark | 210 | 0 |

The scan finds exactly the overlaps the teacher's screenshots show, plus slide 25's timer.

Artifacts under `workshop/artifacts/04b/`:
- `before-after-1.jpg` to `before-after-5.jpg`: each remark, the 04a frame on the left and the 04b frame on the right;
- `contact-*` and `zoomsheet-*`: the suite's sheets for both themes;
- `suite/`: every audit's log and JSON;
- `bench/scratch-check.txt`;
- `overlap/`: the scan script and its three logs.

## Repo state
- `unit4/slides-4-5.html`: 307,664 bytes, md5 `25d4b747e33dd6640319510f738fabd1` (04a: `c3886bd78f9f546e5690a4e2e08fef1a`). Built only by `build.py 4 5`.
- Reference decks (no shared part changed, not rebuilt): 4.1 `ebd342f1ee0e11c47157141cf3b2a59b`, 4.2 `c3fa219a806963f9a66c3baf643153f4`.
- `git status --short` before the commit:
```
 M tools/slides-kit/parts/lessons/4-5/chem.js
 M tools/slides-kit/parts/lessons/4-5/css.css
 M tools/slides-kit/parts/lessons/4-5/gen_slides.py
 M tools/slides-kit/parts/lessons/4-5/scratch-check.js
 M tools/slides-kit/parts/lessons/4-5/sims.html
 M tools/slides-kit/parts/lessons/4-5/slides.html
 M unit4/slides-4-5.html
 M workshop/log.md
 M workshop/status.md
?? workshop/artifacts/04b/
?? workshop/reports/04b-teacher-review.md
```

## Deviations
1. **No brief.** The teacher's remarks, in this session, are the instructions. `briefs/` is not edited. `status.md` and `log.md` follow the protocol as for any step.
2. **Texts the orchestrator had fixed word for word** were changed on the teacher's fidelity review:
   - the exit-ticket sample (brief 04a item 4);
   - slide 18's option A;
   - checkpoint 1's prompt, frame and sample;
   - checkpoint 2's bank item;
   - prediction 3's reason.
   Each new text keeps the 35-word visible-prose budget, the 14-word sentence limit and grade 8 or lower (readability PASS).
3. **The plan's snow** was "three water molecules … linked by two hydrogen bonds", and its **salt** a 3 × 3 grid. Neither fits the 245 px panel with every sphere 60 px or more. Snow is now two molecules and one hydrogen bond; salt is 2 × 4 (also neutral).
4. **The "?" circle** on slides 15 and 16 was not asked for. It keeps those slides under the 33% emptiness gate once the repeated question is gone. The gate was not loosened.
5. **Slide 13's thread line** leaves on the write frame (it was on screen with the frame before).
6. **The overlap scan** is a script written for this round. It is not a kit audit and is not in `suite.py` (open question 1).

## Open questions
1. Should the overlap scan become a kit audit (RULES section 11) for every deck? It found the slide-25 timer, which no audit catches, and is clean on 4.5 after this round.
2. The exit ticket answers the melting-point part of the driving question; conductivity and hardness are assessed by checkpoints 2 and 3. Is that the intended split, or should the exit ticket take all three in fewer words each?
3. The methane solid stays packed at brief 04a's 40% block, so its attraction lines are short (two dashes each, in the gaps). A looser block would give longer lines but break the 40% threshold. Keep it?
