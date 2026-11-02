# Plan: rebuild the Unit 4 slide decks for lessons 4.1 and 4.2

Target files: `unit4/slides-4-1.html`, `unit4/slides-4-2.html`, plus slide references in `unit4/blueprint.html`.
Branch: `claude/unit-4-chemistry-slides-j62190`.
Implementer: Opus 5.5 in a new thread. Every numbered step in section 11 ends with a confirmation gate.

---

## 1. What exists today (evaluation)

### 1.1 Reading material (source of truth for content)
- `reading-4-1.html`: five sections (three kinds of bonds, forming ions, ionic bonds and the crystal, covalent bonds, polar and nonpolar, metallic bonds, the electronegativity difference, evidence from the periodic table, writing a bonding argument). Objectives 4.1.1 to 4.1.5. Guide: below 0.4 nonpolar, 0.4 to 1.8 polar, above 1.8 ionic, taught as a continuum with exceptions. Pauling values: Na 0.93, Cl 3.16, H 2.20, O 3.44, F 3.98, C 2.55, S 2.58, N 3.04, Mg 1.31, K 0.82, Li 0.98, Ca 1.00, Fe 1.83.
- `reading-4-2.html`: charges from the group number, transition metals (Fe, Cu two ions; Ag, Zn one ion), balancing charges (tile model), writing the formula (lowest ratio, crisscross as a check), naming binary compounds (-ide), Stock system, six polyatomic ions (ammonium, hydroxide, nitrate, carbonate, sulfate, phosphate), parentheses, name to formula and back, checking errors. Objectives 4.2.1 to 4.2.5.
- Every slide check item already exists in each deck's item bank (`u41-s1` to `u41-s8`, `u42-s1` to `u42-s8`). Keep them: the blueprint's alignment matrix depends on them.

### 1.2 The existing decks (what to keep)
- Standalone HTML, everything inline. No build kit in this repo (the blueprint mentions `kit/build.py`, which is not here). Edits are made directly in the built HTML. Both decks carry an identical copy of the engine and of the simulation kit, so engine changes are made once and copied.
- Canvas 1600 x 900 scaled to the screen, `#deck` base font 32 px. Sections, step rail, `data-step` builds (`.fut` hides future steps), teacher notes panel (N), overview (O), zoom (Z or double click), theme, full screen, auto-fit text, timers, predictions saved in `localStorage`, checkpoint routine with Think/Talk/Write timers, CER exit ticket, self-rating.
- Simulations (canvas 2D, in the shared `U2` kit): `ionTransfer` (Atoms, Transfer, Ions, Attract, Crystal; Touching/Spread out; pick Center/Face/Edge/Corner), `molView` (molecules and polyatomic ions, ball-and-stick/space-filling/textbook views, drag to turn), `bondExplorer` (pair selector, continuum bar, "Choose from the table"), `metalSea` (Cations, Electrons, Moving, Current; Na/Mg/Al), `ionTiles` (Ions, Balance, Formula, Name; cation and anion selects; +/− tiles; free mode). All good and chemically careful. Keep all five.

### 1.3 Where the decks fail the brief
1. Clicker. PageDown/PageUp drive deck steps only. Every simulation stage, pair/ion/view selector, "Play", answer check, prediction button, timer restart and zoom needs the mouse. F5 reloads the page. The period key does nothing. Key repeat is not guarded (a held button skips steps). If a `<select>` has focus after a mouse click, the key handler ignores the clicker.
2. Legibility from the back row. On the 900 px canvas: body 32 px (about 19 pt on a printed slide), `.sm` 27 px (16 pt), simulation messages 21 px (13 pt), source lines 15 px, rail 18 px, readout labels 19 px. Rule of thumb for a classroom projector: nothing student-facing under 24 pt, which is 40 px on this canvas. Roughly half of each slide is below that.
3. Openers. Driving-question slides are observation tables. No kid-level hook, no physical metaphor, no animation on entry.
4. Scaffolding and retrieval. Order of concepts is right, but each slide is three dense cards plus a simulation. One multiple-choice check per slide, mouse-driven. No retrieval at the start of period 2, no quick "your turn" after each concept, no one-picture summary.
5. Animations. The five sims are the only motion. The continuum, the ions periodic table, the crisscross and the Stock breakdown are static SVG.
6. ELL. Sentence frames and word banks exist. Spanish terms exist only in the reading glossary. No color legend, no icons beside terms.
7. Teacher mobility. Notes live in a laptop-only panel. Nothing on screen tells the teacher what the next press will do.

---

## 2. End goal (work backwards from this)

