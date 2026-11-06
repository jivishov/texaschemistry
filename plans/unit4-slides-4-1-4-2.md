# Plan: new slide decks for Unit 4 lessons 4.1 and 4.2

Clean-slate build. The current `unit4/slides-4-1.html` and `unit4/slides-4-2.html` are ignored and replaced at the same paths (the unit index and the readings link to those names). Sources of content: `unit4/reading-4-1.html`, `unit4/reading-4-2.html`, `unit4/blueprint.html`. `unit4/blueprint.html` gets its slide references updated at the end.
Branch: `claude/unit-4-chemistry-slides-j62190`. Implementer: Opus 5.5 in a new thread. Every step in section 11 ends with a confirmation gate.

---

## 1. End goal (work backwards from this)

A deck is done when:
- The teacher runs both periods of the lesson with the four buttons of a Logitech R800 and never touches the laptop after opening the deck. Every reveal, animation stage, answer, timer and zoom is one Next press. Back restores the previous state exactly.
- A student in the back row reads everything: body text 44 px on the 1600 x 900 canvas (about 26 pt on a printed slide), nothing student-facing under 34 px, animations drawn with shapes at least 60 px.
- Each lesson runs hook → concept in one picture → worked example → your turn → next concept, with a one-picture summary closing period 1 and a retrieval warm-up opening period 2. Two periods per lesson, as the blueprint says.
- Every concept slide carries one animation or simulation, scripted to the presses.
- Every student-facing line reads as simplified textbook language: short declarative sentences, the real chemistry terms, no thesis-style sentences (section 7). Readability audit passes.
- English learners get a word with its icon, its Spanish cognate and a one-line meaning the first time it appears, sentence frames on every writing step, and a fixed color code.
- A Playwright walk of every press of both decks shows no overflow, no console errors and a footer cue at every press. Blueprint slide numbers match.

---

## 2. Domain model

| Entity | Meaning | Representation |
|---|---|---|
| Deck | One lesson, two periods, 25 to 26 slides | one standalone HTML file |
| Slide | One screen: title, section label, reading reference, frames, notes | `<section class="slide" data-title data-sec data-ref>` |
| Frame | The state the slide is in after n presses; frame 0 is the slide as entered | `frames: [state, state, ...]` in the slide's script |
| State | Declarative: which blocks are shown, which animation stage, zoom target, timer, cue text | `{show:[...], stage:{sim:'tug', s:2}, zoom:'#card', timer:60, cue:'...'}` |
| Block | A card, picture, line or table that a frame shows or hides | element with an `id` |
| Animation | A canvas or SVG model with a small set of named stages; each stage is a full state, so Back replays it | `sim.set(stage)`, `sim.get()` |
| Cue | One-line footer text saying what Next will do | `state.cue`, default "Next: <next block's label>" |
| Check | A question block followed by an answer block (students answer by hand signal or notebook) | two frames |
| Hook | Opening scene from everyday life, animated, one line of text | first content slide |
| Routine | Checkpoint (think, talk, write, self-check, compare) and CER exit ticket, timed by frames | fixed templates |
| Clicker map | R800 button → key → runtime action | runtime key handler |

Rule: the runtime computes frame n by replaying states 0..n, so Back never needs a reverse action and no animation keeps hidden state between presses.

---

## 3. Runtime (new, lean, inline in each deck; written once, copied into both files)

### 3.1 Clicker map (Logitech R800 sends four keys)
| Button | Key | Action |
|---|---|---|
| Next ▶ | `PageDown` | next frame; after the last frame, next slide at frame 0 |
| Back ◀ | `PageUp` | previous frame; at frame 0, previous slide at its last frame |
| Start/stop | `F5` then `Escape` | `F5`: `preventDefault`, enter full screen if not in it, else nothing. `Escape`: close in order blank screen → zoom → notes; otherwise let the browser exit full screen |
| Blank | `.` (also `b`) | one press: zoom the frame's focus block (or the animation) to fill the slide, press again to unzoom; two presses within 400 ms: blank screen (black), any key clears it |

Guards: ignore `e.repeat`; 180 ms debounce on Next/Back; keys work whatever has focus except a `textarea`; any mouse click on a control is followed by `blur()`. Laptop keys kept for desk use: arrows, Home, End, N (notes), O (overview), Z (zoom), T (theme).

