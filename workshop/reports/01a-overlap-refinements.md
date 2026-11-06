# Report 01a: Overlap measurement refinements, the motion-on pass, the reference-deck baselines, two stale texts

Step: 01a · Lesson: 5.1 · Commit: none by the implementer (working tree on `workshop/unit5-5-1` over 0935a5b, the orchestrator's work-in-progress snapshot of an earlier `layout.js`; diffs below are against 1ff2f97, the brief's base)

## Done
Diff summary per kit file (against 1ff2f97):
- `tools/slides-kit/audits/layout.js` (+169/−70): disc test, block-only DOM boxes, `Deck.spheres` scenes, covered labels, the motion-on pass, the baseline match; the older layout checks are unchanged.
- `tools/slides-kit/registry.json` (+2): `"overlap_baseline"` for 4.1 and 4.2.
- `tools/slides-kit/parts/lessons/4-1/overlap-baseline.json`, `4-2/overlap-baseline.json` (new): 60 and 30 entries.
- `tools/slides-kit/README.md` (+52/−18): the overlap section (discs, block boxes, scenes, covered labels, live stages, baselines), the `overlap_baseline` row, "no `overlap_baseline`" in "Add a lesson", and the `keys_cfg` row.
- `tools/slides-kit/split_parts.py` (+1/−1): docstring only.
- Not changed: `lib.js` (its `open({browser})` already makes the second context), `suite.py`, the other audits, the shared parts, the decks.

Per item:
1. **Discs.** `circle`, `electron` and `badge` record `disc = {cx, cy, r}` in host px, with half the stroke included as before. The radius is scaled by √|det| of the transform at the call. Their box is kept for the report. A label is inside when all four corners are within r − 2 px of the centre, and cuts the disc when the box's nearest point is within r − 2 px and it is not inside. `rrect` stays a rectangle. Shape kinds print as before. The reported `(w × h px)` for a disc is the overlap with its bounding square.
2. **Inline text is part of its block.** A DOM element takes part only when its computed display is `block`, `flex`, `grid`, `list-item`, `table-cell` or `table-row`, or `inline-block` (also `inline-flex` and `inline-grid`) and it matches the card, chip or footer lists. The chip list already contains `.badge` and `.opt`. Each visible text node is attributed to its nearest such ancestor, which then counts as a text box (`own` text). The `TEXT`-list rule, the kinds, containment and the ancestor rule are kept. The box is the border box. Text inside `.notes`, `script`, `style`, `svg`, `.zoomed` or a non-running `.timer` is skipped as before.
3. **`D.spheres` scenes.** The `window.Deck` setter also installs a setter for `spheres`, wrapped as `canvasSim` is. A call on an instrumented painter (the proxy exposes its record) numbers a scene, and every label and shape recorded during the call carries that number. Nothing within one scene is tested against the same scene, and everything is still tested against what lies outside it. Scenes and their boxes are listed in `overlap-<theme>.txt` and `layout-<theme>.json`, and the verdict line gives the count.
4. **Hidden labels.** Every record carries its paint order. A shape is opaque when its fill alpha and `globalAlpha` are both 0.9 or more. Fill alpha is a colour string read back through a scratch context; for a gradient it is the least opaque stop, recorded by a test-time wrapper of `CanvasGradient.prototype.addColorStop`. A label fully under (within 2 px) an opaque shape drawn after it is a covered label. It is not tested, is listed and is counted per frame (`rec[].overlap.covered`), in the summary and in the verdict line. Covered labels include s16's small "Na"/"Cl" under the enlarged cells in 4.1, and in 4.2 the "OH⁻" under the bus and three far "O" symbols at live moments.
5. **Motion-on pass.** The proxy sets `host.__live = !!(spec.live && spec.live(info.stage))` on each on-screen paint, and `overlap()` returns the visible live hosts. After the reduced pass, `L.open({browser, reduced: false, theme, init: instrument})` opens a second context. Each live frame then runs `Deck.go`, waits 1.4 s, runs the overlap check, waits 1.0 s and runs it again. The same assertions apply (hits and unrecorded paints), tagged `s<N>f<F>@live1` and `@live2`. The results are written to `overlap-<theme>.txt` (lines plus a "live frames" section), to `layout-<theme>.json` (`overlap.live`, `overlap.moments`, failing frames) and to the verdict line (`live: K frames at two moments`). Console errors of the second context are reported with a "(motion on)" prefix. A crop of a live moment would be taken in that context at the same delay. No live moment was cropped in this run, because the reduced frames filled the six slots first.
6. **Baselines.** `layout.js` finds the deck's registry entry by its `file` (resolved against the repo) and reads `overlap_baseline`, a path relative to the kit. The file is `{"deck", "theme", "note", "entries": [{"frame", "a", "b"}]}`. A hit whose tag, A and B strings equal an entry's is baselined: it is marked `[baselined]`, counted, and does not fail. Other hits fail. Unmatched entries are listed as "stale baseline entries" and do not fail. A named file that cannot be read fails the audit. The files were written by a one-off scratch script, `write_baselines.js` in the scratchpad, from the refined runs' JSON. The kit has no option that writes them.
7. **Stale texts.** README `keys_cfg`: "`tm` (the slide whose frame 1 starts a timer; the audit reads that timer's own length)". `split_parts.py`: "… or css-51 inside 01-head-51 of 5.1)".

