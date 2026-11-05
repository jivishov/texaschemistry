# Report 02: Period-1 animations for 4.5 on scratch slides (plus kit follow-ups K1 to K3)

Step: 02 · Lesson: 4.5 · Commit: the commit `[implementer] 02: 4.5 period-1 animations on scratch; kit follow-ups` on `workshop/unit4-5-6`, parent `9b9372f` (its hash is in the pull-request comment `report 02 ready`)

## Done

### K. Kit follow-ups (proved on 4.1 and 4.2 first)
- **K1, generic zoom checks and per-lesson lists.** `audits/zoom.js` now runs two generic checks on every deck, scratch decks included: "every zoomed check shows its options" and "every prompt on a routine slide is a unit". The second covers each `t-routine` slide that carries a `.prompt` or `.dq` (see Deviation 1). After them it runs the lesson's own list from `ZOOM_CHECKS`, which `suite.py` sets from the new registry field `zoom_checks` (not for a scratch deck). The 4.1 and 4.2 lists moved word for word to `parts/lessons/4-1/zoomchecks.js` (9 entries) and `parts/lessons/4-2/zoomchecks.js` (12 entries), each `module.exports=(rec,{has,cnt})=>[[name, ok], …]`. The generic entries were taken out of both lists: 4.1 "A1 checks: every zoomed check shows its options" and "B6 slides 20 to 24: the prompts are units"; 4.2 "every prompt on slides 20 to 24 is a unit", plus the second half of "every check card with its options, and every zoomed check shows its options". That 4.2 entry keeps its count half as "every check card with its options" (≥ 9 zoomed checks; Deviation 2). `LESSON` is no longer read by any audit and `suite.py` no longer sets it. README layout, environment and registry tables updated.
- **K2, the keys timer.** `audits/keys.js` reads the `tm` slide's frame-1 timer in the page (`Deck.slides[TM].frames[1].timer`) and derives the expected texts from it: after about 2 s the timer must read between `fmt(sec−3)` and `fmt(sec−1)`; after Back then Next it must read `fmt(sec)`. The three assertion names are unchanged. If the `tm` slide's frame 1 has no timer, all three fail with "keys_cfg tm <id>: frame 1 of that slide has no timer". The check count stays 48.
- **K3, scratch runs and the emptiness gate.** On a scratch deck (one with a `scratch-<U><L>` part), `suite.py --deck` gives walk and layout `EMPTY_MAX=1` unless the environment already sets `EMPTY_MAX`. It prints "scratch deck: EMPTY_MAX=1 for walk and layout (emptiness gate off); every other gate unchanged". Every other audit gets the unchanged environment. The README line now describes this instead of "a brief has to say when".

### A. The 4.5 lesson folder and registry entry
`tools/slides-kit/parts/lessons/4-5/`:
- `sims.html`: the six animations below. No `css.css`; everything is in canvas or set inline by the sims.
- `gen_scratch.py` → `scratch.html`, the bench. There is one slide per instance, in the deck's template and at the deck's host size: `brickBag` in `t-hook` (host 1472 × 519), `meltScale` in `t-launch` (1472 × 603; 345 once the driving-question card shows), `threeSolids`, `attractions` × 3 and `bpPlot` in `t-concept cw` (749 × 687), and `forceDecider` in `t-cer` (1472 × 616). Each slide has one frame per stage, labelled with the stage name. The `meltScale` slide adds one last frame that shows the driving question under the animation, which tests the shrink.
- `scratch-check.js`: the meta checks (C3).
- Placeholders the deck step replaces: `gen_slides.py` writes a one-slide `slides.html` (a cover), `budget.json` is `{}`, and `chem.js` prints `chem: PASS 0 checks`.
- Registry entry 4.5:
  - Fields as brief 02 A2: `file` `unit4/slides-4-5.html`, `title` "Bonds, Forces and Properties Slides", `description` "Unit 4, Lesson 4.5 projector slides: Bonds, forces and properties (TEKS C.7(D)).", `periods` `[[1, 13], [14, 27]]`, `checks` 10.
  - `markers` `01-head-45`, `02-runtime`, `02b-shared`, `sims-45`, `slides-45`; `css` `null`.
  - `blueprint` `{"section": "45", "next": "case"}`; `matrix` `4.5.1` to `4.5.5`; `mentions` `{}`; `extra_audits` `[]`; `extra_slides` `null`; no `zoom_checks`.
  - Provisional `keys_cfg` and `extras_cfg` on bench ids. `extras_cfg` is `{"hash": "#2.2", "canvas": "#ms-sim canvas", "block": "ms-dq", "slides": 8}`, which makes the extras audit meaningful on the bench; `keys_cfg` is not usable on the bench (no timer).
