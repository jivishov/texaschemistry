# Report 03: Final: four fidelity refinements, the dark-theme particle color, the blueprint numbers, the dark theme and the zoom matrix, the final suites, the kit records

Step: 03 · Lesson: 5.1 · Commit: none by the implementer (in-session; this report describes the working tree on `workshop/unit5-5-1` over 9a0c24b)

## Done
Order as the brief: A (lesson parts) → B (blueprint) → C (builds and suites) → D (kit records) → V. Every lesson file is under `tools/slides-kit/parts/lessons/5-1/`. No shared part, audit, `build.py`, `suite.py` or `split_parts.py` changed; nothing under `unit4/` changed; no git state change.

**A1. Slide 7, `centJar` stage `isotopes`** (`sims.html`). The six copper atoms are drawn at one size (radius 46 px, every label "Cu" at 44 px) in the two browns already used (`--rope` for four, `--rope` mixed 15% toward black for two); nothing added. Before: four at 40 px radius and two at 52 px. `meta()` now reports `spheres`, `sizes` and `shades` from the drawn list (6, 1, 2). No assertion tested two sizes; the existing isotope assertions of `chem.js` and `scratch-check.js` now also require 6 atoms, 1 size, 2 shades, and `scratch-check.js` adds one assertion that the instrumented discs of that paint all have one radius (six discs, r 47.5 px with the stroke). Shape floor 92 px (60 px floor), label floor 36 px. Frame note (slide 7, the `isotopes` frame): "The coins become atoms: one element, a mix of isotopes. The two shades stand for two masses. Isotopes of one element have the same size. The periodic table gives the average mass: copper 63.546. No isotope masses are needed." The slide note's old sentence about two sizes now reads: "The isotope picture draws every copper atom at one size in two shades: the shades stand for two masses, and isotopes of one element have the same size."

**A2. Slide 12, `moleHistory` stage `avogadro`.** Caption row `s12-p0`: "1811: Avogadro's idea. At one temperature and pressure, equal gas volumes hold equal numbers of particles. He never knew the number." Canvas card (it fits at 36 px with no overlap: widths 554, 484, 350 and 450 px in a 610 px text column): "At one temperature and pressure," / "equal gas volumes hold equal" / "numbers of particles." / "He never knew the number." Four lines at 36 px on a 44 px pitch (the other cards keep up to three lines at 36 to 40 px on a 50 px pitch), so the last line ends 15 px above the card's bottom edge. Frame note: "1811, Amedeo Avogadro: equal volumes of gases at the same temperature and pressure hold equal numbers of particles. The condition matters: both gases at one temperature and one pressure. He never knew how large that number was. Misconception: "Avogadro measured the number"."

**A3. Slide 13, `siliconSphere` stage `cube`.** Card `s13-cube`: "X-rays measure one cube's edge: 543.102 pm. Corner and face atoms are shared: 8 atoms per cube." The canvas chip "8 atoms per cube" stays. Frame note: "X-rays measure the edge of one cube: 543.102 pm. The picture rings the 18 atoms that touch the cube; corner and face atoms are shared with the next cubes. Each cube holds the equivalent of 8 atoms: 8 corners × 1/8 + 6 faces × 1/2 + 4 inside = 8." Answer line `s13-ans`: "A. Those measurements gave the value fixed in 2019." Option A now reads "count atoms: mass, density, atom spacing" (was "count its atoms: …"; Deviation 2).

**A4. Slide 2, frame `scale`, note only:** "The scale reads the coins: 2,000.0 g. Every nickel has a mass of 5.000 g. The scale was zeroed with the empty jar; slide 6 teaches zeroing." No on-screen change. The "slide 6" mention is the registry's existing `s02:6` (Counting by weighing); xcheck finds it.

