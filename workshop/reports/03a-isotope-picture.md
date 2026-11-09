# Report 03a: Fix: the isotope picture on slide 7 (the word-card icon and the second shade), the final suites again

Step: 03a · Lesson: 5.1 · Commit: none by the implementer (in-session; no git state change by the agent). While the suites ran, two work-in-progress snapshot commits appeared on the branch from outside this agent: `0e042dd` (the four source and built files below) and `5746720` (the six crops and `logs/cu-label-contrast.txt`). This report describes the working tree over `102ad41`.

## Done
Only lesson parts under `tools/slides-kit/parts/lessons/5-1/` were edited by hand; `slides.html` and the deck were written by the build.

**A1. Icon `ic-avgmass`** (`gen_slides.py`, symbol in the sprite). Before: `<circle cx="28" cy="46" r="18" class="f-rope"/>` and `<circle cx="72" cy="42" r="24" class="f-rope" style="filter:brightness(.82)"/>`. After: `<circle cx="27" cy="46" r="20" class="f-rope"/><circle cx="73" cy="46" r="20" style="fill:color-mix(in srgb,var(--rope) 60%,#000)"/>`. One radius (20 in the 100 × 100 viewBox, between the old 18 and 24), side by side with a 6-unit gap, bottoms at y 66; the balance line (`M8 80h84`, stroke 5, so its top edge at 77.5) and the tick (`M50 70v20`) are unchanged and not touched by either circle. The darker circle (right, as the heavier one was before) uses `color-mix(in srgb, --rope 60%, #000)`: the same 40% mix toward black as the canvas (`D.mix` interpolates in sRGB, so the two agree exactly). Computed fills read in the deck: light `rgb(155,106,44)` and `color(srgb 0.3647 0.2494 0.1035)` = (93,64,26) = #5d401a; dark `rgb(209,161,94)` and (125,97,56) = #7d6138: identical to the canvas shade in each theme (`logs/crops.log`). `color-mix` was picked over `filter: brightness(...)` because it gives the canvas color exactly in both themes; the inline style needs no CSS change (`css.css` not touched). The svg measures 124.8 px at 1920 × 1080 (104 px on the 1600 canvas); the card's text did not move.
Alt text: "Icon: two isotopes of one size and different mass, and their average".

**A2. Second shade of `centJar` stage `isotopes`** (`sims.html`). New constant beside `ISO_R`: `const ISO_DK=.4; /* the heavier isotope's shade: --rope mixed 40% toward black (review 03 F2); the icon ic-avgmass uses the same mix */`, and the two `dk` atoms now use `D.mix(rp,'#000000',ISO_DK)` (was `.15`). Radius 46, the `lt` and `dk` positions, the 44 px label size, the "isotopes" label and the frame note are unchanged. Shades: light #9b6a2c and #5d401a (luminance contrast between the two 2.03:1; at 15% it was 1.29:1); dark #d1a15e and #7d6138 (2.47:1; was 1.36:1). 40% was chosen from 35/40/45% (computed 1.85/2.03/2.24 light, 2.17/2.47/2.80 dark) and judged on the crops: at 40% the two darker atoms read at a glance in both themes, and the "Cu" label keeps clear contrast in the dark theme without making the dark atom near-black in the light theme.

`chem.js` and `scratch-check.js`: no assertion reads the mix value (they check 6 atoms, 1 size, 2 shades and one instrumented radius), so neither changed. `scratch.html` was regenerated identical by `gen_scratch.py`. `docs/handoff-5-1.md` names no mix value ("six Cu atoms, one size, two shades" stays true), so it was not changed.

**A3.** No other text, note, stage, shared part, blueprint or README changed.

## Verification
**C1. Builds.** `python3 tools/slides-kit/build.py 5 1`: `5.1: unit5/slides-5-1.html  255203 bytes, 2493 lines, md5 f5bdd830591d8d23583af5409ad4dc98`. `build.py --all`: `4.1 ... 194646 bytes, 2077 lines, md5 ebd342f1ee0e11c47157141cf3b2a59b`, `4.2 ... 203769 bytes, 2153 lines, md5 c3fa219a806963f9a66c3baf643153f4` (both unchanged), 5.1 as above (logs `build-51.txt`, `build-all.txt`).

**C2. Bench.** `build.py 5 1 --scratch --out <scratchpad>/fix03a/scratch51.html`: 188,949 bytes, 2,336 lines, md5 0a4c3650589b9a73984c7b35ff2cd65f. `scratch-check.js`: **`scratch-check 5.1: PASS 348 assertions`**, 0 FAIL; the isotope lines: `centJar:isotopes: labels at 36 px or more (painter minFont 36)`, `primary shapes at 60 px or more (smallest 92)`, `six Cu atoms at one size in two shades`, `the painted spheres (instrumented discs) all have one radius`. `suite.py 5 1 --deck <scratch> --only walk,layout --theme both`: **`== 5.1: 4 of 4 pass, 0 fail, 258.1 s`**; walk light and dark 78 states PASS; layout light and dark 78 frames, clipped 0, **overlap 0 intersections on 0 frames, no baseline** (3,998 boxes, 78 of 78 canvas animations instrumented, live 7 frames at two moments). Logs in `logs/bench/`.