- `build.py 4 5` was not run without `--out`. Nothing under `unit4/` changed.
- CPK colors added in a lesson-local table, Jmol values, because the shared table has only H C N O S P: **F** `#90e050`, **Cl** `#1ff01f`, **Br** `#a62929`, **Si** `#f0c8a0`. Na, K, Ca and Cu were not needed: ions use the cation and anion colors, and copper cores use the metal gray. `02b-shared.html` is unchanged.

### B. The six animations
All six register with `Deck.sim`. The five canvas ones use `D.canvasSim` (named stages, `set(stage, instant)`, `get`, `bounds`, `units`, `resize`, `redraw`, `active`, `meta`); `forceDecider` is a DOM sim built the way `cerBuilder` is. Tweens run 600 to 900 ms. Under reduced motion every stage lands at its end state and the loops (shake, drift, flicker, turn) stand still. Colors come from the theme tokens, plus CPK for atoms. The smallest canvas label is 36 px in every animation (`brickBag` 40 px). No text is cut at a canvas edge (`outText` 0 on every frame). There are no raster images and no library. Smallest drawn circle measured on every frame (`artifacts/02/scratch/build-and-shapes.txt`): `meltScale` 36 px (the snowman icon's head; ice-ring H atoms 40 px), `threeSolids` 46 px (the back Na⁺ ions of the 3-row salt block), dispersion family 55 px (an electron dot's halo), dipole family 60 px, hydrogen family 60 px. `brickBag` bricks are 88 × 70 px and up. Shapes under 60 px are Deviation 5.

1. **`brickBag`** (stages `models`, `shake`, `pour`, `words`).
   - Three snap-together brick models in a clear bag: yellow (4 bricks), orange (4) and pink (3), 11 bricks in all, each brick with its studs.
   - The counter "Bricks snapped: 11 of 11" sits in a card beside the bag during `models` and `shake`, and on one line at the top right during `pour` and `words`. It never changes.
   - `shake`: the bag rocks and the models tumble apart inside it, whole.
   - `pour`: the bag fades, a table appears, and the models stand far apart on it.
   - `words`: "a snap between bricks = a bond within" over the yellow model, with a pointer to a seam; "models side by side = an attraction between" over the gap between the orange and pink models, with a dashed gray line in the gap. Each label breaks before the "=" when it needs two lines.
   - Units: the bag (or the table), each model, the counter, each label in `words`. `meta()`: `{stage, models:3, bricks:11, snapped:11, counter, labels, inBag, onTable}`.
2. **`meltScale`** (stages `three`, `melt`, `numbers`).
   - Three columns: snow, salt and sand. Each has an icon (snowman, salt crystals on a step, sandbox) and its name, plus a particle panel:
     - snow: six water molecules (CPK) in an open six-sided ring;
     - salt: a 4 × 4 grid of Na⁺ (red "+") and Cl⁻ (blue "−") at 102 and 181 pm, 282 pm spacing, to scale;
     - sand: an Si–O fragment, four Si each bonded to four O, the O bridging.
   - Under the panels, a linear scale from −200 to 1800 °C, labelled −200, 0, 400 … 1600 and "°C".
   - `melt`: the snow's molecules leave their places and drift (live), each whole and kept inside the panel, while salt and sand stay; the snowman slumps into a puddle.
   - `numbers`: the label line "Melting point", chips "snow 0.0 °C", "salt 801 °C" and "sand near 1700 °C", and a marker on the scale at each value.
   - Under 470 px of height (the driving question shown) the panels give way to icons, chips and the scale.
   - Units: each solid's column, the scale, the melting-point row. `meta()`: `{values:{snow:0.0, salt:801, sand:'near 1700'}, snowMoleculesIntact:true, snowMoved, saltMoved:false, sandMoved:false, chips, label, scale:[-200,1800]}`.