**A5. Dark-theme particle color** (`css.css`, marker `css-51`). The head selects the dark theme with `:root[data-theme="dark"]` (the attribute set before first paint from `?theme=dark` or the stored choice; dark `--warm` #e6bd6c, `--e` #f6d84a, `--accent` #73c7b4). `css-51` (inserted after the shared rules, so it wins at equal specificity) adds `:root[data-theme="dark"]{--e:#cc99ff}`. The canvas painter reads colors with `D.tok`, which is `getComputedStyle(document.documentElement).getPropertyValue('--'+name)` (cache cleared on a theme change), so the one override covers the `.chip.n` chips, the legend dot `.i-n` on slide 5, the word-card icons (`f-e`, `f-sea`) and every canvas (`g.c('e')`: chips, counters, the ladder, the cube fill, the particle dots). Contrast of #cc99ff: 7.1:1 on `--card` #1a2623, 7.6:1 on the animation panel (#16201e) and on `--card2` #16211e, 5.5:1 on a canvas chip's fill, 4.8:1 on the lit ladder row of slide 9 (20% violet); the "#" on the legend dot (`--on-ion` #0d1614) 8.4:1. Hue 270°, apart from the anion blue #8fb3ff (221°), the moles teal (166°) and the grams amber (40°). The light theme keeps the shared `--e` #7a2fc0. `chem.js` adds one check: grams, moles and particles have three different colors in each theme, particles #7a2fc0 light and #cc99ff dark.

**B1 to B3. Blueprint** (`unit5/blueprint.html`, numbers only, section `l51` and section `matrix`):
- Deck line (l51): "Deck: 28 slides. Checkpoints 22 to 25, predictions revisited 26, CER exit ticket 26, self-rating 27."
- Objectives, Slides cells: 5.1.1 "6, 7"; 5.1.2 "8 to 13, 21"; 5.1.3 "16 to 18"; 5.1.4 "19, 20".
- Matrix: C.8(A) "Deck 5.1, slides 6 to 13, 21"; C.8(B) "Deck 5.1, slides 16 to 20; Deck 5.3, slides 5 to 14" (the 5.3 part unchanged).
The same old sentence "Deck: 22 slides. Checkpoints 16 to 19, …" also stands in section `l52` (5.2's deck line); the edit was confined to `l51` and left it alone (open question 1).

**B4.** Grep of section `l51` for slide numbers in prose: none besides the deck line. The other matches are the "Slides" column header, the card label "Slides and missions" and "Item bank: 22 items (14 reading, 8 slides)" (an item count, not a slide number). Nothing listed for the orchestrator.

**C1.** `python3 tools/slides-kit/build.py 5 1` → `unit5/slides-5-1.html`, 255,040 bytes, 2,492 lines, md5 **3c86da493034ed29c283551925ea3b30**. `python3 tools/slides-kit/build.py --all`: 4.1 `ebd342f1ee0e11c47157141cf3b2a59b` (194,646 B) and 4.2 `c3fa219a806963f9a66c3baf643153f4` (203,769 B) unchanged, 5.1 as above.

**C2. Bench.** `build.py 5 1 --scratch --out <scratchpad>/scratch51.html` (md5 0b3dd2e4b0cc864f1f4e2f62349f66a6, 78 scratch slides); `scratch-check.js` **PASS 348 assertions** (346 + 2: the instrumented-disc radius check of `isotopes` and the condition in the `avogadro` card); `suite.py 5 1 --deck <scratch> --only walk,layout,zoom --theme both` (the whole bench): **6 of 6 PASS**, 0 intersections in both themes (3,998 boxes, one canvas label more than step 02: the fourth line of the 1811 card).

**C3. Deck suite** `suite.py 5 1 --theme both --matrix --out <scratchpad>/final` (3,353 s): **23 of 23 PASS** (table below); overlap 0 intersections with no baseline in both themes; xcheck **60 of 60** (Deviation 1); contact and zoom sheets in both themes. The suite runs fonts once (light) with `--theme both`, so `suite.py 5 1 --only fonts --theme dark` was run as well: **fonts: PASS** (log `fonts-dark.log`).

**D1. `tools/slides-kit/README.md`**: the decks list names `unit5/slides-5-1.html`; the intro and the layout table name `docs/handoff-5-1.md`; the `gen_scratch.py` row says 4.2 and 5.1 have one; the build block has `python3 build.py 5 1  # 5.1 -> unit5/slides-5-1.html`; the marker paragraph reads "Lesson 5.1 (built, `unit5/slides-5-1.html`): … and the CSS marker `css-51` (it has a `css.css`)"; "Add a lesson" keeps 5.1 as the example and says it "carried `"built": false` until its deck step wrote `unit5/slides-5-1.html` and is now `"built": true` (a new lesson starts the same way)"; step 4 says the older deck goes to `unit<U>/old-slides/`, "as 5.1's rejected deck was". The absolute-path grep still finds only `docs/handoff-4-1-4-2.md`.

**D2. `tools/slides-kit/docs/handoff-5-1.md`** (new, 58 lines, no path outside the repo): the deck facts, the pointer to the clicker map and run steps of `handoff-4-1-4-2.md` plus 5.1's timers, the eleven animations with their stages and slides, the live and turning stages and reduced-motion behavior, the Unit 5 color code with light and dark values (and contrast), the known limitations of review 02 F7 (the ✓ badge offset, unrecorded canvas strokes, the live first-stage time workaround in `secondsLine`) plus the 4.1/4.2 ones, and the blueprint form.

**D3. `registry.json`**: unchanged. `built: true` was already set; checks 11 and periods `[[1, 14], [15, 28]]` hold; the new "slide 6" note mention on slide 2 is the existing `s02:6` entry.

## Verification
**V1. Final deck suite** (matrix on, both themes, deck md5 3c86da49…):

| Audit | Result | Time | Verdict line |
|---|---|---|---|
| walk light | PASS | 241.6 s | walk light: 197 states, max empty 26% (s14f8), PASS |
| walk dark | PASS | 240.9 s | walk dark: 197 states, max empty 26% (s14f8), PASS |
| back light | PASS | 96.6 s | back: 197 forward, 197 back, PASS |
| back dark | PASS | 96.6 s | back: 197 forward, 197 back, PASS |
| fonts light | PASS | 56.6 s | fonts: PASS |
| fonts dark (separate run) | PASS | 56.5 s | fonts: PASS |
| keys | PASS | 37.4 s | keys: PASS 48 checks |
| readability | PASS | 3.3 s | readability: PASS |
| print | PASS | 2.1 s | print: PASS stage hidden=true, 28 slides, 197 frame lines, 11 PDF page(s) |
| render3d | PASS | 2.3 s | render3d: PASS |
| extras | PASS | 5.5 s | extras: PASS |
| chem | PASS | 1.9 s | chem51 (deck): PASS 94 checks |
| timing | PASS | 1.2 s | timing: period 1 43.75 min, period 2 46 min, PASS |
| supgap | PASS | 4.8 s | supgap: 107 symbol+charge pairs checked, PASS |
| zoom light | PASS | 1199.0 s | zoom light: 1072 zoomed states over 197 frames (re-flow 458, transform 614), … ; min fill 62%; Back tests 28; PASS |
| zoom dark | PASS | 1196.0 s | zoom dark: 1072 zoomed states over 197 frames (re-flow 458, transform 614), … ; min fill 62%; Back tests 28; PASS |
| click | PASS | 33.9 s | click: 11 graded checks, 3 Predict-now questions, 55 assertions, PASS |
| layout light | PASS | 57.4 s | layout light: 197 frames, 28 visible option lists (stacked 19, row 9), max empty 26% (s14f8), gate 33%, clipped or ellipsized text: 0, overlap: 0 intersections on 0 frames, no baseline (8671 boxes (2603 DOM boxes, 2173 canvas labels, 3895 canvas shapes), 210 covered canvas labels, 85 spheres scenes (live moments included), 16 of 16 canvas animations instrumented), live: 12 frames at two moments, PASS |
| layout dark | PASS | 57.6 s | layout dark: (the same numbers as light), live: 12 frames at two moments, PASS |
| xcheck | PASS | 1.6 s | xcheck: 60 of 60 pass |
| contact light | PASS | 5.2 s | contact sheets light: contact-light-1.png (94 shots), -2.png (102 shots), -3.png (1 shot) |
| contact dark | PASS | 5.3 s | contact sheets dark: contact-dark-1.png (94 shots), -2.png (102 shots), -3.png (1 shot) |
| zoomsheet light | PASS | 3.3 s | zoom sheet light: zoomsheet-light-1.png (102 shots), -2.png (7 shots) |
| zoomsheet dark | PASS | 3.3 s | zoom sheet dark: zoomsheet-dark-1.png (102 shots), -2.png (7 shots) |

Suite line: `== 5.1: 23 of 23 pass, 0 fail, 3353.4 s`. **Matrix**: in each theme 12 of 12 PASS (1024 × 768, 1366 × 768, 1536 × 864 and 1920 × 1080 at device scale 1, 1.25 and 1.5, each loaded at another size), 375 zoomed states measured per combination, 0 fails (4,500 per theme); the 18 generic and lesson zoom checks PASS in both themes. Overlap: `overlap-light.txt` and `overlap-dark.txt` both say "no intersections, 197 frames, 8671 boxes …; live: 12 frames at two moments". xcheck: `xcheck: 60 of 60 pass` (every deck-line, objective, matrix, review-line, mention and footer-cue row; the rows that read the blueprint now read 28 slides, checkpoints 22 to 25, 26, 26, 27 and the new slide lists).

**V2.** `scratch-check 5.1: PASS 348 assertions` (step 02: 346; +1 the six isotope discs share one radius, +1 the 1811 card states the condition; the existing isotope assertion also requires 6 atoms, 1 size, 2 shades). `chem51 (deck): PASS 94 checks` (step 02: 91; +1 the 1811 card's lines, +1 the slide 12 caption row, the slide 13 cube card and the slide 13 answer line as quoted above, +1 the three Unit 5 colors in both themes; the slide 7 isotope check also requires one size and two shades).

**V3. md5s.**

| File | Before | After |
|---|---|---|
| `unit5/slides-5-1.html` | be9bc2c7219d78dc9b6433ae31e2d8d3 (253,526 B) | 3c86da493034ed29c283551925ea3b30 (255,040 B, 2,492 lines) |
| `unit5/blueprint.html` | 0b7dbba88781ca560acdd200ac320a1f (57,938 B) | 5975fb9cdfa6f57cef0cdb26a5f623be (57,944 B) |
| `unit4/slides-4-1.html` | ebd342f1ee0e11c47157141cf3b2a59b | ebd342f1ee0e11c47157141cf3b2a59b (unchanged) |
| `unit4/slides-4-2.html` | c3fa219a806963f9a66c3baf643153f4 | c3fa219a806963f9a66c3baf643153f4 (unchanged) |

`git diff --stat unit5/blueprint.html`: `1 file changed, 7 insertions(+), 7 deletions(-)`; the seven changed lines differ in the numbers of B1 to B3 only (word diff: the deck line 22, 16, 19, 20, 21, 22 → 28, 22, 25, 26, 26, 27; the Slides cells "5, 6" → "6, 7", "7 to 11, 15" → "8 to 13, 21", "12, 13" → "16 to 18", "14" → "19, 20"; the matrix lists "5 to 11, 15" → "6 to 13, 21" and "12 to 14" → "16 to 20"). Size +6 bytes.

**V4. Artifacts** (`workshop/artifacts/03/`, 10 MB, JPEG and text only, no PNG, no per-press folder):
- `sheets/`: contact sheets `contact-light-1-1.jpg` to `contact-light-3-1.jpg` and `contact-dark-1-1.jpg` to `contact-dark-3-1.jpg` (5 each, each tall sheet cut at a blank gap into two), zoom sheets `zoomsheet-light-1-1.jpg`, `-1-2`, `-2-1` and the same for dark; 38 to 765 KB each.
- `logs/`: every audit log of the final run (`walk-light.log` … `zoomsheet-dark.log`, `fonts-light.log`, `fonts-dark.log` from the separate run), `suite-final.txt`, `matrix.txt` (both themes' matrix lines), `overlap-light.txt`, `overlap-dark.txt`, `xcheck.log`, `chem.log`, `readability.log`, `timing.log`; `logs/bench/`: the bench suite log, its walk, zoom and layout logs, its two overlap files and `scratch-check-51.log`.
- `crops/` (1920 × 1080 full frames, reduced motion, 151 to 248 KB): `s07f7-isotopes-light.jpg` and `-dark`, `s12f0-avogadro-light.jpg` and `-dark`, `s13f3-cube-light.jpg` and `-dark`, `s13f8-answer-light.jpg` and `-dark`, `s05f2-legend-dark.jpg` (grams amber, moles teal, particles violet), `s06f4-count-dark.jpg` (the amber 1,250.0 g and 5.000 g chips beside the violet "1 nickel" and "250 nickels").

**V5. Readability and layout after the wording changes.** Readability PASS. Visible prose words (the audit's 35-word budget, its own counting: words with a letter): slide 12 frame 0 (the 1811 caption) 20; slide 13 frame 3 (the cube card; the crystal card above it is compacted to its title) 15; slide 13 frame 8 (the answer frame) 35, the slide's maximum; slide 7 frame 7 13. Slide 12 FK 5.7 (step 02 5.4), prose FK 6.4; slide 13 FK 3.7, prose FK 4.1. Every new sentence is 14 words or fewer: "At one temperature and pressure, equal gas volumes hold equal numbers of particles." 13; "Corner and face atoms are shared: 8 atoms per cube." 9 (the number not counted as a word by the audit); "A. Those measurements gave the value fixed in 2019." 8. Layout PASS in both themes with 0 intersections at rest and at the 12 live frames; the 1811 card's four lines, the isotope atoms and the cube card read clear on the crops.

## Repo state
- `unit5/slides-5-1.html` 255,040 bytes, md5 3c86da493034ed29c283551925ea3b30 (built by `build.py 5 1`, never hand-edited); `unit5/blueprint.html` 57,944 bytes, md5 5975fb9cdfa6f57cef0cdb26a5f623be; `unit4/slides-4-1.html` ebd342f1…, `unit4/slides-4-2.html` c3fa219a… (unchanged).
- `git status --short` (over 9a0c24b), before this report was written:
```
 M tools/slides-kit/README.md
 M tools/slides-kit/parts/lessons/5-1/chem.js
 M tools/slides-kit/parts/lessons/5-1/css.css
 M tools/slides-kit/parts/lessons/5-1/gen_slides.py
 M tools/slides-kit/parts/lessons/5-1/scratch-check.js
 M tools/slides-kit/parts/lessons/5-1/sims.html
 M tools/slides-kit/parts/lessons/5-1/slides.html
 M unit5/blueprint.html
 M unit5/slides-5-1.html
?? tools/slides-kit/docs/handoff-5-1.md
?? workshop/artifacts/03/
```
plus this report (`?? workshop/reports/03-final.md`). `registry.json`, `scratch.html` (regenerated identical by `gen_scratch.py`), the shared parts, audits, `build.py`, `suite.py`, `workshop/status.md` and `workshop/log.md` unchanged. No git state change by the implementer.

## Deviations
1. **xcheck 60 of 60, not 54 of 54.** xcheck checks every slide a blueprint cell lists, one row each. The new lists name six more slides than the old ones (objectives: 5.1.2 7 slides instead of 6, 5.1.3 3 instead of 2, 5.1.4 2 instead of 1; matrix: C.8(A) 9 instead of 8, C.8(B) 5 instead of 3), so the same checks make 60 rows. The 17 rows that failed in step 02 all pass, and no row fails.
2. **Slide 13, option A cut by one word** ("count its atoms: mass, density, atom spacing" → "count atoms: mass, density, atom spacing"). With the brief's answer line ("Those measurements" for "They", one word more) the answer frame (frame 8) showed 36 words and readability failed its 35-word budget. Option A is the smallest cut that keeps the brief's answer line, the stem and the other options. The alternative is a stem cut ("The Avogadro project used a silicon sphere to…", two words fewer); open question 2.
3. **The 1811 card uses four lines at 36 px on a 44 px pitch.** At the usual 50 px pitch the fourth line would cross the card's lower edge (card bottom 465 px, line bottom 470 px). The brief allowed the condition in the card only at 36 px with no overlap; at 36 px and 44 px it fits with 15 px to spare, and the other five cards are unchanged.
4. **Notes beyond the brief's sentences**, so they do not contradict the picture: slide 7's slide note (it said the picture had "two atom sizes") now describes one size in two shades; slide 13's cube frame note also says the picture rings the 18 atoms that touch the cube and adds "= 8" to the arithmetic.
5. **Isotope size**: one radius of 46 px (between the old 40 and 52) and every label at 44 px, so the six atoms keep their places and gaps (28 px across, 32 px down).
6. **Extra assertions** in `chem.js` (91 → 94) and `scratch-check.js` (346 → 348), described under V2; none was removed or loosened.
7. **A separate dark fonts run**, because `suite.py --theme both` runs fonts once, in light.
8. **`logs/bench/`** in the artifacts (the bench logs of C2), beside the folders V4 names.

## Open questions
1. Section `l52` of the blueprint prints the same old sentence "Deck: 22 slides. Checkpoints 16 to 19, predictions revisited 20, CER exit ticket 21, self-rating 22." for 5.2; left alone (not 5.1's numbers).
2. Slide 13's answer frame: keep the one-word cut of option A (Deviation 2), or cut the stem instead ("The Avogadro project used a silicon sphere to…")?
3. The two browns of the isotope picture are close in the light theme (`--rope` and 15% darker); the brief asked for the shades already used. A stronger second shade would be a one-number change in `sims.html` if the teacher wants it.
4. The dark violet lives in `css-51`. Later Unit 5 decks keep the code only if each copies that rule; a shared dark `--e` for Unit 5 would be a shared-part change and re-audit every deck (4.1 and 4.2 draw electrons with `--e`).