### 3.2 Frame engine
- `go(slide, frame)`: hide all blocks of the slide, replay states 0..frame, apply the last state's `stage`, `zoom`, `timer`, `cue`. Entering a slide forward lands on frame 0; entering backward lands on the last frame.
- Blocks appear with a 250 ms fade-up; animation stages run their own transitions (300 to 900 ms); reduced-motion jumps to the end state.
- Timers: a frame with `timer` starts a large countdown (visible from the back: 96 px digits); Back then Next restarts it.
- Progress: a thin bar across the top, slide counter bottom-right, section name bottom-left. No other chrome on screen.
- Footer cue: 28 px, bottom center, "Next ▶ …". Teacher reads it from anywhere in the room; students may see it, so cues never give away an answer ("Next ▶ answer" is fine, "Next ▶ MgO" is not).
- Notes: laptop panel (N) listing the current slide's frames with timing and talk points; `@media print` prints a run-sheet of all slides (number, title, frame list, notes) so the teacher can carry two or three pages.
- Zoom: CSS transform of the block to fit the slide at up to 3x; canvases re-render at the zoomed resolution.
- Themes: light by default (bright classrooms), dark available. Colors from tokens so every drawing works in both.
- Mobile reflow is not a goal for the projector decks; a minimum fallback (scrolling page under 760 px) is enough.

### 3.3 Visual system
- Type: DM Sans for everything on the slides (sans reads better at distance than the serif of the readings), IBM Plex Mono only for numbers in a calculation. Base 44 px, headings 64 px, big statements 56 px, small 34 px floor, cue 28 px, section label 26 px (teacher-facing). Subscripts and charges set as real `<sub>`/`<sup>` at 0.7em.
- Budget: at most 35 words of student-facing prose per slide outside tables and labels. One idea per block. A block is a picture, a rule, an example or a question, never two.
- Layout templates, six only: Hook (full-width animation, one line under it), Concept (animation 60% left, one rule card right), Example (steps appear down the right, picture left), Your turn (question top, answer below), Summary (one diagram), Routine (checkpoint, exit ticket, predictions).
- Color code, fixed for both lessons and printed as a legend on slide 5 of each: cation red, anion blue, electron dot yellow on dark / violet on light, metal gray, nonmetal green, δ+ warm, δ− teal. Shapes carry a symbol as well as a color (+, −, dots) for color-blind students.
- Icons: flat inline SVG, two fills and one accent, 3 px strokes at canvas scale, `role="img"` with `aria-label`. No raster images unless the user supplies them (then base64 WebP, as `unit4/index.html` already does).

---

## 4. Animations and simulations (new, projector-first, scripted)

Canvas 2D or SVG with JS. Big shapes, few labels, every label at least 36 px. Each exposes `set(stage)` and `get()`. Mouse controls are optional and never required.

### 4.1 For lesson 4.1
| Name | Stages | What it shows |
|---|---|---|
| `tugOfWar` | teams, even, uneven, blowout, labels | Two stick-figure teams, a rope, the knot drawn as two glowing dots (the shared pair). even: same strength, knot stays centered. uneven: right team stronger, knot slides toward it, both still hold. blowout: knot pulled all the way, the rope fades, the teams gain + and − badges and slide together ("the pull between + and − is now the bond"). labels: three mini-frames captioned nonpolar covalent, polar covalent, ionic. Strength numbers shown as electronegativity values in the chemistry stages. |
| `ionHop` | atoms, hop, ions, attract, grow | Na and Cl atoms drawn with outer-shell dots only. hop: the one Na dot jumps to Cl. ions: badges Na⁺ (smaller) and Cl⁻ (larger), proton and electron counts. attract: the two slide together. grow: a 3 x 3 x 2 isometric block of alternating red and blue spheres builds up, "no molecules, a ratio: NaCl". A center ion lights with its six neighbors on the last press. |
| `sharedPair` | H2, Cl2, HCl, HO, HF | Two atoms as soft clouds, the pair as two dots. Pair position moves with the difference (0.00, 0.00, 0.96, 1.24, 1.78); δ+ and δ− badges fade in from 0.4 up; tiny tug-of-war icon under the pair repeats the metaphor. |
| `electronSea` | crowd, cores, sea, drift, Mg, Al | crowd: heads passing beach balls (the hook). cores: heads become + circles in a grid. sea: balls become drifting dots. drift: a battery appears, dots stream one way, cores stay. Mg and Al: two and three dots per core. |
| `enMeter` | bar, lines, place(bond) | A horizontal bar from 0 to 3.3 with gradient regions, 0.4 and 1.8 lines, a pointer that drops onto the bar for a named bond with its subtraction shown above (3.16 − 0.93 = 2.23). |
| `ptMap` | outline, metals, nonmetals, pair(a,b) | Periodic table outline, metals tint from the left, nonmetals from the right, staircase. pair lights two cells and draws the line between them. |
| `cerBuilder` | claim, evidence, reasoning, strength | Four big boxes fill one per press with the argument for the named bond; used for I do (KF) and we do (HCl). |