Definition of done, checked by the verification scripts in section 10:
- A teacher runs each lesson, both periods, start to finish with only the four R800 buttons. The laptop is never touched after opening the deck in full screen.
- Every reveal, simulation stage, zoom, timer start and answer is one Next press. Back restores the previous state exactly.
- No student-facing text below 30 px on the canvas; body text 40 px; headings 60 px.
- Each lesson follows: hook (real life, kid level) → concept in one picture → example → your turn → next concept, with a one-picture summary at the end of period 1 and a retrieval warm-up at the start of period 2.
- Eight item-bank checks per deck kept, so the blueprint's "slide checks: 8" and alignment matrix stay true after the slide numbers are updated.
- Playwright walk-through of every step of both decks: no overflow, no console errors, every step has a footer cue, screenshots archived.

---

## 3. Domain model

| Entity | Meaning | Where it lives |
|---|---|---|
| Deck | One lesson, 25 to 26 slides, two periods | `section.slide` list |
| Slide | One screen with a title, eyebrow (section · reading §), beats, notes | `section.slide[data-title][data-sec]` |
| Beat | A labeled teaching move shown as a rail pill (at most 4 per slide) | `data-rail="Teams|Even match×2|Blowout×3|So what"`; `×n` declares n micro-steps |
| Step | Flat integer the clicker advances; beats own consecutive steps | existing `step`, `K(i)` |
| Action | What a step does: reveal (default), sim state, zoom target, timer, sample answer, blank | `TOUR[slide][step]` table in deck JS, plus `data-step` on elements |
| SimController | Methods a simulation exposes for scripted use | `root.api` set by each `U2.*` sim |
| Tour | Ordered sim states for one slide, one per step, each a full state (idempotent) | `TOUR` entries, e.g. `{sim:0, state:{stage:2}}` |
| Cue | Short footer text saying what Next does | `data-cue` per step element, default = next beat label |
| Clicker map | R800 button → key → deck action | engine key handler |
| Check | Item-bank question rendered as reveal (question step, answer step) | `data-q` rendered in `reveal` mode |
| Hook | First content slide of a lesson: real-life scene with animation | new sims `tugOfWar`, `labelRead` |

Rule for tours: a step declares the complete sim state, never a delta, so PageUp re-applies the earlier state and the sim lands where it was.

---

## 4. Engine changes (identical in both decks)

### 4.1 Clicker map (Logitech R800)
| Button | Key sent | Deck action |
|---|---|---|
| Next (▶) | `PageDown` | `next()`: next step, or next slide after the last step |
| Back (◀) | `PageUp` | `prev()`: previous step with state restored, or previous slide at its last step |
| Start/stop (slideshow) | `F5` first press, `Escape` second | `F5`: `preventDefault`, request full screen if not in it, else no-op. `Escape`: close in this order: blank screen, zoom, overlay, notes; otherwise leave to the browser (exits full screen) |
| Blank screen | `.` (map `b`/`B` too) | Single press: zoom toggle on the current step's focus. Second press within 400 ms: undo the zoom and toggle the blank (black) overlay. Any key leaves the blank |

Rules:
- Ignore `e.repeat` for PageDown, PageUp, period and F5. Debounce PageDown/PageUp at 180 ms.
- Handle the keys regardless of focus except inside `textarea`. After any mouse click on a sim control, `blur()` it so the clicker keeps working.
- Keep laptop keys: arrows, Shift+arrows, N, O, Z, Home, End.
- Update the cover's "how to" strip to show the four R800 buttons with their actions, plus the laptop keys in smaller type.

### 4.2 Step actions
- Add `TOUR` (per deck): `TOUR[slideIndex] = {stepNumber: {sim: indexWithinSlide, state: {...}, zoom: 'selector', timer: seconds, sample: true, cue: 'text'}}`.
- In `setStep()`, after `applySteps`, apply the action for the new step: find `[data-sim]` elements in the slide, call `el.api.set(state)`; apply zoom (`zoomOn(target)`) when `zoom` is set, `zoomOff` otherwise; start the timer; toggle `show-sample`.
- When entering a slide at step 1 (forward) or at the last step (backward), apply that step's action too, so a slide always opens in a consistent state.
- Rail: a beat label with `×n` covers n flat steps. The pill shows the beat label plus a dot row for its micro-steps (`●●○`). Pills stay at most 4 per slide.

