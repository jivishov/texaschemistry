# Report 01: Kit check and generalization

Step: 01 · Lesson: 4.5 (kit step; no deck built) · Commit: the commit `[implementer] 01: kit generalized, decks byte-identical` on `workshop/unit4-5-6`, parent `b8823d9` (its hash is in the pull-request comment `report 01 ready`; a file cannot carry the hash of the commit it is in)

## Done
`tools/slides-kit/` moved from the deck-specific `step1/`, `step6/`, `step7/`, `step10/`, `final/` layout into the layout of `workshop/KIT.md`, by `git mv`. Both reference decks rebuild byte-identical from it; every audit passes on both decks in both themes with the matrix off. No file outside `tools/slides-kit/` and `workshop/` changed.

### New layout
```
tools/slides-kit/
  README.md                      rewritten (layout, build, test, registry fields, add a lesson, split, marker convention, no absolute paths)
  registry.json                  new: one entry per deck (full text below)
  build.py                       new: replaces step1/build.sh and step1/build42.sh
  suite.py                       new: replaces step1/run-all.sh and step1/run-all42.sh
  split_parts.py                 from step10/split_parts.py (any deck, any CSS marker)
  docs/handoff-4-1-4-2.md        from final/handoff.md, one line added at the top
  parts/shared/01-head.html      from step1/src/01-head.html, the 4.1 strings replaced by {{TITLE}} and {{DESCRIPTION}}
  parts/shared/02-runtime.html   from step1/src/02-runtime.html (unchanged)
  parts/shared/02b-shared.html   from step1/src/02b-shared.html (unchanged)
  parts/lessons/4-1/             sims.html (03-sims.html), gen_slides.py (gen_slides.py), slides.html (04-slides.html),
                                 budget.json (new: the default BUDGET object of timing.js), chem.js (chem-deck.js), scratch.html (05-scratch.html)
  parts/lessons/4-2/             css.css (01c-css-42.css), sims.html (06-sims-42.html), gen_slides.py (gen_slides42.py), slides.html (08-slides-42.html),
                                 budget.json (step6/budget42.json), chem.js (chem42-deck.js), scratch.html (07-scratch-42.html), gen_scratch.py (gen_scratch42.py)
  audits/                        lib, walk, back, fonts, keys, readability, print, render3d, extras, timing, supgap, zoom, click, layout,
                                 contact, zoomsheet (all from step1/), xcheck (step7/), units (step10/units67.js), cycle (step10/cyclecheck.js)
```
Removed: `step1/build.sh`, `build42.sh`, `run-all.sh`, `run-all42.sh` and the empty folders `step1/`, `step6/`, `step7/`, `step10/`, `final/`. No copies left behind, no new audits, one way to build.

### Head placeholders
`parts/shared/01-head.html`: "Predicting Bond Type Slides" → `{{TITLE}}` (in `<title>` and `og:title`), "Unit 4, Lesson 4.1 projector slides: Predicting bond type (TEKS C.7(A))." → `{{DESCRIPTION}}` (in `meta name="description"` and `og:description`). `build.py` fills them from the registry (each must appear exactly twice) and inserts the lesson's `css.css` before `</style>` between `/* part: <css> start */` and `/* part: <css> end */` exactly as `build42.sh` did (4.1: no insertion; 4.2: `css.css`, marker `01c-css-42`).

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
`keys_cfg` for 4.1 is the old default of `keys.js`, for 4.2 the `KEYS_CFG` of `run-all42.sh`; `extras_cfg` likewise; `mentions` is the old `MENTIONS` map of `xcheck.js`, per deck, verbatim. The README documents the marker convention for a new lesson (`01-head-<U><L>`, `02-runtime`, `02b-shared`, `sims-<U><L>`, `slides-<U><L>`, CSS `css-<U><L>`; 4.5: `01-head-45`, `sims-45`, `slides-45`, `css-45`; blueprint `{"section": "45", "next": "case"}`).