### 4.2 For lesson 4.2
| Name | Stages | What it shows |
|---|---|---|
| `labelRead` | shelf, focus 0..2, code | Toothpaste (sodium fluoride), antacid (calcium carbonate), lawn fertilizer (ammonium sulfate) on a shelf; focus zooms one label with the name at 56 px; code: "a name is a code you will read by the end". |
| `ionTable` | outline, g1, g2, g13, g17, g16, g15, tm | Periodic table; each group lights in order with its charge badge (1+, 2+, 3+, 1−, 2−, 1−); -ide names appear on the anion groups; tm lights Fe, Cu, Ag, Zn with their ions. |
| `chargeBlocks` | ions(c,a), add, balance, formula, name | LEGO-style tiles: a cation tile with as many + studs as its charge, anion tiles with − sockets. add drops tiles one at a time, balance snaps rows when studs equal sockets and shows the totals, formula assembles the symbols and subscripts from the counts, name writes the name under it. Supports a `reduce` stage for Mg₂O₂ → MgO (two pairs collapse to one, "2 : 2 → 1 : 1"). Polyatomic ions are one tile with the group drawn inside; parentheses appear when the tile repeats. |
| `crisscross` | ions, cross, reduce, check | Charge digits travel diagonally into subscript positions; reduce strikes the common factor; check shows 2 × 3+ = 6+ and 3 × 2− = 6−. |
| `nameBuilder` | parts, numeral, join | Tiles cation name, (numeral), anion root, -ide slide together into one name; numeral tile only for Fe and Cu. |
| `stockDetective` | anion, total, metal, name | Works backward from a formula: the anion charge appears, the total needed, the metal charge, the Stock name. Used for CuO, Cu₂O, FeCl₂. |
| `polyIons` | NH4, OH, NO3, CO3, SO4, PO4 | Six big 2D structural drawings (atoms as circles with symbols, bonds as sticks), one at a time, with the charge badge on the whole group and the name; a dashed outline shows "one unit". No 3D needed for the projector. |
| `parenBus` | one, two, wrong | A squad (OH) in a rounded box; two squads become parentheses with a subscript outside, Ca(OH)₂; wrong draws CaOH₂ with a red strike and "1 O, 2 H". |

---

## 5. Lesson 4.1, Predicting bond type: 25 slides

Period 1: slides 1 to 13 (ionic, covalent, metallic). Period 2: slides 14 to 25 (predicting, arguing, checkpoint, exit ticket).
Format: number, title, template, frames in order (one press each), check.