### 4.3 Sim APIs (`root.api`)
Each sim sets `root.api = {set(state), get()}` and keeps its mouse controls. `set` updates internal state, syncs the visible control buttons (`seg.set`, `steps.set`, selects) and kicks the loop.
- `ionTransfer`: `{stage: 0..4, spread: bool, pick: null|'center'|'face'|'edge'|'corner'}`.
- `molView`: `{mol: key, view: 'ball'|'space'|'text', angles: bool}`. Also `spin: bool` for a slow auto-turn while the step is shown (stop on reduced motion).
- `bondExplorer`: `{pair: 'H-Cl'}` from the configured pairs; `{a: 'Fe', b: 'Cl'}` for any pair (same as "Choose from the table").
- `metalSea`: `{stage: 0..3, metal: 'Na'|'Mg'|'Al'}`.
- `ionTiles`: `{stage: 0..3, cation: 'calcium', anion: 'chloride', nCat: n, nAn: n}` (counts only in free mode).
- New sims in section 6 follow the same pattern.

### 4.4 Checks as reveals
- Render `[data-q]` items in reveal mode: step n shows the question and the three options (students answer by fingers A/B/C, whiteboards or notebooks); step n+1 marks the correct option, dims the others and shows the feedback line of the correct option. Wrong-option feedback goes into the teacher notes for that step ("if students chose B: ...").
- Mouse clicks on options still grade immediately (laptop use), but the clicker path never needs them.
- Predictions slide: keep the buttons (optional mouse polling), but the flow is hands-up. The revisit slide shows "Answer: ... because ..." and "Hands up if you predicted this." Remove the "You predicted: no prediction" text when nothing is stored.
- Exit ticket: "Show the sample answer" becomes a step (`sample: true`) instead of a button.

### 4.5 Footer cue
- Replace the small footer title with `#cue`: "Next ▶ Transfer the electron" at 26 px, from `data-cue` on the step element or the tour entry, default the next beat's label, "Next slide: <title>" at the last step. Keep the slide counter.

### 4.6 Type scale (student-facing floor 30 px, body 40 px)
| Element | Now | New |
|---|---|---|
| `#deck` base | 32 px | 40 px |
| `h2` | 1.55em (50 px) | 1.5em (60 px) |
| `.eyebrow`, `.label` | 0.56em (18 px) | 0.65em (26 px), teacher-facing meta only |
| `.sm` | 0.86em (27 px) | 0.85em (34 px) |
| `.dq`, key idea | 1.22em (39 px) | 1.2em (48 px) |
| Check question `h3` / options | 32 / 27 px | 40 / 34 px |
| Table `table.t` | 0.92em | 0.9em (36 px), fewer columns |
| Rail pills | 18 px | 22 px, at most 4 pills |
| `window.U2FONTK` (canvas text) | 1.35 | 1.75 |
| `.slide .say` (sim message) | 21 px | `max(.75em, 30px)` |
| `.slide .simnote` (sources) | 15 px | `display:none` on slides; text moved to notes |
| `.ros` readouts | 19 / 30 px | 26 / 34 px |
| Sim step/seg buttons | 22 px | 28 px |
| Footer cue | 13 px | 26 px |
| Projector floor rule (line ~654) | 18 px | 30 px for student-facing text, 24 px for `.eyebrow/.label` |
| Auto-fit minimum scale | 0.76 (body), 0.66 (cards) | 0.85 and 0.8; if a slide still overflows, cut words, never shrink further |

Content budget: at most 40 words of student-facing prose per slide outside tables and sim labels. One idea per card. A card is either a picture, a rule, an example or a question, never two of those.

### 4.7 Other engine items
- Blank overlay: full-canvas black `div`, `z-index` above zoom; exits on any key.
- Zoom: for a sim step the target is the `.cv` canvas; cards stay the default target; cap `k` at 3 (exists).
- Print run-sheet: `@media print` hides the deck and prints, per slide: number, title, beats, notes list. Two or three pages per lesson for the teacher's hand.
- Reduced motion: existing `REDUCED` flag applies to every new animation (jump to end state).
- Color code everywhere: cation red (`#B5523B` family, existing tile red), anion blue (existing tile blue), shared pair / electrons the existing violet dot, δ+ warm, δ− accent. Add a one-line legend strip on slides that use the colors.

---

## 5. Lesson 4.1, Predicting bond type: 25 slides

Period 1: slides 1 to 13. Period 2: slides 14 to 25.
Slide line format: number, title, beats (×micro-steps), what each Next press shows, check item.

1. **Cover.** Title, existing Na/Cl/salt illustration, R800 how-to strip. No steps.
2. **Hook: Tug of war** (new sim `tugOfWar`). Beats: Teams | Even match ×2 | Mismatch ×2 | Blowout ×3 | So what.
   Teams: two teams of stick figures hold a rope; the knot is a glowing pair of dots. "Who wins the rope?"
   Even match: same strength → knot stays in the middle (label: "shared equally").
   Mismatch: right team stronger → knot slides toward them, both still hold ("shared, but unequally").
   Blowout: right team far stronger → rope yanked all the way over; the rope fades; the teams now carry + and − signs and slide together ("the pull between + and − is the bond").
   So what: "Atoms do this with electrons. Pulling strength = electronegativity (Lesson 3.3)." Three labels appear under the three outcomes: nonpolar covalent, polar covalent, ionic. Metallic is not on this slide (slide 11 gets its own hook).
