#!/bin/sh
# Assemble the Lesson 4.1 deck from its parts into the repo path (scratch parts never enter it).
# Each part is wrapped in "<!-- part: NAME start -->" and "<!-- part: NAME end -->" lines, so it can be split back out:
# a part's text is exactly what lies between its start line (with its newline) and its end line.
cd "$(dirname "$0")/src" && for p in 01-head 02-runtime 02b-shared 03-sims 04-slides; do
  printf '<!-- part: %s start -->\n' "$p"; cat "$p.html"; printf '<!-- part: %s end -->\n' "$p"
done > /home/user/texaschemistry/unit4/slides-4-1.html && wc -l /home/user/texaschemistry/unit4/slides-4-1.html
