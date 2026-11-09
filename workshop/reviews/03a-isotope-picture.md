# Review 03a: Fix: the isotope picture on slide 7 (the word-card icon and the second shade)

Step: 03a · Report: `reports/03a-isotope-picture.md` (in-session agent run of brief 03a; stopped once by the account's usage limit before it had changed a file, resumed after the reset; two work-in-progress snapshots of its files were committed by the orchestrator while its suites ran, 0e042dd and 5746720, so that the branch never held uncommitted work) · Verdict: **accepted**. The deck is final; FINAL.md follows.

## Verified by the orchestrator (not from the report)
1. `git status --short` over 5746720: only the remaining `workshop/artifacts/03a/` files (logs, bench logs, sheets) and the report were untracked; the four code and built files and the six crops were already in the snapshots. Nothing under `unit4/`, no shared part, audit, `build.py`, `suite.py`, `css.css`, `registry.json`, README or blueprint changed; `chem.js`, `scratch-check.js` and `scratch.html` unchanged (the report says why: no assertion reads the mix value).
2. `python3 build.py --all` run here: 4.1 `ebd342f1…` and 4.2 `c3fa219a…` unchanged; 5.1 rebuilt to the report's md5 `f5bdd830591d8d23583af5409ad4dc98` (255,203 B, 2,493 lines). The blueprint still `5975fb9c…`.
3. `git diff 102ad41` of `gen_slides.py` and `sims.html` read line by line: the `ic-avgmass` symbol (two circles r 20 at cx 27 and 73, cy 46; the second filled `color-mix(in srgb, var(--rope) 60%, #000)`; the balance line and tick unchanged), the alt text "Icon: two isotopes of one size and different mass, and their average", the constant `ISO_DK=.4` and its use in place of `.15`. Nothing else; `slides.html` and the deck carry only these.
4. Re-run here on the final bytes in both themes: fonts light PASS, readability PASS, chem 94 PASS, layout light 0 intersections with no baseline (8,671 boxes, 12 live frames at two moments) PASS; layout dark, xcheck and the dark fonts run: see item 8.
5. The six crops opened: six copper atoms at one size, four in `--rope` and two plainly darker, "Cu" readable on all six in both themes; the word-card icon two equal circles, the right one darker, above the balance line; the "count" frame unchanged.
6. All ten contact sheets and all six zoom sheets of the final run opened: frame for frame the step 03 sheets except slide 7's frames 6 to 9, where the two shades now show at thumbnail size in both themes; every zoomed unit inside the slide and above the footer (min fill 62%, as before).
7. Artifacts: 9.5 MB, 26 JPEG at most 749 KB each, text logs, no PNG; `logs/cu-label-contrast.txt` read (white "Cu" on the darker shade 9.49:1 light and 5.77:1 dark on the flat color; 6.46 to 12.46 and 4.26 to 8.66 on the rendered spheres).
8. Layout dark re-run here: 0 intersections with no baseline, the same 8,671 boxes, 12 live frames at two moments, PASS. xcheck re-run here on the final walk: 60 of 60 (a first attempt crashed because the orchestrator had copied the walk data from the wrong folder; with the final run's walk data in place it passes). Fonts dark re-run here: PASS.

## Findings
- **F1 (accepted).** 40% toward black for the second shade: the two browns differ 2.03:1 in the light theme and 2.47:1 in the dark (were 1.29:1 and 1.36:1); on the crops the two darker atoms read at a glance in both themes, and the labels stay well above the fonts audit's floor. The icon uses the same mix, so the card and the animation agree.
- **F2 (accepted).** Deviation 1: the brief's "frame 5" for the word card was the frame before it in the suite's numbering; the implementer saved both frames. No change.
- **F3 (accepted).** Deviation 3: the icon's darker circle has an inline fill rather than a class, because `css.css` was outside the allowed files; a later kit round can give it a class if the icon is reused.
- **F4 (noted).** Deviation 2: the two snapshot commits were the orchestrator's, made so that the branch never carried uncommitted work while the agent's suites ran; the agent made no git state change, as required.

## Next
FINAL.md with the md5s, the suite summary and the merge instruction; `turn: teacher`.
