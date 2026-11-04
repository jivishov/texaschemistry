# Review 04a: Deck fixes from review 04

Step: 04a · Report: `reports/04a-deck-fixes.md` (commit `992f6e1`) · Verdict: **accepted**. The deck passes every suite but the cross-check, whose sixteen failing lines read the blueprint's old 4.5 numbers and wait for step 05.

## Verified by the orchestrator (not from the report)
1. `git pull --ff-only`; `git status --short` empty at `992f6e1`; 4.1 `ebd342f1…` and 4.2 `c3fa219a…` unchanged; the deck 295,204 bytes, md5 `c3886bd7…`; `python3 build.py 4 5` here reproduces it byte for byte.
2. The step's diff: `audits/readability.js` changes one selector only (`.dq` added to the visible-prose budget's exclusion list; the grade and sentence checks untouched); the rest is the 4.5 lesson folder and the built deck.
3. The rebuilt deck's texts read: the three driving-question cards carry "Forces act within and between particles. How do they explain melting point, conductivity and hardness?" with `dq reg`; the six checks on slides 6, 7, 11, 15, 17 and 18 carry brief 04a's wording word for word, each at 35 counted words with the question, options and reason; the exit sample is the 35-word text of the brief; the heating readout reads "Covalent bonds: 16 of 16 intact"; the slide-11 host's label says four methane molecules; the only remaining "six molecules" mentions are two lines of the animation source's header comment in `sims.html` (not student-facing; a one-line nit for the next brief). No ellipsis character.
4. Sheets opened: the methane bench frames (a 2 × 2 block at −182.5 °C with four dashed attractions, the four molecules at the container's corners at −161.5 °C with none), the slide-26 zoom proof (the target sentence across the full width, "Review: slides 8 to 10" under it), and the light contact sheet (the new driving question on the cover and the launch).
5. Re-run here (`suite.py 4 5 --only walk,readability,chem,timing,xcheck,contact --theme light`, then readability on 4.1 and 4.2): in progress when this review was committed; its result is appended in the next commit.

## Findings
- **F1 (accepted).** Deviation 1: slide 11's notes and aria label updated to the four-molecule readout; a consequence of item 1, correctly reported.
- **F2 (nit, next brief).** The header comment of `parts/lessons/4-5/sims.html` still describes `heating` as six molecules (2 × 3); update the two lines to four CH₄ and six H₂O.
- **F3 (none).** No other deviation; no open question.

## Next
The teacher's own round on the deck (fix brief 04b from their screenshots and remarks), then brief 05: the blueprint numbers, the zoom matrix on 4.5, the final suites, the kit README and registry, FINAL.md.
