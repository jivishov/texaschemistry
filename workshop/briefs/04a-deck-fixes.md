# Brief 04a: Deck fixes from review 04

Step: 04a · Kind: fix · Lesson: 4.5 · Effort: high · Time box: the six items below only, no refactoring, one report

## Goal
The three failing audits pass (chem, readability, and xcheck down to its blueprint-number lines only), with the deck otherwise unchanged. Items 1 to 5 change the animation, the texts and one audit rule; item 6 is the proof.

## Read first
`workshop/reviews/04-deck.md` (findings F1, F2, F3, F6); your `reports/04-deck.md`; `parts/lessons/4-5/gen_slides.py`, `sims.html` (`heating`), `chem.js`, `scratch-check.js`; `audits/readability.js` (the visible-prose budget selector near line 26).

## Items
1. **`heating` with four CH₄ molecules** (2 × 2), water unchanged at six. The methane solid block takes at most 40% of the container and the gas spreads over all of it, area per molecule 2.5 times or more; readouts "Covalent bonds: 16 of 16 intact" (water "12 of 12"); attraction counts fall to 0 in the gas; `meta().molecules` 4 for CH₄; `scratch-check.js` and `chem.js` targets updated to the same two thresholds (40%, 2.5) and passing for both substances. Bench frames `CH4/solid` and `CH4/gas` as one JPEG under `artifacts/04a/`.
2. **Six check texts trimmed to the 35-word budget on their answer frames** (the budget counts the question, the options and the reason line; the brief's other words stay):
   - Slide 6: options "weak attractions between molecules" · "covalent bonds between molecules" · "ionic bonds"; reason "A. The Cl–Cl bond is inside each molecule. Only weak attractions act between molecules."
   - Slide 7: question "Why does bromine boil higher than chlorine?" (the plot on screen shows −34.0 °C and 58.8 °C); options and reason unchanged.
   - Slide 11: option A "The molecules move far apart, still whole."; reason "A. Each molecule keeps its two O–H bonds."; options B and C unchanged.
   - Slide 15: question "Why does molten NaCl conduct, but solid NaCl not?"; options "In the liquid, the ions can move." · "Melting turns atoms into ions." · "Melting frees sodium's electrons."; reason "A. The ions were always there. Now they can move."
   - Slide 17: reason "A. Ionic does not mean it dissolves. Check the data."; the rest unchanged.
   - Slide 18: question "A sharp blow splits a salt crystal. Why?"; options "Shifted layers put like charges together; they repel." · "Ionic bonds are weak." · "Electrons flow out of the crystal."; reason "A. Like charges repel and push the layers apart."
   The per-option feedback lines (`fb`) stay as they are. Update `chem.js` where it asserts these texts.
3. **The driving question on the slides** (slides 1, 3 and 25, the `.dq` cards; the notes may keep the blueprint's wording when quoting the reading): "Forces act within and between particles. How do they explain melting point, conductivity and hardness?" Keep the `dq` class; it may also carry `reg` if the register audit then passes (report the grade either way).
4. **The exit-ticket sample (slide 25)**: "The forces that come apart set the melting point. Snow melts at 0 °C: only attractions between molecules let go. Salt needs 801 °C: ionic bonds. Sand needs near 1700 °C: covalent bonds. Attractions are weaker than bonds." (35 words, each sentence 14 or fewer). And in `audits/readability.js`, the visible-prose budget no longer counts text inside `.dq` (the driving question is a fixed prompt that RULES 6 keeps on screen); add `.dq` to the budget's exclusion selector only, nothing else in the audit changes (the FK and sentence-length checks still see the driving question). Prove on the reference decks: `suite.py 4 1 --only readability` and `suite.py 4 2 --only readability` PASS as before.
5. **Rate slide zoom** (and the "I can" card on slide 5 if it shares the markup): when a target line is zoomed, its sentence runs the full width of the zoomed clone and "Review: slides …" sits under it, instead of a narrow column beside the review line. CSS for the zoomed clone (the runtime adds a class to the re-flowed copy; look at how 4.1 or 4.2 style `.rate li` when zoomed) in `parts/lessons/4-5/css.css`; no runtime change. A zoom-sheet frame of slide 26 as proof.
6. **Prove**: `python3 build.py 4 5`; `python3 suite.py 4 5 --theme both` (matrix off): every audit PASS except xcheck, whose failing lines are only the blueprint-number ones listed in report 04 (no new ones); `chem` 100%; `readability` PASS with no failing line; the two reference decks' readability PASS; 4.1 and 4.2 md5 unchanged; `git status --short` clean after the commit. Artifacts under `artifacts/04a/`: the suite console and the readability, chem and xcheck logs, the walk contact sheets of both themes (JPEG, split as needed), the slide-26 zoom frame, the D1 frames. The deck's new md5 and size in the report.

## Constraints
- Files allowed to change: `tools/slides-kit/parts/lessons/4-5/**`, `tools/slides-kit/audits/readability.js` (item 4 only: one selector), `unit4/slides-4-5.html` (by `build.py` only), `workshop/reports/04a-deck-fixes.md`, `workshop/artifacts/04a/**`, `workshop/status.md`, `workshop/log.md`. No other file; no shared part; no blueprint.
- No git state changes beyond one commit on `workshop/unit4-5-6` and one push; `git pull --ff-only` first; never force-push; never push to `main`.
- Never read `unit4/old-slides/*`. No refactoring; nothing beyond the six items; a text not named here does not change.
- Do not retry the pull-request subscription.

## Report
`workshop/templates/report.md` → `workshop/reports/04a-deck-fixes.md`: each item with its proof line; the full suite table; the xcheck failing lines (blueprint numbers only); md5 and size of the deck, md5s of 4.1 and 4.2; `git status --short`; the commit hash; deviations; open questions. Flip `workshop/status.md` to `turn: orchestrator`, append one line to `workshop/log.md`, commit `[implementer] 04a: deck fixes (heating, texts, driving question, budget)`, push, comment `report 04a ready` on pull request #1. Stop and report.