## Verification
Refined runs, before the baselines: `suite.py 4 1|4 2 --only layout --theme light --out <scratchpad>/kit-out-01a`. Both FAIL as expected. The text is in `artifacts/01a/overlap-4-1-light-refined.txt` and `overlap-4-2-light-refined.txt`.

| Deck (light) | Step 01 | Refined, at rest (reduced) | Refined, live moments | Disc cut | Rrect cut | Label ∩ label | DOM | Covered labels | Spheres scenes |
|---|---|---|---|---|---|---|---|---|---|
| 4.1 (156 frames) | 175 on 22 frames | 75 on 15 frames | 84 on 17 of 28 moments | 44 rest + 84 live | 31 | 0 | 0 | 6 | 13 (5 rest + 8 live) |
| 4.2 (173 frames) | 95 on 38 frames | 10 on 10 frames | 20 on 20 of 20 moments | 10 rest + 20 live | 0 | 0 | 0 | 5 | 30 (10 rest + 20 live) |

What remains:
- **4.1 s10** (`#s10-sim`, live in every stage). At rest: the ball over "sodium" (f1), and electrons over the core labels "+", "2+" and "3+" (f2 to f9, 37 hits). With motion on, the same kinds of hit at both moments on f1 to f9. These are real overlaps (review F3).
- **4.1 s16** (`#s16-sim`, f3 to f5): the enlarged cell (rrect) cuts the neighbours' symbols Li, Be, Mg, K, Ca, O, F, Ne, Ar, Se, Br and Kr (31 hits). These are real. The small "Na", "Cl", "H" and "Cu" under the enlarged copies are now covered labels.
- **4.1 s17** (`#s17-sim`, f4 to f6): the digits "1" and "2" inside small stroke-only circles (r ≈ 21.5). The label box is the 36 px em box, so the corners pass r − 2 even though the glyphs sit inside the ring (crop `4-1-s17f4.jpg`). This is a measurement limit and is in the baseline (open question 2).
- **4.2 s15** (`#s15-sim`, f0 to f9, at rest and both live moments): the charge badge's own "+", "−", "2−" or "3−" against the dashed "one unit" ring. The badge is placed on the ring by design, and the ring is hidden under the opaque badge (crop `4-2-s15f0.jpg`). It is not a visible overlap, but no rule covers a hidden shape (open question 3).
- Gone, compared with step 01: every DOM hit (4.1: 3; 4.2: 75, the superscripts and the K₂S inline-block); the corner-of-the-box circle hits (4.1 s6 and s7f0, 4.2 s15 "one unit"); the within-scene hits of 4.1 s7 and 4.2 s15 (H ∩ N and others); 4.1 s16's hidden small symbols.

**Motion-on pass, 4.1 slide 10** (from `overlap-4-1-light-refined.txt`): 14 live frames, which are s7f2 to f5 (`#cr-sim` turn: 0 hits at both moments) and s10f0 to f9. For s10: f0 0/0, f1 1/0, f2 4/4, f3 1/7, f4 8/7, f5 10/12, f6 4/3, f7 5/6, f8 4/2, f9 2/4 (live1/live2). Example lines:
```
s10f2@live1: 4 intersections
  - canvas #s10-sim [sea]: label "+" ∩ electron (14 × 20 px)  A [168, 261, 194, 305]  B [151, 250, 182, 281]
s10f3@live2: 7 intersections
```
The electrons move on the page clock (`I.clock`), so the counts differ from run to run. Across five 4.1 runs, the totals were 158 or 159 hits with 59 or 60 distinct (frame, A, B) keys. The only key that came and went was `s10f1@live2 … "sodium" ∩ circle`.

**Baselines.**
- 4.1: 60 entries (disc 33, rrect 27) on 33 frames: s10f1 to f9 with @live1 and @live2 (27), s16f3 to f5, s17f4 to f6. It is the union of five refined runs.
- 4.2: 30 entries (disc 30) on 30 frames: s15f0 to f9 with @live1 and @live2. It is the union of two runs, which gave identical keys.

**Final proof** (`<scratchpad>/kit-out-01a-final`; logs in `artifacts/01a/logs/`):
```
== 4.1
  PASS  layout light  57.7 s  ... overlap: 158 intersections on 32 frames, 158 baselined (parts/lessons/4-1/overlap-baseline.json, 60 entries, 1 stale), 0 not in the baseline (6215 boxes (2633 DOM boxes, 1690 canvas labels, 1892 canvas shapes), 6 covered canvas labels, 13 spheres scenes (live moments included), 10 of 10 canvas animations instrumented), live: 14 frames at two moments, PASS
  PASS  xcheck         1.7 s  xcheck: 42 of 42 pass
== 4.2
  PASS  layout light  50.2 s  ... overlap: 30 intersections on 30 frames, 30 baselined (parts/lessons/4-2/overlap-baseline.json, 30 entries, 0 stale), 0 not in the baseline (6763 boxes (2516 DOM boxes, 2278 canvas labels, 1969 canvas shapes), 5 covered canvas labels, 30 spheres scenes (live moments included), 14 of 14 canvas animations instrumented), live: 10 frames at two moments, PASS
  PASS  xcheck         1.7 s  xcheck: 40 of 40 pass
```
The 4.1 stale entry is `s10f1@live2: canvas #s10-sim [cores]: label "sodium" ∩ circle` (the moving ball missed the label at that moment). The other older checks are unchanged: max empty 29% (4.1 s4f0) and 32% (4.2 s10f1), 0 clipped, no option wraps.

