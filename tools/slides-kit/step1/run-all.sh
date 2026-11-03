#!/bin/sh
# Lesson 4.1 suite (plan section 10, items 1-4, 6, 7, plus the teacher-round audits zoom, click, layout) against unit4/slides-4-1.html.
# Results land in $OUT (default: next to this script).
cd "$(dirname "$0")"
st=0
for c in "walk.js light" "walk.js dark" "back.js light" "back.js dark" "fonts.js light" "keys.js" "readability.js" "print.js" "render3d.js" "extras.js" "chem-deck.js" "timing.js" "supgap.js" "zoom.js light" "zoom.js dark" "click.js" "layout.js"; do
  node $c || st=1
done
node contact.js light && node contact.js dark && node zoomsheet.js light && node zoomsheet.js dark
exit $st
