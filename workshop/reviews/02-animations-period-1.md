# Review 02: Period-1 animations on scratch slides, kit follow-ups K1 to K3

Step: 02 · Report: `reports/02-animations-period-1.md` (commit `1202db2`) · Verdict: **accepted**, with six fix items (M1 to M6) placed at the head of brief 03 so the period-2 work and the fixes ride one turn; the deck step (04) does not start before every M item is confirmed.

## Verified by the orchestrator (not from the report)
1. `git pull --ff-only`; `git status --short` empty at `1202db2`; `unit4/` identical to the base (`git diff --stat` empty); 4.1 `ebd342f1…` and 4.2 `c3fa219a…` unchanged; no shared part changed.
2. The step's kit diff read in full: `zoom.js` now runs the two generic checks for every deck and loads the lesson list from `ZOOM_CHECKS`; the 4.1 and 4.2 lists in `parts/lessons/4-1/zoomchecks.js` and `4-2/zoomchecks.js` are the old entries word for word, minus the two generic ones (the 4.2 count half kept, as the report says); `keys.js` reads the `tm` slide's own timer and keeps its three assertion names; `suite.py` sets `EMPTY_MAX=1` for walk and layout on a scratch deck only; the 4.5 registry entry is as brief 02 asked. K-proof logs: 4.1 zoom light and dark PASS (571 states, explicit 11), 4.2 zoom PASS (707 states, explicit 14), keys 48 checks PASS on both with the timer text "2:58, expected 2:57 to 2:59".
3. `python3 build.py 4 5 --scratch --out …` here: md5 `e1aa2f76…`, as reported; `scratch-check.js` here: 73 of 73 PASS; a light walk here: 47 states PASS (max empty 75% at s6f0 with the gate off).
4. All four sheets opened (`contact-scratch45-light.jpg`, `-dark.jpg`, `reduced-motion-end-states-light.jpg`, `-dark.jpg`): every stage of every instance present, dark theme tokens right (electrons yellow on dark as in 4.1), reduced-motion end states correct. Seven frames regenerated at full size (melt scale, three-row solids, dispersion flicker, hydrogen bond pair, the four hydrogen bonds, the plot at `reveal`).
5. Every label, caption, chip and box text read against `lessons/4-5.md`: values (−188.1, −34.0, 58.8, 184.4, −161.5, −33.3, 100.0, −85.1 °C; 18, 34, 70, 106, 10 electrons; 0.0, 801, near 1700 °C; Br 2.96, H 2.20, 0.76; 102 and 181 pm, 282 pm; 5 to 10%), δ signs (H δ+, Cl δ−; H δ+, Br δ−; N δ−), lone pairs (two on O, one on N, none on C), the hydrogen bond from an H to a lone pair and drawn longer than the O–H stick, the four hydrogen bonds of water (two given, two received), the Cl₂ sticks and dashed attractions, the triplet-1 wording. All correct, every sentence 14 words or fewer, no ellipsis character in `sims.html` or `scratch.html`, no clipped or edge-cut text (layout PASS, `outText` 0).
6. Artifacts: text logs plus four JPEG sheets under 800 KB; no per-press folders; 2.2 MB.

## Findings
- **F1 (fix, RULES 3).** Shapes under 60 px: the water hydrogens in the melt scale's snow panel (40 px), the oxygens of its Si–O fragment (about 44 px), the snowman icon (head 36 px, the whole icon about 100 px tall). The implementer reported them (Deviation 5, open question 1). Dots, badges and plot markers are exempt as in 4.1 and 4.2 (electron dots 22 to 26 px there); spheres that stand for atoms or ions are not. Fix M1: the melt scale is laid out again (icon row above three equal panels; three water molecules at full size instead of a six-ring; a smaller Si–O fragment; icons at least 120 px tall) and reports its smallest atom or ion sphere in `meta()`.
- **F2 (fix).** `bpPlot` at `reveal`: the faint Cl₂ marker sits under the "−" of "NH₃ −33.3 °C" and the faint F₂ marker touches the "CH₄" label; readable, but a label over a marker reads as a smudge from the back row. Fix M4: labels get a halo in the slide background and faint markers draw beneath labels.
- **F3 (fix, small).** Dispersion `flicker`: the δ+ and δ− badges float at the top of the host, 50 px above the cloud; they should sit on the cloud's two ends. Fix M5.
- **F4 (accepted).** `threeSolids` three-row layout: the back Na⁺ of the 3D salt block at 46 px by perspective; the nearest Na⁺ is about 65 px and Cl⁻ about 110 px. Accepted with the rule that the nearest sphere of each kind is 60 px or more; M6 asks for that measurement in the report.
- **F5 (accepted).** Deviations 1 to 4, 6, 7 and 8 of the report: the routine-prompt check over routine slides that carry a prompt; the 4.2 count half kept; `LESSON` dropped; bench captions as non-units; the `attractions` foot captions (wording accepted as written); the "Not needed." box; the `hidden` attribute for the other drawings.
- **F6 (accepted, guarded).** Deviation 9: `build.py --all` wrote a placeholder `unit4/slides-4-5.html` once (untracked, deleted at once, not committed, the archived deck untouched). Fix M3 adds a registry flag `built: false` so `--all` skips 4.5 until step 04; no further `--all` runs write anything for 4.5.

## Decisions on the open questions
1. Shape floor: F1, F4 (M1, M6).
2. Caption "Atom colors show the element, not the charge" on slide 3: yes, in the slide's DOM; plan section 3 updated.
3. The three solids of slide 3 appear one per press: `meltScale` gets the cumulative stages `snow`, `salt`, `sand` before `melt` and `numbers` (M1); plan section 4 and slide 3 updated.
4. `forceDecider` gets an `empty` stage (M2); plan section 4 and slide 10 updated.
5. `keys_cfg` and `extras_cfg` for 4.5: brief 04, as review 01 F3 says.
6. Registry flag `built` (M3); plan section 9 updated.

## Next
Brief 03: M1 to M6 first, proved on the scratch deck and the reference decks; then the five period-2 animations (`heating`, `iceLattice`, `conductTester` with its dissolve family, `hammerBlow`, `networkVsMolecules`) on the same bench.
