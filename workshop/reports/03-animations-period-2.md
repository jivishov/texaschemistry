# Report 03: Period-2 animations for 4.5 on scratch slides, after fixes M1 to M6

Step: 03 · Lesson: 4.5 · Commit: the commit `[implementer] 03: 4.5 period-2 animations on scratch; fixes M1 to M6` on `workshop/unit4-5-6`, parent `7860f1e` (its hash is in the pull-request comment `report 03 ready`)

## Done

### M. Fixes from review 02
- **M1 `meltScale`.**
  - Stages: `snow`, `salt`, `sand` (cumulative: each adds one solid with its icon, name and panel), `melt`, `numbers`.
  - Layout: a row of icons, each 130 px tall:
    - a two-ball snowman whose head is 60 px across;
    - a salt pile with crystals on a step;
    - a sandbox with a bucket.
  - The names sit under the icons. Below them are three equal particle panels (470 × 320 px on the 1472 × 687 host), then the scale.
  - Panels:
    - Snow: three water molecules at full size (H spheres 60 px, O 90 px). The top one gives each of its H to a lone pair of the other two, along two dashed teal hydrogen bonds; the open ring is left to slide 12.
    - Salt: a 3 × 3 grid at 0.30 px per pm, so Na⁺ is 61 px and Cl⁻ 109 px across, at an 85 px (282 pm) spacing.
    - Sand: two Si bridged by one O, each Si with its four O (O 60 px, Si 85 px, Si–O 161 pm × 0.55).
  - `melt`: the molecules let go of their hydrogen bonds and drift to three separate places, each whole; the snowman slumps into a puddle; salt and sand stay.
  - `numbers`: the label line "Melting point" sits on the chip row's left, then the chips "snow 0.0 °C", "salt 801 °C" and "sand near 1700 °C" with markers on the scale (now drawn from x 320).
  - Short layout (height 360 to 599 px; the driving question shown): icons, names, chips, scale. Under 360 px: names, chips, scale.
  - `meta()` adds `shown` (the solids visible), `layout`, and `minSphere`: the smallest atom or ion sphere drawn in canvas px, 60 at every tall stage and `null` in the short layout, where no particles are drawn.
  - The bench's caption line under `meltScale` is gone (Deviation 1), so the host keeps the deck's 687 px.
- **M2 `forceDecider` `empty`**: the first stage shows the four titled boxes with nothing filled, no drawing and no chips. `meta()` gives `molecule:null`, `drawing:false` and all answers `null`.
- **M3 registry flag `built`.**
  - The 4.5 entry has `"built": false`.
  - `build.py --all` prints `4.5: not built yet (registry built: false); skipped` and builds 4.1 and 4.2.
  - `build.py 4 5` without `--out` refuses: "4.5 is not built yet (registry built: false): build it with --out <path> or --scratch --out <path>; the deck step sets built to true". `--out` and `--scratch --out` still work.
  - `suite.py --all` prints the same skip line and runs 4.1 and 4.2.
  - README: a registry-table row for `built`. Docstrings of both scripts updated.
- **M4 `bpPlot` labels.**
  - Two passes: all markers first, faint ones included; then every label with a 10 px halo in the slide colour. A label now always lies over every marker.
  - The NH₃ label sits 46 px above its point and the CH₄ label 22 px above its point, so at `reveal` neither touches the faint Cl₂ and F₂ markers. The F₂ label keeps its 30 px lift.
  - Proof: `artifacts/03/m4-bpPlot-reveal.jpg` and `m4-bpPlot-HCl.jpg`.
- **M5 dispersion badges.** At `flicker`, `neighbor` and `attract`, the δ+ and δ− badges sit centred on each cloud's edge at its two ends, overlapping the outline. The clouds are 172 px apart, so the dashed line between the facing badges stays visible. The cloud width (`rx` = (w − 88 − 172)/4) keeps the outer badges inside the canvas. Proof: `artifacts/03/m5-dispersion-flicker.jpg` and `m5-dispersion-attract.jpg`.
- **M6 nearest-sphere measurement.**
  - Every canvas animation of the lesson now records what it paints into `meta().drawn`: the smallest sphere that stands for an atom or an ion (2D: every one; 3D: per kind the nearest, i.e. the largest projected), and separately the exempt electron dots, δ badges and plot markers. It does this through a lesson-local wrapper (`sim()`, `spheres3d()`, `ion()`).
  - `artifacts/03/scratch/build-and-shapes.txt` lists, per animation and stage (104 frames, reduced motion), the nearest atom or ion sphere and the smallest label: meltScale 60 px, threeSolids 60, attractions (dipole) 60, attractions (H-bond) 60, heating 60, iceLattice 60, conductTester 60 on each of its three slides, hammerBlow 61, networkVsMolecules 65 (`brickBag`, `bpPlot`, `forceDecider` and the dispersion family draw no atom or ion sphere); the smallest canvas label in any frame is 36 px. Every atom or ion sphere is 60 px or more at its nearest depth, step 02's included.
  - Two step-02 changes were needed: the three-row `threeSolids` layout gives the salt row more height (its copper picture is narrower and its label column wider), so its nearest Na⁺ is 60 px; and `meltScale` (M1).