3. **`threeSolids`** (stages `chlorine`, `within`, `between`, `salt`, `copper`). The panels lay out by stage: chlorine alone fills the host (`chlorine` to `between`); chlorine and salt share it (`salt`); all three panels show (`copper`). The layouts cross-fade, and each row is as tall as its labels and its smallest readable picture need.
   - `chlorine`: six Cl₂ molecules, ball-and-stick with a gray stick, "Cl" on every sphere.
   - `within`: the sticks glow warm; label "bond within" with a stick in front.
   - `between`: dashed gray lines between neighboring molecules flicker (still under reduced motion); label "attraction between (much weaker)" with a dashed line in front.
   - `salt`: a 3D NaCl block from `Deck.spheres` (3 × 3 × 3, or 3 × 2 × 2 in the three-row layout), Shannon radii, 282 pm spacing, "+" and "−" on every ion, a slow turn; label "ionic bonds through the whole crystal, no molecules".
   - `copper`: one layer of gray "+" cores in a violet sea of "−" dots that drift; label "metallic bonds through the whole metal".
   - Units: each panel, each label shown. `meta()`: `{panels, molecules, sticksWithin, dashedBetween, withinGlow, naclRadii:[102,181], naclSpacing:282, saltIons, copper:'delocalized electrons', labels}`.
4. **`attractions`**: one type, three instances; every instance's `stages` holds all fourteen. Each stage of the dispersion and dipole families draws a short muted caption at the foot of the host, so the drawing fills the column (Deviation 6).
   - **Dispersion** (`cloud`, `flicker`, `neighbor`, `attract`): two nonpolar molecules as violet electron clouds, each with two nuclei and ten moving electron dots with "−".
     - `flicker`: the electrons crowd to one end for an instant (live), with δ− there and δ+ at the other end.
     - `neighbor`: the neighbor's electrons shift the same way.
     - `attract`: a dashed gray line between the facing ends forms, fades and forms again, its direction flipping each cycle; label "dispersion forces".
     - Captions: "electrons always moving", "for an instant: one end δ−, one end δ+", "the neighbor's electrons shift too", "it forms, fades and forms again".
   - **Dipole** (`F2`, `HCl`, `turn`, `face`, `compare`):
     - `F2`: two F₂ molecules (CPK) with a flickering dashed gray line and no δ labels; label "dispersion forces only".
     - `HCl`: two HCl molecules turned at random, δ+ (warm) on H and δ− (teal) on Cl, with the F₂ pair faint above.
     - `turn`: they rotate head to tail.
     - `face`: a dashed warm-to-teal line from H to the next Cl; label "dipole-dipole forces".
     - `compare`: the F₂ pair back in full; label line "Electrons per molecule" with chips "F₂ 18" and "HCl 18"; label line "Boiling point" with chips "F₂ −188.1 °C" and "HCl −85.1 °C".
     - Captions: "F₂ is nonpolar: no δ+, no δ−", "HCl is polar: δ+ on H, δ− on Cl", "they turn: δ+ toward δ−", "δ+ of one pulls δ− of the next".
   - **Hydrogen** (`water`, `hbond`, `ammonia`, `methane`, `four`):
     - `water`: two water molecules (104.5°) with two violet lone-pair lobes on each O.
     - `hbond`: a heavy dashed teal line from an H of one to a lone pair on the next O. The H to O distance is 194 px against the 96 px O–H bond. Label "hydrogen bond:" / "about 5 to 10% of a covalent bond".
     - `ammonia`: the same kind of line between two NH₃; label "hydrogen bond:" / "H on N to a lone pair on N".
     - `methane`: two CH₄ with a crossed-out dashed line; label "H on C: no hydrogen bond".
     - `four`: one water molecule with four neighbors and four dashed teal lines, two from its own H atoms and two to its lone pairs; label "up to four hydrogen bonds".
   - Units: each molecule pair (or the center and its neighbors), each label, each chip row, the caption.
   - `meta()`: dispersion `{family:'dispersion', polar:false, deltaLabels:'instant', neighborShift, line, label}`; dipole `{family:'dipole', HCl:{dplus:'H', dminus:'Cl'}, F2:{dplus:null, dminus:null, line:'dashed gray'}, headToTail, line, label, electrons:{F2:18, HCl:18}, bp:{F2:-188.1, HCl:-85.1}}`; hydrogen `{water:{donor:'H on O', acceptor:'lone pair on O'}, hbondLonger, label}`, `{ammonia:{donor:'H on N', acceptor:'lone pair on N'}}`, `{methane:'none'}`, `{waterMax:4, hbonds:4, neighbors:4}`.
