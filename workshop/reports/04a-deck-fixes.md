# Report 04a: Deck fixes from review 04

Step: 04a · Lesson: 4.5 · Commit: the commit `[implementer] 04a: deck fixes (heating, texts, driving question, budget)` on `workshop/unit4-5-6`, parent `d28c37f` (its hash is in the pull-request comment `report 04a ready`)

## Done
1. **`heating` with four CH₄ molecules (2 × 2); water unchanged at six (2 × 3).**
   - `sims.html`: a molecule count per substance (`HT_N`) and attraction pairs per substance.
   - The methane solid is a 2 × 2 block at 166 × 206 px, turned −30°, 2 px between neighbours' atoms. The gas puts the four at the container's corners.
   - Readouts: "Covalent bonds: 16 of 16 intact" (water "12 of 12"). Attractions drawn: CH₄ 4, 2, 2, 1, 0; H₂O 7, 1, 0. `meta().molecules` is 4 for CH₄, 6 for H₂O.
   - Measured on the 733 × 519 px container, the same on the bench and in the deck:

     | | solid block | area per molecule | nearest neighbours |
     |---|---|---|---|
     | CH₄ | 40% (39.8) | 2.78 times (34,196 → 95,107 px²) | 166 → 256 px |
     | H₂O | 32% | 3.48 times | 98 → 248 px |

   - `scratch-check.js` and `chem.js` keep the two thresholds (40%, 2.5) for both substances and now pass.
   - Proof:
     - bench: `scratch-check 4.5: PASS 150 checks` (`artifacts/04a/bench/scratch-check.txt`);
     - deck: `chem45 (deck): PASS 156 checks`;
     - `artifacts/04a/d1-heating-CH4-solid-gas.jpg` (bench frames `CH4/solid` and `CH4/gas`).
   - Consequence: slide 11's teacher notes and the animation's aria label said "24 of 24" and "six"; they now say "16 of 16" and "four" (Deviation 1).
2. **Six check texts trimmed**, word for word as brief 04a item 2:
   - slide 6: two options and the reason;
   - slide 7: the question;
   - slide 11: option A and the reason;
   - slide 15: the question, the three options and the reason;
   - slide 17: the reason;
   - slide 18: the question, the three options and the reason.
   The per-option feedback lines are unchanged. `chem.js` asserts no check wording, only that each check has three feedback lines, one right option and a reason starting "A.", which still pass.
3. **Driving question on slides 1, 3 and 25:** "Forces act within and between particles. How do they explain melting point, conductivity and hardness?" The three `dq` cards carry `reg` again: register grade 7.8 on all three, PASS.
4. **Exit-ticket sample (slide 25):** "The forces that come apart set the melting point. Snow melts at 0 °C: only attractions between molecules let go. Salt needs 801 °C: ionic bonds. Sand needs near 1700 °C: covalent bonds. Attractions are weaker than bonds."
   - `audits/readability.js`: `.dq` added to the visible-prose budget's exclusion selector, the only change in the file. The grade and sentence-length checks still read the driving question.
   - Proof on the reference decks (`artifacts/04a/kit/readability-reference-decks.txt`): 4.1 readability PASS, 4.2 readability PASS.
5. **Rate slide zoom:** in `css.css`, `.zflow .rate li` is one column, so a zoomed target runs the clone's width with "Review: slides …" under it. The "I can" card on slide 5 uses its own markup (`.ican`), zooms as one card and is not affected. Proof: `artifacts/04a/zoom-s26-target2.jpg`.
6. **Proof:** below.

