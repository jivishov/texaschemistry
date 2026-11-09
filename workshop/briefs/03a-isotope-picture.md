# Brief 03a: Fix: the isotope picture on slide 7 (the word-card icon and the second shade), the final suites again

Step: 03a · Kind: fix · Lesson: 5.1 · Effort: high · Time box: the two items below, the rebuild and the suites; no other change to any slide, animation or text

## Goal
Review 03 found two things the step 03 crops show on slide 7. First, the word card "average atomic mass" (`#s07-word`, icon `ic-avgmass` in `gen_slides.py`) still draws its two atoms at two sizes (radii 18 and 24), the heavier one bigger: the same wrong picture that review 02 F1 removed from the animation. Second, the two browns of the `isotopes` stage are too close to be told apart at a glance in the light theme (`--rope` and `--rope` mixed 15% toward black), so the frame note "The two shades stand for two masses." points at a difference the room cannot see. After this brief the icon and the animation agree: isotopes of one element at one size, two shades that are plainly different in both themes.

## Read first
1. `workshop/reviews/03-final.md` (findings F1 and F2 of that review; everything else is accepted).
2. `workshop/reports/03-final.md` A1 (the current isotope stage: radius 46, label 44 px, `lt` and `dk` positions) and `tools/slides-kit/parts/lessons/5-1/sims.html` at `ISO_R` and the `isotopes` stage.
3. `workshop/RULES.md` legibility and drawing lines (label 36 px floor on canvas, shape 60 px floor, no overlap); `workshop/KIT.md`.
4. `workshop/artifacts/03/crops/s07f7-isotopes-light.jpg` and `-dark.jpg`: what the picture looks like now.

## Build (lesson parts only: `parts/lessons/5-1/`)
A1. **The icon `ic-avgmass`** (`gen_slides.py`): two circles of one radius, side by side inside the 100 × 100 viewBox, not touching the balance line; one in `--rope`, the other in the same darker shade the animation uses after A2 (a CSS `filter: brightness(...)` or a `color-mix(...)` fill: pick the one that matches the canvas shade best in both themes). Keep the balance line and the tick. Alt text: "Icon: two isotopes of one size and different mass, and their average". The icon is 104 px on the card; the card's text does not move.
A2. **The second shade of the `isotopes` stage** (`sims.html`): make the darker shade plainly darker, a mix of `--rope` toward black between 35% and 45% (pick the value at which the two shades differ at a glance on both the light and the dark crop while every "Cu" label stays readable: the fonts audit must pass on the canvas labels). Radius 46, the `lt` and `dk` positions, the label size and the frame note stay as they are. Update any assertion in `chem.js` or `scratch-check.js` that reads the mix value (the shade count stays 2).
A3. Nothing else changes: no text, no note, no other stage, no shared part, no blueprint, no README. `docs/handoff-5-1.md` names no mix value; leave it unless A1 or A2 makes one of its lines untrue.

## Rebuild and the suites
C1. `python3 tools/slides-kit/build.py 5 1`, then `build.py --all`: 4.1 `ebd342f1…` and 4.2 `c3fa219a…` unchanged.
C2. Bench: `build.py 5 1 --scratch` to the scratchpad; `node parts/lessons/5-1/scratch-check.js` passes; `suite.py 5 1 --deck <scratch> --only walk,layout --theme both` on the bench passes with 0 overlaps.
C3. Deck: `suite.py 5 1 --theme both` (no matrix: it ran once this workshop in step 03 and nothing here changes a size, a position or a viewport behaviour) with an output folder in the scratchpad, plus `suite.py 5 1 --only fonts --theme dark` as in step 03: every audit PASS in both themes, overlap 0 intersections with no baseline in both themes, xcheck 60 of 60, contact and zoom sheets in both themes.

## Verify
V1. C3's suite tables for both themes (verdict lines) and the dark fonts line.
V2. `scratch-check.js` and `chem.js` PASS lines and counts.
V3. md5 of `unit5/slides-5-1.html` before (3c86da49…) and after; 4.1 and 4.2 unchanged; `unit5/blueprint.html` unchanged (5975fb9c…).
V4. Artifacts under `workshop/artifacts/03a/` (JPEG at most 800 KB each, text, no PNG, no per-press folders): `sheets/` contact and zoom sheets of both themes (these become the final sheets); `logs/` every audit log of the final run in both themes, `overlap-light.txt`, `overlap-dark.txt`, the xcheck log, the bench logs; `crops/` full frames of slide 7 frame 5 (the word card, `s07f5`) and frame 7 (`isotopes`, `s07f7`) in both themes.
V5. In the report, the two mix values chosen (icon and canvas) and the contrast of the "Cu" label on the darker shade in both themes.

## Constraints
- Files allowed to change: `tools/slides-kit/parts/lessons/5-1/gen_slides.py`, `sims.html`, `slides.html` (built by `gen_slides.py`), `chem.js`, `scratch-check.js`, `scratch.html` (built), `unit5/slides-5-1.html` (built, never hand-edited), `tools/slides-kit/docs/handoff-5-1.md` (only if A3 says so), `workshop/reports/03a-isotope-picture.md`, `workshop/artifacts/03a/**`.
- No change to `parts/shared/`, `audits/`, `build.py`, `suite.py`, `split_parts.py`, `css.css`, `budget.json`, `zoomchecks.js`, `registry.json`, `README.md`, `unit5/blueprint.html`; nothing under `unit4/`; no edits to `workshop/status.md`, `workshop/log.md`, the plan, the lesson sheet, RULES, KIT, PROTOCOL, the step 03 artifacts or report.
- No git state changes (no add, commit, stash, checkout, branch); the orchestrator commits after the review.
- Never open `unit5/old-slides/slides-5-1.html`.
- Long suites run in the background with their output in the scratchpad; the artifacts folder gets the JPEG sheets and the text logs only.

## Report
`workshop/reports/03a-isotope-picture.md` from `templates/report.md`: A1 and A2 with the values chosen, the suite tables (both themes), xcheck 60 of 60, md5s before and after, `git status --short`, deviations with reasons, open questions. Stop and report.