1. **Cover.** Title, driving question in one line, R800 button strip (Next, Back, Blank = zoom, Start = full screen).
2. **Hook: Tug of war.** Hook. `tugOfWar` teams → "Who wins the rope?" (students predict) → even → uneven → blowout → labels. Last line: "Atoms do this with electrons. Pulling strength = electronegativity (Lesson 3.3)."
3. **Sodium, chlorine, salt.** Concept. Three icons appear (soft metal cut with a knife, yellow-green gas, white crystals that melt at 801 °C) → driving question at 56 px → 60 s timer with the sentence starter "I think sodium and chlorine bond differently from two chlorine atoms because…". Notes: video of sodium in chlorine, never performed.
4. **Predict now.** Routine. Three questions, hands up per option: solid salt is made of (ions / NaCl molecules / atoms); in HCl the shared pair is (closer to Cl / closer to H / in the middle); a copper wire is held together by (cations in an electron sea / shared pairs / + and − copper ions). Answers return on slide 23.
5. **Targets and words.** Summary. Five "I can" lines in kid wording → word strip with icon, Spanish, meaning: ionic bond (enlace iónico), covalent bond (enlace covalente), metallic bond (enlace metálico), electronegativity (electronegatividad), partial charge (carga parcial), crystal (cristal), molecule (molécula). Color legend.
6. **Forming ions.** Concept. `ionHop` atoms → "Which atom lets go?" → hop → ions (counts, sizes) → rule card "metal loses, nonmetal gains; the hop alone costs energy" → check: "Magnesium loses two electrons. Which ion forms?" (Mg²⁻ / Mg⁺ / Mg²⁺) → answer with reason.
7. **The crystal.** Concept. `ionHop` attract → grow → center ion with six neighbors → rule card "the bond is the attraction between + and −; NaCl is a ratio, not a molecule" → check: "How many Cl⁻ touch each Na⁺ inside the crystal?" (1 / 6 / 8) → answer.
8. **Covalent bonds.** Concept. `tugOfWar` even (one press, recap) → `sharedPair` H2 → Cl2 ("each Cl now has eight around it") → rule card "a shared pair is a covalent bond; a group of atoms joined this way is a molecule" → check: "Cl₂: how many electrons does each Cl count around itself?" (7 / 8 / 14) → answer.
9. **Polar and nonpolar.** Concept. `sharedPair` H2 → HCl (predict first: "which pulls harder?") → HO → HF → rule card "unequal sharing: δ− on the stronger puller, δ+ on the other; a partial charge is smaller than an ion's charge" → check: "O–H: O is 3.44, H is 2.20. Which atom is δ+?" (H / O / neither) → answer.
10. **Metallic bonds.** Concept. `electronSea` crowd ("balls belong to everyone") → cores → sea → drift ("why a wire carries current") → Mg → Al → rule card "cations in a sea of electrons; the model draws dots, real electrons are waves" → check: "Why can a copper wire carry a current?" (electrons move / copper ions move / atoms share pairs) → answer.
11. **One picture for three bonds.** Summary. Three columns build: ionic (+ − grid), covalent (two atoms, a dot pair), metallic (+ cores in a sea); rows appear: who (ions / atoms / cations + electrons), what holds (attraction + − / shared pair / cations + sea), one example (NaCl / Cl₂ / Cu) → the rule in one line: "metal + nonmetal → ionic; nonmetal + nonmetal → covalent; metal alone → metallic".
12. **Backpack sort.** Your turn. Six icons: salt packet, water bottle, charger cable (copper), soda can (aluminum), pencil graphite, the O₂ you breathe → students call the bond → each press flips one item to its type with a four-word reason.
13. **Period 1 exit.** Routine. One sentence in notebooks with frame: "The three bonds differ in what holds the particles: …" 2 min timer. (Period 1 ends here.)
14. **Warm-up.** Your turn. Three questions, answer each on the next press: what particles are in solid salt; which atom in HCl is δ−; what moves in a copper wire.
15. **The electronegativity difference.** Concept. `enMeter` bar → lines 0.4 and 1.8 ("a guide, not a wall") → place Cl–Cl 0.00 → place H–Cl 0.96 → place Na–Cl 2.23 → rule card "larger minus smaller; below 0.4 nonpolar, 0.4 to 1.8 polar, above 1.8 ionic" → check: "Ca 1.00 and O 3.44. What does the guide predict?" (nonpolar / polar / ionic) → answer 2.44, ionic.
16. **Evidence from the table.** Concept. `ptMap` outline → metals → nonmetals → pair(Na, Cl) → pair(H, Cl) → pair(Cu, Cu) → rule card (the three lines from slide 11) → check: "Which pair forms a covalent bond?" (K and Br / N and O / Mg and O) → answer.
17. **Near the line.** Example. `enMeter` place H–F 1.78 ("molecules, boils at 20 °C") → place Mg–Cl 1.85 ("ionic solid, melts at 714 °C") → "0.07 apart, very different substances: near 1.8 the number alone is weak evidence" → place Fe–Cl 1.33 → "still named as an ionic compound: names follow metal + nonmetal (Lesson 4.2)" → check: "MgCl₂ has a difference of 1.85. How strong is that number alone as evidence that it is ionic?" (strong / weak / against) → answer.
18. **Bonding argument: I do, we do.** Example. Four-part table claim, evidence, reasoning, strength → `cerBuilder` KF, one part per press → `cerBuilder` HCl, students supply each part before the press (0.96, both nonmetals, strong because far from both lines) → check: "Which evidence best supports 'KF is ionic'?" (K is a metal and F a nonmetal, difference 3.16 / KF is white / F is a gas) → answer.
19. **You do: three bonds.** Your turn. LiF, N–H in ammonia, C–S in carbon disulfide with values → 3 min timer ("predict each; write a full argument for one") → answers one row per press (3.00 ionic strong; 0.84 polar, N δ−; 0.03 nonpolar).
20. **Checkpoint routine.** Routine. Think 30 s, talk 60 s, write 2 min, self-check, compare.
21. **Checkpoint 1** (4.1.1). "A student says the ionic bond in NaCl is the electron that moves from Na to Cl. What is wrong? What holds solid salt together?" Frames: think (timer) → talk (timer) → write (frames + word bank) → success criteria → sample answer.
22. **Checkpoint 2** (4.1.2). "Cl₂ and HCl each have one shared pair. Why is one nonpolar and the other polar? Which atom in HCl is δ−?"
23. **Checkpoint 3** (4.1.3). "Use the electron-sea model to explain why a copper wire carries a current, and name one thing the model leaves out."
24. **Predictions and exit ticket.** Routine. The three slide-4 answers with "hands up if you predicted this" → CER exit ticket on the driving question: claim frame → evidence frame → reasoning frame → self-check criteria → sample answer.
25. **Rate your learning.** Routine. Five targets with fingers 1 to 3; the review line names the slide to revisit (6–7, 8–9, 10, 15–17, 18–19).