The gate stays absolute without a baseline. The refined runs above had no baseline and failed on every hit. A `--deck` run, or a new deck without the field, gets none.

Artifacts: `artifacts/01a/overlap-4-1-light-refined.txt`, `overlap-4-2-light-refined.txt`; `overlap/4-1-s10f1.jpg`, `4-1-s10f2.jpg`, `4-1-s10f3.jpg`, `4-1-s10f4.jpg`, `4-1-s16f3.jpg`, `4-1-s17f4.jpg`, `4-2-s15f0.jpg` to `4-2-s15f5.jpg` (4 to 52 KB each); `logs/4-1/`, `logs/4-2/` (walk, layout and xcheck logs, `overlap-light-final.txt`), `logs/suite-final-walk.txt`, `logs/suite-final-layout-xcheck.txt`.

## Repo state
- `python3 build.py --all` gives 4.1 `ebd342f1ee0e11c47157141cf3b2a59b` (194,646 bytes) and 4.2 `c3fa219a806963f9a66c3baf643153f4` (203,769 bytes), both unchanged.
- `git status --short` before this report and the artifacts:
```
 M tools/slides-kit/README.md
 M tools/slides-kit/audits/layout.js
 M tools/slides-kit/registry.json
 M tools/slides-kit/split_parts.py
?? tools/slides-kit/parts/lessons/4-1/overlap-baseline.json
?? tools/slides-kit/parts/lessons/4-2/overlap-baseline.json
```
- Plus `workshop/artifacts/01a/` and `workshop/reports/01a-overlap-refinements.md`. Nothing under `unit4/` or `unit5/`.

## Deviations
1. **A badge's own label is not tested against its own disc.** Under item 1 as written, the label that the same `badge` call draws inside a small badge (4.2 s6 and s7, r ≈ 27.5) failed by under 1 px, because its box is the font's em box (36 px tall). That made 89 hits that step 01's rectangle containment never flagged, and every small badge in 5.1 would have failed too. The badge label records the index of its badge shape and skips only that pair. It is still tested against every other shape and label. To reverse it, remove the `own` check in `overlap()`.
2. **One baseline entry matches every hit with the same strings** (set, not count). On a live stage, the moving electrons all print as `electron` and the same "+" string repeats across cores, so hit counts vary from run to run while the strings stay the same. One-to-one matching would make the gate flaky.
3. **The baseline is the union of several refined runs** (five for 4.1, two for 4.2), not a single run. The live moments move, and a single run missed `s10f1@live2 … "sodium" ∩ circle`.
4. **The baseline file is an object with `deck`, `theme`, `note` and `entries`.** Each entry is exactly `{"frame", "a", "b"}`. The audit also accepts a bare array.
5. **`inline-flex` and `inline-grid` are treated like `inline-block`** in item 2: a box only when they are a card, chip or footer span. The `.timer` is `inline-grid`, and its grid items are blockified, so they are still measured.
6. **Gradient fills count as opaque from their stops,** recorded by a test-time wrapper of `CanvasGradient.prototype.addColorStop` in the instrumentation. Patterns count as not opaque. The runtime is not touched.
7. **The final proof ran `walk` first** (`suite.py --all --theme light --only walk` into the same `--out`). `xcheck` reads `walk-light.json` from that folder, so `--only layout,xcheck` alone fails xcheck with ENOENT. The brief's command was then run unchanged.
8. The verdict line's covered-label and scene counts include the live moments (said in the line).

## Open questions
1. 4.1 s10 (ball over "sodium", electrons over "+", "2+" and "3+") and s16 (the enlarged cell cutting its neighbours) are real overlaps, now in the 4.1 baseline. Fixing them is the teacher's decision (review F5).
2. 4.1 s17's digits in small rings are flagged only because a label box is the em box. Should the label height come from the glyphs (`measureText` `actualBoundingBoxAscent` and `Descent`)? This would change a definition the brief keeps, so I left it.
3. 4.2 s15's charge badge sits on the dashed "one unit" ring, which is hidden under the opaque badge. Should a shape segment hidden under a later opaque shape count, as item 4 does for labels? It is in the baseline for now.
4. Live-moment hits depend on the page clock. A new deck with a live stage (5.1's turning models and the ticking counter) is measured at two arbitrary moments, so an overlap that appears only part of the time may pass one run and fail the next. Should the pass sample more moments, or use a fixed clock?
