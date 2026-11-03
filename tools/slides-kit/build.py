#!/usr/bin/env python3
"""Build projector decks from the kit's parts (README.md has the layout and the conventions).

  python3 build.py <U> <L>                         build one registered deck into the repo (its registry "file")
  python3 build.py --all                           build every registered deck into the repo
  python3 build.py <U> <L> --out <path>            write the deck to <path> instead (for example a scratchpad)
  python3 build.py <U> <L> --scratch --out <path>  assemble the lesson's scratch.html in place of slides.html (runs gen_scratch.py
                                                   first if the lesson has one); a scratch build never enters the repo

A deck is five parts in this order, each between "<!-- part: NAME start -->" and "<!-- part: NAME end -->" lines, NAME taken
from the registry's "markers" in the same order:
  1. head     parts/shared/01-head.html, {{TITLE}} and {{DESCRIPTION}} filled from the registry; when the lesson has css.css, it is
              inserted before </style> between "/* part: CSS start */" and "/* part: CSS end */" lines (CSS = the registry's "css")
  2. runtime  parts/shared/02-runtime.html
  3. shared   parts/shared/02b-shared.html
  4. sims     parts/lessons/<U>-<L>/sims.html
  5. slides   parts/lessons/<U>-<L>/slides.html, written first by the lesson's gen_slides.py
              (scratch build: scratch.html, with the marker "scratch-<U><L>")
The repo root is two folders above this file; no path in the kit is absolute.
"""
import argparse, hashlib, html, json, os, subprocess, sys

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(KIT, '..', '..'))
SHARED = os.path.join(KIT, 'parts', 'shared')


def registry():
    with open(os.path.join(KIT, 'registry.json'), encoding='utf-8') as f:
        return json.load(f)['decks']


def entry(u, l):
    for d in registry():
        if d['unit'] == u and d['lesson'] == l:
            return d
    sys.exit(f'build.py: lesson {u}.{l} is not in registry.json (add an entry first; README.md, "Add a lesson")')


def lesson_dir(d):
    return os.path.join(KIT, 'parts', 'lessons', f"{d['unit']}-{d['lesson']}")


def read(p):
    with open(p, encoding='utf-8', newline='') as f:
        return f.read()


def mark(name, text):
    return '<!-- part: %s start -->\n%s<!-- part: %s end -->\n' % (name, text, name)


def run(script):
    r = subprocess.run([sys.executable, script], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'build.py: {os.path.relpath(script, KIT)} failed\n{r.stdout}{r.stderr}')
    return r.stdout.strip()


def head(d):
    h = read(os.path.join(SHARED, '01-head.html'))
    for key, value in (('{{TITLE}}', d['title']), ('{{DESCRIPTION}}', d['description'])):
        assert h.count(key) == 2, f'01-head.html: {key} must appear twice (page and og: tags)'
        h = h.replace(key, html.escape(value, quote=True))
    assert '{{' not in h, '01-head.html: a placeholder is left unfilled'
    css = os.path.join(lesson_dir(d), 'css.css')
    if os.path.exists(css):
        m = d.get('css')
        assert m, f"{os.path.relpath(css, KIT)} exists but the registry entry has no \"css\" marker name"
        assert h.count('</style>\n</head>') == 1, '01-head.html: expected one "</style>" line right before "</head>"'
        h = h.replace('</style>\n</head>', '/* part: %s start */\n%s/* part: %s end */\n</style>\n</head>' % (m, read(css), m))
    else:
        assert not d.get('css'), f"registry names the css marker {d['css']} but {os.path.relpath(css, KIT)} is missing"
    return h


def build(d, out=None, scratch=False):
    ld = lesson_dir(d)
    names = d['markers']
    assert len(names) == 5, 'registry "markers": five names (head, runtime, shared, sims, slides)'
    if scratch:
        gen = os.path.join(ld, 'gen_scratch.py')
        if os.path.exists(gen):
            run(gen)
        last, last_name = os.path.join(ld, 'scratch.html'), f"scratch-{d['unit']}{d['lesson']}"
    else:
        run(os.path.join(ld, 'gen_slides.py'))
        last, last_name = os.path.join(ld, 'slides.html'), names[4]
    texts = [head(d), read(os.path.join(SHARED, '02-runtime.html')), read(os.path.join(SHARED, '02b-shared.html')),
             read(os.path.join(ld, 'sims.html')), read(last)]
    deck = ''.join(mark(n, t) for n, t in zip(names[:4] + [last_name], texts))
    path = os.path.abspath(out) if out else os.path.join(REPO, d['file'])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(deck)
    data = deck.encode('utf-8')
    shown = os.path.relpath(path, REPO) if path.startswith(REPO + os.sep) else path
    print(f"{d['unit']}.{d['lesson']}{' scratch' if scratch else ''}: {shown}  {len(data)} bytes, {deck.count(chr(10))} lines, md5 {hashlib.md5(data).hexdigest()}")
    return path


def main():
    a = argparse.ArgumentParser(description='Build projector decks from the kit parts.')
    a.add_argument('unit', nargs='?', type=int)
    a.add_argument('lesson', nargs='?', type=int)
    a.add_argument('--all', action='store_true', help='build every registered deck into the repo')
    a.add_argument('--out', help='write the deck here instead of the repo path')
    a.add_argument('--scratch', action='store_true', help="assemble the lesson's scratch.html (needs --out)")
    o = a.parse_args()
    if o.all:
        if o.unit is not None or o.out or o.scratch:
            a.error('--all takes no lesson, --out or --scratch')
        for d in registry():
            build(d)
        return
    if o.unit is None or o.lesson is None:
        a.error('give <U> <L>, or --all')
    if o.scratch and not o.out:
        a.error('--scratch needs --out <path>: a scratch build never enters the repo')
    if o.scratch and os.path.abspath(o.out).startswith(REPO + os.sep):
        a.error('--scratch --out: write scratch builds outside the repo (for example the session scratchpad)')
    build(entry(o.unit, o.lesson), o.out, o.scratch)


if __name__ == '__main__':
    main()