Blueprint alignment after the build: 4.1.1 → 6–7; 4.1.2 → 8–9; 4.1.3 → 10; 4.1.4 → 11, 15–17; 4.1.5 → 18–19, 24. Slide checks: 8 (slides 6, 7, 8, 9, 10, 15, 16, 18).

---

## 6. Lesson 4.2, Ionic compounds: formulas and names: 26 slides

Period 1: slides 1 to 13 (ion charges, formulas, names, Stock). Period 2: slides 14 to 26 (polyatomic ions, translating, checkpoint, exit ticket).

1. **Cover.** Title, driving question, R800 strip.
2. **Hook: Read the label.** Hook. `labelRead` shelf → focus toothpaste "sodium fluoride" → antacid "calcium carbonate" → fertilizer "ammonium sulfate" → code. The three return on slide 18.
3. **Two copper oxides.** Concept. Red powder (boat paint) and black powder (pottery glaze) icons → "both are only copper and oxygen" → driving question at 56 px → 60 s timer, starter "I think the two powders have different formulas because…".
4. **Predict now.** Routine. Mg²⁺ with O²⁻ gives (MgO / Mg₂O₂ / MgO₂); the III in iron(III) chloride means (charge 3+ / three iron atoms / three electrons gained); calcium hydroxide is (Ca(OH)₂ / CaOH₂ / CaO₂H₂).
5. **Targets and words.** Summary. Five "I can" lines → words with icon, Spanish, meaning: cation (catión), anion (anión), charge (carga), formula (fórmula), subscript (subíndice), polyatomic ion (ion poliatómico), Roman numeral (número romano), parentheses (paréntesis). Color legend.
6. **Charges from the group.** Concept. `ionTable` g1 → g2 → g13 → g17 → g16 → g15 (-ide names appear) → rule card "metals lose 1, 2, 3; nonmetals gain to reach 8; anion name ends in -ide" → check: "Which ion does magnesium form?" (Mg⁺ / Mg²⁺ / Mg²⁻) → answer; two oral calls in the cue: K? S?
7. **The four to memorize.** Concept. `ionTable` tm → Fe²⁺/Fe³⁺ and Cu⁺/Cu²⁺ cards ("a version number, not a count") → Ag⁺ and Zn²⁺ ("one ion, no numeral") → real life: rust and hematite hold Fe³⁺ → memory card with the four, large → check: "Which metal needs a Roman numeral in its compound's name?" (zinc / silver / copper) → answer.
8. **Balancing the charges.** Concept. "Every + stud needs a − socket" → `chargeBlocks` ions(Ca, Cl) → add → balance (2+ and 2−) → formula CaCl₂ → name calcium chloride → rule card "total charge zero; the formula is the smallest set that balances" → check: "Na⁺ with O²⁻ balances as" (NaO / NaO₂ / Na₂O) → answer.
9. **Writing the formula.** Example. Rules appear: cation first, subscripts count ions, no 1 written → `chargeBlocks` ions(Al, O) → balance 6+ 6− → formula Al₂O₃ → `chargeBlocks` Mg/O reduce (Mg₂O₂ → MgO, "lowest ratio") → your turn: potassium sulfide → K₂S; calcium nitride → Ca₃N₂.
10. **The crisscross shortcut.** Example. `crisscross` Al/O ions → cross → check → Mg/O cross → reduce → rule card "cross, reduce, check: it is a shortcut, not the final answer" → check: "Crisscross gives Ca₂O₂. The formula is" (Ca₂O₂ / CaO / CaO₂) → answer.
11. **Naming binary compounds.** Concept. `nameBuilder` parts (potassium, sulf, -ide) → join "potassium sulfide" → anion table (fluoride, chloride, bromide, iodide, oxide, sulfide, nitride) → rule card "cation name, then anion root + -ide; no prefixes, the charges fix the ratio" → check: "Name CaBr₂" (calcium bromine / calcium bromide / calcium dibromide) → answer (note: dibromide accepted by IUPAC, not the common name); oral: MgO? Na₂S?
12. **The Stock system.** Concept. "iron(II) and iron(III) are two different ions, like version numbers" → `nameBuilder` numeral: iron(III) chloride FeCl₃ → iron(II) chloride FeCl₂ (same anion, different numeral and formula) → silver chloride, zinc oxide (no numeral) → `stockDetective` CuO → copper(II) oxide → `stockDetective` Cu₂O → copper(I) oxide ("two coppers share 2+, so each is 1+") → "this is the driving question answered" → check: "Name FeCl₂" (iron(I) chloride / iron(II) chloride / iron chloride) → answer.
13. **Formula in 3 steps, name in 2 parts.** Summary. Diagram builds: Ions → Balance → Write; Cation (+ numeral for Fe, Cu) → Anion -ide → retrieval, four items one per press: AlCl₃ name; K₂O name; calcium sulfide formula; FeO name. (Period 1 ends here.)
14. **Warm-up.** Your turn. Charge of a group 16 ion; formula of magnesium chloride; what the (III) means. Answer on each next press.
15. **Polyatomic ions.** Concept. "A squad: atoms that travel together and share one charge" → `polyIons` NH4 → OH → NO3 → CO3 → SO4 → PO4 (table row appears with each) → pattern card: "-ate means it has oxygen; nitrate is not nitride, sulfate is not sulfide" → memory card: "Nick the Camel ate Supper in Phoenix" (consonants = oxygens, vowels = charge) → check: "Sulfate, SO₄²⁻: which statement is right?" (each O is an oxide ion / it is the same as sulfide / the whole group carries 2−) → answer.
16. **Parentheses.** Concept. `parenBus` one (NaOH, no parentheses) → two → Ca(OH)₂ → wrong CaOH₂ → `chargeBlocks` NH4/SO4 → (NH₄)₂SO₄ → `chargeBlocks` Na/NO3 → NaNO₃ ("one squad, no parentheses") → rule card "never change the numbers inside a squad" → check: "Formula of magnesium nitrate" (MgNO₃ / Mg(NO₃)₂ / MgN₂O₆) → answer.
17. **The two-way road.** Example. Name → formula: aluminum sulfate: ions Al³⁺, SO₄²⁻ → balance 6 → Al₂(SO₄)₃ → formula → name: Cu₂S: anion 2− → each Cu 1+ → copper(I) sulfide → "check both ways: name it again, write it again" → check: "Name Fe₂(SO₄)₃" (iron(II) sulfate / iron(III) sulfate / iron sulfide) → answer.
18. **You do: six compounds.** Your turn. Sodium fluoride, calcium carbonate, ammonium sulfate (the shelf labels), MgBr₂, FeO, Zn(OH)₂ → 3 min timer → answers one row per press.
19. **Spot the error.** Your turn. Six wrong items, students call the fix, one press each: NaSO₄ → Na₂SO₄; Mg₂O₂ → MgO; CaOH₂ → Ca(OH)₂; Cu₂O "copper(II) oxide" → copper(I) oxide; FeCl₃ "iron chloride" → iron(III) chloride; NaNO₃ "sodium nitride" → sodium nitrate.
20. **Checkpoint routine.**
21. **Checkpoint 1** (4.2.2). "Al³⁺ and O²⁻: write the formula of aluminum oxide and explain how you know the ratio is right."
22. **Checkpoint 2** (4.2.3). "Iron forms FeCl₂ and FeCl₃. Name both and explain how you found each numeral."
23. **Checkpoint 3** (4.2.4). "Aluminum hydroxide is in some antacids. Write its formula and explain why it needs parentheses but NaOH does not."
24. **Predictions and exit ticket.** Routine. Slide-4 answers with hands up → CER exit ticket on the driving question, evidence from the two copper oxides.
25. **Rate your learning.** Review lines: 6–7, 8–10, 11–12, 15–16, 17–19.
26. **Next.** One line: missions for 4.2 (Name the compound, Build the formula, Find the error) and what Lesson 4.3 adds (prefix names for two nonmetals).