5. **`bpPlot`** (stages `axes`, `F2`, `Cl2`, `Br2`, `I2`, `trend`, `trio`, `reveal`, `HCl`).
   - Boiling point from −200 to 200 °C (ticks every 100) against electrons per molecule from 0 to 110 (ticks every 20). Axis numbers are 36 px; axis titles are "Boiling point (°C)" and "Electrons per molecule".
   - Points appear one per press with formula and value: F₂ 18, −188.1 °C; Cl₂ 34, −34.0 °C; Br₂ 70, 58.8 °C; I₂ 106, 184.4 °C.
   - `trend`: a dashed line through the halogens and the caption "more electrons," / "higher boiling point".
   - `trio`: CH₄, NH₃ and H₂O as three unlabelled points on the 10-electron line, with the halogens faint.
   - `reveal`: their labels (−161.5, −33.3, 100.0 °C).
   - `HCl`: HCl at 18, −85.1 °C beside F₂ at 18, −188.1 °C, with the others faint.
   - There is no "all eight" stage. All markers share the accent color, because warm and teal stay reserved for δ+ and δ−.
   - Units: the axes, each labelled point (at least 260 px wide, so it fills 60% at the 4× cap), the trend caption. `meta()`: `{points:[{f, e, bp, force, faint, labelled}], trend, xAxis, yAxis, xRange, yRange}`. `force` is "dispersion forces" for the halogens and CH₄, "hydrogen bonding" for NH₃ and H₂O, and "dipole-dipole forces" for HCl.
6. **`forceDecider`** (stages `NH3/polar`, `NH3/H`, `NH3/lone`, `NH3/strongest`, `CO2/polar`, `CO2/H`, `CO2/strongest`, `HBr/EN`, `HBr/polar`, `HBr/H`, `HBr/strongest`).
   - Four boxes in the `cerBuilder` style (`.cer-grid`, `.cer-box`, 40 px text, the current box highlighted): "Polar?", "H on N, O or F?", "Lone pair on N, O or F?", "Strongest attraction".
   - NH₃: "Yes. It is trigonal pyramidal (Lesson 4.4)." → "Yes. H is on N." → "Yes. N has a lone pair." → "Hydrogen bonding."
   - CO₂: "No. It is linear, so the pulls cancel." → "No. CO₂ has no H." (the lone-pair box shows "Not needed." at the same press) → "Dispersion forces."
   - HBr: `EN` highlights "Polar?" and shows, under the drawing, the label line "Electronegativity (pull on electrons)" with chips "Br 2.96", "H 2.20" and "difference 0.76" (the 4.1 `en()` markup) → "Yes. The difference is 0.76." → "No. H is on Br, not N, O or F." (with "Not needed.") → "Dipole-dipole forces."
   - Beside the boxes is a 400 × 300 SVG drawing (CPK, gray sticks, symbol on every atom) with its name ("ammonia, NH₃", "carbon dioxide, CO₂", "hydrogen bromide, HBr"). It shows δ− on N and δ+ on two H atoms, with the lone pair as a lobe in the electron token, for NH₃; no δ for CO₂; δ+ on H and δ− on Br for HBr.
   - Units: each box, the drawing, the electronegativity row. `meta()`: `{stage, molecule, answers:{polar, H, lone, strongest}, en, boxes}`. `answers` holds the boxes filled so far: "yes", "no" or "not needed", and `strongest` is exactly "hydrogen bonding", "dispersion forces" or "dipole-dipole forces".

