# Kit conventions (tools/slides-kit/)

The kit holds the source parts, generators, build scripts and audit scripts. Decks are built only through the kit, never hand-edited. Built decks carry comment markers `<!-- part: NAME start -->` / `<!-- part: NAME end -->` so parts can be split back out with `split_parts.py`.

## Layout after generalization (step 01 of the first workshop after 4.1/4.2; implementer's job, spec below)
- `parts/shared/`: `01-head.html` (head template with placeholders for title, description, unit and lesson), `02-runtime.html`, `02b-shared.html` (chemistry data used by more than one lesson).
- `parts/lessons/<U>-<L>/`: `css.css` (lesson-only CSS, optional), `sims.html` (the lesson's animations), `gen_slides.py` (writes `slides.html` from Python data), `budget.json` (per-slide minutes and period split), `chem.js` (the lesson's chemistry audit).
- `build.py <U> <L>`: assembles head + shared + lesson parts into `unit<U>/slides-<U>-<L>.html` with markers; `build.py --all` rebuilds every registered deck.
- `suite.py <U> <L> [--matrix] [--theme light|dark|both]`: runs every audit for a deck and writes logs and sheets to an output folder; `suite.py --all` for every registered deck.
- `registry.json`: every built deck with unit, lesson, title, description, period split, check count; the blueprint cross-check reads it.
- `audits/`: walk, back, fonts, keys, readability, print, render3d, extras (reduced motion, narrow fallback), timing, supgap, zoom (with settle wait and the viewport matrix), click, layout (including the overlap check: no intersecting bounding boxes among visible text, cards, chips and badges beyond 2 px, and canvas label boxes recorded by the painter), contact, zoomsheet, xcheck (parametrized by unit and lesson rows).
- `README.md`: how to add a lesson, build, run suites, split parts, and the absolute paths to change if the repo moves.

## Rules
- A change to a shared part rebuilds every registered deck and re-runs their suites with `MATRIX=0`; the report lists the md5 of every deck before and after. Decks whose lesson parts did not change must come out byte-identical when the shared parts did not change.
- Lesson parts never redefine shared behavior; new engine features go into the shared runtime behind a per-lesson option, with the reference decks re-audited.
- Playwright and Chromium exist in a Claude cloud session; never run "playwright install". Decks open with `file://` URLs.

## Generalization step (brief 01 whenever the kit is still deck-specific)
Move the current step1/step6/step7/step10 layout into the structure above without changing any deck's bytes: the reference decks must rebuild byte-identical from the new layout (same md5s). Convert the hard-coded scripts (`build.sh`, `build42.sh`, `run-all.sh`, `run-all42.sh`, deck-specific environment variables) into `build.py`, `suite.py` and `registry.json`. Keep every audit's assertions. Write the README. Report the md5s before and after.

## If the kit is absent from the base branch
The built reference decks carry the part markers, so `split_parts.py` logic can be recreated: cut each deck at its markers into the shared parts and the lesson parts. Generators and audits must then be rewritten from RULES.md section 11 and from how the reference decks behave. This is slow; the teacher should commit the kit to `main` once so no workshop has to do it.
