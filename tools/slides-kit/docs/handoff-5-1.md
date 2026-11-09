# Unit 5 deck 5.1: handoff

**Deck.** `unit5/slides-5-1.html`, Lesson 5.1 Counting particles with the mole (TEKS C.8(A), C.8(B)): 28 slides, 197 frames, 11 checks
(slides 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 19); period 1 = slides 1 to 14 (43.75 min), period 2 = 15 to 28 (46 min). Built by
`python3 build.py 5 1` from `parts/shared/` and `parts/lessons/5-1/` (markers `01-head-51`, `css-51`, `02-runtime`, `02b-shared`,
`sims-51`, `slides-51`); audited by `python3 suite.py 5 1 --theme both` (add `--matrix` once per workshop). The rejected older deck is
in `unit5/old-slides/` and is never read.

**Running it and the clicker map.** Exactly as `docs/handoff-4-1-4-2.md` ("Run a deck", "Clicker map"): the same runtime and keys.
In 5.1 the timers are on slides 3 (60 s), 14 and 15 (90 s), 20 (180 s), 23 to 25 (30, 60 and 90 s each: think, talk, write) and 26 (180 s).

**Animations** (`parts/lessons/5-1/sims.html`; the bench is `gen_scratch.py`, 78 scratch slides, one per stage, checked by `scratch-check.js`):

| Animation | Stages | Slides |
|---|---|---|
| coinScale | jar, guess, tally (live), scale, reveal; bag, zero, read, divide, count; roll | 2, 6 |
| centJar | jar, wrong, sample, average, count, isotopes (six Cu atoms, one size, two shades) | 7 |
| countingUnits | dozen, ream, mole, exact, constant | 8 |
| howMany | one, dozen, thousand, zoom (live), mole, spoon | 9 |
| moleKinds | al, cu, compare, oxygen, four | 10 |
| secondsLine | line (live), year, earth, universe, mole, times, spoon | 11 |
| moleHistory | avogadro, loschmidt, ostwald, perrin, si, exact | 12 |
| siliconSphere | sphere, crystal (turns), cube (turns), atom, divide | 13 |
| moleMap | map; Cu, Fe, CO2m, H2Om × setup, cancel, result; half; energy/mole, energy/one, energy/why | 16, 17, 20, 21 |
| naclCrystal | crystal (turns), unit (turns), count, wrong | 18 |
| atomCounter | H2O/one, H2O/mol, CO2/mol, CO2/atoms, NaCl/mol, NH3/mol | 19, 20 |

**Live stages and reduced motion.** The three live stages move numbers inside their own boxes only (the coin counter, the cascade's
counter and ladder, the time-line clock); the two 3D crystals turn slowly. Under reduced motion every stage jumps to its end state,
each live or turning stage holds one still frame, and the crystals stay at a fixed three-quarter view.

**Unit 5 color code** (legend on slide 5; plan section 3):

| Quantity | Token | Light | Dark |
|---|---|---|---|
| mass in grams | `--warm` | #835811 | #e6bd6c |
| amount in moles | `--accent` | #0b5951 | #73c7b4 |
| number of particles | `--e` | #7a2fc0 | #cc99ff (set in `css-51`; the shared dark `--e` is amber #f6d84a) |
| conversion factor / canceled unit | `--muted` / `--bad` | #4b5c57 / #a8402f | #a9bab3 / #f39886 |

Ions keep Unit 4's cation red "+" and anion blue "−" (`--cat`, `--an`); atoms are CPK with the symbol on every sphere and the caption
"Atom colors show the element, not the charge." on slides 10 and 19; nickel `--metal`, cent made before 1982 `--rope`. The dark violet
reads 7.1:1 on `--card`, 7.6:1 on the animation panel and on `--card2`, 5.5:1 on a canvas chip's fill.

**Known limitations** (review 02 F7; candidates for a later kit round, all handled by layout in 5.1):
- The ✓ / ✗ badge of an option in a row is a pseudo-element 24 px above the option; the overlap check measures boxes, not
  pseudo-elements. `css-51` keeps 28 px (20 px in a band check row) free above row options.
- Lines, arcs, arrowheads and markers drawn straight on the context (time-line markers, the map's bridge arc, the cube's edge
  measure) are not recorded by the overlap instrumentation; they are kept clear of labels by layout and checked on the sheets.
- A live stage that is an animation's first stage gets its time from page load (the runtime resets the stage time only on a stage
  change); `secondsLine` restarts its own clock when its slide is entered. A shared fix would reset the time in `active(true)`.
- The limitations of `docs/handoff-4-1-4-2.md` (Escape keyboard lock, offline fonts, narrow screens, projector ratio, zoom re-flow) apply.

**Blueprint form** (`unit5/blueprint.html`, registry `blueprint.form` `"unit5"`): only numbers change. In section `l51`, the deck line
"Deck: 28 slides. Checkpoints 22 to 25, predictions revisited 26, CER exit ticket 26, self-rating 27." and the Slides cells of the
objectives table (5.1.1 6, 7; 5.1.2 8 to 13, 21; 5.1.3 16 to 18; 5.1.4 19, 20); in section `matrix`, C.8(A) "Deck 5.1, slides 6 to
13, 21" and C.8(B) "Deck 5.1, slides 16 to 20". The blueprint prints no check count or period split: xcheck asserts those against the
registry and the deck.