## Verification
| Item | Result |
|---|---|
| C1 `python3 build.py 4 5 --scratch --out <scratchpad>/scratch45.html` | 139,735 bytes, 1,636 lines, md5 `e1aa2f76cb31d597a2e3b7709ff4a4ae`; 8 slides, 47 frames |
| C2 `python3 suite.py 4 5 --deck <scratch45> --only walk,back,fonts,render3d,extras,zoom,layout,contact --theme both` (K3 set `EMPTY_MAX=1` for walk and layout) | 12 of 12 PASS, exit 0, 373 s. walk light and dark: 47 states, no overflow, cue, advance or console-error failure. back light and dark: 47 forward, 47 back. fonts: PASS (canvas labels 36 px or more, SVG and DOM text 34 px or more). render3d PASS. extras PASS. zoom light and dark: 224 zoomed states, min fill 65%, 8 Back tests, the 2 generic checks PASS. layout: no clipped or ellipsized text, no canvas text cut at an edge. contact sheets light and dark. |
| C3 `DECK=<scratch45> OUT=<folder> node parts/lessons/4-5/scratch-check.js` | PASS, 73 checks, exit 0 (`artifacts/02/scratch/scratch-check.txt`) |
| C5 `suite.py 4 1 --only zoom,keys --theme both` | 3 of 3 PASS, 482 s: keys 48 checks; zoom light and dark: 571 zoomed states, min fill 64%, explicit 11 of 11 (2 generic + 9 from `parts/lessons/4-1/zoomchecks.js`); timer "2:58, expected 2:57 to 2:59", restart "3:00" |
| C5 `suite.py 4 2 --only zoom,keys --theme both` | 3 of 3 PASS, 561 s: keys 48 checks; zoom light and dark: 707 zoomed states, min fill 67%, explicit 14 of 14 (2 generic + 12 from `parts/lessons/4-2/zoomchecks.js`); timer "2:58, expected 2:57 to 2:59", restart "3:00" |

- C2 includes `render3d` (deck-independent: it draws its own scene with the shared renderer), `extras` (reduced motion on the `meltScale` slide and the narrow-screen fallback, with the provisional `extras_cfg`), and `zoom`. Zoom is not asked for this step; it ran as a check of the `units()` geometry. The bench's own caption cards carry `data-zoom="none"`, so zoom measures only the animations: 224 zoomed states, minimum fill 65%.
- C4 sheets in `workshop/artifacts/02/`: `contact-scratch45-light.jpg` and `contact-scratch45-dark.jpg` (the walk: every stage of every instance, 47 presses; about 670 KB each), and `reduced-motion-end-states-light.jpg` and `-dark.jpg` (each animation at its last stage under `prefers-reduced-motion: reduce`, made by `artifacts/02/rmsheet.js`; about 240 KB each).
- Text under `artifacts/02/scratch/`: the suite console, `suite.json`, every audit's log and JSON, `scratch-check.txt` and `scratch-check.json`, and `build-and-shapes.txt` (C1 line and measured minimums). Under `artifacts/02/kproof/`: the 4.1 and 4.2 zoom and keys logs, `suite.json`, the explicit-check lists, and `md5.txt`. There are no per-press folders and no PNGs.

## Repo state
- `unit4/slides-4-1.html` `ebd342f1ee0e11c47157141cf3b2a59b` (194,646 bytes) and `unit4/slides-4-2.html` `c3fa219a806963f9a66c3baf643153f4` (203,769 bytes) after `build.py --all`: unchanged. `unit4/blueprint.html` `ed3bf8e23e1616d95014f0614c74e8d1` is unchanged. No shared part changed.
- Scratch deck (not committed): `e1aa2f76cb31d597a2e3b7709ff4a4ae`, 139,735 bytes.
- `git status --short` before the commit: `M` README.md, audits/keys.js, audits/zoom.js, registry.json, suite.py; `A` parts/lessons/4-1/zoomchecks.js, parts/lessons/4-2/zoomchecks.js, parts/lessons/4-5/{budget.json, chem.js, gen_scratch.py, gen_slides.py, scratch-check.js, scratch.html, sims.html, slides.html} (all under `tools/slides-kit/`); `M` workshop/log.md, workshop/status.md; `A` workshop/reports/02-animations-period-1.md and 47 files under workshop/artifacts/02/. Nothing else; `unit4/` clean. After the commit: in the pull-request comment.

