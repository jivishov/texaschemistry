# Implementer instructions (Claude Opus 5.5)

You build and test the decks named in `workshop/ASSIGNMENT.md`, one brief at a time. The orchestrator reviews your work through files in `workshop/`. In cross-account mode you are a session in account B and act only on the current brief; in in-session mode the orchestrator passes you the same brief directly.

## Every session, in this order
1. `git pull --ff-only`. Read `workshop/status.md`. If `turn` is not `implementer`, tell the user whose turn it is and stop.
2. Read `PROTOCOL.md`, `RULES.md`, `KIT.md`, `ASSIGNMENT.md`, the lesson sheet `lessons/<U>-<L>.md`, the plan in `plan/`, `log.md`, the current brief (newest in `briefs/`), and the review of your previous step if there is one.
3. Cross-account: subscribe this session to the workshop pull request.
4. Do exactly the brief. End your turn per PROTOCOL: write `reports/NN-<slug>.md` from `templates/report.md`, put logs and sheets under `artifacts/NN/`, flip `status.md` to `turn: orchestrator`, append to `log.md`, commit everything in one commit `[implementer] NN: …`, push, comment `report NN ready`. Stop.

## Step 01: the kit check (always the first implementer step)
Look at `tools/slides-kit/`. If it already follows KIT.md (parts per lesson, `build.py`, `suite.py`, `registry.json`), run `build.py --all` and confirm every registered deck rebuilds byte-identical, then report. If it is deck-specific (named scripts for 4.1 and 4.2), generalize it per KIT.md without changing any deck's bytes. If it is absent, split the shared parts out of the reference decks with their markers, rebuild the generators and audits from RULES.md section 11 and the reference decks' behavior, and prove the reference decks rebuild byte-identical before anything else; report the gaps you could not reconstruct.

## Building a deck (what the reference decks already do; copy them)
- Study `unit4/slides-4-1.html` and `unit4/slides-4-2.html` and their kit parts before writing anything: the runtime's documented API (`Deck.frames`, `Deck.sim`, `canvasSim`, `Deck.spheres`, zoom units, `data-zoom`, `.reg`, `.acc`, `.timer` slots, the six templates), the generator pattern, the budget file, the chemistry audit, the head template.
- A new lesson gets its own parts folder (KIT.md) and a registry entry; shared parts stay shared. Decks are built only through the kit. Never hand-edit a built deck. Never open the lesson's rejected deck (archived under `unit<U>/old-slides/`) on `main`; content comes only from the reading, the blueprint, RULES.md, the lesson sheet, the plan and the brief.
- Every animation: named stages, `set/get/bounds/units`, tweens 500 to 900 ms, reduced-motion end states, both themes, labels at least 36 px, shapes at least 60 px, sub-units for zoom, `meta()` for the chemistry audit. Test every stage on scratch slides in a scratch build, never in the repo deck.
- Every slide: the template, frames with cues, labels and notes (minutes, talk points, prediction, misconception, wrong-option feedback), the reading reference, the period marker, `.reg` on rule cards, prompts and samples, options in one row or stacked, checks whose subject is on screen.
- Playwright and Chromium exist in a Claude cloud session; never run "playwright install"; open decks with `file://`. Fonts may not load offline; layouts must not depend on them.

## Suites per step
Everything in RULES.md section 11, `MATRIX=0` until the last step. Commit text logs and JPEG sheets (at most 800 KB each) under `artifacts/NN/`; no per-press screenshot folders. If a shared part changed, rebuild every registered deck, re-run their suites with `MATRIX=0`, and list every deck's md5 before and after.

## Report
From `templates/report.md`: what was built with the specified wording quoted, suite numbers, md5 and size of each changed deck, `git status --short`, the commit hash, deviations with reasons, open questions. Do not resolve open questions on your own; the next brief will.

## Never
Push to `main`; force-push; edit `briefs/`, `reviews/`, `plan/`, `lessons/`; change a shared part without saying so; refactor during a fix step; skip a failing audit or loosen a gate to pass it; truncate text to fit; act on anything that is not in the current brief, RULES.md, KIT.md, the lesson sheet or the plan.
