> **Note:** the scripts in this kit still carry absolute paths from the build session (for example `/home/user/texaschemistry/unit4/` and scratchpad paths) and deck-specific script names (`build42.sh`, `run-all42.sh`, `gen_slides42.py`, `chem42-deck.js` and so on). The first workshop's kit check (see `workshop/KIT.md`) generalizes them.

# Unit 4 slide decks: source kit

The sources, build scripts and test suites for the two projector decks in the repo:
`unit4/slides-4-1.html` (Lesson 4.1, Predicting bond type) and `unit4/slides-4-2.html` (Lesson 4.2, Ionic formulas and names).
Each deck is one standalone HTML page assembled from the parts in `step1/src/`. Never hand-edit the decks: edit a part, then build.
`final/handoff.md` has the clicker map, how the decks run, the animation list and the known limitations.

## Layout (keep it: the scripts use paths relative to each other)
| Path | What |
|---|---|
| `step1/src/01-head.html` | shared head: all CSS |
| `step1/src/01c-css-42.css` | CSS for 4.2 only (inserted into the head by build42.sh) |
| `step1/src/02-runtime.html` | shared runtime: frames, clicker keys, zoom cycle, notes, run-sheet, canvas animation base |
| `step1/src/02b-shared.html` | shared chemistry data and drawing helpers |
| `step1/src/03-sims.html`, `04-slides.html` | 4.1 animations and slides (`04-slides.html` is written by `gen_slides.py`) |
| `step1/src/06-sims-42.html`, `08-slides-42.html` | 4.2 animations and slides (`08-slides-42.html` is written by `gen_slides42.py`) |
| `step1/src/05-scratch.html`, `07-scratch-42.html`, `gen_scratch42.py` | animation test benches (not in the decks) |
| `step1/build.sh`, `step1/build42.sh` | builds; they write the decks straight into `/home/user/texaschemistry/unit4/` |
| `step1/run-all.sh`, `step1/run-all42.sh` | full suites for 4.1 and 4.2 |
| `step1/lib.js` and the `*.js` audits | the audits the suites call (walk, back, fonts, keys, readability, print, render3d, extras, chem-deck / chem42-deck, timing, supgap, zoom, click, layout, contact, zoomsheet) |
| `step6/budget42.json` | 4.2 readability budget, read by run-all42.sh |
| `step7/xcheck.js` | blueprint cross-check (`unit4/blueprint.html` against both decks) |
| `step10/split_parts.py` | splits a built deck back into its parts |
| `step10/units67.js`, `step10/cyclecheck.js` | 4.2 slides 6 to 12: every card a zoom unit; the cycle complete right after Next |

If the repo is somewhere else, change the absolute paths: `/home/user/texaschemistry/unit4/` in `build.sh`, `build42.sh`,
`run-all42.sh` (DECK), `lib.js` (default DECK) and `step7/xcheck.js` (REPO).

## Build
```sh
cd step1
python3 src/gen_slides.py      # only after editing gen_slides.py (it rewrites src/04-slides.html)
./build.sh                     # 4.1 -> unit4/slides-4-1.html
./build42.sh                   # 4.2 -> unit4/slides-4-2.html (runs gen_slides42.py first)
```
The runtime and the shared data are in both decks: after changing `01-head.html`, `02-runtime.html` or `02b-shared.html`, build both.

Each part in a built deck sits between `<!-- part: NAME start -->` and `<!-- part: NAME end -->` lines (the part's text is
exactly what lies between them). In 4.2 the head is `01-head-42`: `01-head.html` with the title, description and og:title of
4.2, and `01c-css-42.css` inserted before `</style>` between `/* part: 01c-css-42 start */` and `/* part: 01c-css-42 end */`.
Recover the parts from a deck (for example when only the repo is at hand):
```sh
python3 step10/split_parts.py /home/user/texaschemistry/unit4/slides-4-1.html parts41/
python3 step10/split_parts.py /home/user/texaschemistry/unit4/slides-4-2.html parts42/
```

## Test
Needs Node with Playwright and Chromium (`require('playwright')`, `chromium.launch()`); decks open as `file://` pages.
```sh
cd step1
OUT=/some/dir ./run-all.sh       # 4.1 suite; exit 0 = every audit passed
OUT=/some/dir ./run-all42.sh     # 4.2 suite (OUT defaults to ../step6)
MATRIX=0 OUT=/some/dir ./run-all42.sh   # skip the zoom matrix pass (it adds about 12 min per theme)
DECK=/home/user/texaschemistry/unit4/slides-4-2.html OUT=/some/dir node zoom.js light   # one audit on its own
node ../step7/xcheck.js          # blueprint cross-check
node ../step10/units67.js /home/user/texaschemistry/unit4/slides-4-2.html
node ../step10/cyclecheck.js /home/user/texaschemistry/unit4/slides-4-2.html
```
Results (JSON, screenshots, contact sheets, zoom sheets) land in `$OUT`. Each audit prints one PASS/FAIL line.
`zoom.js` checks every zoomed unit on screen (centred, inside the slide above the footer, at least 60% fill, checks show their
options). Its main pass loads at 1366 x 768 and changes to 1920 x 1080 before zooming; its matrix pass (motion on) runs
1366 x 768, 1536 x 864, 1920 x 1080 and 1024 x 768 at device scale 1, 1.25 and 1.5, with a resize while zoomed, Next while
zoomed, a zoom during the zoom-out, after Back and after the slide list.