## Deviations
1. **The generic prompt check covers routine slides that carry a prompt.** Brief K1 computes it over every `t-routine` slide. Slide 25 ("Rate your learning") is `t-routine` in both reference decks and has no `.prompt` or `.dq`, so that formula would fail both decks. The check covers 4.1 slides 4, 13 and 20 to 24 and 4.2 slides 4 and 20 to 24, which includes the old lists' slides 20 to 24.
2. **The 4.2 list keeps its check count.** The old 4.2 entry asserted two things: at least 9 zoomed checks, and every zoomed check showing its options. The second is now generic; the first stays in `zoomchecks.js` as "every check card with its options", so no assertion was lost. 4.2 therefore prints 14 explicit checks (2 + 12), where the brief expected 13.
3. **`LESSON` removed from `suite.py`**: no audit reads it after K1. The first 4.1 K-proof still had it set (unused); the K-proofs were re-run with the final kit for the committed logs.
4. **Bench captions use `data-zoom="none"`**, so a zoom audit on the bench measures only the animations. Deck slides are not affected.
5. **Shapes under 60 px.**
   - `meltScale`'s ice-ring H atoms are 40 px across, with 36 px "H" labels that fit. Six water molecules in an open ring do not fit the 336 × 365 particle panel with 60 px hydrogens.
   - The snowman icon's head is 36 px.
   - In the three-row `threeSolids` layout, the back Na⁺ ions of the salt block are 46 px. The front ones are larger, and Na⁺ stays to scale with Cl⁻ (102 : 181 pm).
   - Electron dots (22 to 26 px with their halo, as in 4.1), lone-pair electron dots and the 32 px plot markers are under 60 px by design.
   - Open question 1.
6. **Captions at the foot of the `attractions` host** (dispersion and dipole stages; wording quoted above). Without them a single pair of molecules fills less than half the host, and the deck's one-third emptiness gate would fail on those frames (4.1's `sharedPair` likewise draws down to the bottom of its host). The wording is mine; the orchestrator may change it.
7. **`forceDecider` lone-pair box:** for CO₂ and HBr the flow stops after "H on N, O or F?", so the box shows "Not needed." in muted color at the same press, and `meta()` reports `lone:'not needed'`. At `HBr/EN` no box is filled yet; "Polar?" is highlighted and the electronegativity chips appear.
8. **`forceDecider` hides the other molecules' drawings with the `hidden` attribute.** With `display:none` on a wrapper, the fonts audit read their SVG text at an unscaled CTM (33 px for 40 px text) and failed.
9. **A placeholder 4.5 deck was written to `unit4/` once and deleted (my mistake).** With the 4.5 registry entry in place, `build.py --all` builds 4.5 too. I ran it to recheck the reference md5s, and it wrote the one-slide placeholder to `unit4/slides-4-5.html`. The file was untracked; I deleted it at once and confirmed `git status --short unit4` is empty. The rejected deck is archived at `unit4/old-slides/slides-4-5.html` and was not touched or read. Nothing under `unit4/` is in the commit. Until step 04 builds the real deck, the reference decks rebuild with `build.py 4 1` and `build.py 4 2`; likewise `suite.py --all` would stop at 4.5 ("does not exist"). See open question 6.

## Open questions
1. **Shape floor in two magnified views:** the ice ring (H 40 px) and the three-row salt block (back Na⁺ 46 px). Accept, or change the design: for example fewer water molecules or no icons in `meltScale`, or a two-row last layout in `threeSolids`?
2. **Slide 3 shows ions (salt) and atoms (water, Si–O) on one slide.** RULES 8 asks for the caption "Atom colors show the element, not the charge" there, but plan section 3 lists only slides 6, 15, 17, 18 and 19. The canvas has no room for it, so the deck step would put it in the DOM.
3. **Slide 3's plan reveals the three icons one per press;** `meltScale` has a single `three` stage. Should the deck reveal three DOM captions one per press, or should `meltScale` get `snow`, `salt` and `sand` stages in step 03?
4. **`forceDecider` has no empty stage.** Slide 10 shows the steps card first, so the deck can keep the host hidden until `NH3/polar`, or an `empty` stage can be added.
5. **`keys_cfg` and `extras_cfg` for 4.5 are provisional** (bench ids), per review 01 F3; brief 04 replaces them.
6. **`build.py --all` and `suite.py --all` include 4.5 from now on** (Deviation 9). Should a registry entry be able to mark a deck as not built yet, so `--all` skips it until its deck step? That needs a `build.py` change outside this step's allowed files. The alternative is to name the decks explicitly until step 04.