3. **Driving question.** Beats: Observe | Ask | Write (timer 60 s). Observe card is one line each for sodium, chlorine, salt (video cue in notes). The question in 48 px. Sentence starter.
4. **Predict now.** Beats: Q1 | Q2 | Q3 | Confidence. Same three questions as today (salt particles, HCl pair, copper wire). Hands up per option.
5. **Targets and words.** Beats: Targets | Words. Five "I can" lines in kid wording. Word strip: ionic bond (enlace iónico), covalent bond (enlace covalente), metallic bond (enlace metálico), electronegativity (electronegatividad), partial charge (carga parcial), crystal lattice (red cristalina), molecule (molécula), electron sea (mar de electrones). Each term gets a 60 px icon that returns later on the summary slide.
6. **Three kinds at one scale.** Beats: Sodium | Chlorine | Salt | Bond ×2. Existing to-scale SVG, one panel per press, then the definition "a chemical bond is a strong attraction between + and −". Check `u41-s1` (what is a chemical bond): question, then answer.
7. **Forming ions.** Beats: Two atoms | Transfer ×2 | Ions | Your turn ×2. `ionTransfer` tour: stage 0 → 1 (electron moves) → 2 (charges and sizes) with the energy readout called out in the cue ("the transfer alone costs energy"). Check `u41-s2` (Mg loses two electrons → Mg²⁺).
8. **The crystal.** Beats: Attract | Crystal ×3 | Key idea | Your turn ×2. Tour: stage 3 → stage 4 → spread out → pick center (six neighbors highlighted) → pick corner (fewer only because the drawing stops). Key idea card: "the bond is the attraction; NaCl is a ratio, not a molecule". Check `u41-s3` (six chloride ions).
9. **Covalent bonds.** Beats: Even teams | Share ×3 | Molecule. Small `tugOfWar` replay of the even match (one press), then `molView` tour: H₂ textbook drawing (the shared pair) → H₂ ball-and-stick → Cl₂ textbook (eight around each Cl) → Cl₂ space-filling with spin. One card: "covalent bond = a shared pair; a group of atoms joined this way = a molecule." History reduced to one line in notes.
10. **Polar and nonpolar.** Beats: Equal | Unequal ×3 | δ marks | Your turn ×2. `bondExplorer` tour: H–H → C–H → H–Cl → H–O → H–F, cue before each: "predict: which atom pulls harder?" Card with δ+/δ− rule. Check `u41-s4` (O–H: hydrogen is δ+).
11. **Metallic bonds.** Beats: Beach ball | Electron sea ×4 | Other metals ×2 | Limits | Your turn ×2. Hook: `crowdBall` mini-animation (a crowd passing beach balls that belong to everyone). `metalSea` tour: Cations → Electrons → Moving → Current, then Mg, then Al (more balls per person). Limits card: "real electrons are waves, real metal is 3D". Check `u41-s5` (why copper conducts).
12. **One picture for three bonds** (period 1 summary, the memory anchor). Beats: Pictures | Who | What holds | Rule. A three-column diagram built in SVG: ionic (+ − grid), covalent (two atoms with a shared dot pair), metallic (+ cores in a tinted sea), each with its slide-5 icon. Rows appear per press: particles, what holds them, one example. Last press: the one-sentence rule "metal + nonmetal → ionic; nonmetal + nonmetal → covalent; metal alone → metallic".
13. **Backpack sort** (retrieval). Beats: Items | Sort ×6. Six icons: salt packet, water bottle, phone charger cable (copper), soda can (aluminum), pencil graphite, the O₂ you breathe. Students call the bond type; each press flips one item to its answer with a four-word reason ("metal + nonmetal: ionic"). Timer 2 min optional on the Items beat.
14. **Warm-up: three quick questions** (period 2 start). Beats: Q1 ×2 | Q2 ×2 | Q3 ×2. "What particles are in solid salt?", "Which atom in HCl is δ−?", "What moves in a copper wire?" Question, then answer.
15. **The electronegativity difference.** Beats: Continuum | Guide ×3 | Example ×4. Existing continuum SVG made animated: the bar draws first, then the 0.4 and 1.8 marks, then the ten example bonds drop onto it one group per press. Worked NaCl: look up → subtract → place → check (the step cards). Cue: "always larger minus smaller".
16. **Evidence from the table.** Beats: Map ×2 | Rule | Near the line ×2 | Disagree | Your turn ×4. New `ptMap` SVG: periodic table outline, metals tint from the left, nonmetals from the right, staircase. Rule card (three lines from slide 12). `bondExplorer` tour: H–F (1.78, molecular, boils at 20 °C) then Mg–Cl (1.85, melts at 714 °C): "near 1.8 the number alone is weak evidence". Disagree: Fe–Cl (1.33) still named ionic, names follow composition. Checks `u41-s6` (CaO) and `u41-s7` (FeCl₃).
17. **Bonding argument: I do, we do.** Beats: Parts | KF ×4 | HCl ×4. Four-part table (claim, evidence, reasoning, strength). KF filled one part per press. HCl: students supply each part before the press (difference 0.96, both nonmetals, strong because far from both lines). Check `u41-s8` folded in as the last press of the HCl column (which evidence best supports the KF claim).
18. **You do: three bonds.** Beats: Predict (timer 3 min) | Answers ×3. LiF, N–H, C–S cards; answer table reveals one row per press.
19. **Checkpoint routine.** Beats: Routine | Self-check. Unchanged.
20. **Question 1** (4.1.1, transfer is not the bond). Think 30 s | Talk 60 s | Write | Self-check | Compare. Unchanged content.
21. **Question 2** (4.1.2, Cl₂ vs HCl). Unchanged.
22. **Question 3** (4.1.3, copper wire). Unchanged.
23. **Check your predictions.** Beats: Salt | Shared pair | Copper | Reflect. Hands-up wording.
24. **Exit ticket: CER.** Beats: Claim | Evidence | Reasoning | Self-check | Sample. Sample shown by step.
25. **Rate your learning.** Review buttons jump to slides 6–8, 9–10, 11, 12–16, 17–18.