### B. The five period-2 animations
Same contract as step 02 (named stages, tweens of 500 to 900 ms, reduced-motion end states, both themes, `units()`, `meta()`, labels 36 px or more, no text cut at an edge, no raster, no library). Iodine was added to the lesson-local tables: CPK `#940094`, covalent radius 139 pm. `02b-shared.html` and the runtime are unchanged.

1. **`heating`** (stages `CH4/solid`, `CH4/melt`, `CH4/liquid`, `CH4/boil`, `CH4/gas`, `H2O/solid`, `H2O/boil`, `H2O/gas`, `energy`; host 749 × 687).
   - Three readouts at 36 px on top: "Temperature" with a chip of the value; "Covalent bonds: 36 of 36 intact" (H₂O 18 of 18); "Attractions drawn: M".
   - Below, a container with nine molecules, 3 × 3, ball-and-stick CPK (H 60 px, C 98 px, O 90 px):
     - solid: a packed block on the floor, neighbouring CH₄ turned 45° to interlock;
     - `melt`: the top row leaves its places first, each molecule whole;
     - liquid: the block opens a little and the molecules move;
     - boil and gas: the molecules spread to the container's limits, each turned its own way, moving.
   - Dashed gray attraction lines between neighbours: CH₄ 12, 7, 6, 2, 0; H₂O 12, 2, 0.
   - Temperatures word for word from brief 03: "−182.5 °C (melting point)", "−182.5 °C, melting", "liquid", "−161.5 °C, boiling", "−161.5 °C (boiling point)", "0.0 °C (melting point)", "100.0 °C, boiling", "100.0 °C (boiling point)".
   - `energy`: the block fades behind two bars to one scale: "Boiling 18 g of water: 40.7 kJ" (the short bar keeps 28 px with its label beside it) and "Breaking all its O–H bonds: about 928 kJ"; caption "more than 20 times as much".
   - Units: the molecules (container), each readout, each bar, the caption. `meta()`: `{substance, stage, phase, molecules:9, bondsTotal, bondsIntact, attractionsDrawn, temperature, energies:{boil:40.7, bonds:928}, energyBars, caption}`.
2. **`iceLattice`** (stages `molecules`, `hbonds`, `neighbors`, `rings`, `float`; 3D with `Deck.spheres`).
   - The fragment: two stacked chair rings of six molecules (ideal tetrahedral oxygen framework, O···O 276 pm, an open six-sided tunnel down the c axis), plus one molecule more, so one oxygen has all four neighbours. That makes 13 molecules, 26 O–H bonds and 16 O···O links, each holding one H (ice rules). Hydrogen directions are simplified as the data notes allow: free H point along free tetrahedral directions.
   - The view turns slowly while the slide shows and is fixed at three-quarter under reduced motion. "O" and "H" are on every sphere; the nearest H is 61 px.
   - `hbonds`: dashed teal lines, short segments between tiny anchor points, from each H to the next O.
   - `neighbors`: the chosen O ringed warm and its four neighbours ringed teal, the rest faded; label "four neighbors, 276 pm away".
   - `rings`: the view tips to look down the axis and the hexagon reads; label "open six-sided rings".
   - `float`: a tank with a block of ice floating 8.3% above the surface (to scale), the label "8.3% above the surface", and bars "100.0 cm³ of water" and "109.1 cm³ of ice, about 9% more" (to scale). The label line "Density (mass in each cm³)" has chips "ice 0.9167 g/cm³" and "water 0.99984 g/cm³". The lattice gives way to this picture (Deviation 3).
   - Units: the lattice, the ringed oxygen with its neighbours, the label, the floating ice, the bars, the densities. `meta()`: `{molecules:13, bondsOH:26, hbonds:16, hbondsDrawn, neighborsOfChosen:4, distancePm:276, view, lattice, densities:{ice:0.9167, water:0.99984}, volumes:{water:100.0, ice:109.1}, aboveSurfacePct:8.3, reducedView:'fixed', label}`.
