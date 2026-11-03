#!/bin/sh
# Lesson 4.2 suite (plan section 10) against unit4/slides-4-2.html; results land in verify/step6.
cd "$(dirname "$0")"
export DECK=/home/user/texaschemistry/unit4/slides-4-2.html OUT=${OUT:-$(cd ../step6 && pwd)} DECKNAME=slides-4-2.html BUDGET=$(cd ../step6 && pwd)/budget42.json
export KEYS_CFG='{"cr":"s12","sim":"s12-nb","card":"s12-c1","tm":"s18","ex":"s09","hk":"s02","notes":["s15",0]}'
export EXTRAS_CFG='{"hash":"#15.1","canvas":"#s15-sim canvas","block":"s15-r3","slides":26}'
st=0
for c in "walk.js light" "walk.js dark" "back.js light" "back.js dark" "fonts.js light" "keys.js" "readability.js" "print.js" "render3d.js" "extras.js" "chem42-deck.js" "timing.js" "supgap.js" "zoom.js light" "zoom.js dark" "click.js" "layout.js"; do
  node $c || st=1
done
node contact.js light && node contact.js dark && node zoomsheet.js light && node zoomsheet.js dark
exit $st
