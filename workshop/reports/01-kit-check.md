# Report 01: Kit check (generalized kit adopted, overlap check, Unit 5 cross-check form)

Step: 01 · Lesson: 5.1 · Commit: none (in-session; no git state changes by the implementer, the orchestrator commits)

## Done
1. **Baseline (item 0)**, recorded before anything was touched (13:41 UTC). The expected md5s matched (table under "Verification").
2. **Kit adopted (item 1).** Removed today's layout: `tools/slides-kit/step1` (35 files), `step6`, `step7`, `step10` (3), `final`, `README.md`
   (42 tracked files). Extracted `git archive 52e1f8e7c0112fe92e412d2d98f30c5cb9dd7f6e tools/slides-kit | tar -x -C /home/user/texaschemistry`.
   Removed `parts/lessons/4-5/` (10 files) and the 4.5 entry of `registry.json`. Kept `docs/handoff-4-1-4-2.md`.
   `parts/shared/02-runtime.html` is the same text as the old `step1/src/02-runtime.html` (md5 `ca9c23d7bbdfed4244590833e27e42fe` both).
3. **Byte identity (item 2).** `python3 tools/slides-kit/build.py --all` right after the adoption: 4.1 `ebd342f1ee0e11c47157141cf3b2a59b`,
   4.2 `c3fa219a806963f9a66c3baf643153f4`, equal to step 0; `git status --short` showed nothing under `unit4/` or `unit5/`. No
   `git checkout` was needed.