## Verification
| Audit | Theme | Verdict | Line |
|---|---|---|---|
| walk | light | PASS | walk light: 210 states, max empty 33% (s18f1), PASS |
| walk | dark | PASS | walk dark: 210 states, max empty 33% (s18f1), PASS |
| back | light | PASS | back: 210 forward, 210 back, PASS |
| back | dark | PASS | back: 210 forward, 210 back, PASS |
| fonts | light | PASS | fonts: PASS |
| keys |  | PASS | keys: PASS 48 checks |
| readability |  | PASS | readability: PASS |
| print |  | PASS | print: PASS stage hidden=true, 27 slides, 210 frame lines, 12 PDF page(s) |
| render3d |  | PASS | render3d: PASS |
| extras |  | PASS | extras: PASS |
| chem |  | PASS | chem45 (deck): PASS 156 checks |
| timing |  | PASS | timing: period 1 45.5 min, period 2 47 min, PASS |
| supgap |  | PASS | supgap: 56 symbol+charge pairs checked, PASS |
| zoom | light | PASS | zoom light: 1224 zoomed states over 210 frames (re-flow 562, transform 662), prompt 35, r800 1, animation 147, part 515, card 219, caprow 28, caption 49, frames 1, check 26, wcard 16, legend 1, rule 22, hdr 13, row 41, p 5, dissolving table 6, sizes 1, rail 29, li 60, handsup 3, scale 6; min fill 65%; Back tests 27; PASS |
| zoom | dark | PASS | zoom dark: 1224 zoomed states over 210 frames (re-flow 562, transform 662), prompt 35, r800 1, animation 147, part 515, card 219, caprow 28, caption 49, frames 1, check 26, wcard 16, legend 1, rule 22, hdr 13, row 41, p 5, dissolving table 6, sizes 1, rail 29, li 60, handsup 3, scale 6; min fill 65%; Back tests 27; PASS |
| click |  | PASS | click: 10 graded checks, 3 Predict-now questions, 51 assertions, PASS |
| layout |  | PASS | layout: 210 frames, 26 visible option lists (stacked 23, row 3), max empty 33% (s18f1), gate 33%, clipped or ellipsized text: 0, PASS |
| xcheck |  | FAIL | xcheck: 27 of 43 pass, 16 FAIL |
| contact | light | PASS | contact sheets light: contact-light-1.png (98 shots, 3710 px tall), contact-light-2.png (97 shots, 3710 px tall), contact-light-3.png (15 shots, 1000 px tall) |
| contact | dark | PASS | contact sheets dark: contact-dark-1.png (98 shots, 3710 px tall), contact-dark-2.png (97 shots, 3710 px tall), contact-dark-3.png (15 shots, 1000 px tall) |
| zoomsheet | light | PASS | zoom sheet light: zoomsheet-light-1.png (102 shots, 3710 px tall), zoomsheet-light-2.png (3 shots, 1000 px tall) |
| zoomsheet | dark | PASS | zoom sheet dark: zoomsheet-dark-1.png (102 shots, 3710 px tall), zoomsheet-dark-2.png (3 shots, 1000 px tall) |

`python3 suite.py 4 5 --theme both` (matrix off): 21 of 22 pass, 1 fail, 1852.4 s. Logs and JSON: `artifacts/04a/suite/` (readability, chem, xcheck, suite console).



`xcheck`: 27 of 43 pass. Every failing line reads the blueprint's old numbers for 4.5 (step 05 updates them). They are the same 16 lines as report 04; none is new:
- FAIL 4.5 "The deck has 28 slides": deck has 27
- FAIL 4.5 "period 1 uses slides 1 to 12": last period-1 slide is 13, all of 1..12 are period 1
- FAIL 4.5 "period 2 slides 13 to 28": first period-2 slide is 14, all of 13..28 are period 2
- FAIL 4.5 "Slide checks: 9": slides with a check are 6, 7, 8, 9, 11, 12, 15, 17, 18, 19
- FAIL 4.5.1 → slide 5 (Targets and words): exists and carries 4.5.1 (footer "Reading §4.5 Vocabulary", no check)
- FAIL 4.5.1 → slide 8 (Dipole-dipole forces): exists and carries 4.5.1 (footer "Reading §4.5.2", a check on the slide but its footer does not name 4.5.1)
- FAIL 4.5.2 → slide 11 (Molecules stay whole): exists and carries 4.5.2 (footer "Reading §4.5.3", a check on the slide but its footer does not name 4.5.2)
- FAIL 4.5.2 → slide 12 (Why ice floats): exists and carries 4.5.2 (footer "Reading §4.5.3", a check on the slide but its footer does not name 4.5.2)
- FAIL 4.5.3 → slide 15 (Does it conduct?): exists and carries 4.5.3 (footer "Reading §4.5.4", a check on the slide but its footer does not name 4.5.3)
- FAIL 4.5.3 → slide 16 (Predict the bulb: I do, we do, you do): exists and carries 4.5.3 (footer "Reading §4.5.4", no check)
- FAIL 4.5.4 → slide 18 (Malleable or brittle): exists and carries 4.5.4 (footer "Reading §4.5.5", a check on the slide but its footer does not name 4.5.4)
- FAIL 4.5.5 → slide 20 (Four kinds of solids): exists and carries 4.5.5 (footer "Reading §4.5 Review", no check)
- FAIL 4.5 rate slide 26: 4.5.2 "Review: 8 to 10" are slides that carry 4.5.2 and are in the matrix row (9 to 12) (matrix also lists 11, 12)
- FAIL 4.5 rate slide 26: 4.5.3 "Review: 11 and 12" are slides that carry 4.5.3 and are in the matrix row (13 to 16) (matrix also lists 13, 14, 15, 16)
- FAIL 4.5 rate slide 26: 4.5.4 "Review: 15 to 17" are slides that carry 4.5.4 and are in the matrix row (17 to 18) (same set)
- FAIL 4.5 rate slide 26: 4.5.5 "Review: 18 and 19" are slides that carry 4.5.5 and are in the matrix row (19 to 21) (matrix also lists 20, 21)