3. **`conductTester`**: three bench instances, one per deck slide.
   - Slide 15 (`t-concept wide`): the 236 px `.ptrow` band is kept free through `data-reserve="236"`.
   - Slide 16 (`t-example cb`): host 835 × 687 with the 58/42 split; see open question 3.
   - Slide 17: the dissolve family, in `t-concept cw`.
   - The circuit: the battery on the top wire (− and + at its ends), a switch (open lever at `predict`, closed from `close`), a bulb, and a beaker with two electrodes. The bulb sits on the top wire, or on the right-hand wire when the host is narrow. The sample's name is under the beaker at 40 px (36 px on the narrow host): "solid NaCl", "molten NaCl, 801 °C", "salt water", "copper", "sugar water", "distilled water", "molten KCl", "solid CaCl₂".
   - `close`: the bulb lights (warm glow and rays) for molten NaCl, salt water, copper and molten KCl, and stays dark for the other four.
   - `zoom`: a magnified circle linked to the beaker by a dashed line. Every ion is to scale at 0.30 px per pm (Na⁺ 61, K⁺ 83, Ca²⁺ 60, Cl⁻ 109, Cu cores 77 px); water molecules are CPK at full size.
     - solid NaCl: a 3 × 3 grid, locked;
     - solid CaCl₂: 2 Ca²⁺ and 4 Cl⁻ in two rows, locked;
     - molten NaCl and molten KCl: ions drifting, with short trails;
     - salt water: two ions drifting among three water molecules;
     - copper: gray "+" cores with violet "−" electrons streaming one way and an arrow;
     - sugar water: a compact blob labelled "sugar molecule", no charge sign, among water molecules;
     - distilled water: four water molecules.
   - A readout line, right-aligned under the magnified view on the wide host and at the foot on the narrow one: "Close the switch. Does the bulb light?", "Lights or stays dark?", "The bulb lights." or "The bulb stays dark.", then per sample at `zoom`: "Na⁺ and Cl⁻ locked in place", "Na⁺ and Cl⁻ free to move", "ions move among water molecules", "delocalized electrons move", "whole molecules, no charge", "very few ions", "K⁺ and Cl⁻ free to move", "Ca²⁺ and Cl⁻ locked in place".
   - Dissolve family: the beaker alone with the sample's name above it ("sodium chloride, NaCl", "sucrose (table sugar)", "calcium carbonate, CaCO₃", "iodine, I₂", "quartz, SiO₂", "copper, Cu"). The sample drops in and settles within 1 s.
     - NaCl breaks into six ions that spread: "dissolves: yes" / "ions spread out: an electrolyte".
     - Sucrose spreads as four whole blobs, one labelled: "dissolves: yes" / "whole molecules spread out".
     - CaCO₃ sits as a chunk with a Ca²⁺ and a CO₃²⁻ near it: "dissolves: barely".
     - I₂ tints the water pale yellow-brown, with two I₂ molecules out (I spheres 76 px): "dissolves: slightly".
     - SiO₂ and Cu sit: "dissolves: no".
   - Units: the circuit, the beaker, the magnified view, the readout; dissolve: the beaker, the sample name, the result.
   - `meta()`: tester `{sample, name, state, chargedParticles, freeToMove, lit, litWhenClosed, switchClosed, zoom, carriers}`, holding the table of `lessons/4-5.md`; dissolve `{sample, name, type, dissolves, label}`.
4. **`hammerBlow`** (stages `before`, `blow`, `shift`, `result`; `t-concept wide`, band kept free). Two front layers to one scale (0.30 px per pm), 4 × 3 each, with a faint back layer behind for depth:
   - copper: touching gray "+" cores of 128 pm (77 px) in a violet sea of drifting "−" electrons;
   - salt: Na⁺ 102 pm (61 px) and Cl⁻ 181 pm (109 px) at 282 pm.
   - The stages:
     - `before`: a hammer above each block.
     - `blow`: the hammers strike, with impact strokes.
     - `shift`: both top rows move one spacing. Copper's electrons stream faster with the shift. In salt, every shifted ion now sits over an ion of the same charge, and those three pairs are ringed in `--bad`.
     - `result`: the hammers go. Copper's middle row follows half a spacing, so the block bends in one piece; label "malleable" in `--ok`. Salt's top row lifts away above a `--bad` zigzag crack; label "brittle" in `--bad`.
   - Names "copper" and "salt, NaCl". Units: each block, each hammer, each result label. `meta()`: `{stage, copper:{offsetSpacings, onePiece:true, label}, nacl:{offsetSpacings, likeChargePairs, split, label}, hammer, radii:{Na:102, Cl:181, Cu:128}, spacingPm:282}`, with `likeChargePairs` 3 from `shift` on.
