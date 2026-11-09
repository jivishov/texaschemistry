# FINAL: Unit 5, Lesson 5.1 deck (Counting particles with the mole)

Workshop `workshop/unit5-5-1` over `main` (11d08fe), in-session lean mode, run per `workshop/ORCHESTRATOR.md`. Pull request: https://github.com/jivishov/texaschemistry/pull/2 (draft, to `main`). Turn: **teacher**.

## What is on the branch
- `unit5/slides-5-1.html`: 28 slides, 197 frames, 11 graded checks (slides 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 19), 3 Predict-now questions, period 1 slides 1 to 14 (43.75 min), period 2 slides 15 to 28 (46 min). Built by `python3 tools/slides-kit/build.py 5 1`, never hand-edited. **md5 `f5bdd830591d8d23583af5409ad4dc98` (255,203 bytes, 2,493 lines)**, reproduced by the orchestrator's own rebuild.
- `tools/slides-kit/parts/lessons/5-1/`: eleven animations (78 stages) in `sims.html`, the deck generator `gen_slides.py`, `budget.json`, `chem.js` (94 checks), `zoomchecks.js`, `css.css` (`css-51`, with the dark-theme particle violet), the bench `gen_scratch.py` and `scratch-check.js` (348 assertions).
- `unit5/blueprint.html`: the 5.1 numbers only (deck line, four Slides cells, two matrix rows; 7 lines, numbers only). md5 `5975fb9cdfa6f57cef0cdb26a5f623be`.
- `unit5/old-slides/slides-5-1.html`: the rejected 22-slide deck, byte for byte (`f35ed835ae94844c7df7e1c42e14dcd9`), with a five-line README; never read.
- Reference decks unchanged throughout: `unit4/slides-4-1.html` `ebd342f1ee0e11c47157141cf3b2a59b`, `unit4/slides-4-2.html` `c3fa219a806963f9a66c3baf643153f4`. No shared part changed after step 01a.
- Kit: the overlap check (DOM boxes, canvas labels and shapes, a motion-on pass at two moments), the reference-deck overlap baselines, the Unit 5 cross-check form, `registry.json` with 5.1 built, the README, `docs/handoff-5-1.md`.
- Workshop record: `ASSIGNMENT.md`, `lessons/5-1.md`, `plan/5-1.md` (revision 2), briefs 01, 01a, 02, 03, 03a with their reports and reviews, `log.md`, `artifacts/02`, `/03`, `/03a` (the final sheets are in `artifacts/03a/sheets/`).

## Suite summary (final deck `f5bdd830…`, both themes)
`suite.py 5 1 --theme both`: **23 of 23 PASS** (walk 197 states; back 197 forward and 197 back; fonts in both themes; keys 48; readability; print 28 slides, 11 pages; render3d; extras; chem 94; timing 43.75 and 46 min; supgap 107; zoom 1,072 zoomed states per theme, min fill 62%; click 11 checks, 3 Predict-now, 55 assertions; layout 0 intersections in both themes with no baseline, 8,671 boxes, 16 of 16 canvases instrumented, 12 live frames at two moments; xcheck 60 of 60; contact and zoom sheets in both themes). Bench: scratch-check 348 of 348, walk and layout in both themes with 0 overlaps. The orchestrator re-ran fonts, layout, chem, readability and xcheck on the final bytes in both themes: identical.

The full zoom matrix ran in step 03 on deck `3c86da49…`: 12 of 12 viewport and scale combinations per theme, 375 zoomed states each, 0 fails. Step 03a changed two colors and one icon's circle sizes (no size, position or viewport behaviour of any zoom unit), so the matrix was not re-run; every other audit was.

## Judgment calls for the teacher (all made; say the word to change any)
1. **Isotopes (slide 7).** The six copper atoms are one size in two plainly different browns (the plan had two sizes; isotopes of one element have the same size). The word-card icon matches: two equal circles, one darker.
2. **Avogadro (slide 12).** Card and caption: "At one temperature and pressure, equal gas volumes hold equal numbers of particles. He never knew the number."
3. **Silicon cube (slide 13).** The card says "Corner and face atoms are shared: 8 atoms per cube." while the picture rings the 18 atoms that touch one cube; the frame note carries the arithmetic (8 × ⅛ + 6 × ½ + 4 = 8). The answer line reads "A. Those measurements gave the value fixed in 2019." and option A lost the word "its" to keep the frame at 35 words.
4. **Dark theme.** Particles are violet `#cc99ff` in the dark theme by a rule in the lesson's own CSS, because the shared dark tokens make grams and particles both amber. Later Unit 5 decks copy the rule, or a kit round moves it to the shared head and re-audits every deck.
5. **Wording tightenings** from step 02 (report 02 Deviation 4), among them "10²³ has 23 zeros" in place of the plan's false "6.022 × 10²³ has 23 zeros".
6. **4.1's two real overlaps** (slide 10 electron balls over labels, slide 16 the enlarged cell cutting its neighbours) stay in the reference-deck baseline; fixing them is a Unit 4 change, not this workshop's.

## Left for later (not in this branch)
- `unit5/blueprint.html` section `l52` carries the old sentence "Deck: 22 slides. Checkpoints 16 to 19, …" for 5.2; the 5.2 workshop writes 5.2's numbers.
- Pull request https://github.com/jivishov/texaschemistry/pull/1 (the 4.5 workshop, branch `workshop/unit4-5-6`, based on `claude/unit-4-chemistry-slides-j62190`) touches the same kit files as this branch (`registry.json`, `suite.py`, `README.md`, `audits/lib.js`, `audits/layout.js`, `audits/xcheck.js`); whichever merges second needs those reconciled by hand, and the 4.5 deck has not been through the overlap check.
- Three kit items for a kit round (review 02 F7): the ✓ badge pseudo-element above row options, canvas strokes the overlap instrumentation does not record, the stage time of a live first stage.

## Merge instruction
1. The teacher says **"merge"** (or asks for changes first; a change reopens a fix brief).
2. On "merge", the implementer makes one last commit on `workshop/unit5-5-1` that removes `workshop/artifacts/` (there are no brief images); nothing else changes. The orchestrator pushes it.
3. The teacher merges pull request 2 into `main` (or says "commit and push" and merges later). Nobody but the teacher merges or pushes to `main`.