Alignment after the rebuild: 4.1.1 → 6 to 8; 4.1.2 → 9 to 10; 4.1.3 → 11; 4.1.4 → 12, 13, 15, 16; 4.1.5 → 17, 18, 24. Checks: s1 slide 6, s2 slide 7, s3 slide 8, s4 slide 10, s5 slide 11, s6 and s7 slide 16, s8 slide 17.

---

## 6. Lesson 4.2, Ionic compounds: formulas and names: 26 slides

Period 1: slides 1 to 13. Period 2: slides 14 to 26.

1. **Cover.** Existing copper oxides illustration, R800 strip.
2. **Hook: Read the label** (new `labelRead` SVG scene). Beats: Labels ×3 | Code. Three products from a store shelf: toothpaste (sodium fluoride), antacid (calcium carbonate), lawn fertilizer (ammonium sulfate). Each press zooms one label and reads the chemical name aloud. Last press: "Chemical names are a code. By the end of this lesson you can read all three and write their formulas." (The three come back on slide 18 as practice.)
3. **Driving question: two copper oxides.** Beats: Powders | Ask | Write (timer 60 s). Red powder in boat paint, black powder in pottery glaze; both only copper and oxygen. Question in 48 px.
4. **Predict now.** MgO formula, the III in iron(III), Ca(OH)₂. Hands up.
5. **Targets and words.** Terms with Spanish: cation (catión), anion (anión), charge (carga), formula (fórmula), subscript (subíndice), polyatomic ion (ion poliatómico), Roman numeral (número romano), parentheses (paréntesis). Color legend: cation red, anion blue.
6. **Charges from the group.** Beats: Lose ×3 | Gain ×3 | Your turn ×2. New `ionTable` SVG (existing table redrawn as a stepped reveal): group 1 lights red with 1+, group 2 with 2+, group 13 (Al) with 3+; then group 17 blue 1−, 16 2−, 15 3−, with the -ide names appearing. Check `u42-s1` (Mg²⁺) plus two oral calls (K? S?).
7. **The four to memorize.** Beats: Two ions ×2 | One ion | Memory. Fe²⁺/Fe³⁺ and Cu⁺/Cu²⁺ ("a version number, not a count"), Ag⁺ and Zn²⁺. Real life: rust and hematite hold Fe³⁺. Memory card: the four symbols with charges, large.
8. **Balancing the charges.** Beats: Fit ×1 | Calcium chloride ×4 | Aluminum oxide ×3 | Your turn ×2. LEGO framing: "every + stud needs a − socket" (the tiles already draw studs and sockets). `ionTiles` tour: Ca/Cl Ions → Balance → Formula → Name; then Al/O Ions → Balance → Formula. Check `u42-s2` (Na₂O).
9. **Writing the formula.** Beats: Rules ×3 | Lowest ratio ×2 | Try two ×2. Order, subscripts, no 1. Lowest ratio: `ionTiles` Mg/O shows Mg₂O₂ tiles collapsing to one pair → MgO (new `reduce` state in the sim, or an SVG animation). Try two: K₂S and Ca₃N₂ revealed.
10. **The crisscross shortcut.** Beats: Cross ×2 | Reduce | Check ×2. New `crisscross` SVG animation: the charge numbers slide diagonally into the subscript positions for Al³⁺/O²⁻, then for Mg²⁺/O²⁻ with the reduce step. Check `u42-s3` (CaO, not Ca₂O₂).
11. **Naming binary compounds.** Beats: Two parts ×3 | -ide table | Your turn ×3. New `nameBuilder` DOM widget: cation name tile + anion root tile + "-ide" tile snap together (potassium + sulf + ide). Anion table (seven rows, 36 px). Check `u42-s4` (CaBr₂) plus two oral calls (MgO, Na₂S).
12. **The Stock system.** Beats: Version number | Iron ×3 | No numeral ×2 | Detective ×4 | Your turn ×2. `ionTiles` tour: iron(II) chloride → iron(III) chloride (same anion, different numeral and formula) → silver chloride → zinc oxide (no numeral). Detective: CuO: anion 2− → copper 2+ → copper(II) oxide; Cu₂O: two coppers share 2+ → copper(I) oxide. This answers the driving question. Check `u42-s5` (FeCl₂).
13. **Formula in 3 steps, name in 2 parts** (period 1 summary). Beats: Formula ×3 | Name ×2 | Retrieval ×4. Diagram: Ions → Balance → Write; Cation (+ numeral if Fe or Cu) → Anion -ide. Retrieval: four fast items revealed one by one (AlCl₃, name of K₂O, formula of calcium sulfide, name of FeO).
14. **Warm-up: three quick questions.** Charge of a group 16 ion; formula of magnesium chloride; what the (III) means.
15. **Polyatomic ions.** Beats: A squad | Six ions ×6 | Pattern ×2 | Your turn ×2. "A squad: atoms that travel together with one charge." `molView` tour through NH₄⁺, OH⁻, NO₃⁻, CO₃²⁻, SO₄²⁻, PO₄³⁻ with slow spin; table row appears with each. Pattern: "-ate has oxygen; nitrate is not nitride, sulfate is not sulfide" and the mnemonic "Nick the Camel ate Supper in Phoenix" (consonants = oxygens, vowels = charge: NO₃⁻, CO₃²⁻, SO₄²⁻, PO₄³⁻). Check `u42-s6` (sulfate).
16. **Parentheses.** Beats: The squad bus ×2 | Build ×3 | Your turn ×2. New `parenBus` SVG: one OH⁻ squad, then two squads each boxed → Ca(OH)₂; the wrong CaOH₂ crossed out with "one O, two H". `ionTiles` tour: Ca/OH → NH₄/SO₄ → Na/NO₃ (no parentheses). Check `u42-s7` (Mg(NO₃)₂).
17. **The two-way road.** Beats: Name → formula ×3 | Formula → name ×3 | Check both ways | Your turn ×2. Al₂(SO₄)₃ built step by step; Cu₂S named step by step; "name it again, write it again". Check `u42-s8` (Fe₂(SO₄)₃).
18. **You do: six compounds.** Beats: Work (timer 3 min) | Answers ×6. Three names to formulas including the three label compounds from slide 2 (sodium fluoride, calcium carbonate, ammonium sulfate), three formulas to names (MgBr₂, FeO, Zn(OH)₂). One row per press.
19. **Spot the error.** Beats: Errors ×6. The reading's six mistakes (NaSO₄, Mg₂O₂, CaOH₂, Cu₂O as copper(II) oxide, FeCl₃ as iron chloride, NaNO₃ as sodium nitride). Students name the fix; each press shows it.
20. **Checkpoint routine.**
21. **Question 1** (4.2.2, Al₂O₃). 22. **Question 2** (4.2.3, FeCl₂ and FeCl₃). 23. **Question 3** (4.2.4, Al(OH)₃). Unchanged content.
24. **Check your predictions.** 25. **Exit ticket: CER.** 26. **Rate your learning** (review 6–7, 8–10, 11–12, 15–16, 17–19).

