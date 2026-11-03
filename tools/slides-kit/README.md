# Slides kit: parts, builds and audits for the projector decks

Every projector deck of the site (today `unit4/slides-4-1.html` and `unit4/slides-4-2.html`) is one standalone HTML page assembled
from the parts in `parts/` by `build.py`, and audited by `suite.py`. Never hand-edit a built deck: edit a part or a generator, then build.
`registry.json` lists every built deck and holds all of its deck-specific settings. `docs/handoff-4-1-4-2.md` has the clicker map,
how the decks run, the animation list and the known limitations.

No path in the kit is absolute. `build.py` and `suite.py` find the repo root two folders above themselves (`../..`); the audits get
every path from the environment that `suite.py` sets. If the repo moves, nothing in the kit changes. (`docs/handoff-4-1-4-2.md`
still quotes the old build session's absolute paths as history; its first line says so. The `/tmp/...` paths below are examples.)

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
| `parts/lessons/<U>-<L>/gen_scratch.py` | optional: writes `scratch.html` (4.2 has one; 4.1's `scratch.html` is hand-written) |
| `registry.json` | every built deck: file, head strings, periods, checks, markers, audit settings (fields below) |
| `build.py` | assembles decks (repo, `--out`, `--scratch`) |
| `suite.py` | runs a deck's audits and writes logs, JSON, screenshots and sheets outside the repo |
| `audits/` | `lib.js` (shared helpers) and the audits: walk, back, fonts, keys, readability, print, render3d, extras, timing, supgap, zoom, click, layout, contact, zoomsheet, xcheck, units, cycle |
| `split_parts.py` | splits a built deck back into its parts |
| `docs/handoff-4-1-4-2.md` | the 4.1 and 4.2 handoff (clicker map, animations, limitations) |

## Build
```sh
cd tools/slides-kit
python3 build.py 4 2                                   # 4.2 -> unit4/slides-4-2.html (runs parts/lessons/4-2/gen_slides.py first)
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
`css-<U><L>` if it has a `css.css`. Lesson 4.5: `01-head-45`, `02-runtime`, `02b-shared`, `sims-45`, `slides-45`, `css-45`.

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
xcheck, then the contact sheets and the zoom sheets. walk, back, zoom, contact and zoomsheet run once per theme; fonts once (light,
or dark with `--theme dark`). The suite prints one PASS or FAIL line per audit with its duration and verdict line, then a summary,
and exits 1 if any audit failed.

Results land in `<out>/<U>-<L>/`: `suite.json` (the summary), `logs/<audit>[-<theme>].log` (each audit's stdout and stderr), each
audit's JSON, the walk screenshots (`shots-<theme>/`), zoom screenshots, the run-sheet PDF, contact and zoom sheets. `<out>` is
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
| `XCHECK` | registry `matrix`, `blueprint`, `mentions`, `file`; `unit<U>/blueprint.html`; `<out>/walk-light.json` | xcheck |
| `EMPTY_MAX` | your environment if set; else `1` for walk and layout on a scratch deck; else the default (one third) | walk, layout |

Run one audit by hand with the same variables, for example
`DECK=$PWD/../../unit4/slides-4-2.html OUT=/tmp/o DECKNAME=slides-4-2.html node audits/walk.js light`.

## registry.json
One entry per deck in `decks`:
| Field | Meaning |
|---|---|
| `unit`, `lesson` | numbers; the lesson parts are in `parts/lessons/<unit>-<lesson>/` |
| `file` | the built deck, relative to the repo root (`unit4/slides-4-2.html`) |
| `title`, `description` | the head strings (`<title>` and `og:title`; `meta description` and `og:description`) |
| `periods` | slide ranges per period, `[[1, 13], [14, 26]]` |
| `checks` | the number of slides with a check ("Slide checks: N" in the blueprint) |
| `markers` | the five part markers in build order (head, runtime, shared, sims, slides) |
| `css` | the CSS marker name if the lesson has `css.css`, else `null` |
| `keys_cfg` | slide and element ids the keys audit drives: `cr` (a slide whose frames drive an animation), `sim` (that animation's id), `card` (a card the zoom cycle reaches on frame 3), `tm` (the timer slide, 180 s timer on frame 1), `ex` (a slide used for the blank-screen tests), `hk` (a slide with a frame 1 and no `.timer` slot), `notes` (slide id and frame for the notes screenshot) |
| `extras_cfg` | `hash` (a frame with the turning 3D model), `canvas` (its canvas selector), `block` (a block revealed on the next press), `slides` (the slide count) |
| `budget`, `chem` | paths relative to the kit |
| `zoom_checks` | optional: path of the lesson's `zoomchecks.js`, relative to the kit |
| `blueprint` | `section`: the deck's section id in `unit<U>/blueprint.html`; `next`: the id of the section after it |
| `matrix` | the lesson's objectives, as the blueprint's matrix rows name them |
| `mentions` | every "slide N" mention in the deck's notes and text: `"<slide id>:<N>"` → the title of the slide meant |
| `extra_audits`, `extra_slides` | additional audits (`units`, `cycle`) and the slide range they cover |

## Add a lesson
1. Folder `parts/lessons/<U>-<L>/` with `sims.html`, `gen_slides.py` (writing `slides.html` next to itself; copy the pattern of
   `parts/lessons/4-2/gen_slides.py`), `budget.json`, `chem.js` (requires `../../../audits/lib`, as the 4.1 and 4.2 ones do), and
   `css.css` only if the lesson needs CSS of its own; `zoomchecks.js` if the teacher asks for zoom checks of this deck. Lesson parts never redefine shared behavior; an engine feature goes into the
   shared runtime behind a per-lesson option, and every registered deck is then rebuilt and re-audited.
2. A registry entry with every field above; markers per the convention (`01-head-<U><L>`, `02-runtime`, `02b-shared`,
   `sims-<U><L>`, `slides-<U><L>`, `css-<U><L>`). For 4.5: `blueprint` `{"section": "45", "next": "case"}`, `matrix` `4.5.1` to `4.5.5`.
3. Animations first, on a bench: `scratch.html` (or `gen_scratch.py`) in the lesson folder, then
   `python3 build.py <U> <L> --scratch --out <scratchpad>/scratch.html` and `python3 suite.py <U> <L> --deck <that file> --only walk,...`.
4. The deck: `python3 build.py <U> <L>` writes `unit<U>/slides-<U>-<L>.html` (move an older deck at that path to `unit<U>/old-slides/`
   first); `python3 suite.py <U> <L>` audits it.

## Split a deck into its parts
```sh
python3 split_parts.py ../../unit4/slides-4-2.html /tmp/parts42/
```
It writes `<NAME>.html` for every part and `<CSS>.css` for a lesson CSS block inside the head. The split head is the filled head
(titles in place, lesson CSS inserted); `parts/shared/01-head.html` is the same text with `{{TITLE}}` and `{{DESCRIPTION}}` and
without the lesson CSS. If the kit is ever lost, the reference decks carry every marker needed to recover the parts this way.
