#!/bin/sh
# Assemble the Lesson 4.2 deck: the shared head (its own title and description, plus 01c-css-42.css), runtime, shared data,
# the 4.2 animations and the 4.2 slides. The 4.1 parts are not changed. Each part is wrapped in part start/end comment lines.
S="$(dirname "$0")/src"
python3 "$S/gen_slides42.py" >/dev/null && python3 - "$S" <<'PY'
import sys,os
S=sys.argv[1];h=open(os.path.join(S,'01-head.html')).read()
rep=[('<title>Predicting Bond Type Slides</title>','<title>Ionic Formulas and Names Slides</title>'),
 ('content="Unit 4, Lesson 4.1 projector slides: Predicting bond type (TEKS C.7(A))."','content="Unit 4, Lesson 4.2 projector slides: Ionic compounds: formulas and names (TEKS C.7(B))."'),
 ('<meta property="og:title" content="Predicting Bond Type Slides">','<meta property="og:title" content="Ionic Formulas and Names Slides">')]
for a,b in rep:
    assert h.count(a)>=1,a
    h=h.replace(a,b)
assert 'Lesson 4.1' not in h and 'Predicting' not in h
css=open(os.path.join(S,'01c-css-42.css')).read()
assert h.count('</style>\n</head>')==1
h=h.replace('</style>\n</head>','/* part: 01c-css-42 start */\n'+css+'/* part: 01c-css-42 end */\n</style>\n</head>')
# each part between "<!-- part: NAME start -->" and "<!-- part: NAME end -->" lines; the head is 01-head-42 (01-head with the
# title, description and og:title replaced and 01c-css-42.css inserted before </style>, inside its own /* part: */ comments)
mark=lambda n,t:'<!-- part: %s start -->\n%s<!-- part: %s end -->\n'%(n,t,n)
parts=[mark('01-head-42',h)]+[mark(f[:-5],open(os.path.join(S,f)).read()) for f in ['02-runtime.html','02b-shared.html','06-sims-42.html','08-slides-42.html']]
open('/home/user/texaschemistry/unit4/slides-4-2.html','w').write(''.join(parts))
PY
wc -l /home/user/texaschemistry/unit4/slides-4-2.html
