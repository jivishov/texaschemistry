> **Layout replaced (workshop step 01, 2026-11-03):** the `step1/`, `step6/`, `step7/`, `step10/` and `final/` layout and the absolute paths named below no longer exist; the kit is now `parts/`, `build.py`, `suite.py`, `registry.json` and `audits/` (see `../README.md`). The clicker map, the animation list and the known limitations below still hold.

# Unit 4 slide decks: handoff

## Files (repo)
| File | Size | md5 | What |
|---|---|---|---|
| `/home/user/texaschemistry/unit4/slides-4-1.html` | 194,646 bytes (2,077 lines) | ebd342f1ee0e11c47157141cf3b2a59b | Lesson 4.1 Predicting bond type: 25 slides, 156 frames; period 1 = slides 1 to 13, period 2 = 14 to 25 |
| `/home/user/texaschemistry/unit4/slides-4-2.html` | 203,769 bytes (2,153 lines) | c3fa219a806963f9a66c3baf643153f4 | Lesson 4.2 Ionic formulas and names: 26 slides, 173 frames; period 1 = slides 1 to 13, period 2 = 14 to 26 |
| `/home/user/texaschemistry/unit4/blueprint.html` | 45,017 bytes | 636e06f86bbac2407542f07d77fc1279 | Slide checks, slide counts, period splits and matrix slide numbers for both decks |

Each deck is one standalone page: all CSS, JS and SVG are inline. There are no libraries and no images.

## Run a deck
1. Open the file in Chrome or Edge (double-click or `file://`).
2. Press **F5** on the clicker (or keyboard) for full screen.
3. Use the four R800 buttons (table below). One Next press shows one frame: a reveal, an animation stage or a timer.
4. The footer cue tells you what the next press shows; while zoomed it reads "Zoom 2 of 5 · Blank ▶ next · Back ▶ exit".
5. **Zoom cycle:** press Blank to zoom the first part of the slide (the animation first), press again for the next part, and so on; the press after the last part exits. Back or Escape exits the zoom at once.
6. **Mouse grading:** click an answer option on a check. A right option turns green with its reason; a wrong one turns red with its own feedback line. Click another option to re-mark. Next still shows the answer as before. On Predict now, a click only highlights the option.
7. **Slide list:** click the slide number or the section label (bottom of the slide) to open the list of every slide; click a slide to jump to it. O does the same from the keyboard.
8. On the laptop, **N** opens the speaker notes: every frame's note, its minutes and the slide note.
9. **Ctrl+P** prints the run-sheet (a two-period plan with minutes per slide and per frame) instead of the slides.

## Clicker map (Logitech R800)
| R800 button (key) | Action |
|---|---|
| Next ▶ (PageDown; laptop →, ↓, Space) | Next frame; after a slide's last frame, the next slide at frame 0 |
| Back ◀ (PageUp; laptop ←, ↑) | Previous frame; at frame 0, the previous slide at its last frame. While zoomed: exits the zoom without moving |
| Start/stop (F5, then Escape) | F5: full screen (Chrome/Edge also hold Escape). Escape: closes the blank screen, then the zoom, then the notes, then leaves full screen |
| Blank (. or B) | Zoom cycle: each press zooms the next part of the slide (animation first, then top-left to bottom-right); the press after the last part exits. Text parts are re-flowed larger (up to 2.2x); animations zoom as pictures (up to 4x). Two fast presses on an unzoomed slide blank the screen; any key brings it back without moving |
| Mouse on a check option | Green mark and its reason, or red mark and that option's feedback line; Predict now only highlights |
| Mouse on the slide number or section label | Slide list with every slide's number and title; a click jumps |
| Guards | Held buttons advance once; Next/Back presses within 180 ms count once; keys work whatever has focus except a text box |
| Laptop: N / O / Z / T | Notes panel / slide overview (arrows + Enter) / zoom toggle / light-dark theme |
| Laptop: Home / End | First slide / last frame of the deck |

## Animations
- **4.1:** tugOfWar (slides 2, 8), ionHop with the 3D sphere crystal (6, 7), sharedPair (8, 9), electronSea with the copper stage (10), enMeter (15, 17), ptMap (16), cerBuilder (18).
- **4.2:** labelRead (2), ionTable (6, 7), chargeBlocks (8, 9, 16, 17), crisscross (10), nameBuilder (11, 12), stockDetective (12, 17), polyIons in 3D (15), parenBus (16).

## Sources and scripts (scratchpad, not in the repo)
Root: `/tmp/claude-0/-home-user-texaschemistry/c6972a9b-3815-5999-9496-13829ff2b217/scratchpad/verify/`
- **Parts:** `step1/src/`
  - shared: `01-head.html`, `02-runtime.html`, `02b-shared.html`
  - 4.1: `03-sims.html`, `04-slides.html` (from `gen_slides.py`)
  - 4.2: `01c-css-42.css`, `06-sims-42.html`, `08-slides-42.html` (from `gen_slides42.py`)
- **Builds:** `step1/build.sh` (4.1) and `step1/build42.sh` (4.2) write the repo files. Each part sits between `<!-- part: NAME start -->` and `<!-- part: NAME end -->` lines in the built deck (4.2 head: `01-head-42`, with `01c-css-42.css` inside `/* part: 01c-css-42 start|end */`); `step10/split_parts.py <deck> <dir>` splits a deck back into its parts.
- **Kit:** `final/slides-kit.tar.gz` holds the parts, generators, builds, suites, audits, the split script and this file, with a README.
- **Suites:** `step1/run-all.sh` (4.1) and `step1/run-all42.sh` (4.2), results in `$OUT` (last full runs: `step10/d41`, `step10/d42`; after the ionTable change: `step10/d42b` with `MATRIX=0`, and the 4.1 zoom audit in `step10/d41b`).
  - Each runs walk, back, fonts, keys, readability, print, render3d, extras (reduced motion and the narrow-screen fallback), chemistry checks, timing, supgap, zoom (both themes), click, layout, the contact sheets and the zoom sheets.
  - zoom.js measures every zoomed unit live on screen (centred, inside the slide above the footer, at least 60% fill). Its main pass loads at 1366 x 768 and changes to 1920 x 1080 before zooming; its matrix pass (motion on) runs 1366 x 768, 1536 x 864, 1920 x 1080 and 1024 x 768 at device scale 1, 1.25 and 1.5, with a resize while zoomed, Next while zoomed, a zoom during the zoom-out, after Back and after the slide list. `MATRIX=0` skips the matrix (about 12 min per theme).
- **Zoom fix (step 10):** `step10/` holds the reproduction scripts, the before/after screenshots of the teacher's four cases (`step10/teacher-cases/`) and the zoom sheets.
- **Animation test bench:** `step5/` (scratch deck of every 4.2 animation stage and its checks).
- **Blueprint cross-check:** `step7/xcheck.js`.
- **Final artifacts:** `final/` (contact sheets and zoom sheets for both decks in both themes, both run-sheet PDFs, the click screenshots, this file).

## Known limitations
- **Escape keyboard lock:** headless Chromium cannot test it. In a browser without `navigator.keyboard.lock`, Escape leaves full screen at once.
- **Fonts:** without network the Google Fonts do not load, and the decks use the system fallback fonts.
- **Narrow screens:** under 760 px wide the deck shows a scrolling fallback page of all slides instead of the projector view.
- **Projector:** the decks are laid out for a 16:9 projector; other ratios letterbox.
- **Zoom re-flow:** a text part zooms as a larger copy laid out again; a very wide one-line part (a rail of step names) gains little.