### build.py and suite.py
- `python3 build.py <U> <L>` runs the lesson's `gen_slides.py`, assembles head (filled, CSS inserted) + `02-runtime` + `02b-shared` + `sims.html` + `slides.html` between the registry's markers and writes the registry's `file`; `--all` builds every registered deck; `--out <path>` writes elsewhere; `--scratch --out <path>` assembles `scratch.html` (after `gen_scratch.py` if present) with the marker `scratch-<U><L>` and refuses an `--out` inside the repo. Each build prints path, bytes, lines, md5. Repo root = `../..` from the kit.
- `python3 suite.py <U> <L> [--matrix] [--theme light|dark|both] [--out <folder>] [--only …] [--deck <path>]` and `--all`: runs the audits in the old `run-all` order (walk light/dark, back light/dark, fonts, keys, readability, print, render3d, extras, chem, timing, supgap, zoom light/dark, click, layout, the deck's extra audits, xcheck, contact light/dark, zoomsheet light/dark), one PASS/FAIL line per audit with its duration and the audit's verdict line, a summary, exit 1 on any failure. Results in `<out>/<U>-<L>/` (`suite.json`, `logs/*.log`, each audit's JSON, screenshots, sheets); default `<out>`: `$SLIDES_KIT_OUT`, else `<system temp>/slides-kit-out`; a folder inside the repo is refused. Matrix only with `--matrix` or `MATRIX=1`. `--deck` skips xcheck; a scratch deck (it carries a `scratch-<U><L>` part) also runs without the lesson's explicit zoom checks.
- Configuration reaches the audits through the environment that `suite.py` sets: `DECK`, `OUT`, `DECKNAME`, `LESSON`, `BUDGET`, `KEYS_CFG`, `EXTRAS_CFG`, `MATRIX`, `SLIDES`, `XCHECK`.

### Diff summary per file (configuration plumbing only; every assertion kept)
| File | Change |
|---|---|
| `audits/walk.js`, `back.js`, `fonts.js`, `readability.js`, `print.js`, `render3d.js`, `supgap.js`, `click.js`, `layout.js` | moved, not changed |
| `audits/lib.js` | `DECK` and `OUT` now required from the environment (old defaults: the absolute 4.1 deck path and the kit folder); both resolved to absolute paths; `OUT` created if missing; header comment |
| `audits/keys.js` | the inline 4.1 ids removed; `KEYS_CFG` (registry `keys_cfg`) required |
| `audits/extras.js` | the inline 4.1 settings removed; `EXTRAS_CFG` (registry `extras_cfg`) required |
| `audits/timing.js` | the inline 4.1 budget moved to `parts/lessons/4-1/budget.json` (checked equal to the old object); `BUDGET` required |
| `audits/zoom.js` | the teacher's explicit checks are chosen by `LESSON` (`4.1`, `4.2`) instead of `/4-2/` in the deck path; a lesson without a list gets none (before: any other path got the 4.1 list). The 4.1 (11) and 4.2 (13) lists are word for word |
| `audits/contact.js`, `audits/zoomsheet.js` | `OUT` required (old default: the kit folder); the sheet title uses `DECKNAME` or the deck's file name (old default: `slides-4-1.html`) |
| `audits/xcheck.js` | deck list, blueprint path, section ids, objectives, mention map and walk JSON from `XCHECK`; output to `OUT/xcheck.json`; the matrix rows are those of the listed objectives (regex `\d+\.\d+\.\d+` filtered by them instead of `4\.[12]\.[1-5]`), the per-objective loop and the rate-slide regex take the objectives list instead of `1..5` / `<L>.[1-5]`; the matrix-row assertion is labelled with its count and range (see Deviations) |
| `audits/units.js`, `audits/cycle.js` | renamed from `units67.js`, `cyclecheck.js`; slide range from `SLIDES` (registry `extra_slides`) instead of the hard-coded `5..11`; exit code set from the verdict each already printed (see Deviations) |
| `parts/lessons/4-1/chem.js`, `4-2/chem.js` | `require('../../../audits/lib')`; 4.2: the hard-coded absolute `DECK` default removed |
| `parts/lessons/*/gen_slides.py`, `4-2/gen_scratch.py` | output file `slides.html` / `scratch.html` next to the script; header comment |
| `parts/shared/01-head.html` | the two 4.1 head strings → `{{TITLE}}`, `{{DESCRIPTION}}` (two places each) |
| `split_parts.py` | writes `<CSS>.css` for any `/* part: CSS start|end */` block (before: only `01c-css-42`); reads and writes with `newline=''` |

## Verification
### Byte identity (step 0 and after)
| File | Before (old `build.sh`, `build42.sh`) | After (`build.py --all`) | Size before / after |
|---|---|---|---|
| `unit4/slides-4-1.html` | `ebd342f1ee0e11c47157141cf3b2a59b` | `ebd342f1ee0e11c47157141cf3b2a59b` | 194,646 / 194,646 bytes |
| `unit4/slides-4-2.html` | `c3fa219a806963f9a66c3baf643153f4` | `c3fa219a806963f9a66c3baf643153f4` | 203,769 / 203,769 bytes |
| `unit4/blueprint.html` | `ed3bf8e23e1616d95014f0614c74e8d1` | `ed3bf8e23e1616d95014f0614c74e8d1` | 44,978 / 44,978 bytes |
The old builds reproduced the repo files and the handoff md5s before anything moved; the generated `slides.html` parts are unchanged too (4.1 `99b93e8af8a67d6647159ee7eb089480`, 4.2 `afe99626152d35cd214a2e9c0a9ab790`), as is the regenerated 4.2 `scratch.html`. Also checked: `build.py 4 1 --out <scratchpad>/deck41.html` is identical to the repo deck; `split_parts.py` on both decks returns `02-runtime`, `02b-shared`, `01c-css-42.css`, `06-sims-42`, `04-slides` identical to the kit parts. Lines in `workshop/artifacts/01/md5.txt`.

### suite.py --all --theme both, matrix off (exit 0)
| Audit | Theme | 4.1 | 4.1 s | 4.2 | 4.2 s |
|---|---|---|---|---|---|
| walk | light | PASS (156 states, max empty 29%) | 190.5 | PASS (173 states, max empty 32%) | 210.3 |
| walk | dark | PASS | 189.8 | PASS | 210.5 |
| back | light | PASS (156 / 156) | 76.9 | PASS (173 / 173) | 84.5 |
| back | dark | PASS | 77.0 | PASS | 84.6 |
| fonts | light | PASS | 47.7 | PASS | 51.1 |
| keys | - | PASS (48 checks) | 35.5 | PASS (48 checks) | 35.2 |
| readability | - | PASS | 2.6 | PASS | 3.0 |
| print | - | PASS (25 slides, 156 frame lines, 9 pages) | 2.0 | PASS (26 slides, 173 frame lines, 8 pages) | 2.0 |
| render3d | - | PASS | 2.3 | PASS | 2.4 |
| extras | - | PASS | 5.5 | PASS | 5.3 |
| chem | - | PASS (32 checks) | 1.5 | PASS (39 checks) | 1.5 |
| timing | - | PASS (47 / 47 min) | 1.2 | PASS (47 / 46.5 min) | 1.3 |
| supgap | - | PASS (25 pairs) | 4.5 | PASS (139 pairs) | 4.6 |
| zoom | light | PASS (571 states, min fill 64%, explicit 11 of 11) | 225.2 | PASS (707 states, min fill 67%, explicit 13 of 13) | 261.0 |
| zoom | dark | PASS (same) | 223.4 | PASS (same) | 262.8 |
| click | - | PASS (9 graded, 3 Predict now, 47 assertions) | 27.8 | PASS (9, 3, 47) | 30.1 |
| layout | - | PASS (24 option lists, no clipping) | 19.4 | PASS (24, no clipping) | 21.8 |
| units | - | not registered | | PASS (63 frames, 89 cards, 0 missing) | 10.2 |
| cycle | - | not registered | | PASS (112 checks, 0 short cycles) | 157.6 |
| xcheck | - | PASS (42 of 42) | 1.6 | PASS (40 of 40) | 1.6 |
| contact | light | PASS | 4.3 | PASS | 4.5 |
| contact | dark | PASS | 4.1 | PASS | 4.1 |
| zoomsheet | light | PASS | 2.3 | PASS | 2.3 |
| zoomsheet | dark | PASS | 2.4 | PASS | 2.1 |
| total | | 22 of 22 | 1147.6 | 24 of 24 | 1454.4 |

xcheck against the old script: the base commit's `step7/xcheck.js`, run on the same two `walk-light.json` files, gives 81 of 81 PASS; the new per-deck runs give 42 + 40 = 82. The 80 deck assertions are identical in name, verdict and detail; the old single "matrix: ten rows 4.1.1 to 4.2.5 found" is now "matrix: 5 rows 4.1.1 to 4.1.5 found" and "matrix: 5 rows 4.2.1 to 4.2.5 found" (`workshop/artifacts/01/xcheck-old-vs-new.txt`).

Artifacts (text only, no screenshots, no per-press folders, no sheets): `workshop/artifacts/01/suite-all.txt` (console), `4-1/` and `4-2/` (`suite.json`, every audit's JSON, `logs/<audit>[-<theme>].log`), `md5.txt`, `xcheck-old-vs-new.txt`; 86 files, 1.7 MB.

### Scratch path (not committed)
- `python3 build.py 4 2 --scratch --out <scratchpad>/scratch42.html` → 129,238 bytes, 1,611 lines, md5 `990dd279f85f821ccc0ee7e1161feb42`.
- `python3 suite.py 4 2 --deck <scratchpad>/scratch42.html --only walk --theme light` → **FAIL**: 127 states walked; all 119 failures are the emptiness gate (scratch slides hold one animation and a label; max empty 70%); no overflow, cue, advance or console-error failure. A diagnostic run of the same command with `EMPTY_MAX=1` (the existing environment knob of walk.js, set for that run only; nothing in the kit changed) → PASS, 127 states. See open question 1.

## Repo state
- Decks: no deck changed (md5s and sizes above, before = after); `unit4/` untouched.
- `git status --short` before the commit (all staged): 47 entries under `tools/slides-kit/` (renames, the edited moves, the new `build.py`, `suite.py`, `registry.json`, `parts/lessons/4-1/budget.json`, the removed `step1/*.sh` and `step10/split_parts.py` [git pairs the rewritten `split_parts.py` as delete + add]) and, under `workshop/`, `reports/01-kit-check.md`, `artifacts/01/**` (86 files), `status.md`, `log.md`. Nothing else.
- `git status --short` after the commit: in the pull-request comment `report 01 ready`.

## Deviations
1. **Registry fields `css` and `extra_slides`.** `css` holds the CSS marker name (`01c-css-42`, `null` for 4.1) next to the five `markers`; `extra_slides` holds the slide range the 4.2 extra audits cover (`[6, 12]`), which `units67.js` and `cyclecheck.js` hard-coded as `5..11`. Both are configuration that moved, not new behavior.
2. **`units.js` and `cycle.js` set an exit code.** They printed a verdict but always exited 0, so the old `run-all` scripts did not run them and a suite could not grade them. Each now sets `process.exitCode` from the verdict it already printed (`bad.length`); the checks themselves are unchanged.
3. **xcheck runs per deck.** `suite.py` runs xcheck in each deck's sequence, so each run checks the matrix rows of that deck's objectives; the assertion "matrix: ten rows 4.1.1 to 4.2.5 found" became one assertion per deck with its count and range in the label (digits). The deck list in `XCHECK` can hold several decks, and then one assertion covers all of them, as before.
4. **zoom.js explicit checks by lesson.** Chosen by `LESSON` instead of the deck's file name, so a deck at another path (for example `--out`) keeps its checks, and a new lesson no longer inherits the 4.1 list. A scratch deck gets none.
5. **`suite.py --deck` always skips xcheck,** not only for a scratch deck: the cross-check compares the blueprint with the repo deck.
6. **Guards not in the brief:** `suite.py` refuses an output folder inside the repo; `build.py --scratch` refuses an `--out` inside the repo. Results go to `<out>/<U>-<L>/` also for a single deck.
7. **Small run differences from `run-all`:** the contact and zoom sheets now count toward the exit code (`run-all` ignored their status; all passed); with `--theme dark` alone, fonts runs in dark (before: always light; the full runs here used light, as before).
8. **Pull-request subscription:** `subscribe_pr_activity` on pull request #1 was refused for this session (no reason given beyond "Could not subscribe"; likely the orchestrator's session holds it). The `report 01 ready` comment is posted anyway.

## Open questions
1. **Scratch decks and the emptiness gate.** Scratch slides fail walk (and would fail layout) on "at most one third of the slide body empty" by design. For the animation steps 02 and 03: may scratch runs set `EMPTY_MAX=1` (the walk and layout knob that already exists), should the scratch slides be filled (for example with the band the deck will use), or should the animation steps run the other audits only (`--only back,fonts,...`)? Not decided here.
2. **keys and extras need deck features.** `keys.js` asserts a 180 s timer on frame 1 of the `tm` slide, a `hk` slide whose frame 1 has no `.timer` slot, and a card on frame 3 of the `cr` slide that the zoom cycle reaches; `extras.js` asserts a turning 3D model on the `hash` frame (reduced motion holds it still). The 4.5 deck needs slides that provide these (or a brief that says how to configure them), so its registry entry can be written.
3. **KIT.md lists placeholders for unit and lesson** in the head template; the brief named only `{{TITLE}}` and `{{DESCRIPTION}}`, and the head uses nothing else today. Add them only if a later deck needs them?
4. **Handoff blueprint numbers.** `docs/handoff-4-1-4-2.md` lists `unit4/blueprint.html` as 45,017 bytes, md5 `636e06f8…`; the file is now 44,978 bytes, md5 `ed3bf8e2…` (it changed after the handoff). The doc was moved as is, with its top line only.