**C3/V1. Deck suite** `suite.py 5 1 --theme both --out <scratchpad>/fix03a/final` (no matrix): **`== 5.1: 23 of 23 pass, 0 fail, 1678.8 s`**.

| Audit | Result | Time | Verdict line |
|---|---|---|---|
| walk light | PASS | 240.8 s | walk light: 197 states, max empty 26% (s14f8), PASS |
| walk dark | PASS | 241.5 s | walk dark: 197 states, max empty 26% (s14f8), PASS |
| back light | PASS | 96.9 s | back: 197 forward, 197 back, PASS |
| back dark | PASS | 97.0 s | back: 197 forward, 197 back, PASS |
| fonts light | PASS | 56.7 s | fonts: PASS |
| fonts dark (separate run) | PASS | 56.6 s | fonts: PASS (`== 5.1: 1 of 1 pass, 0 fail, 56.6 s`) |
| keys | PASS | 37.5 s | keys: PASS 48 checks |
| readability | PASS | 3.1 s | readability: PASS |
| print | PASS | 2.1 s | print: PASS stage hidden=true, 28 slides, 197 frame lines, 11 PDF page(s) |
| render3d | PASS | 2.4 s | render3d: PASS |
| extras | PASS | 5.6 s | extras: PASS |
| chem | PASS | 2.1 s | chem51 (deck): PASS 94 checks |
| timing | PASS | 1.3 s | timing: period 1 43.75 min, period 2 46 min, PASS |
| supgap | PASS | 5.8 s | supgap: 107 symbol+charge pairs checked, PASS |
| zoom light | PASS | 359.4 s | zoom light: 1072 zoomed states over 197 frames (re-flow 458, transform 614), …; min fill 62%; Back tests 28; PASS |
| zoom dark | PASS | 358.1 s | zoom dark: 1072 zoomed states over 197 frames (re-flow 458, transform 614), …; min fill 62%; Back tests 28; PASS |
| click | PASS | 34.0 s | click: 11 graded checks, 3 Predict-now questions, 55 assertions, PASS |
| layout light | PASS | 57.5 s | layout light: 197 frames, 28 visible option lists (stacked 19, row 9), max empty 26% (s14f8), gate 33%, clipped or ellipsized text: 0, overlap: 0 intersections on 0 frames, no baseline (8671 boxes (2603 DOM boxes, 2173 canvas labels, 3895 canvas shapes), 210 covered canvas labels, 85 spheres scenes (live moments included), 16 of 16 canvas animations instrumented), live: 12 frames at two moments, PASS |
| layout dark | PASS | 58.4 s | layout dark: (the same numbers as light), live: 12 frames at two moments, PASS |
| xcheck | PASS | 1.5 s | xcheck: 60 of 60 pass |
| contact light | PASS | 5.3 s | contact-light-1.png (94 shots), -2.png (102 shots), -3.png (1 shot) |
| contact dark | PASS | 5.3 s | contact-dark-1.png (94 shots), -2.png (102 shots), -3.png (1 shot) |
| zoomsheet light | PASS | 3.3 s | zoomsheet-light-1.png (102 shots), -2.png (7 shots) |
| zoomsheet dark | PASS | 3.2 s | zoomsheet-dark-1.png (102 shots), -2.png (7 shots) |

`overlap-light.txt` and `overlap-dark.txt`: "no intersections, 197 frames, 8671 boxes (2603 DOM boxes, 2173 canvas labels, 3895 canvas shapes); 210 covered canvas labels, 85 spheres scenes (live moments included); live: 12 frames at two moments". Every number equals step 03's (the change moves no box).

**V2.** `scratch-check 5.1: PASS 348 assertions`; `chem51 (deck): PASS 94 checks` (the isotope line: "slide 7 centJar isotopes: the table's average mass, no isotope masses; six Cu atoms at one size in two shades"). Counts unchanged from step 03, as no assertion was added or changed.

**V3. md5s**