Blueprint alignment: 4.2.1 → 6–7; 4.2.2 → 8–10; 4.2.3 → 11–12; 4.2.4 → 15–16; 4.2.5 → 17–19. Slide checks: 8 (slides 6, 7, 8, 10, 11, 12, 15, 16, 17 hold nine; the blueprint line becomes "Slide checks: 9").

---

## 7. Language and narrative (every student-facing line)

Register: academic textbook language, simplified for 10th graders who are often English learners. The real terms stay (cation, anion, electronegativity, formula unit, polyatomic ion). Each term is introduced with a plain phrase once, then used in its academic form every time after. Teacher notes may use full academic register.

Sentence rules:
- One idea per sentence, 6 to 14 words, subject, verb, object, present tense, active voice.
- No thesis-style sentences: no "This lesson explores…", "It is important to note that…", "In order to…", no sentence that chains three claims with "because… which… so that…".
- No stacked nouns or passives ("the formation of ions is followed by the attraction of…"). Say what happens in order: "The atoms become ions. Then the ions attract."
- Symbols get words the first time: δ− "a small negative charge", ΔEN "the difference, larger minus smaller", subscript "the small number".
- Rule cards are complete sentences a student can copy into a notebook. Questions and cues are short imperatives: "Predict: which atom pulls harder?"
- Plain word first, academic word after, once: "pull (attraction)", "lets go of an electron (loses an electron)", "group of atoms with one charge (polyatomic ion)".
- Spanish cognates in parentheses once per term; never translate whole sentences.
- Each rule card restates the reading's Key idea in this register with the same glossary terms, so the slide and the reading agree.

