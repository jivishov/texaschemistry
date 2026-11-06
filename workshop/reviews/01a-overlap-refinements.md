# Review 01a: Overlap measurement refinements, the motion-on pass, the reference-deck baselines, two stale texts

Step: 01a · Report: `reports/01a-overlap-refinements.md` (in-session agent run of brief 01a, interrupted once by the account's usage limit and resumed with its work intact) · Verdict: **accepted**. Step 02 (the animations and the deck) is released.

## Verified by the orchestrator (not from the report)
1. `git status --short`: `README.md`, `audits/layout.js`, `registry.json`, `split_parts.py` modified; `parts/lessons/4-1/overlap-baseline.json` and `4-2/overlap-baseline.json` new; `workshop/artifacts/01a/` (444 KB, text and twelve JPEG crops) and the report new; nothing under `unit4/` or `unit5/`. Diff against 1ff2f97: four kit files, +224/−89, no shared part, no other audit.
2. `python3 build.py --all` run here: 4.1 `ebd342f1…`, 4.2 `c3fa219a…`, both unchanged; `git status` clean under `unit4/`.
3. The two baseline files read: 4.1 60 entries on s10f1 to f9 (at rest and at both live moments), s16f3 to f5, s17f4 to f6; 4.2 30 entries on s15f0 to f9 (rest and both live moments); each entry exactly frame, A and B strings; the registry names both files; the README says a new deck gets none.
4. `suite.py 4 1 --only layout --theme light` and `4 2` re-run here: 4.1 PASS, 158 intersections on 32 frames, all 158 baselined (60 entries, 1 stale), 0 outside the baseline, 6 covered labels, 13 spheres scenes, 10 of 10 canvas animations instrumented, 14 live frames at two moments; 4.2 PASS, 30 baselined of 30 (0 stale), 5 covered labels, 30 scenes, 14 of 14 instrumented, 10 live frames. Identical to the report.
5. The two stale texts fixed as the brief says (README `keys_cfg` row; `split_parts.py` docstring with `css-51`).
6. Crops viewed: `4-1-s17f4` (the digit "1" sits inside its small ring: the em-box height alone flags it), `4-2-s15f0` (the charge badge covers the dashed "one unit" ring: hidden, not visible), `4-1-s16f3` (the enlarged Na cell covers parts of Li, Be, Mg and K: real), `4-1-s10f1` to `f4` (electron balls over the core labels and "sodium": real).
7. The refined measurement matches brief 01a: discs as discs, inline text as part of its block (every DOM hit of step 01 gone), `D.spheres` scenes by depth, covered labels counted and not failed, the motion-on pass at 1.4 s and 2.4 s on live frames, the baseline matched by strings with stale entries reported; the gate without a baseline still fails on every hit (the refined runs did).

## Findings
- **F1 (for the teacher, unchanged from review 01 F5).** The real overlaps of 4.1 (slide 10: electron balls over "+", "2+", "3+" and "sodium"; slide 16: the enlarged cell cutting Li, Be, Mg, K and others) are now listed, one entry each, in `parts/lessons/4-1/overlap-baseline.json`. A fix round on 4.1 would change its md5 and re-run its suites and matrix in step 03; the orchestrator does not order it without the teacher's word.
- **F2 (later, step 03 or a kit round).** A label's height is the font's em box; glyphs are shorter, so a digit inside a small stroke-only ring (4.1 slide 17) counts as a cut. Using the glyph box (`measureText`'s `actualBoundingBoxAscent` and `Descent`) would remove that class. Left for step 03 unless the 5.1 bench runs into it; brief 02 tells the implementer to report such a hit as an open question rather than redraw around it.
- **F3 (no change).** A shape segment hidden under a later opaque shape (4.2 slide 15's ring under the badge) is not a visible overlap and stays baselined; 5.1's drawings place badges beside rings, not on them.
- **F4 (design rule for 5.1).** Live moments are sampled at two arbitrary times, so a live stage must keep its labels clear of shapes at every moment, not only at rest; brief 02 says so (the counter, the cascade and the clock move numbers inside their own boxes).
- **Deviations 1 to 8 accepted**: a badge's own label not tested against its own disc (the em box would fail every small badge by under 1 px); baseline entries matched as a set of strings; the baselines as the union of several runs; the baseline file as an object; `inline-flex` and `inline-grid` as `inline-block`; gradient opacity from the stops through a test-time wrapper; `walk` first so that `xcheck` finds its input; covered and scene counts including the live moments.

## Decisions on the open questions
1. The fix of 4.1 is the teacher's decision (F1).
2. Glyph-box label height: step 03 or a later kit round (F2).
3. Hidden shape segments: no rule change (F3).
4. Live moments: two moments stay; the deck is designed so that no moment can collide (F4).

## Next
Brief 02: the eleven animations on the bench, then the 28-slide deck.