Alignment after the rebuild: 4.2.1 → 6 to 7; 4.2.2 → 8 to 10; 4.2.3 → 11 to 12; 4.2.4 → 15 to 16; 4.2.5 → 17 to 19. Checks: s1 slide 6, s2 slide 8, s3 slide 10, s4 slide 11, s5 slide 12, s6 slide 15, s7 slide 16, s8 slide 17.

---

## 7. New animations and simulations (specs)

All canvas 2D or inline SVG in the existing kit style (`shell`, `loop`, `fit`, theme tokens, `REDUCED`). Each exposes `root.api.set(state)`. Text inside them at least 30 px on the canvas (use `F()` with `U2FONTK`).

| Name | Type | States | Notes |
|---|---|---|---|
| `tugOfWar` | canvas | `{mode: 'teams'|'even'|'uneven'|'blowout'|'labels', strength: [a,b]}` | Stick-figure teams (4 each), rope, knot = two violet dots. `uneven` eases the knot toward the stronger side in proportion to the difference; `blowout` pulls it fully, fades the rope, paints + and − on the teams and slides them together. `labels` prints the three bond names under three mini-frames. Honest caption: "a model: the knot is the shared pair; in the blowout the rope is gone and the pull between + and − is the bond". |
| `crowdBall` | canvas | `{mode: 'crowd'|'balls'|'pass'}` | 6 x 4 grid of heads (+ cores) and 6 beach balls drifting between them. Two presses, then the slide switches to `metalSea`. |
| `continuum` | SVG + JS | `{marks: bool, group: 0..3}` | The existing continuum drawing with staged reveal: bar, 0.4/1.8 lines, then bond markers in four groups. Marker drop animation 300 ms. |
| `ptMap` | SVG + JS | `{metals: bool, nonmetals: bool, pair: ['Na','Cl']}` | Periodic table outline, tints, staircase; `pair` lights two cells and draws a line between them. |
| `ionTable` | SVG + JS | `{groups: ['1','2','13','17','16','15'] prefix, tm: bool}` | Existing ions table redrawn so each group lights in order with its charge and -ide name. `tm` shows Fe/Cu/Ag/Zn. |
| `crisscross` | SVG + JS | `{pair: 'AlO'|'MgO', phase: 'ions'|'cross'|'reduce'|'check'}` | Charge digits travel diagonally (600 ms) to subscript positions; reduce shows ₂₂ → nothing; check shows 2×3+ = 6+, 3×2− = 6−. |
| `nameBuilder` | DOM | `{cation, anion, numeral, phase: 'parts'|'join'}` | Three tiles slide together into one name; numeral tile only for Fe/Cu. Reverse mode for the detective on slide 12. |
| `parenBus` | SVG + JS | `{ion: 'OH', n: 1|2, wrong: bool}` | A squad in a rounded box; with n = 2 two boxes become parentheses with a subscript outside; `wrong` draws CaOH₂ with a red strike and "1 O, 2 H". |
| `labelRead` | SVG + JS | `{focus: 0|1|2|null}` | Three product drawings; `focus` scales one label to full width with the name in 48 px. |
| `backpackSort` | DOM + SVG icons | `{revealed: n}` | Six item cards; each reveal flips to bond type and reason. |