| File | Before | After |
|---|---|---|
| `unit5/slides-5-1.html` | 3c86da493034ed29c283551925ea3b30 (255,040 B) | f5bdd830591d8d23583af5409ad4dc98 (255,203 B, 2,493 lines) |
| `unit4/slides-4-1.html` | ebd342f1ee0e11c47157141cf3b2a59b | ebd342f1ee0e11c47157141cf3b2a59b (unchanged) |
| `unit4/slides-4-2.html` | c3fa219a806963f9a66c3baf643153f4 | c3fa219a806963f9a66c3baf643153f4 (unchanged) |
| `unit5/blueprint.html` | 5975fb9cdfa6f57cef0cdb26a5f623be | 5975fb9cdfa6f57cef0cdb26a5f623be (unchanged) |

The deck differs from 3c86da49… in four lines: the `ISO_DK` constant, the `dk` atoms' color, the `ic-avgmass` symbol and the `#s07-word` aria-label.

**V4. Artifacts** (`workshop/artifacts/03a/`, 9.5 MB, JPEG and text only, no PNG, none over 800 KB):
- `sheets/`: `contact-light-1-1.jpg` … `contact-light-3-1.jpg` and `contact-dark-*` (5 each; each tall sheet cut at a blank row into two), `zoomsheet-light-1-1`, `-1-2`, `-2-1` and the same for dark; 40 to 749 KB. These are the final sheets.
- `logs/`: every audit log of the final run (`walk-light.log` … `zoomsheet-dark.log`, `fonts-light.log`, `fonts-dark.log` from the separate run), `suite-final.txt`, `suite-fonts-dark.txt`, `overlap-light.txt`, `overlap-dark.txt`, `xcheck.log`, `chem.log`, the three build logs, `crops.log` (icon fills and sphere stats as read in the deck), `cu-label-contrast.txt`; `logs/bench/`: `bench-suite.txt`, its walk and layout logs, its two overlap files and `scratch-check-51.log`.
- `crops/` (1920 × 1080 full frames, reduced motion, 184 to 213 KB): `s07f7-isotopes-light.jpg` and `-dark`; `s07f6-word-light.jpg` and `-dark` (the word card); `s07f5-count-light.jpg` and `-dark` (see Deviation 1).

**V5. Mix values and label contrast.** Icon: `color-mix(in srgb, var(--rope) 60%, #000)` (40% toward black). Canvas: `D.mix(--rope, #000, 0.4)` (`ISO_DK=.4`). "Cu" label on the darker shade (white in both themes; the painter picks white below luminance 0.3): against the flat shade 9.49:1 light (#5d401a) and 5.77:1 dark (#7d6138); measured on the rendered spheres (four samples just outside the glyphs, on the sphere's gradient; `cu-label-contrast.txt`): light 6.46 to 12.46, dark 4.26 to 8.66 (lowest at the highlight above the label). For comparison the lighter shade's labels: light white 3.64 to 7.32, dark ink 4.17 to 8.19 (unchanged from step 03).

## Repo state
- `unit5/slides-5-1.html` 255,203 bytes, md5 f5bdd830591d8d23583af5409ad4dc98 (built by `build.py 5 1`, never hand-edited); 4.1, 4.2 and the blueprint unchanged (table above).
- Changed against `102ad41`: `tools/slides-kit/parts/lessons/5-1/gen_slides.py`, `sims.html`, `slides.html` (built), `unit5/slides-5-1.html` (built); new `workshop/artifacts/03a/` and this report. `chem.js`, `scratch-check.js`, `scratch.html`, `css.css`, `docs/handoff-5-1.md`, shared parts, audits, `build.py`, `suite.py`, `registry.json`, README, `workshop/status.md`, `workshop/log.md` unchanged.
- `git status --short` (over `5746720`, the second outside snapshot, which already holds the four code files, the crops and `cu-label-contrast.txt`), before this report was written: `?? workshop/artifacts/03a/logs/…` (every log listed in V4 except `cu-label-contrast.txt`, plus `logs/bench/`) and `?? workshop/artifacts/03a/sheets/`; this report adds `?? workshop/reports/03a-isotope-picture.md`.

## Deviations
1. **The word-card crop is frame 6, not frame 5.** In the suite's numbering (0-based, the same that names `s07f7` for `isotopes`), slide 7's frames are jar, (note), wrong, sample, average, count, word, isotopes, …: frame 5 is "count" (cue "Next ▶ new word") and the word card `#s07-word` first shows on frame 6. Both are in `crops/` (`s07f5-count-*` as named by the brief, `s07f6-word-*` with the card); the icon also shows on the `s07f7-isotopes-*` crops.
2. **Two commits appeared on the branch during the run** (`0e042dd`, `5746720`, "[implementer] 03a: work-in-progress snapshot …"), not made by this agent, which made no git state change. They hold exactly the four changed source/built files and the crops plus contrast log as they stood at the time; the files have not changed since.
3. The icon's darker circle has no `f-rope` class (the inline `fill` sets its color); `css.css` is outside the allowed files, so no class was added.

## Open questions
None.