Narrative thread, one per lesson, carried by the hook and returned to on every concept slide:
- 4.1, the rope. Tug of war → atoms pull on electrons the same way → even pull, shared pair → uneven pull, the pair leans → a blowout, the electron changes sides and the rope is gone, the pull between + and − remains → the meter (ΔEN) measures how uneven the pull is → the argument says how sure we are.
- 4.2, the code. Store labels are a code → the letters are ions and their charges → the rule is zero total charge → the name is the code read aloud → version numbers (Stock) → squads (polyatomic ions) and buses (parentheses) → read the code both ways.

Examples of the register:
| Not this | This |
|---|---|
| An ionic bond is the electrostatic attraction between oppositely charged ions that results from the transfer of valence electrons from a metal to a nonmetal. | A metal atom gives one electron to a nonmetal atom. Now both are ions. The + ion and the − ion pull on each other. That pull is the ionic bond. |
| The crisscross method, while expedient, necessitates subsequent reduction to the lowest whole-number ratio. | Crisscross is a shortcut. It can give Mg₂O₂. Reduce it to MgO. |
| Polyatomic ions retain their structural integrity across compounds. | A polyatomic ion stays together. Its atoms move as one group with one charge. |
| Electronegativity differences near the boundary values provide weak evidence for bond classification. | MgCl₂ scores 1.85, just above 1.8. The number alone is weak evidence. Look at the table too: a metal with a nonmetal. |

Readability target: Flesch-Kincaid grade 6 to 7 for the student-facing text of each slide, never above 8 (checked by the audit in section 10).