4. **Adopted suite as is (item 3)**, before any kit change: every audit PASS (table under "Verification").
5. **Overlap check (item 4)** in `audits/layout.js`, theme argument `layout.js light|dark` (default light); `suite.py` runs layout once per
   theme. Per frame: the older checks run after 100 ms exactly as before; then a settle wait (the boxes of `.acc` cards, options and
   footer spans equal two animation frames apart, at most 15 tries); then:
   - DOM boxes on `.slide.current` and in `#foot`, in 1600 x 900 canvas px: text lines (every visible element with its own visible text,
     plus the brief's list `p, li, td, th, h2, .line, .cell, .rh, .q, .ans, .fb, .tag, .term, .mean, .k, .small, .cap, .nm, .fm, .bt, .why,
     .big, .hdr` when they hold visible text), cards (`.card, .phase, .wcard, .item, .key, .colh, .cer-box`), chips and badges (`.chip,
     .badge, .es, .rail li, .legend>span, .scale span, .opt`), footer spans `#sec, #cue, #count`. Block elements: border box; inline
     elements (`sup`, `b`, …): one rectangle per line (`getClientRects`). Skipped: hidden, `display: none`, zero-size, opacity 0
     (multiplied up the ancestors), inside `.notes`, `script`, `style`, `svg`, `.timer:not(.run)`, `.zoomed`.
   - Intersection: overlap > 2 px in both directions and neither box inside the other (within 2 px); ancestor pairs skipped.
   - Canvas labels by instrumentation through `page.addInitScript` (the runtime is unchanged): a setter for `window.Deck` installs a setter
     for `Deck.canvasSim`; the wrapped `canvasSim(host, spec)` replaces `spec.draw` with a function that hands the sim a `Proxy` of the
     painter `g`. `text`, `chem`, `badge`, `fit` record label boxes (x from x and align, width from `ctx.measureText` with the painter's font,
     `chem` its returned width, y from y and the baseline, height the font size); `circle`, `rrect`, `electron` (the dot, r + 1.5),
     `badge` record shape boxes (half the stroke included). `host.__boxes = {labels, shapes, stage}` is cleared at the start of each
     on-screen paint; the renders of `bounds()` (on a detached canvas) are not recorded; calls at `globalAlpha` ≤ 0.01 are not recorded.
     `D.spheres` draws through the proxy, so its spheres and symbols are covered. The wrap is reliable here: 10 of 10 (4.1) and 14 of
     14 (4.2) canvas animations wrapped, every visible canvas had a recorded paint on every frame; the audit fails if either breaks.
   - Canvas assertions per frame and animation: no two labels intersect by more than 2 px both ways; no label partly cuts a shape (a
     label inside one shape, within 2 px, is that shape's label). Reported with the animation id, stage, label text and shape kind.
   - Gate: any intersection fails the frame and the audit. Output: `layout-<theme>.json`, `overlap-<theme>.txt`, crops of up to six
     failing frames (one per slide first) in `overlap-<theme>/`, A outlined red and B blue.
6. **Unit 5 form (item 5)** in `audits/xcheck.js`, chosen by `blueprint.form` (`"unit4"` when absent: the Unit 4 parser and assertions,
   unchanged). `suite.py` now passes `form`, `teks_rows`, `checks` and `periods` in `XCHECK`. For `"unit5"`, inside `section`..`next`:
   the deck line (N = slide count; A..B = four slides, titles starting "Checkpoint", the first the routine; C = D = "Predictions and exit
   ticket"; E = "Rate your learning"); the objectives table rows `<tr><td>5.1.k</td><td>…</td><td>…</td><td>SLIDES</td></tr>` (each slide
   exists and its footer reference names the objective, the Unit 4 `covers` rule); in section `matrix`, per TEKS code of `teks_rows`, the
   one row whose first cell carries the code and holds "Deck 5.1, slides …" (its objectives cell names the code's objectives; each
   listed slide carries one of them; the listed slides equal the union of the objectives' slides); checks and periods against the
   registry and the deck; rate slide, mentions and footer cues as today. Dry run: `--dry` or `XCHECK_DRY=1` (no deck, no browser).
7. **README (item 6)**: "The overlap check (layout audit)" and "The blueprint cross-check (xcheck) and its forms" sections, the dry-run
   command, `blueprint.form` / `teks_rows` in the registry table, `XCHECK` row, layout per theme and its outputs, the Lesson 5.1 marker
   example (`01-head-51`, `02-runtime`, `02b-shared`, `sims-51`, `slides-51`, `css-51` if it has a `css.css`) in place of 4.5's, "Add a
   lesson" with the 5.1 registry fields and `python3 build.py 5 1` → `unit5/slides-5-1.html` (`unit5/old-slides/`), and the line "No
   absolute path remains: `grep -rnE -- '/(home|tmp)/' tools/slides-kit` finds only `docs/handoff-4-1-4-2.md` … as history". The
   `/tmp/` examples became `<scratchpad>`.

### Tree of the adopted layout
```
tools/slides-kit/
├── audits/   back.js click.js contact.js cycle.js extras.js fonts.js keys.js layout.js lib.js print.js readability.js
│             render3d.js supgap.js timing.js units.js walk.js xcheck.js zoom.js zoomsheet.js
├── docs/     handoff-4-1-4-2.md
├── parts/
│   ├── lessons/
│   │   ├── 4-1/  budget.json chem.js gen_slides.py scratch.html sims.html slides.html zoomchecks.js
│   │   └── 4-2/  budget.json chem.js css.css gen_scratch.py gen_slides.py scratch.html sims.html slides.html zoomchecks.js
│   └── shared/   01-head.html 02-runtime.html 02b-shared.html
├── README.md
├── build.py
├── registry.json
├── split_parts.py
└── suite.py
```

### registry.json (in full)
```json
{
  "decks": [
    {
      "unit": 4,
      "lesson": 1,
      "file": "unit4/slides-4-1.html",
      "title": "Predicting Bond Type Slides",
      "description": "Unit 4, Lesson 4.1 projector slides: Predicting bond type (TEKS C.7(A)).",
      "periods": [[1, 13], [14, 25]],
      "checks": 9,
      "markers": ["01-head", "02-runtime", "02b-shared", "03-sims", "04-slides"],
      "css": null,
      "keys_cfg": {"cr": "s07", "sim": "cr-sim", "card": "cr-rule", "tm": "s19", "ex": "s03", "hk": "s02", "notes": ["s09", 6]},
      "extras_cfg": {"hash": "#7.2", "canvas": "#cr-sim canvas", "block": "cr-rule", "slides": 25},
      "budget": "parts/lessons/4-1/budget.json",
      "chem": "parts/lessons/4-1/chem.js",
      "zoom_checks": "parts/lessons/4-1/zoomchecks.js",
      "blueprint": {"section": "41", "next": "42"},
      "matrix": ["4.1.1", "4.1.2", "4.1.3", "4.1.4", "4.1.5"],
      "mentions": {
        "s02:5": "Targets and words", "s02:6": "Forming ions", "s02:7": "The crystal", "s02:8": "Covalent bonds", "s02:9": "Polar and nonpolar", "s02:10": "Metallic bonds",
        "s04:24": "Predictions and exit ticket", "s05:25": "Rate your learning", "s05:11": "One picture for three bonds", "s06:7": "The crystal", "s11:5": "Targets and words",
        "s15:17": "Near the line", "s16:11": "One picture for three bonds", "s20:21": "Checkpoint 1", "s20:22": "Checkpoint 2", "s20:23": "Checkpoint 3", "s24:4": "Predict now"
      },
      "extra_audits": [],
      "extra_slides": null
    },
    {
      "unit": 4,
      "lesson": 2,
      "file": "unit4/slides-4-2.html",
      "title": "Ionic Formulas and Names Slides",
      "description": "Unit 4, Lesson 4.2 projector slides: Ionic compounds: formulas and names (TEKS C.7(B)).",
      "periods": [[1, 13], [14, 26]],
      "checks": 9,
      "markers": ["01-head-42", "02-runtime", "02b-shared", "06-sims-42", "08-slides-42"],
      "css": "01c-css-42",
      "keys_cfg": {"cr": "s12", "sim": "s12-nb", "card": "s12-c1", "tm": "s18", "ex": "s09", "hk": "s02", "notes": ["s15", 0]},
      "extras_cfg": {"hash": "#15.1", "canvas": "#s15-sim canvas", "block": "s15-r3", "slides": 26},
      "budget": "parts/lessons/4-2/budget.json",
      "chem": "parts/lessons/4-2/chem.js",
      "zoom_checks": "parts/lessons/4-2/zoomchecks.js",
      "blueprint": {"section": "42", "next": "43"},
      "matrix": ["4.2.1", "4.2.2", "4.2.3", "4.2.4", "4.2.5"],
      "mentions": {
        "s02:18": "You do: six compounds", "s03:12": "The Stock system", "s04:24": "Predictions and exit ticket", "s05:25": "Rate your learning", "s08:9": "Writing the formula",
        "s10:8": "Balancing the charges", "s11:15": "Polyatomic ions", "s12:3": "Two copper oxides", "s16:2": "Read the label", "s18:2": "Read the label",
        "s20:21": "Checkpoint 1", "s20:22": "Checkpoint 2", "s20:23": "Checkpoint 3", "s24:4": "Predict now", "s24:3": "Two copper oxides"
      },
      "extra_audits": ["units", "cycle"],
      "extra_slides": [6, 12]
    }
  ]
}
```

### Changed kit files against the adopted commit 52e1f8e (one line each)
| File | Change |
|---|---|
| `registry.json` | the 4.5 entry removed (26 lines); 4.1 and 4.2 entries unchanged (no `form`: absent means `"unit4"`) |
| `parts/lessons/4-5/` | removed (10 files) |
| `audits/layout.js` | theme argument; settle wait; the overlap check (DOM boxes, canvas labels by instrumentation), `layout-<theme>.json`, `overlap-<theme>.txt`, crops; helpers exported; the older per-frame checks' code unchanged, `open` now gets the theme and the init script (+158/−8 lines) |
| `audits/lib.js` | `open()` takes an optional `init` script, added with `page.addInitScript` before the deck loads (+1 line) |
| `audits/xcheck.js` | `blueprint.form`: the Unit 5 parser and assertions, `--dry` / `XCHECK_DRY=1`; the Unit 4 matrix pre-pass limited to Unit 4-form decks; Unit 4 assertions unchanged (+84/−7) |
| `suite.py` | layout runs once per theme; `XCHECK` carries `form`, `teks_rows`, `checks`, `periods`; docstring (+8/−4) |
| `README.md` | item 6 (+82/−17) |
Unchanged from 52e1f8e: `build.py`, `split_parts.py`, every other audit, all parts of 4.1 and 4.2 (`build.py` regenerated both `slides.html` byte-identical), `docs/`.

## Verification
### md5 and size (all unchanged; `artifacts/01/md5.txt`)
| File | Step 0 (before) | Step 2 (kit adopted) | Step 7 (after the kit changes) | Bytes (all three) |
|---|---|---|---|---|
| `unit4/slides-4-1.html` | `ebd342f1ee0e11c47157141cf3b2a59b` | same | same | 194,646 |
| `unit4/slides-4-2.html` | `c3fa219a806963f9a66c3baf643153f4` | same | same | 203,769 |
| `unit4/blueprint.html` | `ed3bf8e23e1616d95014f0614c74e8d1` | same | same | 44,978 |
| `unit5/blueprint.html` | `0b7dbba88781ca560acdd200ac320a1f` | same | same | 57,938 |

### Suites, light theme, matrix off (`artifacts/01/suite-before.txt`, `suite-after.txt`, `logs-before/`, `logs-after/`)
**4.1**: before 17 of 17 PASS in 667.6 s; after 16 of 17 PASS in 673.0 s (FAIL: layout light, in the overlap check only).

| Audit | Before | s | After | s | After: verdict line (cut at 150 characters) |
|---|---|---|---|---|---|
| walk light | PASS | 195.7 | PASS | 193.9 | walk light: 156 states, max empty 29% (s4f0), PASS |
| back light | PASS | 77.5 | PASS | 77.8 | back: 156 forward, 156 back, PASS |
| fonts light | PASS | 48.0 | PASS | 48.3 | fonts: PASS |
| keys | PASS | 36.1 | PASS | 36.0 | keys: PASS 48 checks |
| readability | PASS | 3.0 | PASS | 3.0 | readability: PASS |
| print | PASS | 2.2 | PASS | 2.1 | print: PASS stage hidden=true, 25 slides, 156 frame lines, 9 PDF page(s) |
| render3d | PASS | 2.4 | PASS | 2.6 | render3d: PASS |
| extras | PASS | 5.7 | PASS | 6.0 | extras: PASS |
| chem | PASS | 1.6 | PASS | 1.7 | chem (deck): PASS 32 checks |
| timing | PASS | 1.3 | PASS | 1.4 | timing: period 1 47 min, period 2 47 min, PASS |
| supgap | PASS | 4.6 | PASS | 4.6 | supgap: 25 symbol+charge pairs checked, PASS |
| zoom light | PASS | 233.1 | PASS | 233.3 | zoom light: 571 zoomed states over 156 frames (re-flow 432, transform 139), prompt 45, r800 1, animation 75, card 137, part 42, frames 1, check 24, w… |
| click | PASS | 28.2 | PASS | 28.7 | click: 9 graded checks, 3 Predict-now questions, 47 assertions, PASS |
| layout light (before: layout) | PASS | 19.7 | **FAIL** | 24.4 | layout light: 156 frames, 24 visible option lists (stacked 7, row 17), max empty 29% (s4f0), gate 33%, clipped or ellipsized text: 0, overlap: 175 in… |
| xcheck | PASS | 1.7 | PASS | 1.7 | xcheck: 42 of 42 pass |
| contact light | PASS | 4.4 | PASS | 4.9 | contact sheets light: contact-light-1.png (102 shots, 3710 px tall), contact-light-2.png (54 shots, 1990 px tall) |
| zoomsheet light | PASS | 2.5 | PASS | 2.6 | zoom sheet light: zoomsheet-light-1.png (79 shots, 3065 px tall) |

**4.2**: before 19 of 19 PASS in 917.4 s; after 18 of 19 PASS in 921.4 s (FAIL: layout light, in the overlap check only).

| Audit | Before | s | After | s | After: verdict line (cut at 150 characters) |
|---|---|---|---|---|---|
| walk light | PASS | 212.9 | PASS | 213.2 | walk light: 173 states, max empty 32% (s10f1), PASS |
| back light | PASS | 85.7 | PASS | 85.6 | back: 173 forward, 173 back, PASS |
| fonts light | PASS | 51.7 | PASS | 51.5 | fonts: PASS |
| keys | PASS | 35.9 | PASS | 36.0 | keys: PASS 48 checks |
| readability | PASS | 3.4 | PASS | 3.1 | readability: PASS |
| print | PASS | 2.3 | PASS | 2.2 | print: PASS stage hidden=true, 26 slides, 173 frame lines, 8 PDF page(s) |
| render3d | PASS | 2.7 | PASS | 2.6 | render3d: PASS |
| extras | PASS | 5.7 | PASS | 5.7 | extras: PASS |
| chem | PASS | 1.7 | PASS | 1.7 | chem42 (deck): PASS 39 checks |
| timing | PASS | 1.3 | PASS | 1.3 | timing: period 1 47 min, period 2 46.5 min, PASS |
| supgap | PASS | 4.7 | PASS | 4.8 | supgap: 139 symbol+charge pairs checked, PASS |
| zoom light | PASS | 276.7 | PASS | 276.0 | zoom light: 707 zoomed states over 173 frames (re-flow 503, transform 204), prompt 35, r800 1, animation 96, part 108, card 159, frames 1, check 24, … |
| click | PASS | 31.0 | PASS | 31.1 | click: 9 graded checks, 3 Predict-now questions, 47 assertions, PASS |
| layout light (before: layout) | PASS | 22.7 | **FAIL** | 26.8 | layout light: 173 frames, 24 visible option lists (stacked 15, row 9), max empty 32% (s10f1), gate 33%, clipped or ellipsized text: 0, overlap: 95 in… |
| units | PASS | 10.5 | PASS | 10.6 | 63 frames, 89 visible cards and captions, 0 frames with a card missing or twice: PASS |
| cycle | PASS | 159.0 | PASS | 159.3 | 112 checks, 0 short cycles |
| xcheck | PASS | 1.8 | PASS | 1.8 | xcheck: 40 of 40 pass |
| contact light | PASS | 5.2 | PASS | 5.5 | contact sheets light: contact-light-1.png (101 shots, 3710 px tall), contact-light-2.png (72 shots, 2635 px tall) |
| zoomsheet light | PASS | 2.6 | PASS | 2.6 | zoom sheet light: zoomsheet-light-1.png (83 shots, 3065 px tall) |

### Overlap results (light)
The check fails on both reference decks. Per the brief, the decks and the check were left as they are; every failing frame and its boxes is listed in
`artifacts/01/overlap-4-1-light.txt` and `overlap-4-2-light.txt` (A and B as `[x0, y0, x1, y1]` in canvas px). The dev run and the proof run gave
the same frames and boxes.

| Deck | Frames | Failing frames | Intersections | Boxes measured (DOM / canvas labels / canvas shapes) | Canvas animations instrumented | Repeated labels |
|---|---|---|---|---|---|---|
| 4.1 | 156 | 22 | 175 | 6,395 (2,813 / 1,690 / 1,892) | 10 of 10 | 0 |
| 4.2 | 173 | 38 | 95 | 7,259 (3,012 / 2,278 / 1,969) | 14 of 14 | 0 |

Failing frames. 4.1: s6f2 to s6f5, s7f0 to s7f5, s10f1 to s10f9, s16f3 to s16f5. 4.2: s4f0, s7f4, s7f6, s8f2 to s8f10, s9f6, s9f7,
s10f2 to s10f4, s15f0 to s15f9, s16f0 to s16f2, s17f0 to s17f6, s24f0.

The kinds of intersection come from a scratchpad script, not part of the kit or the gate. It splits the hits and re-tests each label against a round shape with the circle itself instead of its box:

| Deck | Kind | Count | Frames | What it is (crops under `artifacts/01/overlap/`) |
|---|---|---|---|---|
| 4.1 | label cuts a circle (the circle itself too) | 61 | s7f1–f5, s10f1 | s7: the 3D NaCl lattice (`D.spheres`), labels of far, fogged ions under nearer spheres; s10f1: the "sodium" label over an electron ball (47 × 16 px), plainly visible (`4-1-s10f1.jpg`) |
| 4.1 | label cuts an electron (the dot itself too) | 37 | s10f2–f9 | electron-sea still positions: electron dots over the core labels "+", "2+", "3+", plainly visible |
| 4.1 | label ∩ rrect | 35 | s16f3–f5 | periodic table: the enlarged highlight of the chosen element cuts the neighbours' symbols (Li, Be, Mg, …) (`4-1-s16f3.jpg`) |
| 4.1 | label only in the box corner of a circle | 26 | s6f2–f5, s7f0–f5 | the "+" badge beside Na⁺ lies inside the ion circle's bounding box but outside the circle (`4-1-s7f0.jpg`) |
| 4.1 | label ∩ label | 12 | s7f1–f5, s16f3–f5 | lattice labels under each other; s16: the chosen cell's small symbol hidden under its highlight's large one |
| 4.1 | DOM: a sup inline box | 3 | s6f2, s7f4, s7f5 | the "+" or "−" superscript box reaches 7 px into the tag line above |
| 4.1 | label only in the box corner of an electron | 1 | s10f4 | |
| 4.2 | DOM: a sup/sub inline box | 69 | 36 frames | a charge superscript's box reaches 7 to 15 px into the line box above ("Question 1", "Check", "Squad", "Ions", "Balance", the six ion names of s15); the glyphs nearly touch (`4-2-s4f0.jpg`, `4-2-s15f0.jpg`) |
| 4.2 | DOM: other | 6 | s9f6, s9f7 | the inline-block formulas K₂S and Ca₃N₂ (73 px tall boxes) overlap the lines next to them by 3 to 9 px; the subscript 2 of K₂S almost touches Ca₃N₂ (`4-2-s9f6.jpg`) |
| 4.2 | label only in the box corner of a circle | 10 | s15f0–f9 | "one unit" crosses the box of the dashed ring, not the ring |
| 4.2 | label cuts a circle | 7 | s15f0, s15f4–f9 | 3D models: the central atom's symbol ("N", "S", "P") over the box of an atom drawn behind that atom's own sphere |
| 4.2 | label ∩ label | 3 | s15f0, s16f1, s16f2 | s15f0 "H" ∩ "N"; s16: two stacked OH⁻ cards, the back card's label under the front card |

Crops (A red, B blue), 13 to 61 KB each: `overlap/4-1-s7f0.jpg`, `4-1-s10f1.jpg`, `4-1-s16f3.jpg`, `4-2-s4f0.jpg`, `4-2-s9f6.jpg`,
`4-2-s15f0.jpg`.

### Proofs that nothing else changed
- xcheck Unit 4 form: the adopted `xcheck.js` and the new one run with the same configuration on 4.1 and 4.2 (the before-run's walk files):
  `xcheck.json` and the logs byte-identical (4.1 42 of 42, 4.2 40 of 40).
- layout's older checks: per-frame records (emptiness, option lists) and failures of the before run and the new audit identical on
  4.1 (156 frames) and 4.2 (173 frames), zero non-overlap failures in both.
- Unit 5 path smoke test (not an artifact): the 4.1 deck against the Unit 5 blueprint with form `"unit5"` ran to the end; the deck line,
  rows and unions parsed and passed, the deck-dependent assertions failed as they must for a different deck.

### xcheck dry run (`artifacts/01/xcheck-unit5-dry.txt`)
```
# cd tools/slides-kit; XCHECK='[{"lesson": "5.1", "blueprint": "../../unit5/blueprint.html", "section": "l51", "next": "l52", "form": "unit5", "teks_rows": {"C.8(A)": ["5.1.1", "5.1.2"], "C.8(B)": ["5.1.3", "5.1.4"]}, "objectives": ["5.1.1", "5.1.2", "5.1.3", "5.1.4"]}]' node audits/xcheck.js --dry
# unit5/blueprint.html md5 0b7dbba88781ca560acdd200ac320a1f
xcheck --dry: 5.1, ../../unit5/blueprint.html, form unit5, section l51 (to l52), no deck
  deck line: "Deck: 22 slides. Checkpoints 16 to 19, predictions revisited 20, CER exit ticket 21, self-rating 22."
  section l51: deck 22, checkpoints 16 to 19, predictions 20, exit 21, rating 22
  objectives: 5.1.1 "5, 6", 5.1.2 "7 to 11, 15", 5.1.3 "12, 13", 5.1.4 "14"
  matrix: C.8(A) "5 to 11, 15", C.8(B) "12 to 14"
    C.8(A): row "C.8(A) the mole", objectives cell "§5.1.1, §5.1.2"; slides 5, 6, 7, 8, 9, 10, 11, 15; union of 5.1.1, 5.1.2: 5, 6, 7, 8, 9, 10, 11, 15 (equal)
    C.8(B): row "C.8(B)", objectives cell "§5.1.3, §5.1.4, §5.3.1 to §5.3.3"; slides 12, 13, 14; union of 5.1.3, 5.1.4: 12, 13, 14 (equal)
xcheck --dry: every item found; no assertion run against a deck
# exit 0
```

### Absolute paths
`grep -rn -- '/home/\|/tmp/' tools/slides-kit` → only `tools/slides-kit/docs/handoff-4-1-4-2.md` (lines 8, 9, 10, 43).

## Repo state
md5s: table above (no deck changed; no shared part changed). Branch `workshop/unit5-5-1`; no git state change by the implementer.
HEAD moved during the step from `455d263` to `68e76ce` through the orchestrator's own commit ("[orchestrator] 02: draft brief 02", 13:43:13
UTC, only `workshop/briefs/02-animations-and-deck.md`), which touches none of this step's files. `git status --short` (51 lines: the 42
removed files of the old layout, then the new layout and this step's workshop files):
```
 M tools/slides-kit/README.md
 D tools/slides-kit/final/handoff.md
 D tools/slides-kit/step1/back.js
 D tools/slides-kit/step1/build.sh
 D tools/slides-kit/step1/build42.sh
 D tools/slides-kit/step1/chem-deck.js
 D tools/slides-kit/step1/chem42-deck.js
 D tools/slides-kit/step1/click.js
 D tools/slides-kit/step1/contact.js
 D tools/slides-kit/step1/extras.js
 D tools/slides-kit/step1/fonts.js
 D tools/slides-kit/step1/keys.js
 D tools/slides-kit/step1/layout.js
 D tools/slides-kit/step1/lib.js
 D tools/slides-kit/step1/print.js
 D tools/slides-kit/step1/readability.js
 D tools/slides-kit/step1/render3d.js
 D tools/slides-kit/step1/run-all.sh
 D tools/slides-kit/step1/run-all42.sh
 D tools/slides-kit/step1/src/01-head.html
 D tools/slides-kit/step1/src/01c-css-42.css
 D tools/slides-kit/step1/src/02-runtime.html
 D tools/slides-kit/step1/src/02b-shared.html
 D tools/slides-kit/step1/src/03-sims.html
 D tools/slides-kit/step1/src/04-slides.html
 D tools/slides-kit/step1/src/05-scratch.html
 D tools/slides-kit/step1/src/06-sims-42.html
 D tools/slides-kit/step1/src/07-scratch-42.html
 D tools/slides-kit/step1/src/08-slides-42.html
 D tools/slides-kit/step1/src/gen_scratch42.py
 D tools/slides-kit/step1/src/gen_slides.py
 D tools/slides-kit/step1/src/gen_slides42.py
 D tools/slides-kit/step1/supgap.js
 D tools/slides-kit/step1/timing.js
 D tools/slides-kit/step1/walk.js
 D tools/slides-kit/step1/zoom.js
 D tools/slides-kit/step1/zoomsheet.js
 D tools/slides-kit/step10/cyclecheck.js
 D tools/slides-kit/step10/split_parts.py
 D tools/slides-kit/step10/units67.js
 D tools/slides-kit/step6/budget42.json
 D tools/slides-kit/step7/xcheck.js
?? tools/slides-kit/audits/
?? tools/slides-kit/build.py
?? tools/slides-kit/docs/
?? tools/slides-kit/parts/
?? tools/slides-kit/registry.json
?? tools/slides-kit/split_parts.py
?? tools/slides-kit/suite.py
?? workshop/artifacts/01/
?? workshop/reports/01-kit-check.md
```

## Deviations
1. **`fit` labels are recorded too.** The brief lists `text`, `chem` and `badge`; `g.fit` also draws labels (the periodic-table symbols
   of 4.1 slide 16 and 4.2's table), and RULES 11 says the painter records every label box. Recorded as kind `fit`, the drawn width.
2. **A label drawn twice at the same place counts once** (same text, box within 0.5 px). Counted and printed as "repeated canvas labels"
   when it happens; it did not happen on 4.1 or 4.2 (0).
3. **Box definitions the brief left open:** an electron's box is its dot (r + its 3 px stroke), not the faint halo at 30% alpha; circle
   and rrect boxes include half the stroke width; labels with an `alphabetic` baseline are placed 0.8 of the size above y; calls drawn at
   `globalAlpha` ≤ 0.01 are skipped (the sims' own draw gate is `> .01`).
4. **`lib.js` changed by one line** (`open({init})` → `page.addInitScript` before `goto`), the only way to install the setter before the
   runtime runs with `lib.open`; no other audit passes `init`, so their behavior is unchanged.
5. **layout's file names and verdict line**: `layout.json` → `layout-<theme>.json`, log `logs/layout-light.log`, the line starts
   "layout light:" (as walk does) and adds the overlap counts. Nothing reads `layout.json`.
6. **xcheck, Unit 4 pre-pass**: the "matrix: N rows found" pre-pass now reads only Unit 4-form decks; otherwise a Unit 5 deck in
   `XCHECK` would fail a Unit 4 assertion. Output for 4.1 and 4.2 is byte-identical (above).
7. **xcheck, Unit 5 matrix row**: besides the brief's two assertions, the row assertion requires exactly one row per TEKS code naming
   "Deck 5.1" and its objectives cell naming the registry's `teks_rows` objectives, so the registry and the blueprint row cannot
   disagree silently. The deck-line pattern also accepts a clause after "N slides" (", with the Honors hydrate at 14", as 5.4 and 5.5
   print it); 5.1's line has none.
8. **Dry run** supports form `"unit5"` only (the Unit 4 form is parsed inside its assertions, which stay unchanged).
9. **Crops**: the audit writes up to six per deck in the suite output; `artifacts/01/overlap/` holds six in all, three per deck, chosen to show
   different kinds of failure.

## Open questions
1. **The reference decks fail the overlap check** (light): 4.1 has 175 intersections on 22 of 156 frames, 4.2 has 95 on 38 of 173. So `suite.py --all`,
   `suite.py 4 1` and `suite.py 4 2` exit 1 until this is decided; every other audit passes. The options I see, none acted on:
   (a) fix the reference decks' lesson parts. Their md5s would change. The plainly visible cases are 4.1 s10 (electrons over the core labels and "sodium") and
   4.2 s9 (formula lines).
   (b) change what the check measures:
   - round shapes as circles instead of boxes: 4.1 drops 27, 4.2 drops 10;
   - paint order: labels hidden under a shape drawn later (4.1 s16 highlight, 4.2 s16 stacked cards, far atoms in 3D);
   - superscript and subscript inline boxes, which are 69 of 4.2's 95.
   (c) record the reference decks' current intersections as a known baseline, so the gate applies to new decks and to changes.
2. **Live stages with motion on.** Plan section 10 item 1 measures live stages "at their still end state (reduced motion) and at two
   moments with motion on". Brief 01 measures the reduced-motion end state only. Which step adds the two motion-on moments, and in
   which audit, layout or zoom? 4.1 s10 is such a stage.
3. **Dark theme** not run in this step (lean mode, light only); `layout.js dark` is ready for the last step. The geometry is the same in both themes.
4. **Two stale texts inherited from 52e1f8e**, left unchanged because they fall outside item 6:
   - the README's `keys_cfg` row says "the timer slide, 180 s timer on frame 1", but `keys.js` reads the `tm` slide's own frame-1 timer length;
   - `split_parts.py`'s docstring still uses `css-45` of 4.5 as its example.
5. **Pull request #1 merge.** `registry.json`, `suite.py`, `README.md`, `audits/lib.js`, `layout.js` and `xcheck.js` now differ from
   `workshop/unit4-5-6`. The 4.5 entry and parts come back with that merge, and the 4.5 deck has not been through the overlap check.
