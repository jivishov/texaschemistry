# Slides kit: parts, builds and audits for the projector decks

Every projector deck of the site (today `unit4/slides-4-1.html`, `unit4/slides-4-2.html` and `unit5/slides-5-1.html`) is one standalone HTML page assembled
from the parts in `parts/` by `build.py`, and audited by `suite.py`. Never hand-edit a built deck: edit a part or a generator, then build.
`registry.json` lists every built deck and holds all of its deck-specific settings. `docs/handoff-4-1-4-2.md` has the clicker map,
how the decks run, the animation list and the known limitations; `docs/handoff-5-1.md` has the same for 5.1.

No path in the kit is absolute. `build.py` and `suite.py` find the repo root two folders above themselves (`../..`); the audits get
every path from the environment that `suite.py` sets. If the repo moves, nothing in the kit changes. No absolute path remains:
`grep -rnE -- '/(home|tmp)/' tools/slides-kit` finds only `docs/handoff-4-1-4-2.md`, which quotes the old build session's paths as
history (its first line says so). The examples below write `<scratchpad>` for a folder outside the repo.

## Layout
| Path | What |
|---|---|
| `parts/shared/01-head.html` | the head of every deck: all shared CSS, with `{{TITLE}}` and `{{DESCRIPTION}}` placeholders (each used twice: page and `og:` tags) |
| `parts/shared/02-runtime.html` | the runtime: frames, clicker keys, zoom cycle, notes, run-sheet, canvas animation base |
| `parts/shared/02b-shared.html` | chemistry data and drawing helpers used by more than one lesson |
| `parts/lessons/<U>-<L>/css.css` | lesson-only CSS (optional; inserted into the head) |
| `parts/lessons/<U>-<L>/sims.html` | the lesson's animations |
| `parts/lessons/<U>-<L>/gen_slides.py` | writes `slides.html` (the lesson's slides) from Python data; `build.py` runs it |
| `parts/lessons/<U>-<L>/slides.html` | generated, committed (so a deck can be rebuilt and diffed without running Python) |
| `parts/lessons/<U>-<L>/budget.json` | per-slide minutes, read by the timing audit |
| `parts/lessons/<U>-<L>/chem.js` | the lesson's chemistry audit (`meta()` of each placed animation, checked against the reading's data) |
| `parts/lessons/<U>-<L>/zoomchecks.js` | optional: the teacher's explicit zoom checks for this deck (`module.exports=(rec,{has,cnt})=>[[name, ok], …]`), run by the zoom audit after its two generic checks |
| `parts/lessons/<U>-<L>/scratch.html` | animation test bench: scratch slides of every stage (never in a repo deck) |
| `parts/lessons/<U>-<L>/gen_scratch.py` | optional: writes `scratch.html` (4.2 and 5.1 have one; 4.1's `scratch.html` is hand-written) |
| `registry.json` | every built deck: file, head strings, periods, checks, markers, audit settings (fields below) |
| `build.py` | assembles decks (repo, `--out`, `--scratch`) |
| `suite.py` | runs a deck's audits and writes logs, JSON, screenshots and sheets outside the repo |
| `audits/` | `lib.js` (shared helpers) and the audits: walk, back, fonts, keys, readability, print, render3d, extras, timing, supgap, zoom, click, layout (with the overlap check), contact, zoomsheet, xcheck (Unit 4 and Unit 5 blueprint forms), units, cycle |
| `split_parts.py` | splits a built deck back into its parts |
| `docs/handoff-4-1-4-2.md` | the 4.1 and 4.2 handoff (clicker map, animations, limitations) |
| `docs/handoff-5-1.md` | the 5.1 handoff (clicker map, animations and stages, the Unit 5 color code, limitations, blueprint form) |

## Build
```sh
cd tools/slides-kit
python3 build.py 4 2                                   # 4.2 -> unit4/slides-4-2.html (runs parts/lessons/4-2/gen_slides.py first)
python3 build.py 5 1                                   # 5.1 -> unit5/slides-5-1.html
python3 build.py --all                                 # every registered deck
python3 build.py 4 2 --out /path/outside/deck42.html   # the same deck, written elsewhere
python3 build.py 4 2 --scratch --out /path/outside/scratch42.html   # the 4.2 animation bench (runs gen_scratch.py first)
```
Each build prints the path, size, line count and md5. A deck is five parts, each between `<!-- part: NAME start -->` and
`<!-- part: NAME end -->` lines (the part's text is exactly what lies between them), NAME taken from the registry's `markers` in this order:
1. head: `parts/shared/01-head.html` with `{{TITLE}}` and `{{DESCRIPTION}}` filled from the registry's `title` and `description`;
   if the lesson has `css.css`, it is inserted right before `</style>` between `/* part: CSS start */` and `/* part: CSS end */`
   lines, CSS being the registry's `css`;
2. runtime: `parts/shared/02-runtime.html`;
3. shared: `parts/shared/02b-shared.html`;
4. sims: `parts/lessons/<U>-<L>/sims.html`;
5. slides: `parts/lessons/<U>-<L>/slides.html` (in a scratch build `scratch.html`, marker `scratch-<U><L>`).

A change to a shared part (`parts/shared/*`) changes every deck: rebuild them all (`build.py --all`), re-run every deck's suite with
the matrix off, and list every deck's md5 before and after. A deck whose lesson parts did not change and whose shared parts did not
change comes out byte-identical.

### Marker convention
4.1 and 4.2 keep the names their decks were built with, so they rebuild byte-identical:
4.1 `01-head`, `02-runtime`, `02b-shared`, `03-sims`, `04-slides` (no lesson CSS);
4.2 `01-head-42` (CSS marker `01c-css-42`), `02-runtime`, `02b-shared`, `06-sims-42`, `08-slides-42`.
Every new lesson uses `01-head-<U><L>`, `02-runtime`, `02b-shared`, `sims-<U><L>`, `slides-<U><L>`, and the CSS marker
`css-<U><L>` if it has a `css.css`. Lesson 5.1 (built, `unit5/slides-5-1.html`): `01-head-51`, `02-runtime`, `02b-shared`, `sims-51`,
`slides-51`, and the CSS marker `css-51` (it has a `css.css`).

## Test
Needs Node with Playwright and Chromium (`require('playwright')`, `chromium.launch()`; in a Claude cloud session both are installed:
never run `playwright install`). Decks open as `file://` pages.
```sh
python3 suite.py 4 2                          # every audit of 4.2, both themes, matrix off
python3 suite.py --all --theme both           # every registered deck
python3 suite.py 4 2 --matrix                 # with the zoom viewport matrix (about 12 min per theme; once per workshop)
python3 suite.py 4 2 --only walk,zoom --theme light
python3 suite.py 4 2 --deck /path/outside/scratch42.html --only walk --theme light   # a deck built with --out or --scratch
```
Order: walk, back, fonts, keys, readability, print, render3d, extras, chem, timing, supgap, zoom, click, layout, the deck's extra audits,
xcheck, then the contact sheets and the zoom sheets. walk, back, zoom, layout, contact and zoomsheet run once per theme; fonts once
(light, or dark with `--theme dark`). The suite prints one PASS or FAIL line per audit with its duration and verdict line, then a summary,
and exits 1 if any audit failed.

Results land in `<out>/<U>-<L>/`: `suite.json` (the summary), `logs/<audit>[-<theme>].log` (each audit's stdout and stderr), each
audit's JSON, the walk screenshots (`shots-<theme>/`), zoom screenshots, the run-sheet PDF, contact and zoom sheets, and from layout
`layout-<theme>.json`, `overlap-<theme>.txt` and the overlap crops (`overlap-<theme>/`). `<out>` is
`--out`, else `$SLIDES_KIT_OUT`, else `<system temp folder>/slides-kit-out`; the suite refuses a folder inside the repo. Copy the
logs and the sheets a step needs into `workshop/artifacts/NN/` (text logs; JPEG sheets at most 800 KB each; no per-press folders).

- `--deck <path>` audits a deck outside the repo with the lesson's settings; xcheck is skipped (it cross-checks the repo deck and its
  blueprint). A scratch build (it carries a `scratch-<U><L>` part) runs without the lesson's `zoomchecks.js` (the two generic zoom
  checks still run), and its walk and layout run with `EMPTY_MAX=1`: scratch slides hold one animation and a label, so the
  emptiness gate (at most one third of the body empty) is off for them (review 01). The suite prints that it did; an
  `EMPTY_MAX` already set in the environment wins. Every other gate stays, and a repo deck always runs with the default gate.
- `xcheck` reads `walk-light.json` from the same output folder: run walk in light theme first (the full suite does).
- The chemistry audit, the budget and the keys and extras settings refer to the lesson's real slides; on a scratch deck pick audits
  with `--only`.

### What the audits get from `suite.py`
| Variable | From | Used by |
|---|---|---|
| `DECK`, `OUT`, `DECKNAME` | the registry `file` (or `--deck`), the output folder, the deck's file name | every audit (`lib.js`), contact, zoomsheet |
| `ZOOM_CHECKS` | registry `zoom_checks` (absent for a scratch deck) | zoom (the lesson's explicit checks, after the two generic ones: every zoomed check shows its options; every prompt on a routine slide is a unit) |
| `BUDGET` | registry `budget` | timing |
| `KEYS_CFG`, `EXTRAS_CFG` | registry `keys_cfg`, `extras_cfg` | keys, extras |
| `MATRIX` | `0`, or `1` with `--matrix` (or `MATRIX=1`) | zoom |
| `SLIDES` | registry `extra_slides` (`first,last`) | units, cycle |
| `XCHECK` | registry `matrix`, `blueprint` (`section`, `next`, `form`, `teks_rows`), `mentions`, `file`, `checks`, `periods`; `unit<U>/blueprint.html`; `<out>/walk-light.json` | xcheck |
| `EMPTY_MAX` | your environment if set; else `1` for walk and layout on a scratch deck; else the default (one third) | walk, layout |

Run one audit by hand with the same variables, for example
`DECK=$PWD/../../unit4/slides-4-2.html OUT=<scratchpad>/o DECKNAME=slides-4-2.html node audits/layout.js light`.

### The overlap check (layout audit)
RULES.md sections 3 and 11: nothing visible may overlap on any frame, in either theme. `node audits/layout.js [light|dark]` (default
light; `suite.py` runs it once per theme the run asks for) opens the deck with reduced motion, so every animation stage jumps to its
end state, goes to every frame of every slide, runs the older layout checks after 100 ms (options, emptiness, clipped text, canvas
text at the edge), then waits until the frame has settled (the boxes of the `.acc` cards, the options and the footer are the same two
animation frames apart, so compaction is done) and measures (for live stages, also with motion on; below):
- **DOM boxes**, in 1600 x 900 canvas px, on the current slide and in the footer: text lines (every visible element with its own
  visible text, and `p`, `li`, `td`, `th`, `h2`, `.line`, `.cell`, `.rh`, `.q`, `.ans`, `.fb`, `.tag`, `.term`, `.mean`, `.k`, `.small`,
  `.cap`, `.nm`, `.fm`, `.bt`, `.why`, `.big`, `.hdr` with visible text inside), cards (`.card`, `.phase`, `.wcard`, `.item`, `.key`,
  `.colh`, `.cer-box`), chips and badges (`.chip`, `.badge`, `.es`, `.rail li`, `.legend>span`, `.scale span`, `.opt`) and the footer
  spans `#sec`, `#cue`, `#count`. Only block-level boxes take part: computed display `block`, `flex`, `grid`, `list-item`,
  `table-cell` or `table-row`, and an `inline-block` (or `inline-flex`, `inline-grid`) that is a card, chip, badge, option or footer
  span by the lists above. Inline text (`sup`, `sub`, `b`, `span`, `i`, `.es`, `.nw`, `.gap`, inline formulas) and any other
  inline-block are part of their nearest block ancestor, not boxes of their own: a superscript poking into the line above, or a
  formula taller than its line, is the block's own text, not an overlap. A box is the block's border box. Skipped: hidden, `display: none`, zero-size and opacity-0
  elements (opacity multiplied up the ancestors), anything inside `.notes`, `script`, `style`, `svg`, a `.timer` that is not running,
  or a `.zoomed` clone.
- Two DOM boxes **intersect** when their rectangles overlap by more than 2 px in both directions and neither contains the other
  (within 2 px). Containment (a text line inside its card, a chip inside its row) and ancestor pairs are not intersections.
- **Canvas labels**, by test-time instrumentation (the runtime is not changed): `page.addInitScript` defines a setter for
  `window.Deck`; when the runtime assigns the Deck object, the setter installs a setter for its `canvasSim`, and the wrapped
  `canvasSim(host, spec)` replaces `spec.draw` so the animation paints through a proxy of the painter `g`. Each `text`, `chem`, `badge`
  (and `fit`) call records a label box, in paint order: x from the call's x and align, width from `ctx.measureText` with the font the painter set
  (`chem`: the width it returns), y from y and the baseline (centred for `middle`), height the font size. Each `circle`,
  `electron` (the dot, not its faint halo) and `badge` call records a **disc** (centre and radius, half the stroke included);
  each `rrect` a rectangle. A shape is **opaque** when its fill alpha (a gradient: its least opaque stop) and `globalAlpha` at the
  call are both 0.9 or more. Calls drawn at `globalAlpha` 0.01 or less are invisible and skipped. The boxes of the last on-screen
  paint are kept on the host (`host.__boxes = {labels, shapes, stage, scenes}`, cleared at the start of each paint; the off-screen
  renders of `bounds()` are not recorded), with `host.__live` (the spec's `live(stage)`). The same setter wraps `Deck.spheres`:
  each call on an instrumented painter is one **scene**, and every label and sphere it draws carries the scene's number.
- Per visible animation and frame: no two labels intersect by more than 2 px in both directions (one label drawn twice at the same
  place counts once), and no label cuts a shape. Against a disc, a label is **inside** when all four corners of its box lie within
  r − 2 px of the centre (that shape's label) and **cuts** it when the box's nearest point to the centre lies within r − 2 px and it
  is not inside; a label in the empty corner of a circle's bounding square touches nothing. A badge's own label (the same `badge`
  call) is not tested against that badge. Against an `rrect`, a label fully inside (within 2 px) is its label; one crossing the edge
  by more than 2 px cuts it.
- **Scenes**: inside one `D.spheres` scene no label-against-label and no label-against-shape test runs (the renderer draws far to
  near, so a nearer sphere over part of a farther symbol is depth, not overlap); a scene's labels and spheres are still tested
  against everything outside it. The scenes and their boxes are listed.
- **Covered labels**: a label whose box lies fully (within 2 px) under an opaque shape drawn later in the same paint (inside the
  disc's r + 2 px, or inside the rectangle) is hidden: it is counted as a covered label and not tested. A label only partly under
  such a shape is tested as above.
- **Live stages with motion on**: after the reduced-motion pass, every frame on which a visible animation reported a live stage is
  measured again in a second browser context with motion on (same theme, same instrumentation): `Deck.go`, 1.4 s, the overlap
  check, a further 1.0 s, the check again. Its lines carry the frame tags `s<N>f<F>@live1` and `@live2`; the verdict line says
  `live: K frames at two moments`.
- The gate: any intersection fails the audit, unless the deck's baseline lists it (below). The audit also fails if a canvas
  animation of the deck was not wrapped or a visible one has no recorded paint (the instrumentation did not take), or if the
  registry names a baseline file that cannot be read.
- **Baselines** (review 01, F3): the two reference decks, 4.1 and 4.2, were built before the no-overlap rule and still carry
  intersections the teacher has not yet decided to fix. Their registry entries name an `overlap_baseline` file
  (`parts/lessons/4-1/overlap-baseline.json`, `parts/lessons/4-2/overlap-baseline.json`): `{"deck", "theme", "note", "entries":
  [{"frame": "s10f1", "a": "<A as printed>", "b": "<B as printed>"}]}`, strings and not coordinates, so small drifts do not
  matter (the `@live1`/`@live2` tags are part of the frame). A hit whose frame, A and B equal an entry's is **baselined** (marked
  `[baselined]`, counted in the verdict line, not a failure); an entry can match more than one hit with the same strings (the moving
  electrons of a live stage all print as `electron`). A hit with no entry fails as before; entries no hit matches are printed as
  stale baseline entries (not a failure). The baseline is matched to the deck by its registry `file`, so `--deck` runs have none.
  The files are records the orchestrator and the teacher review, written once by hand from a refined run (the union of several
  runs, since live moments move); the kit has no option that writes them. Only those two decks have one: **a new deck gets no
  baseline, and any intersection fails its gate.**

Each intersection is a line `s<N>f<F>: <box A> ∩ <box B> (<w> × <h> px)` with ids or classes and the start of the text (canvas: the
animation id, the stage, the label text and the shape kind; for a disc the numbers are the overlap with its bounding square).
`overlap-<theme>.txt` lists every frame with intersections (baselined ones marked) with both boxes as `[x0, y0, x1, y1]` in canvas
px, or says `no intersections, N frames, M boxes`; then the stale baseline entries, the live frames, the covered labels and the
spheres scenes. `overlap-<theme>/s<N>f<F>.jpg` (a live moment: `s<N>f<F>-live1.jpg`, taken in the motion-on context at the same
delay, so moving shapes may sit a little off their outlines) crops up to six frames with failing intersections (one per slide
first) with box A outlined red and box B blue. The helpers `instrument`, `settle` and `overlap` are
exported (`require('./layout')`) for tools that need the same boxes.

### The blueprint cross-check (xcheck) and its forms
The registry's `blueprint.form` names how `unit<U>/blueprint.html` prints a deck's numbers.
- `"unit4"` (or absent): the sentence "Slide checks: N, … The deck has N slides: period 1 uses slides 1 to A, period 2 slides B to C."
  in the lesson's section, and the objective rows `<tr><td>4.1.1</td><td>…</td><td>SLIDES</td>`.
- `"unit5"`: inside the lesson's section (`section` to `next`) the deck line of "Slides and missions", "Deck: N slides. Checkpoints A
  to B, predictions revisited C, CER exit ticket D, self-rating E." (N is the slide count; A to B the checkpoint routine slide and
  the three checkpoint slides, titles starting with "Checkpoint"; C and D the slide "Predictions and exit ticket"; E "Rate your
  learning"); the objectives table rows `<tr><td>5.1.k</td><td>…</td><td>…</td><td>SLIDES</td></tr>` (each slide exists and its footer
  reference names the objective); and in section `matrix`, for each TEKS code of `teks_rows`, the one row whose first cell carries
  the code and names "Deck 5.1, slides …" (its objectives cell names the code's objectives; each listed slide carries one of them;
  the listed slides equal the union of the objectives' slides). The check count and the period split are asserted against the
  registry's `checks` and `periods` and the deck, since a Unit 5 blueprint does not print them.
- Both forms: the rate slide's review lines, every "slide N" mention (`mentions`) and the footer cues "slide N: title" of the walk.

A dry run reads a Unit 5 blueprint without a deck and prints the numbers it parsed (exit 1 if something is not found):
```sh
cd tools/slides-kit
XCHECK='[{"lesson": "5.1", "blueprint": "../../unit5/blueprint.html", "section": "l51", "next": "l52", "form": "unit5",
  "teks_rows": {"C.8(A)": ["5.1.1", "5.1.2"], "C.8(B)": ["5.1.3", "5.1.4"]}, "objectives": ["5.1.1", "5.1.2", "5.1.3", "5.1.4"]}]' \
  node audits/xcheck.js --dry          # or XCHECK_DRY=1
```

## registry.json
One entry per deck in `decks`:
| Field | Meaning |
|---|---|
| `unit`, `lesson` | numbers; the lesson parts are in `parts/lessons/<unit>-<lesson>/` |
| `built` | optional; `false` while the lesson's deck step has not run: `build.py --all` and `suite.py --all` skip the entry with one line, and `build.py <U> <L>` without `--out` refuses (`--out` and `--scratch --out` still work). The deck step sets it to `true`. Absent means built. |
| `file` | the built deck, relative to the repo root (`unit4/slides-4-2.html`) |
| `title`, `description` | the head strings (`<title>` and `og:title`; `meta description` and `og:description`) |
| `periods` | slide ranges per period, `[[1, 13], [14, 26]]` (the Unit 5 form of xcheck asserts them against the deck) |
| `checks` | the number of slides with a check ("Slide checks: N" in a Unit 4 blueprint; the Unit 5 form asserts it against the deck) |
| `markers` | the five part markers in build order (head, runtime, shared, sims, slides) |
| `css` | the CSS marker name if the lesson has `css.css`, else `null` |
| `keys_cfg` | slide and element ids the keys audit drives: `cr` (a slide whose frames drive an animation), `sim` (that animation's id), `card` (a card the zoom cycle reaches on frame 3), `tm` (the slide whose frame 1 starts a timer; the audit reads that timer's own length), `ex` (a slide used for the blank-screen tests), `hk` (a slide with a frame 1 and no `.timer` slot), `notes` (slide id and frame for the notes screenshot) |
| `extras_cfg` | `hash` (a frame with the turning 3D model), `canvas` (its canvas selector), `block` (a block revealed on the next press), `slides` (the slide count) |
| `budget`, `chem` | paths relative to the kit |
| `zoom_checks` | optional: path of the lesson's `zoomchecks.js`, relative to the kit |
| `blueprint` | `section`: the deck's section id in `unit<U>/blueprint.html`; `next`: the id of the section after it; `form`: `"unit4"` (absent means `"unit4"`) or `"unit5"` (xcheck's forms, above); `teks_rows` (form `"unit5"`): each TEKS code of the matrix section → the lesson's objectives in that row, `{"C.8(A)": ["5.1.1", "5.1.2"], "C.8(B)": ["5.1.3", "5.1.4"]}` |
| `matrix` | the lesson's objectives, as the blueprint's objective rows name them |
| `mentions` | every "slide N" mention in the deck's notes and text: `"<slide id>:<N>"` → the title of the slide meant |
| `extra_audits`, `extra_slides` | additional audits (`units`, `cycle`) and the slide range they cover |
| `overlap_baseline` | optional, relative to the kit: the file of accepted intersections of a reference deck built before the no-overlap rule (4.1 and 4.2 only; the layout audit, "Baselines" above). A new deck has none. |

## Add a lesson
1. Folder `parts/lessons/<U>-<L>/` with `sims.html`, `gen_slides.py` (writing `slides.html` next to itself; copy the pattern of
   `parts/lessons/4-2/gen_slides.py`), `budget.json`, `chem.js` (requires `../../../audits/lib`, as the 4.1 and 4.2 ones do), and
   `css.css` only if the lesson needs CSS of its own; `zoomchecks.js` if the teacher asks for zoom checks of this deck. Lesson parts never redefine shared behavior; an engine feature goes into the
   shared runtime behind a per-lesson option, and every registered deck is then rebuilt and re-audited.
2. A registry entry with every field above (no `overlap_baseline`); markers per the convention (`01-head-<U><L>`, `02-runtime`, `02b-shared`,
   `sims-<U><L>`, `slides-<U><L>`, `css-<U><L>`). For 5.1: `file` `unit5/slides-5-1.html`, `blueprint` `{"section": "l51", "next": "l52",
   "form": "unit5", "teks_rows": {"C.8(A)": ["5.1.1", "5.1.2"], "C.8(B)": ["5.1.3", "5.1.4"]}}`, `matrix` `5.1.1` to `5.1.4`; it carried `"built": false`
   until its deck step wrote `unit5/slides-5-1.html` and is now `"built": true` (a new lesson starts the same way).
3. Animations first, on a bench: `scratch.html` (or `gen_scratch.py`) in the lesson folder, then
   `python3 build.py <U> <L> --scratch --out <scratchpad>/scratch.html` and `python3 suite.py <U> <L> --deck <that file> --only walk,...`.
4. The deck: `python3 build.py <U> <L>` writes `unit<U>/slides-<U>-<L>.html` (for 5.1, `python3 build.py 5 1` writes
   `unit5/slides-5-1.html`; move an older deck at that path to `unit<U>/old-slides/` first, as 5.1's rejected deck was); `python3 suite.py <U> <L>` audits it, and the
   layout audit's overlap check must pass.

## Split a deck into its parts
```sh
python3 split_parts.py ../../unit4/slides-4-2.html <scratchpad>/parts42/
```
It writes `<NAME>.html` for every part and `<CSS>.css` for a lesson CSS block inside the head. The split head is the filled head
(titles in place, lesson CSS inserted); `parts/shared/01-head.html` is the same text with `{{TITLE}}` and `{{DESCRIPTION}}` and
without the lesson CSS. If the kit is ever lost, the reference decks carry every marker needed to recover the parts this way.