5. **`networkVsMolecules`** (stages `co2`, `sublime`, `quartz`, `heat`, `diamond`).
   - `co2`: six linear CO₂ molecules (O 90 px, C 98 px), 2 × 3, with seven dashed gray dispersion lines flickering between neighbours, and a thermometer reading "−78.5 °C".
   - `sublime`: the molecules fly apart whole and turn, the lines vanish; label "sublimes at −78.5 °C: no liquid".
   - `quartz`: a 3D SiO₂ fragment with `Deck.spheres`, slow turn, fixed under reduced motion. A centre Si with four O, the four Si beyond them, and each of those Si's three other O: 5 Si and 16 O, every Si bonded to four O, the four inner O bridging two Si. Straight Si–O–Si, idealized; Si–O 161 pm. Label "quartz, SiO₂: one network, no molecules". The thermometer is low, without a number.
   - `heat`: the thermometer climbs and reads "above 1000 °C"; the network jiggles and stays; label "to melt it, covalent bonds must break: near 1700 °C".
   - `diamond`: a 17-atom carbon network (a centre C, its four neighbours and their twelve), no thermometer; label "diamond: the hardest natural substance".
   - Units: each solid, the thermometer, each label. `meta()`: `{stage, co2:{molecules:6, intactAfterSublime:true, sublimesAt:-78.5, flown, attractionsDrawn}, sio2:{network:true, molecules:0, meltsNear:1700, si:5, o:16, siFourO:true, oBridging:4}, diamond:{element:'C', network:true, atoms:17}, label, thermometer}`.

## Verification
| Item | Result |
|---|---|
| C1 `python3 build.py 4 5 --scratch --out <scratchpad>/scratch45.html` | `4.5 scratch: <scratchpad>/scratch45.html  188230 bytes, 2097 lines, md5 ce35d127bd8dc42f18e33cf8662282d5` |
| C2 `python3 suite.py 4 5 --deck <scratch45> --only walk,back,fonts,render3d,extras,zoom,layout,contact --theme both` | 12 of 12 PASS (782 s). walk 104 states per theme, max empty 75% (s6f0, scratch gate off); back 104 forward and 104 back per theme; fonts; render3d; extras; zoom 468 zoomed states over 104 frames per theme, min fill 65%, 15 Back tests; layout 104 frames, clipped or ellipsized text 0; contact 99 + 5 shots per theme. Log `artifacts/03/scratch/suite-scratch45.txt` |
| C3 `DECK=<scratch45> OUT=<folder> node parts/lessons/4-5/scratch-check.js` | `scratch-check 4.5: PASS 142 checks`, no console errors (the step-02 assertions, M1 `minSphere >= 60` at every tall `meltScale` stage and its cumulative `shown`, M2 `empty`, and every `meta()` value of brief B). Log `artifacts/03/scratch/scratch-check.txt` |
| M6 nearest-sphere measurement | `104 frames, 0 below 60 px: PASS`, smallest label 36 px. `artifacts/03/scratch/build-and-shapes.txt` |
| C5 `python3 build.py --all` | `4.1: unit4/slides-4-1.html  194646 bytes, 2077 lines, md5 ebd342f1ee0e11c47157141cf3b2a59b`; `4.2: unit4/slides-4-2.html  203769 bytes, 2153 lines, md5 c3fa219a806963f9a66c3baf643153f4`; `4.5: not built yet (registry built: false); skipped`. Both md5 match step 02. `git status --short unit4`: 0 entries |
| C5 `python3 suite.py --all --only timing` | `4.5: not built yet (registry built: false); skipped`; 4.1 timing PASS (period 1 47 min, period 2 47 min); 4.2 timing PASS (47 and 46.5 min); exit 0. Log `artifacts/03/kit/kit-proofs.txt` |