`ionTiles` additions: a `reduce` state for slide 9 (two Mg²⁺ and two O²⁻ tiles collapse to one pair with the caption "2 : 2 → 1 : 1"), and `set()`.

---

## 8. Illustrations

- Inline SVG only, flat icon style: two fills plus one accent, 3 px strokes at canvas scale, fills from theme tokens so dark mode works, every label at least 28 px, `role="img"` with `aria-label`.
- Needed sets: tug-of-war figures, crowd and beach balls, backpack items (salt packet, water bottle, charger cable, soda can, pencil, air), store labels (toothpaste tube, antacid bottle, fertilizer bag), red and black powders (exist), squad and bus, periodic-table outline (exists in the kit data).
- Raster "generated images" are not possible for the implementer. `unit4/index.html` already embeds photos as base64 WebP, so if the user supplies photos (a real toothpaste label, rust, copper wire), they go in the same way; otherwise the SVG set stands.

---

## 9. ELL and scaffolding rules the implementer follows on every slide

- Term introduced = term shown with its icon, Spanish cognate in parentheses once, and a one-line meaning. Same icon on the summary slide.
- Sentence frames on every writing step (exist). Word bank chips at 34 px.
- Predict before reveal: every sim stage with a visible outcome gets a cue that asks for a prediction ("Which atom pulls harder?").
- I do, we do, you do order on slides 17/18 (4.1) and 12/17/18 (4.2).
- Retrieval: a "Your turn" on every concept slide, a summary diagram at the end of period 1, a warm-up at the start of period 2, a sort or spot-the-error game before the checkpoint.
- Teacher notes keep the timing per beat, the misconception to listen for, and the feedback for each wrong option of the check.

---

## 10. Verification (scripts in the scratchpad, results archived under `plans/verify/`)