Every other line passes:
- PASS matrix: 5 rows 4.5.1 to 4.5.5 found
- PASS 4.5 blueprint sentence found
- PASS 4.5.1 → slide 6 (Bonds within, attractions between): exists and carries 4.5.1
- PASS 4.5.1 → slide 7 (Dispersion forces): exists and carries 4.5.1
- PASS 4.5.2 → slide 9 (Hydrogen bonding): exists and carries 4.5.2
- PASS 4.5.2 → slide 10 (Name the attraction: I do, we do, you do): exists and carries 4.5.2
- PASS 4.5.3 → slide 13 (One picture: the ladder of attractions): exists and carries 4.5.3
- PASS 4.5.3 → slide 14 (Warm-up): exists and carries 4.5.3
- PASS 4.5.4 → slide 17 (Does it dissolve?): exists and carries 4.5.4
- PASS 4.5.5 → slide 19 (Covalent network solids): exists and carries 4.5.5
- PASS 4.5.5 → slide 21 (Checkpoint routine): exists and carries 4.5.5
- PASS 4.5 rate slide 26: 4.5.1 "Review: 6 and 7" are slides that carry 4.5.1 and are in the matrix row (5 to 8)
- PASS 4.5 s02 mentions slide 6 ("…side only touch, an attraction between. Slide 6")
- PASS 4.5 s04 mentions slide 25 ("…"bond" in the name. Keep the counts for slide 25")
- PASS 4.5 s05 mentions slide 26 ("…4.5.1 to 4.5.5; they rate themselves on slide 26")
- PASS 4.5 s06 mentions slide 5 ("…ules are the "intermolecular forces" of slide 5")
- PASS 4.5 s07 mentions slide 8 ("…ke the lasting δ signs of a polar bond (slide 8")
- PASS 4.5 s10 mentions slide 13 ("…boils at 58.8 °C, far above polar HCl. Slide 13")
- PASS 4.5 s21 mentions slide 22 ("…Routine for slides 22 to 24")
- PASS 4.5 s21 mentions slide 23 ("…Routine for slides 22 to 24")
- PASS 4.5 s21 mentions slide 24 ("…Routine for slides 22 to 24")
- PASS 4.5 s24 mentions slide 18 ("…ompt aloud. Picture the hammer model of slide 18")
- PASS 4.5 s25 mentions slide 4 ("…edicted A. Compare with the counts from slide 4")
- PASS 4.5 s25 mentions slide 3 ("…w day, with the three melting points of slide 3")
- PASS 4.5 s27 mentions slide 12 ("…y 2021 freeze; it uses the ice model of slide 12")
- PASS 4.5 every listed mention was found
- PASS 4.5 footer cues "slide N: title": 26 cues, each names the next slide by its number and title

Artifacts under `workshop/artifacts/04a/`:
- the suite console `suite/suite-4-5.txt`;
- the readability, chem and xcheck logs and JSON (`suite/`);
- the walk contact sheets of both themes (JPEG, each at most 800 KB, split as needed);
- `zoom-s26-target2.jpg`;
- `d1-heating-CH4-solid-gas.jpg`;
- `bench/`;
- `kit/` (`build-all.txt`, `readability-reference-decks.txt`).

## Repo state
- `unit4/slides-4-5.html`: 295,204 bytes, 2,830 lines, md5 `c3886bd78f9f546e5690a4e2e08fef1a` (step 04: `2a2e378a…`), written by `python3 build.py 4 5` only.
- `unit4/slides-4-1.html` `ebd342f1ee0e11c47157141cf3b2a59b` and `unit4/slides-4-2.html` `c3fa219a806963f9a66c3baf643153f4`: unchanged (`artifacts/04a/kit/build-all.txt`).
- The only file changed outside the lesson folder is `audits/readability.js` (one selector).
- `git status --short` before the commit:
  - `M` `tools/slides-kit/audits/readability.js`;
  - `M` in `tools/slides-kit/parts/lessons/4-5/`: `chem.js`, `css.css`, `gen_slides.py`, `scratch-check.js`, `scratch.html`, `sims.html`, `slides.html`;
  - `M` `unit4/slides-4-5.html`, `workshop/status.md`, `workshop/log.md`;
  - `??` `workshop/reports/04a-deck-fixes.md`, `workshop/artifacts/04a/`.
- After the commit: in the pull-request comment.

## Deviations
1. **Slide 11's notes and aria label follow item 1.** They quoted the six-methane readout ("24 of 24", "six molecules"), which would be wrong after the change. Only those numbers and that word changed.

## Open questions
None.
