# Brief 03: Final: four fidelity refinements, the dark-theme particle color, the blueprint numbers, the dark theme and the zoom matrix, the final suites, the kit records

Step: 03 · Kind: final (with a small fix section) · Lesson: 5.1 · Effort: extra-high · Time box: the items listed here only, no refactoring, no redesign of any animation or slide

## Goal
The 5.1 deck passes every audit in both themes with the full zoom matrix, the blueprint's 5.1 numbers match the deck so that xcheck is 54 of 54, four small fidelity refinements from review 02 and the teacher's fidelity round are in the deck, the Unit 5 color code holds in the dark theme, and the kit's README and docs record 5.1. 4.1 and 4.2 stay byte-identical (no shared part changes). The orchestrator then writes FINAL.md.

## Read first
1. `workshop/RULES.md` sections on legibility, language (14-word sentences, grade 8, the 35-word frame budget), drawing conventions and repo numbers; `workshop/KIT.md`; `workshop/ASSIGNMENT.md` (judgment call 3: the Unit 5 blueprint form, numbers only).
2. `workshop/reviews/02-animations-and-deck.md` (findings F1 to F7 and the decisions: this brief does F1, F2 and F6, plus three wording items from the teacher's fidelity round); `workshop/reports/02-animations-and-deck.md` (open questions 1 and 4; Deviation 3 on the isotope picture).
3. `workshop/lessons/5-1.md` (the data section: every number below is there); `workshop/plan/5-1.md` section 5 for slides 2, 7, 12, 13 and the alignment line at its end.
4. `tools/slides-kit/README.md`: the xcheck Unit 5 form (what it reads from the blueprint) and the registry table; `tools/slides-kit/docs/handoff-4-1-4-2.md` (the form of a handoff note).
5. `unit5/blueprint.html`: only the section `l51` and the two matrix rows that name "Deck 5.1". The xcheck log `workshop/artifacts/02/logs/xcheck.log` lists the 17 rows that read the old numbers.
6. `tools/slides-kit/parts/shared/01-head.html`: only to find how the dark theme is selected (the selector or attribute) and the dark values of `--warm`, `--e`, `--accent`; do not change it.

## Build

### A. Fidelity refinements (lesson parts only: `parts/lessons/5-1/`)
A1. **Slide 7, `centJar` stage `isotopes`** (review F1): draw the copper isotopes at one size, two shades (the two browns already used), nothing added. Update the frame note: "The two shades stand for two masses. Isotopes of one element have the same size." Adjust any `meta()`, `chem.js` or `scratch-check.js` assertion that tested two sizes; keep the shape floor (60 px) and the label floor.
A2. **Slide 12, `moleHistory` stage `avogadro`** (teacher's fidelity round): Avogadro's hypothesis needs one temperature and pressure. Caption row (`.caprow`) for the stage: "1811: Avogadro's idea. At one temperature and pressure, equal gas volumes hold equal numbers of particles. He never knew the number." (3 + 13 + 5 words). Inside the canvas card, use "At one temperature and pressure, equal gas volumes hold equal numbers of particles." if it fits at 36 px with no overlap; otherwise keep the card's lines and let the caption row carry the condition. Frame note: state the condition.
A3. **Slide 13, `siliconSphere` stage `cube`** (review F3 and the teacher's fidelity round): the picture rings the 18 atoms that touch one cube while the chip says 8, so the card names the sharing. Card text: "X-rays measure one cube's edge: 543.102 pm. Corner and face atoms are shared: 8 atoms per cube." (7 + 9 words). The chip "8 atoms per cube" stays. The frame note keeps the arithmetic (8 × ⅛ + 6 × ½ + 4 = 8). Check answer line on slide 13: "A. Those measurements gave the value fixed in 2019." (replaces "They gave…").
A4. **Slide 2, frame `scale`, note only**: add "The scale was zeroed with the empty jar; slide 6 teaches zeroing." No on-screen change.
A5. **Dark-theme particle color** (review F2, report open question 1): in `css.css` (`css-51`), under the dark-theme selector the head uses, give the Unit 5 particle quantity its own color so that grams (`--warm`), moles (`--accent`) and particles differ in the dark theme: a violet readable on the dark card background (contrast 4.5:1 or more against the card and the panel; the fonts audit must pass). Cover every place the particle color is used: the `.chip` class of particle values, the legend dot on slide 5, the canvas (find how `sims.html` reads its colors; if it reads the token from computed style, the override in `css-51` covers it, else set the lesson's own token and read that). Light theme unchanged. No shared part changes.

### B. Blueprint numbers (`unit5/blueprint.html`; numbers only, the Unit 5 form; no prose change)
B1. Deck line: "Deck: 22 slides. Checkpoints 16 to 19, predictions revisited 20, CER exit ticket 21, self-rating 22." → "Deck: 28 slides. Checkpoints 22 to 25, predictions revisited 26, CER exit ticket 26, self-rating 27."
B2. Objectives table, Slides cells: 5.1.1 "5, 6" → "6, 7"; 5.1.2 "7 to 11, 15" → "8 to 13, 21"; 5.1.3 "12, 13" → "16 to 18"; 5.1.4 "14" → "19, 20".
B3. Matrix rows: C.8(A) "Deck 5.1, slides 5 to 11, 15" → "Deck 5.1, slides 6 to 13, 21"; C.8(B) "Deck 5.1, slides 12 to 14; Deck 5.3, slides 5 to 14" → "Deck 5.1, slides 16 to 20; Deck 5.3, slides 5 to 14" (the 5.3 part unchanged).
B4. Then grep the `l51` section for any other slide number of the old deck (a "slide N" in prose) and list each in the report without changing it; the orchestrator decides. `suite.py 5 1 --only xcheck` (after a walk, or on the step 02 walk output) must report 54 of 54.

### C. Rebuild and the suites
C1. `python3 tools/slides-kit/build.py 5 1`, then `build.py --all`: 4.1 `ebd342f1…` and 4.2 `c3fa219a…` unchanged (no shared part changed; if one did, stop and report).
C2. Bench: `build.py 5 1 --scratch` to the scratchpad; `node parts/lessons/5-1/scratch-check.js` passes; `suite.py 5 1 --deck <scratch> --only walk,layout,zoom --theme both` on the bench for the changed stages (or the whole bench, your choice) passes with 0 overlaps.
C3. Deck: `suite.py 5 1 --theme both --matrix` (the full zoom matrix) with an output folder in the scratchpad: every audit PASS in both themes, overlap 0 intersections with no baseline in both themes, xcheck 54 of 54, contact and zoom sheets in both themes.

### D. Kit records
D1. `tools/slides-kit/README.md`: the lines that describe 5.1 as not yet built or as an example with `"built": false` now describe it as built (keep the example form if the README needs one); the decks list names 5.1 with its file.
D2. `tools/slides-kit/docs/handoff-5-1.md`: a short handoff in the form of `handoff-4-1-4-2.md`: the clicker map pointer, the eleven animations with their stages, the live stages and reduced-motion behavior, the Unit 5 color code (light and dark values), the known limitations (review 02 F7: the ✓ badge offset, unrecorded canvas strokes, the live first-stage timer workaround in `secondsLine`), the blueprint form. One screen of text, no paths outside the repo.
D3. `registry.json`: no change expected (`built: true` already); if a field must change, say which and why.

## Verify
V1. C3's suite tables for both themes (verdict lines), the matrix summary line, the xcheck 54 of 54 line.
V2. `scratch-check.js` and `chem.js` PASS lines after A1 to A3 (counts may change; say how).
V3. md5 of `unit5/slides-5-1.html` before (be9bc2c7…) and after; 4.1 and 4.2 unchanged; `unit5/blueprint.html` md5 before (0b7dbba8…) and after with `git diff --stat unit5/blueprint.html` (numbers only: a handful of changed characters on the lines of B1 to B3).
V4. Artifacts under `workshop/artifacts/03/` (JPEG at most 800 KB each, text, no PNG, no per-press folders): `sheets/` contact and zoom sheets of both themes; `logs/` every audit log of the final run in both themes, the matrix log, `overlap-light.txt`, `overlap-dark.txt`, the xcheck log; `crops/` full frames of slide 7 `isotopes`, slide 12 `avogadro`, slide 13 `cube` and slide 13's answer frame in both themes, and slide 5's legend plus one chip-heavy frame (slide 6 `count`) in the dark theme to show the three colors.
V5. Readability and layout verdicts after the wording changes (the 35-word budget on the slide 12 caption frame and the slide 13 cube frame).

## Constraints
- Files allowed to change: `tools/slides-kit/parts/lessons/5-1/**`, `unit5/slides-5-1.html` (built, never hand-edited), `unit5/blueprint.html` (B1 to B3 only), `tools/slides-kit/README.md`, `tools/slides-kit/docs/handoff-5-1.md` (new), `tools/slides-kit/registry.json` (only if D3 says so), `workshop/reports/03-final.md`, `workshop/artifacts/03/**`.
- No change to `parts/shared/`, `audits/`, `build.py`, `suite.py`, `split_parts.py`; nothing under `unit4/`; no edits to `workshop/status.md`, `workshop/log.md`, the plan, the lesson sheet, RULES, KIT, PROTOCOL.
- No git state changes (no add, commit, stash, checkout, branch); the orchestrator commits after the review.
- Never open `unit5/old-slides/slides-5-1.html`.
- A shared-part change would mean rebuilding and re-auditing every registered deck with the matrix; this brief forbids it. If a refinement seems to need one, stop and report the need instead.
- Keep every student-facing sentence at 14 words or fewer, grade 8 or below, every label 36 px or more on canvas and 34 px or more in the DOM, no overlap at rest or at the live moments.

## Report
`workshop/reports/03-final.md` from `templates/report.md`: done items A1 to D3 with the exact wording now in the deck, the suite tables (both themes, matrix on), xcheck 54 of 54, md5s before and after, `git status --short`, deviations with reasons, open questions. Stop and report.
