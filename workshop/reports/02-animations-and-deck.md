# Report 02: The 5.1 animations and the 5.1 deck

Step: 02 · Lesson: 5.1 · Commit: none by the implementer (in-session; the orchestrator's work-in-progress snapshots are cccaf74 and 021f067; this report describes the working tree on `workshop/unit5-5-1` over 021f067)

## Done
Order as the brief: A (bench) → B (deck) → V (verification). Every file is under `tools/slides-kit/parts/lessons/5-1/` unless named otherwise.

**A1. `sims.html`**: the eleven animations of plan section 4 with exactly its stage names, each a `Deck.sim` over `Deck.canvasSim`, `params` per stage, tweens 600 to 900 ms, `live` for `coinScale:tally`, `howMany:zoom`, `secondsLine:line` (and the slow turn of the two 3D crystals), `units()` and `meta()` per section 4. Lesson data are constants at the top (coin masses, the bank bag 1,250.0 g / 250, the roll 200.0 g / 40, the hook jar 2,000.0 g / 400 from the reading's "Finish it", the cent jar 1,017.1 g, 267.69 g, 2.6769 g, about 380, about 407 and about 327, 6.02214076 and 6.022 × 10²³, May 20, 2019 and November 16, 2018, 12 and 500, Al 26.982, Cu 63.546, Si 28.085, 543.102 pm, 8 per cube, 564 pm, 3.156 × 10⁷ s, 4.5 × 10⁹ and 1.38 × 10¹⁰ years, 1.908 × 10¹⁶, 1.38 × 10⁶, 18 g, 496 kJ/mol and 8.24 × 10⁻¹⁹ J, the conversions). Drawing data, never printed: Cordero 2008 covalent radii (H 31, C 69, N 71, O 66, Na 166, Al 121, Si 111, Cu 132 pm), Shannon 1976 (Na⁺ 102, Cl⁻ 181 pm), NIST geometries (O–H 95.8 pm at 104.5°, C=O 116.0 pm at 180°, N–H 101.2 pm at 106.7°, O=O 120.8 pm). Molecules are ball and stick through `Deck.spheres` with CPK colors from the shared part and the symbol on every sphere; ions carry "+" or "−"; the silicon cell uses the diamond-cubic positions (95 atoms in a 2 × 2 × 2 block, 128 bonds, 54 cube edges drawn with `lines`). Every label is at 36 px or more; every primary shape (sphere, coin, cell, egg, card, badge) at 60 px or more; numbers are a label line then a chip in the quantity's color (grams `--warm`, moles `--accent`, particles `--e`, factors `--muted`, canceled units struck in `--bad`). Live stages move numbers only inside their own boxes (the coin counter, the cascade's counter and ladder, the time-line clock).

**A2.** `gen_scratch.py` → `scratch.html`: 78 scratch slides, one per stage in section 4's order, each host in the template the deck uses for that stage (hook, 52/48 concept with or without the caption column, wide with a 214 px band, the 40/60 example column). `scratch-check.js`: 346 assertions (every meta() fact of section 4, label floor, shape floor, live flags from meta() and from the layout audit's instrumentation, still frames under reduced motion, motion with motion on, 78 stages covered, no console errors).

**A3. Bench** (scratch deck md5 75ce51c878f92b289fdff7d06e8f5a55; `suite.py 5 1 --deck <scratchpad>/scratch51.html --only walk,back,fonts,layout,render3d,extras,zoom --theme both`): **11 of 11 PASS** (table below), `scratch-check.js` **PASS 346 of 346**. Sheets: `workshop/artifacts/02/bench/bench-light-1.jpg` to `-4.jpg` and `bench-dark-1.jpg` to `-4.jpg` (one frame per stage from the walk at 1.1 s, two motion-on moments at 1.4 s and 2.9 s for each live or turning stage; 33 to 412 KB each).

| Animation | Stages | Deck slides | Live / turning | Scratch-check | Bench audits (both themes) |
|---|---|---|---|---|---|
| coinScale | jar, guess, tally, scale, reveal; bag, zero, read, divide, count; roll (11) | 2, 6 | tally (live) | 57/57 | PASS |
| centJar | jar, wrong, sample, average, count, isotopes (6) | 7 | - | 24/24 | PASS |
| countingUnits | dozen, ream, mole, exact, constant (5) | 8 | - | 20/20 | PASS |
| howMany | one, dozen, thousand, zoom, mole, spoon (6) | 9 | zoom (live) | 30/30 | PASS |
| moleKinds | al, cu, compare, oxygen, four (5) | 10 | - | 20/20 | PASS |
| secondsLine | line, year, earth, universe, mole, times, spoon (7) | 11 | line (live) | 37/37 | PASS |
| moleHistory | avogadro, loschmidt, ostwald, perrin, si, exact (6) | 12 | - | 27/27 | PASS |
| siliconSphere | sphere, crystal, cube, atom, divide (5) | 13 | crystal, cube (turn) | 20/20 | PASS |
| moleMap | map; Cu, Fe, CO2m, H2Om × setup, cancel, result; half; energy/mole, energy/one, energy/why (17) | 16, 17, 20, 21 | - | 67/67 | PASS |
| naclCrystal | crystal, unit, count, wrong (4) | 18 | crystal, unit (turn) | 18/18 | PASS |
| atomCounter | H2O/one, H2O/mol, CO2/mol, CO2/atoms, NaCl/mol, NH3/mol (6) | 19, 20 | - | 24/24 | PASS |

Reduced motion: every live or turning stage holds one still frame (scratch-check, 7 assertions; extras on the bench's turning crystal). Bench overlap: 0 intersections in both themes, 78 frames, 3,997 boxes, 46 spheres scenes, 7 live frames at two moments each, 78 of 78 canvases instrumented.

Bench suite verdict lines:

| Audit | Result | Verdict line |
|---|---|---|
| walk light | PASS | walk light: 78 states, max empty 17% (s34f0), PASS |
| walk dark | PASS | walk dark: 78 states, max empty 17% (s34f0), PASS |
| back light | PASS | back: 78 forward, 78 back, PASS |
| back dark | PASS | back: 78 forward, 78 back, PASS |
| fonts light | PASS | fonts: PASS |
| render3d | PASS | render3d: PASS |
| extras | PASS | extras: PASS |
| zoom light | PASS | zoom light: 338 zoomed states over 78 frames (re-flow 10, transform 328), animation 78, part 250, caption 10; min fill 82%; Back tests 78; PASS |
| zoom dark | PASS | zoom dark: 338 zoomed states over 78 frames (re-flow 10, transform 328), animation 78, part 250, caption 10; min fill 82%; Back tests 78; PASS |
| layout light | PASS | layout light: 78 frames, 0 visible option lists (), max empty 17% (s34f0), gate 100%, clipped or ellipsized text: 0, overlap: 0 intersections on 0 frames, no baseline (3997 boxes (525 DOM boxes, 1208 canvas labels, 2264 canvas shapes), 134 covered canvas labels, 46 spheres scenes (live moments included), 78 of 78 canvas animations instrumented), live: 7 frames at two moment
| layout dark | PASS | layout dark: 78 frames, 0 visible option lists (), max empty 17% (s34f0), gate 100%, clipped or ellipsized text: 0, overlap: 0 intersections on 0 frames, no baseline (3997 boxes (525 DOM boxes, 1208 canvas labels, 2264 canvas shapes), 134 covered canvas labels, 46 spheres scenes (live moments included), 78 of 78 canvas animations instrumented), live: 7 frames at two moments,

**B1.** `mv unit5/slides-5-1.html unit5/old-slides/slides-5-1.html` (never opened); `unit5/old-slides/README.md` is the text of `unit4/old-slides/README.md` with Unit 5 (five lines; the active deck line names `unit5/slides-5-1.html`).

**B2 to B10.** `gen_slides.py` → `slides.html`: the 28 slides of plan section 5, ids `s01` to `s28`, hosts `s<NN>-sim` (slide 20 also `s20-ac`), `data-period` 1 for 1 to 14 and 2 for 15 to 28, every frame with a cue (`data-label` on revealed blocks, `label` on stage-only frames), minutes and a note (what to say or ask, the prediction, the misconception, the feedback per wrong option on answer frames). Eleven checks on slides 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 19 with `check()` (`right`, `ans`, `fb`), cues "check" and "answer"; the check frame re-stages the subject (6 `roll`, 7 `sample`, 8 `constant` on screen, 9 `spoon`, 10 `compare`, 11 `times`, 13 `cube`, 16 `Cu/result`, 17 `half`, 18 `unit`, 19 `CO2/mol`; chem.js asserts each). Predict now (slide 4, `data-mode="pick"`, Q1 stacked, Q2 and Q3 one row as the plan marks) returns on slide 26 with "Hands up if you predicted this." (each answer B; Q1 with the label line "Mass of one mole" and the chips "Al 26.982 g", "Cu 63.546 g"). Words slide: the four "I can" lines, eight `wcard`s with the sprite icons the brief names and the eight cognates (mol, número de Avogadro, constante de Avogadro, cantidad de sustancia, molécula, unidad fórmula, fórmula química, subíndice; chem.js checks them against the reading's glossary), the legend "grams (mass)", "moles (amount)", "particles (number)", "+ cation", "− anion", "atom (CPK color = element)". Caption "Atom colors show the element, not the charge." as a `.simcap` (34 px, a zoom unit) on slides 10 and 19. Timers: 3 60 s, 14 90 s, 15 90 s on frame 1 (`keys_cfg.tm` s15), 20 180 s, checkpoints 30, 60, 90 s, 26 180 s. Slides 11 and 12 on `t-concept wide` with the band row (`.ptrow`, `data-band` 236 and 214), slide 20 on `t-example` with the steps card first. `css.css` (marker `css-51`) holds only lesson rules (copied 4.2 rules: `.leftcol`, `.simcap`, `.mission`, `tfill`, `tnext`, `.tbl.compact`; plus the Unit 5 legend and chip colors and the fixes listed under Deviations). Rule cards as printed by the deck (after the tightenings in Deviations 4): slide 6 "If every object has the same mass, divide the total by one object's mass. The grams cancel. A pure number is left."; 7 "A mix of objects is counted with the average mass of one object. Average atomic masses let chemists count atoms the same way."; 8 "One mole contains exactly 6.02214076 × 10²³ particles. In calculations we round it to 6.022 × 10²³. A mole is a count, not a mass."; 9 "A mole is 6.022 × 10²³ particles. Molecules are so small that a mole of water is only about 18 g."; 10 "Always name the particle. It can be atoms, molecules, formula units or ions."; 11 (three lines) "At one particle each second, a mole takes about 1.9 × 10¹⁶ years." "That is 1.4 million times the age of the universe." "Yet a mole of water is only about 18 g."; 12 "Since May 20, 2019 the number is exact: 6.02214076 × 10²³. It is no longer measured."; 13 "The atoms of a crystal repeat in identical cubes. Count one cube and measure its size. Then the whole sphere is counted."; 16 "Particles = moles × 6.022 × 10²³. The unit mol cancels. Always name the particle."; 17 "Moles = particles ÷ 6.022 × 10²³. A visible sample is a small number of moles."; 18 "Count a metal in atoms. Count a molecular compound in molecules. Count an ionic compound in formula units."; 19 "Moles of an element's atoms = moles of molecules × its subscript. Then multiply by 6.022 × 10²³ to count the atoms."; 21 "A value per mole describes 6.022 × 10²³ particles. Divide by that number to get one particle." `budget.json`: the per-slide sums (period 1 43.75 min, period 2 46 min). `chem.js` (91 checks), `zoomchecks.js` (16 checks). Registry entry: unit 5, lesson 1, `built: true`, the brief's file, title, description, periods `[[1, 14], [15, 28]]`, checks 11, markers, css `css-51`, `keys_cfg {"cr": "s13", "sim": "s13-sim", "card": "s13-cube", "tm": "s15", "ex": "s03", "hk": "s02", "notes": ["s13", 0]}`, `extras_cfg {"hash": "#13.2", "canvas": "#s13-sim canvas", "block": "s13-cube", "slides": 28}`, budget, chem, zoom_checks, blueprint (section l51, next l52, form unit5, teks_rows as the brief), matrix 5.1.1 to 5.1.4, no `overlap_baseline`, ten `mentions` (s02:3, s02:6, s04:26, s05:27, s09:8, s12:13, s22:23, s22:24, s22:25, s26:4), `extra_audits []`, `extra_slides null`.

**B11.** `python3 tools/slides-kit/build.py 5 1` → `unit5/slides-5-1.html`, 253,526 bytes, 2,484 lines, md5 **be9bc2c7219d78dc9b6433ae31e2d8d3**. Never hand-edited.

The 28 slides (P period, Min minutes from the frames, which equal `budget.json`):

| # | Title | Template | Footer reference | P | Frames | Min | Check | Animation instances (stages in frame order) |
|---|---|---|---|---|---|---|---|---|
| 1 | Counting particles with the mole | `t-cover` | Reading §5.1 | 1 | 1 | 0.5 |  | - |
| 2 | The coin jar | `t-hook` | Reading §5.1.1 | 1 | 6 | 2.5 |  | coinScale `s02-sim` (jar, guess, tally, scale, reveal) |
| 3 | A bag of nickels at the bank | `t-launch` | Reading §5.1 opener | 1 | 5 | 3.0 |  | - |
| 4 | Predict now | `t-routine pn` | Reading §5.1 Before you read | 1 | 3 | 2.0 |  | - |
| 5 | Targets and words | `t-words` | Reading §5.1 Vocabulary | 1 | 3 | 2.5 |  | - |
| 6 | Counting by weighing | `t-concept cw` | Reading §5.1.1 | 1 | 8 | 4.0 | yes | coinScale `s06-sim` (bag, zero, read, divide, count, roll) |
| 7 | Counting a mixed jar | `t-concept cw` | Reading §5.1.1 | 1 | 11 | 4.0 | yes | centJar `s07-sim` (jar, wrong, sample, average, count, isotopes, sample) |
| 8 | The mole | `t-concept cw` | Reading §5.1.2 | 1 | 9 | 3.5 | yes | countingUnits `s08-sim` (dozen, ream, mole, exact, constant) |
| 9 | How many is a mole? | `t-concept cw` | Reading §5.1.2 | 1 | 10 | 4.25 | yes | howMany `s09-sim` (one, dozen, thousand, zoom, mole, spoon) |
| 10 | Name the particle | `t-concept cw` | Reading §5.1.2 | 1 | 10 | 3.75 | yes | moleKinds `s10-sim` (al, cu, compare, oxygen, four, compare) |
| 11 | The size of a mole | `t-concept wide` | Reading §5.1.2 | 1 | 11 | 4.0 | yes | secondsLine `s11-sim` (line, year, earth, universe, mole, times, spoon, times) |
| 12 | Who found the number | `t-concept wide` | Reading §5.1.2 | 1 | 8 | 2.75 |  | moleHistory `s12-sim` (avogadro, loschmidt, ostwald, perrin, si, exact) |
| 13 | Counting the atoms in a silicon sphere | `t-concept cw` | Reading §5.1.2 | 1 | 9 | 3.5 | yes | siliconSphere `s13-sim` (sphere, sphere, crystal, cube, atom, divide, cube) |
| 14 | One picture: three ways to count | `t-summary s3` | Reading §5.1.1 and §5.1.2 | 1 | 9 | 3.5 |  | - |
| 15 | Warm-up | `t-turn two` | Reading §5.1.1 and §5.1.2 | 2 | 5 | 2.5 |  | - |
| 16 | Moles to particles | `t-concept cw` | Reading §5.1.3 | 2 | 8 | 3.25 | yes | moleMap `s16-sim` (map, map, Cu/setup, Cu/cancel, Cu/result) |
| 17 | Particles to moles | `t-concept cw` | Reading §5.1.3 | 2 | 9 | 3.5 | yes | moleMap `s17-sim` (Fe/setup, Fe/setup, Fe/cancel, Fe/result, half, half) |
| 18 | Formula units | `t-concept cw` | Reading §5.1.3 | 2 | 8 | 3.25 | yes | naclCrystal `s18-sim` (crystal, unit, unit, count, wrong, unit) |
| 19 | Atoms in a molecule | `t-concept cw` | Reading §5.1.4 | 2 | 9 | 3.5 | yes | atomCounter `s19-sim` (H2O/one, H2O/one, H2O/mol, CO2/mol, CO2/atoms, NaCl/mol, CO2/mol) |
| 20 | Convert: I do, we do, you do | `t-example` | Reading §5.1.3 and §5.1.4 | 2 | 12 | 6.0 |  | moleMap `s20-sim` (map, CO2m/setup, CO2m/cancel, CO2m/result, H2Om/setup, H2Om/cancel, H2Om/result); atomCounter `s20-ac` (NH3/mol) |
| 21 | The mole in earlier lessons | `t-concept cw` | Reading §5.1.2 | 2 | 5 | 2.0 |  | moleMap `s21-sim` (energy/mole, energy/mole, energy/one, energy/why) |
| 22 | Checkpoint routine | `t-routine` | Objectives 5.1.2 to 5.1.4 | 2 | 6 | 1.0 |  | - |
| 23 | Checkpoint 1 | `t-routine` | Objective 5.1.2 | 2 | 6 | 4.5 |  | - |
| 24 | Checkpoint 2 | `t-routine` | Objective 5.1.3 | 2 | 6 | 4.5 |  | - |
| 25 | Checkpoint 3 | `t-routine` | Objective 5.1.4 | 2 | 6 | 4.5 |  | - |
| 26 | Predictions and exit ticket | `t-routine t-exit` | Objectives 5.1.1 to 5.1.4 | 2 | 8 | 5.5 |  | - |
| 27 | Rate your learning | `t-routine` | All objectives | 2 | 5 | 1.5 |  | - |
| 28 | Next | `t-summary tnext` | Missions 5.1 and Lesson 5.2 | 2 | 1 | 0.5 |  | - |

## Verification
**V1. Final suite** (`suite.py 5 1 --theme light --out <scratchpad>/kit-out-51f`, matrix off, one run, 914.9 s): **16 of 17 PASS**, xcheck FAIL on blueprint-side rows only.

| Audit | Result | Time | Verdict line |
|---|---|---|---|
| walk light | PASS | 241.6 s | walk light: 197 states, max empty 26% (s14f8), PASS |
| back light | PASS | 96.6 s | back: 197 forward, 197 back, PASS |
| fonts light | PASS | 56.4 s | fonts: PASS |
| keys | PASS | 37.2 s | keys: PASS 48 checks |
| readability | PASS | 3.0 s | readability: PASS |
| print | PASS | 2.1 s | print: PASS stage hidden=true, 28 slides, 197 frame lines, 11 PDF page(s) |
| render3d | PASS | 2.2 s | render3d: PASS |
| extras | PASS | 5.3 s | extras: PASS |
| chem | PASS | 1.8 s | chem51 (deck): PASS 91 checks |
| timing | PASS | 1.2 s | timing: period 1 43.75 min, period 2 46 min, PASS |
| supgap | PASS | 4.9 s | supgap: 107 symbol+charge pairs checked, PASS |
| zoom light | PASS | 360.2 s | zoom light: 1072 zoomed states over 197 frames (re-flow 458, transform 614), prompt 35, r800 1, animation 133, part 459, card 203, frames 2, check 28, wcard 16, legend 1, rule 18, caption 17, caprow 15, p 3, table 1, column 21, line 1, bank 1, row 30, rail 29, li 50, handsup 3, scale 5; min fill 62%; Back tests 28; PASS |
| click | PASS | 34.1 s | click: 11 graded checks, 3 Predict-now questions, 55 assertions, PASS |
| layout light | PASS | 57.5 s | layout light: 197 frames, 28 visible option lists (stacked 19, row 9), max empty 26% (s14f8), gate 33%, clipped or ellipsized text: 0, overlap: 0 intersections on 0 frames, no baseline (8671 boxes (2604 DOM boxes, 2172 canvas labels, 3895 canvas shapes), 210 covered canvas labels, 85 spheres scenes (live moments included), 16 of 16 canvas animations instrumented), live: 12 frames at two moments, PASS |
| xcheck | FAIL | 1.6 s | xcheck: 37 of 54 pass, 17 FAIL |
| contact light | PASS | 5.5 s | contact sheets light: contact-light-1.png (94 shots, 3495 px tall), contact-light-2.png (102 shots, 3710 px tall), contact-light-3.png (1 shots, 1000 px tall) |
| zoomsheet light | PASS | 3.6 s | zoom sheet light: zoomsheet-light-1.png (102 shots, 3710 px tall), zoomsheet-light-2.png (7 shots, 1000 px tall) |

**xcheck: the 17 failing rows** (identical in the first run and the final run). Every one reads a number of the blueprint's 5.1 section or matrix that came from the rejected 22-slide deck, which step 03 replaces:
- 5.1 "Deck: 22 slides": deck has 28
- 5.1 "Checkpoints 16 to 19": the checkpoint routine slide, then three checkpoint slides (titles start with "Checkpoint")  (16 Moles to particles, 17 Particles to moles, 18 Formula units, 19 Atoms in a molecule)
- 5.1 "predictions revisited 20, CER exit ticket 21": both are the slide "Predictions and exit ticket"  (20 Convert: I do, we do, you do, 21 The mole in earlier lessons)
- 5.1 "self-rating 22": the slide "Rate your learning"  (22 Checkpoint routine)
- 5.1.1 → slide 5 (Targets and words): exists and carries 5.1.1  (footer "Reading §5.1 Vocabulary", no check)
- 5.1.2 → slide 7 (Counting a mixed jar): exists and carries 5.1.2  (footer "Reading §5.1.1", a check on the slide but its footer does not name 5.1.2)
- 5.1.3 → slide 12 (Who found the number): exists and carries 5.1.3  (footer "Reading §5.1.2", no check)
- 5.1.3 → slide 13 (Counting the atoms in a silicon sphere): exists and carries 5.1.3  (footer "Reading §5.1.2", a check on the slide but its footer does not name 5.1.3)
- 5.1.4 → slide 14 (One picture: three ways to count): exists and carries 5.1.4  (footer "Reading §5.1.1 and §5.1.2", no check)
- 5.1 C.8(A) → slide 5 (Targets and words): exists and carries one of 5.1.1, 5.1.2  (footer "Reading §5.1 Vocabulary")
- 5.1 C.8(B) → slide 12 (Who found the number): exists and carries one of 5.1.3, 5.1.4  (footer "Reading §5.1.2")
- 5.1 C.8(B) → slide 13 (Counting the atoms in a silicon sphere): exists and carries one of 5.1.3, 5.1.4  (footer "Reading §5.1.2")
- 5.1 C.8(B) → slide 14 (One picture: three ways to count): exists and carries one of 5.1.3, 5.1.4  (footer "Reading §5.1.1 and §5.1.2")
- 5.1 rate slide 27: 5.1.1 "Review: 6 and 7" are slides that carry 5.1.1 and are in the matrix row (5, 6)  (same set)
- 5.1 rate slide 27: 5.1.2 "Review: 8 to 13 and 21" are slides that carry 5.1.2 and are in the matrix row (7 to 11, 15)  (same set)
- 5.1 rate slide 27: 5.1.3 "Review: 16 to 18" are slides that carry 5.1.3 and are in the matrix row (12, 13)  (same set)
- 5.1 rate slide 27: 5.1.4 "Review: 19 and 20" are slides that carry 5.1.4 and are in the matrix row (14)  (same set)
xcheck: 37 of 54 pass, 17 FAIL

Why each is blueprint-side: rows 1 to 4 compare the old deck line "Deck: 22 slides. Checkpoints 16 to 19, predictions revisited 20, CER exit ticket 21, self-rating 22." with the new deck (28 slides; checkpoints 22 to 25, predictions and exit ticket 26, rating 27). Rows 5 to 9 are the old objective cells "5, 6" (slide 5 is now the words slide), "7 to 11, 15", "12, 13" and "14", whose slide numbers now point at other slides. Rows 10 to 13 are the old matrix rows "5 to 11, 15" and "12 to 14" read against the new slides. Rows 14 to 17 compare the rate slide's new review lines (slides 6 and 7; 8 to 13 and 21; 16 to 18; 19 and 20) with the old objective cells. Every deck-side row passes (37): the deck line found, the registry's 11 checks and the period split against the deck, the four objective rows found, every old cell that happens to land on a slide with the right footer, the two matrix rows parsed with equal unions, the ten mentions and "every listed mention was found", and the footer cues (27 cues, each naming the next slide by number and title). The plan's new numbers (section 5, alignment line) are 5.1.1 → 6, 7; 5.1.2 → 8 to 13, 21; 5.1.3 → 16 to 18; 5.1.4 → 19, 20; C.8(A) "slides 6 to 13, 21"; C.8(B) "slides 16 to 20"; "Deck: 28 slides. Checkpoints 22 to 25, predictions revisited 26, CER exit ticket 26, self-rating 27."

First run (same deck before the fixes of Deviations 4 and 5): readability FAIL (prose over 35 words on 11 frames, one 15-word sentence, three rule cards above grade 8), zoom FAIL (25 table rows re-flowed outside the 60 px margins on slides 15 and 20, one predict card at 57% fill). Logs: `artifacts/02/logs/suite-light-first-run.txt`, `readability-first-run.log`, `zoom-light-first-run.log`. After the fixes: readability PASS (max 35 prose words visible per frame, register max grade 7.9, slide FK max 6.4), zoom PASS (1,072 zoomed states, min fill 62%, all 16 lesson checks and both generic checks PASS).

**V2. chem.js**: PASS 91 checks (every bench fact at the deck's own placed instances by slide id, host and stage; label and shape floors per instance; the check-frame subjects of the eleven checks; warm-up answers; slide-20 you-do answers; the slide-14 table; the review lines; the three slide-26 answers and their letters against slide 4; the eight cognates exactly as the lesson sheet and against the reading's glossary; the legend; the caption on 10 and 19; the eleven check slides; checks and periods against the registry; no console errors).

**V3. zoomchecks.js**: 16 lesson checks PASS (every animation host a unit at fill ≥ 0.6 on every frame that shows it, every animation part ≥ 0.6; the eight word cards and the legend; the three columns of the slide-14 table; the warm-up answer rows (3) and the you-do rows (3); each station and the bridge of moleMap on 16, 17, 20, 21 and the factor, result and check on 16, 17, 20; each history card on 12; the exponent ladder and the spoon on 9; the cards with chip rows; every rule card; every prompt of the routine slides; the caption on 10 and 19; 11 distinct check cards).

**V4. Artifacts** (`workshop/artifacts/02/`, 7.7 MB, no PNG, no per-press folder): `bench/` (8 JPEG sheets; `logs/` the bench suite log, every bench audit log, `overlap-light.txt`, `overlap-dark.txt`, `scratch-check-51.log`; `json/` the bench audits' JSON and `scratch-check-51.json`); `sheets/` contact sheets of the light theme `contact-light-1-1.jpg` to `contact-light-3-1.jpg` (5 JPEG, 54 to 782 KB), zoom sheets `zoomsheet-light-1-1.jpg` to `-2-1.jpg` (3 JPEG, 112 to 618 KB), the run-sheet `runsheet-5-1.pdf` (11 pages); `logs/` every audit log of the final run, `suite-light-final.txt`, `overlap-light.txt`, `timing-table.md`, `readability-table.md`, chem, layout and xcheck logs, and the first run's suite, readability and zoom logs; `json/` every audit's JSON of the final run. The click audit writes no screenshots, so there is no click sheet.

**V5.** `python3 tools/slides-kit/build.py --all`: 4.1 `ebd342f1ee0e11c47157141cf3b2a59b` (194,646 bytes), 4.2 `c3fa219a806963f9a66c3baf643153f4` (203,769 bytes), both unchanged; 5.1 `be9bc2c7219d78dc9b6433ae31e2d8d3`. No shared part, audit, build.py or suite.py changed. `unit5/blueprint.html` unchanged (`0b7dbba8…`).

**V6.** Readability PASS (above). Layout PASS: 197 frames, 28 visible option lists (19 stacked, 9 in a row, no 2 + 1), max empty 26% (s14f8), 0 clipped or ellipsized, **0 intersections** with no baseline (8,671 boxes: 2,604 DOM, 2,172 canvas labels, 3,895 canvas shapes; 210 covered labels; 85 spheres scenes; 16 of 16 canvases instrumented; 12 live frames measured at two moments, 0 hits). Ellipsis grep: 18 "…" in the built deck; the 15 student-facing ones are question stems the plan prints ("A mole is a…", "One mole of copper and one mole of aluminum have…", "…holds 6.022 × 10²³…", "has a mass of about…", "In the Avogadro project, a silicon sphere was used to…", "To change moles into a number of particles, you…") and the reference decks' tags "I can…" and "Self-check: did you write…"; none is a truncation.

## Repo state
- `unit5/slides-5-1.html`: 253,526 bytes, 2,484 lines, md5 be9bc2c7219d78dc9b6433ae31e2d8d3.
- `unit4/slides-4-1.html` ebd342f1ee0e11c47157141cf3b2a59b, `unit4/slides-4-2.html` c3fa219a806963f9a66c3baf643153f4 (unchanged).
- Changes against the brief's base 849bb53 (`git diff --name-status 849bb53`):
```
A	tools/slides-kit/parts/lessons/5-1/budget.json
A	tools/slides-kit/parts/lessons/5-1/chem.js
A	tools/slides-kit/parts/lessons/5-1/css.css
A	tools/slides-kit/parts/lessons/5-1/gen_scratch.py
A	tools/slides-kit/parts/lessons/5-1/gen_slides.py
A	tools/slides-kit/parts/lessons/5-1/scratch-check.js
A	tools/slides-kit/parts/lessons/5-1/scratch.html
A	tools/slides-kit/parts/lessons/5-1/sims.html
A	tools/slides-kit/parts/lessons/5-1/slides.html
A	tools/slides-kit/parts/lessons/5-1/zoomchecks.js
M	tools/slides-kit/registry.json
A	unit5/old-slides/README.md
A	unit5/old-slides/slides-5-1.html
M	unit5/slides-5-1.html
```
- `git status --short` (against the orchestrator's snapshot 021f067):
```
 M tools/slides-kit/parts/lessons/5-1/chem.js
 M tools/slides-kit/parts/lessons/5-1/css.css
 M tools/slides-kit/parts/lessons/5-1/gen_slides.py
 M tools/slides-kit/parts/lessons/5-1/slides.html
 M unit5/slides-5-1.html
?? workshop/artifacts/02/
```
plus this report. No git state change by the implementer.

## Deviations
1. **Bench extras.** The registry's `extras_cfg` describes the deck (slide 13, 28 slides), which the 78-slide bench cannot satisfy; for the bench suite it pointed at the bench's own turning crystal (`#48.0`, `#x48-sim canvas`, block `x49-lab`, 78 slides) and was set back to the brief's values before the deck build. The final registry holds the brief's values.
2. **A background panel in every animation** (a soft card over the host, as 4.2's nameBuilder and stockDetective draw): early stages draw little, and without it the deck's one-third emptiness gate fails. Every label lies inside the panel.
3. **Drawing choices:** the time line labels every fourth power (1 s, 10⁴ s … 10²⁴ s) with a tick at every power, since 25 labels at 36 px cannot sit on one line without overlapping; the cells of the cascade's faces and the dozen carton hold molecule pictograms (the cells are 60 px or more; the pictograms are icons); the silicon spheres use the covalent radius itself (nearly touching) and the NaCl crystal uses Shannon radii at the true 282 pm spacing (space-filling) so that the farthest sphere stays at 60 px or more in the column; Al atoms `--metal` and Cu atoms `--rope` (the shared CPK has neither); the isotope picture uses two sizes as the plan says (the notes say the sizes stand for mass); the beam tips toward aluminum while only aluminum is loaded; the time-line counter runs on its own clock restarted when the slide is entered (its stage is the animation's first stage, so the runtime's stage time would count from page load).
4. **Wording tightened against plan section 5** (the readability audit's 35-word budget per frame, the 14-word sentence rule and grade 8, and fit): slide 4 prompt without "Write your letter."; target 5.1.4 "use a formula to count atoms in a sample." (5 and 27); word meanings "the counting unit: 6.022 × 10²³ particles", "one set of ions: Na⁺ and Cl⁻", "which atoms, how many of each"; slide 7 check "A jar holds both kinds. Which mass do you divide by?" with options "this jar's own average" / "the average of 2.500 g and 3.11 g" / "2.500 g, a newer cent" and reason "Divide a sample's mass by its count."; slide 9 predict "10²³ has 23 zeros." (the plan's "6.022 × 10²³ has 23 zeros" is not true) and "Seven steps, then × 602"; slide 10 rule (above) and check "One mole of aluminum and one mole of copper…" / "hold equal numbers of atoms, different masses" / "have the same mass" / "hold different numbers; copper atoms are larger", reason "Same count; copper atoms have more mass."; slide 11 check on one line "Earth is 4.5 billion years old. About how many Earth ages?" with options "4 million times" / "4,000 times" / "1.4 million times" (one row as the plan marks; "about" moved into the question); slide 13 options "count its atoms: mass, density, atom spacing" / "define the kilogram by its size" / "compare silicon and carbon atoms", reason "They gave the value fixed in 2019."; slide 14 cells "too small, too many", "divide by the average", "count in moles of 6.022 × 10²³"; slide 18 rule (above) and check "Which particles are counted in 1 mol of NaCl?" / "formula units: one Na⁺ and one Cl⁻ each", reason "NaCl has no molecules. Its formula gives the ratio of ions."; slide 19 rule (above); checkpoints: 23 prompt "A student says a mole of copper and of aluminum have equal mass. Explain the error." and sample "A mole is a count, not a mass. Same number of atoms; copper atoms are heavier."; 24 sample "…The particle is wrong: NaCl has no molecules. Count formula units."; 25 prompt "One mole of H₂O holds one mole of H atoms. True or false?" and sample "False. The subscript 2 means two H atoms per molecule. One mole of H₂O has 2 mol of H, 1 mol of O."; slide 26 word bank "6.022 × 10²³ particles, same mass, divide, multiply, subscript, each element". Feedback lines are as the plan prints them.
5. **Layout fixes in the lesson parts:** on slides 7, 8, 9, 10, 13, 16, 18 the rule card leaves the column when the stacked check appears (the rule was on screen on the frame before); the caption leaves slide 10's check frames (only atoms are drawn there); a check inside an accumulating column uses 40 px for its question and stacked options; the word cards use 36/34 px term lines and 100 px icons (34-unit digits render at 34 px); the Predict-now cards fill their row; the summary's thread line and write step sit in an accumulating column; the warm-up and you-do tables have line breaks and a class (the zoom clone drops ids) so each row re-flows inside the margins; slide 17's predict card shows the two ways across the bridge as chips (a 57% zoom fill otherwise); the exit ticket's two-sentence driving question is 40 px; row options get 28 px above them (the head's ✓ badge sits 24 px above an option; see Open question 2); the summary cells carry `lbl` (table cells, not prose).
6. **Minutes**: slide 20 takes 6.0 min (plan 5) and slide 9 4.25 (plan 4); period 1 43.75 min (plan 43.5), period 2 46 min (plan 45), both under 47.
7. **Slide 11's band** is 236 px (`data-band` 236) to hold the check row; slide 12's is 214.
8. **scratch-check's shape floor** passes a stage with no primary shape at all (secondsLine year to times draw only the line, ticks and markers); every other stage reports its smallest shape (60 px or more).
9. **unit5/old-slides/README.md** has the five lines of the Unit 4 README (the brief says two), with Unit 5.
10. **Slide 14 rows** are not separate zoom units: the runtime zooms this summary table by column (as 4.1 slide 11); the three columns are units.

## Open questions
1. **Dark theme, Unit 5 code.** The shared dark tokens make `--warm` (#e6bd6c) and `--e` (#f6d84a) both amber-yellow, so grams and particles are hard to tell apart in the dark theme (labels always say "g", "mol" or the particle). Changing tokens is a shared-head change; not done.
2. **The ✓ / ✗ badge of a row option** (shared head: absolute, 24 px above the option) can touch the question line above; the overlap check measures boxes, not pseudo-elements, so it cannot see this. 5.1 keeps 28 px free above row options in its lesson CSS; 4.1 and 4.2 use the head as it is.
3. **Shapes the overlap check does not record**: lines, arcs, arrowheads, the time-line markers and the bridge arc are drawn with the context, not the painter's circle or rrect; they are kept clear of labels by layout (visible on the sheets), not by the gate.
4. **Isotopes in two sizes** (plan section 4) suggest that isotopes differ in size; the notes say the sizes stand for mass. The teacher may prefer equal sizes with a "heavier/lighter" mark.
5. **Wording**: the tightenings of Deviation 4 change the plan's checks and samples; the teacher may prefer other cuts, a 40-word budget for answer frames, or fewer options words.
6. **Runtime stage time**: a live stage that is also an animation's first stage gets its time from page load (`I.t` resets only on a stage change); 5.1 works around it inside `secondsLine`; a shared fix would reset the time in `active(true)`.
7. **Blueprint numbers** for 5.1 (step 03): the plan's alignment line above; the 17 xcheck rows then pass.