---

## 8. Teacher notes (per frame, in the notes panel and the print run-sheet)

Each frame's note has: time in minutes, what to say or ask in one or two lines, the prediction to collect before the press, the misconception to listen for, and the feedback for each wrong option of a check. Safety and sources go in the cover notes only (sodium in chlorine by video; Pauling values as in Lesson 3.3; NIST energies; OpenStax guide; Shannon ion sizes; IUPAC Red Book 2005 for names).

---

## 9. Files

- `unit4/slides-4-1.html`, `unit4/slides-4-2.html`: new standalone pages. Head block (title, description, icons, Open Graph) in the same form as the other unit pages so the site stays consistent; fonts from Google Fonts as the rest of the site; everything else inline.
- `unit4/blueprint.html`: deck sizes (25, 26), period splits (1–13 / 14–25 and 1–13 / 14–26), slide-check counts, slide numbers in the 4.1 and 4.2 sections and in the matrix rows 4.1.1 to 4.2.5.
- `plans/verify/`: screenshots and audit output from section 10.
- No change to readings, missions, index, case file or other decks.

---

## 10. Verification (Playwright scripts kept in the scratchpad, results in `plans/verify/`)

1. Walk: open the deck at 1920 x 1080, press `F5` (no reload), then `PageDown` until the end, screenshot each press. Assert per press: no console error, cue present, no block extends past the slide by more than 1 px, frame or slide advanced.
2. Back: from the end press `PageUp` to the start; at each landing compare each animation's `get()` with the forward record.
3. Font floor: per slide at its last frame, list visible text below 34 px on the canvas (allow cue and section label at 26 px). Expect an empty list.
4. Clicker keys: `.` zooms, `.` `.` blanks, `Escape` unwinds, `PageDown` with `repeat` is ignored, a focused `<select>` does not swallow keys.
5. Blueprint: every slide number in the 4.1 and 4.2 sections and matrix rows matches the new decks.
6. Both themes for steps 1 and 3; contact sheets viewed before each gate.
7. Readability: a script collects the student-facing text of each slide (all blocks, excluding notes, cue and section label), computes Flesch-Kincaid grade and average sentence length, and flags any slide above grade 8 or above 14 words per sentence, plus any sentence that starts with "This lesson", "It is important", "In order to".

---

## 11. Ordered implementation steps (confirmation gate after each)

Step 0. Setup. Read this plan, both readings and the blueprint sections for 4.1 and 4.2. Copy the head block pattern from `unit4/index.html`. Gate: list any content question.

Step 1. Runtime and visual system (section 3) as a demo deck of six slides, one per template, with a stub animation, timers, zoom, blank, notes, print run-sheet, both themes. Run the walk, keys and font scripts. Gate: screenshots.

Step 2. Animations for 4.1 (section 4.1), each shown on a scratch slide through all stages, both themes, reduced motion. Gate: one screenshot per stage.

Step 3. Deck 4.1 (section 5): 25 slides, frames, cues, checks, notes, Spanish terms, icons. Gate: walk, back, font audit, readability audit, contact sheet.

Step 4. Blueprint references for 4.1; commit "New 4.1 deck: clicker-driven, scaffolded, projector-scale". Gate.

Step 5. Animations for 4.2 (section 4.2). Gate.

Step 6. Deck 4.2 (section 6): 26 slides. Gate: walk, back, font audit, readability audit, contact sheet.

Step 7. Blueprint references for 4.2; all scripts on both decks in both themes; commit "New 4.2 deck: clicker-driven, scaffolded, projector-scale"; push. Gate: final report with contact sheets.

Sizing: runtime about 350 lines; each animation 120 to 250 lines; each deck about 900 lines of markup plus frames and notes.

---

## 12. Assumptions (say so if any is wrong)

1. The new files replace the old ones at the same paths; the old decks are not kept.
2. Blank button: one press zoom, two presses blank screen.
3. Checks are hands-up reveals, not mouse multiple choice.
4. Sans-serif type on the slides, serif stays in the readings.
5. 2D drawings for molecules and polyatomic ions; no 3D on the projector.
6. Illustrations are SVG; photos only if the user supplies files.
7. Decks 4.3 to 4.5 are out of scope; the runtime is written so they can be rebuilt on it later.