1. **Walk script** (Playwright, 1920 x 1080, light and dark): open the deck, press `F5` (expect no reload, full screen attempt), then press `PageDown` until the last slide, screenshot after every press. Assert per step: no console error; `#cue` non-empty; no descendant of the visible slide extends past the slide box by more than 1 px (compute from bounding rects, skip `aside`); step counter advanced or slide changed.
2. **Back script**: from the last slide press `PageUp` to the start; at each landing compare the sim's `api.get()` with the state recorded on the forward pass.
3. **Font floor audit**: for each slide at its last step, list visible text nodes whose computed font size divided by the deck scale is below 30 px (allow `.eyebrow`, `.label`, `#cue` at 24 px). Expect an empty list.
4. **Clicker keys**: `.` zooms the current focus and `.` again within 400 ms blanks; `Escape` unwinds; `PageDown` with `repeat` flag is ignored; a focused `<select>` does not swallow `PageDown`.
5. **Blueprint cross-check**: a grep that every slide number named in `blueprint.html` sections 4.1 and 4.2 and in the matrix rows 4.1.x and 4.2.x matches the new numbering; every in-deck note that says "slide N" is updated (`grep -n "slide [0-9]"`).
6. Contact sheet of all screenshots viewed by the implementer before each gate.

---

## 11. Ordered implementation steps (each ends with a confirmation gate)

Step 0. Setup. Read this plan, the two decks' engine (lines ~2990 to end of `slides-4-1.html`) and the five sims. Run the baseline screenshot script. Create `plans/verify/`. Gate: report what was read and any contradiction found.

Step 1. Engine in `slides-4-1.html`: clicker map (4.1), step actions and `TOUR` (4.2), rail beats with `×n`, footer cue (4.5), blank overlay, zoom focus per step, print run-sheet, type scale (4.6), reveal-mode checks (4.4). No slide content changes yet. Run the walk script on the existing 22 slides. Gate: screenshots plus the audit lists.

Step 2. Sim APIs in `slides-4-1.html`: `ionTransfer`, `molView`, `bondExplorer`, `metalSea` get `root.api` (4.3) and blur-on-click. Wire a temporary tour on slide 6 to prove it. Gate.

Step 3. New sims for 4.1: `tugOfWar`, `crowdBall`, `continuum`, `ptMap`, `backpackSort` (section 7), with reduced-motion fallbacks and dark theme. Each tested on a scratch slide. Gate: screenshots of every state.

Step 4. Rebuild the 4.1 slide markup to section 5: 25 slides, beats, tours, cues, notes, Spanish terms, icons, summary diagram. Keep the item bank, glossary and kit untouched. Gate: full walk, back script, font audit, contact sheet.

Step 5. References for 4.1: `blueprint.html` section 4.1 (deck size 25, period split 1–13 / 14–25, slide numbers in the text), matrix rows 4.1.1 to 4.1.5, in-deck "slide N" mentions, `rateTargets` review numbers. Commit "Rebuild 4.1 deck for clicker-driven, scaffolded teaching". Gate.

Step 6. Port to `slides-4-2.html`: copy the engine block and the `molView` API from 4.1, add the `ionTiles` API with `reduce`. Walk the existing 23 slides. Gate.

Step 7. New sims for 4.2: `labelRead`, `ionTable`, `crisscross`, `nameBuilder`, `parenBus`. Gate: screenshots of every state.

Step 8. Rebuild the 4.2 slide markup to section 6: 26 slides. Gate: full walk, back script, font audit, contact sheet.

Step 9. References for 4.2 in `blueprint.html` and in-deck; final run of all five verification scripts on both decks in both themes; commit "Rebuild 4.2 deck for clicker-driven, scaffolded teaching"; push to `claude/unit-4-chemistry-slides-j62190`. Gate: final report with the contact sheets.

Sizing: steps 1, 4 and 8 are the large ones (engine ~250 lines; each deck's markup ~900 lines plus ~400 lines of tours and notes). Steps 3 and 7 are ~150 to 250 lines per sim.

---

## 12. Decisions needed before step 1

1. **Built files versus kit.** The decks are built output and the kit is not in this repo. Hand edits here are lost if the decks are ever rebuilt from the kit. Options: accept hand-edited builds for 4.1 and 4.2 (assumed), or add the kit to the repo first.
2. **Blank button meaning.** Single press = zoom, double press = blank screen (assumed). Alternative: single press = blank (PowerPoint habit), zoom moves to a tour step only.
3. **Checks as reveals.** Mouse multiple choice becomes question-then-answer with hands-up (assumed). Alternative: keep mouse grading and add a reveal fallback.
4. **Slide counts.** 4.1 grows from 22 to 25, 4.2 from 23 to 26; period 1 ends at slide 13 in both. Blueprint text changes accordingly.
5. **Photos.** None available to the implementer; SVG illustrations throughout unless the user supplies WebP/JPEG files for the store labels and the hook slides.
6. **Other decks.** 4.3 to 4.5 are untouched in this pass; the engine block can be ported to them later in one step each.
