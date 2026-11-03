# Review 01: Kit check and generalization

Step: 01 · Report: `reports/01-kit-check.md` (commit `3816b51`) · Verdict: **accepted**, with three kit follow-ups folded into brief 02 (none blocks the animation work).

## Verified by the orchestrator (not from the report)
1. `git pull --ff-only`; `git status --short` empty at `3816b51`.
2. md5 and size of `unit4/slides-4-1.html` (`ebd342f1…`, 194,646 bytes), `unit4/slides-4-2.html` (`c3fa219a…`, 203,769 bytes), `unit4/blueprint.html` (`ed3bf8e2…`, 44,978 bytes): equal to the base. `git diff --stat base..HEAD` touches only `tools/slides-kit/**` and `workshop/**`.
3. `python3 build.py --all` run here: both decks rewritten byte-identical (same md5s), `git status` still empty.
4. The rename-aware diff of every moved audit read in full: `walk`, `back`, `fonts`, `readability`, `print`, `render3d`, `supgap`, `click`, `layout` unchanged; `lib`, `keys`, `extras`, `timing`, `contact`, `zoomsheet` take their configuration from the environment and refuse to run without it; `units`, `cycle` take the slide range from `SLIDES` and now set an exit code (a tightening); `xcheck` takes decks, blueprint, objectives and mentions from `XCHECK` with the assertions word for word; `zoom` selects the explicit lists by `LESSON` (see follow-up 1); the two `chem.js` files only change their `require` path; the generators only change their output file name; the head only gains the two placeholders; `split_parts.py` generalizes the CSS marker. No assertion loosened, no gate changed.
5. `build.py` and `suite.py` read in full: five markers from the registry, placeholders asserted to appear exactly twice, CSS insertion identical to `build42.sh`, repo root from the kit's location, scratch builds and suite outputs refused inside the repo, exit 1 on any failure, contact and zoom sheets counted.
6. No absolute path left in the kit (`grep` for the old roots finds only the handoff, which says so in its first line).
7. `python3 build.py 4 2 --scratch --out <scratchpad>/scratch42.html`: md5 `990dd279…`, as reported; `EMPTY_MAX=1 python3 suite.py 4 2 --deck … --only walk --theme light`: PASS, 127 states, max empty 70% (s4f1), as reported.
8. `python3 suite.py 4 2 --only walk,timing,chem,xcheck --theme light` re-run here: walk PASS (173 states, max empty 32% at s10f1), chem PASS (39 checks), timing PASS (47 and 46.5 min), xcheck PASS (40 of 40); as reported.
9. Artifacts under `artifacts/01/`: text only, 1.7 MB, 86 files; `md5.txt`, `xcheck-old-vs-new.txt` and `suite-all.txt` read; the suite summary (4.1 22 of 22, 4.2 24 of 24, matrix off) matches the report.

## Findings
- **F1 (follow-up).** `zoom.js`: with `LESSON` the explicit checks are now per lesson, and a lesson without a list gets none. Two of the old entries are generic and must hold for every deck: "every zoomed check shows its options" (4.1 A1; 4.2 has the same with a count) and "every prompt on the routine slides is a unit". A new deck must not lose them, and the per-lesson lists need a home outside `audits/`. Brief 02 item K1.
- **F2 (follow-up).** `keys.js` asserts a 180 s timer on frame 1 of the `tm` slide (`a.timer.sec===180`, text `2:5x`, restart `3:00`). The 4.5 plan has no slide with a 3-minute timer on frame 1 (its you-do timers are 90 s and sit mid-slide). The assertion should read the frame's own timer value; the behavior checked (runs, stops on leaving, restarts on return) stays. Brief 02 item K2.
- **F3 (follow-up).** The 4.5 registry entry needs the slide ids for `keys_cfg` and `extras_cfg` (report open question 2). Decided for brief 04 from the plan: `cr` a slide whose frames 0 to 2 stage one animation and whose frame 3 shows a unit with an id (slide 12, `iceLattice`); `tm` the you-do slide with the timer the deck gives it (follow-up F2 makes that legal); `ex` slide 3; `hk` slide 2; `extras.hash` slide 12 frame 0 with its canvas, `block` the line revealed on its frame 1, `slides` 27. Written into brief 04, not now.
- **Deviations 1 to 7** of the report accepted: registry fields `css` and `extra_slides`; exit codes for `units` and `cycle`; per-deck xcheck with the matrix-row assertion labelled per deck (the 80 deck assertions identical to the old run, checked in `xcheck-old-vs-new.txt`); `--deck` skips xcheck; the two in-repo guards; sheets counted toward the exit code; fonts in dark with `--theme dark`.
- **Deviation 8 (the implementer could not subscribe to pull request #1).** Cause: this platform delivers a pull request's events to one session at a time, and the orchestrator's session holds the subscription. Decision: the orchestrator keeps it (reviews wake at once); the teacher starts account B with its start line after each `brief NN ready`, as START.md already provides for. The implementer does not retry.

## Decisions on the open questions
1. **Scratch decks and the emptiness gate.** Scratch runs set `EMPTY_MAX=1` for `walk` and `layout` only; every other gate stays. The deck step runs with the default gate.
2. **keys and extras need deck features.** See F2 and F3.
3. **Unit and lesson placeholders in the head.** Not needed; the head uses nothing else. KIT.md's wording stays as it is (the orchestrator does not change KIT.md without the teacher's word); the README documents the two placeholders that exist.
4. **Handoff blueprint numbers.** History; left as moved.

## Next
Brief 02: the six period-1 animations on scratch slides, with the three kit follow-ups (K1 to K3) done first and proved on 4.1 and 4.2 by their zoom and keys audits.