The provisional `extras_cfg` now points at the `iceLattice` bench slide: `{"hash": "#10.0", "canvas": "#il-sim canvas", "block": "il-note", "slides": 15}`. The reduced-motion check therefore compares the turning lattice at two moments, and the revealed block is the bench's note line.

Sheets under `workshop/artifacts/03/`:
- the walk contact sheets of both themes, each split in three to stay under 800 KB (`contact-scratch45-light-1.jpg` to `-3.jpg`, `contact-scratch45-dark-1.jpg` to `-3.jpg`);
- the reduced-motion end states (`reduced-motion-end-states-light.jpg`, `-dark.jpg`);
- the M4 and M5 screenshots at full size;
- text under `scratch/` (suite console and summary, every audit's log and JSON, `scratch-check.txt` and `.json`, `build-and-shapes.txt`) and `kit/` (the C5 lines).

## Repo state
- `unit4/slides-4-1.html` `ebd342f1ee0e11c47157141cf3b2a59b` (194,646 bytes) and `unit4/slides-4-2.html` `c3fa219a806963f9a66c3baf643153f4` (203,769 bytes): unchanged. Nothing was written for 4.5 (`git status --short unit4` empty). No shared part or audit changed.
- Scratch deck (not committed): `ce35d127bd8dc42f18e33cf8662282d5`, 188,230 bytes, 2,097 lines.
- `git status --short` before the commit: `M` `tools/slides-kit/README.md`, `build.py`, `suite.py`, `registry.json`, and in `parts/lessons/4-5/`: `gen_scratch.py`, `scratch-check.js`, `scratch.html`, `sims.html`; `M` `workshop/status.md`, `workshop/log.md`; `A` this report and 39 files under `workshop/artifacts/03/`. Nothing else. After the commit: in the pull-request comment.

## Deviations
1. **The bench caption under `meltScale` was removed.** It took 84 px of the host that the deck's slide 3 does not lose before the driving question appears. Without it the tall layout gets the deck's 687 px.
2. **`registry.json` `extras_cfg`** moved to the `iceLattice` bench slide, as brief C1 asks; the constraints list only the `built` flag for the registry.
3. **`iceLattice` `float`: the lattice gives way to the floating ice instead of standing beside it.** With every sphere at 60 px or more at its nearest depth, the 13-molecule lattice needs about 600 × 520 px. The tank, the two bars and the density chips need the rest of the 749 × 687 host, so the two cannot stand side by side. The `rings` stage just before keeps the lattice on screen. Open question 1.
4. **`heating`: the CH₄ gas cannot spread "far apart" in this container.** Nine CH₄ molecules with 60 px hydrogens already fill most of the 733 × 519 container as a packed solid: 190 × 128 px apart, neighbours turned 45° so their H interlock. The gas can only reach 248 × 150 px apart, about 1.5 times the solid's area per molecule. Water spreads more clearly: 172 × 118 to 248 × 160. The readouts carry the rest ("Attractions drawn: 0", the temperatures). Open question 2.
5. **Wording I added, beyond the brief's quoted lines:**
   - `conductTester`: the readout lines (quoted above), "dissolves: …" before each dissolve label, and the "sugar molecule" callout in the dissolve beaker;
   - `iceLattice`: "8.3% above the surface";
   - `networkVsMolecules`: the thermometer's "above 1000 °C" (no number at `quartz`);
   - `hammerBlow`: the names "copper" and "salt, NaCl".
6. **`hammerBlow` is drawn as front layers with a faint offset back layer** (an isometric hint) rather than with `Deck.spheres`, so the two blocks stay to one scale with every front sphere at 60 px or more.
7. **`networkVsMolecules` quartz is idealized** with straight Si–O–Si (cristobalite-like geometry), as `polyIons` idealizes its ions; the reading names no angle.

## Open questions
1. **`iceLattice` `float`:** is the lattice giving way to the floating ice acceptable (Deviation 3)? The alternatives are a smaller lattice there (H under 60 px) or the float picture on the next press without the lattice.
2. **`heating` with CH₄:** accept the modest spread (Deviation 4), or change the design: six molecules, or the gas drawn in a wider host?
3. **Slide 16's `t-example cb` split (58/42)** lives in 4.2's `css.css`. The 4.5 deck needs the same rule: a 4.5 `css.css` with the marker `css-45` (a registry `css` change), or a move of the rule into the shared head (a shared-part change with both reference decks re-audited). The bench sets it inline.
4. **`conductTester` readouts and the "dissolves: …" lines** are my wording (Deviation 5). Confirm, or give the wording in brief 04.
