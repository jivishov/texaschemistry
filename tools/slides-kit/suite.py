#!/usr/bin/env python3
"""Run a deck's audits (RULES.md section 11) and write logs, JSON and sheets to an output folder outside the repo.

  python3 suite.py <U> <L> [--matrix] [--theme light|dark|both] [--out <folder>] [--only walk,zoom,...] [--deck <path>]
  python3 suite.py --all [--matrix] [--theme light|dark|both] [--out <folder>] [--only ...]

Order (as the 4.1 and 4.2 run-all scripts ran them): walk, back, fonts, keys, readability, print, render3d, extras, chem, timing,
supgap, zoom, click, layout, the deck's extra audits (registry "extra_audits"), xcheck, then the contact and zoom sheets.
walk, back, zoom, contact and zoomsheet run once per theme; fonts runs once (light, or dark with --theme dark); the others once.
One PASS or FAIL line per audit with its duration, then a summary; exit 1 if any audit failed.

  --matrix          the zoom audit's viewport matrix pass (MATRIX=1 in the environment does the same); off by default (MATRIX=0)
  --out <folder>    results land in <folder>/<U>-<L>/ (logs/ holds each audit's stdout and stderr; suite.json the summary).
                    Default: $SLIDES_KIT_OUT, else <system temp folder>/slides-kit-out. Never a folder inside the repo.
  --only a,b        run only these audits (names as in the order above; units and cycle only where the registry lists them)
  --deck <path>     audit this deck instead of the registry's file (a deck built with build.py --out). xcheck is skipped (it
                    cross-checks the repo deck against the blueprint). A scratch deck (build.py --scratch) also runs without the
                    lesson's explicit zoom checks.

Environment each audit receives: DECK, OUT, DECKNAME, LESSON, BUDGET, KEYS_CFG, EXTRAS_CFG, MATRIX, SLIDES (extra audits),
XCHECK (xcheck). The registry is the only source of deck-specific configuration; no path in the kit is absolute.
"""
import argparse, json, os, subprocess, sys, tempfile, time

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(KIT, '..', '..'))
AUD = os.path.join(KIT, 'audits')
ORDER = ['walk', 'back', 'fonts', 'keys', 'readability', 'print', 'render3d', 'extras', 'chem', 'timing', 'supgap', 'zoom',
         'click', 'layout', 'units', 'cycle', 'xcheck', 'contact', 'zoomsheet']
THEMED = {'walk', 'back', 'zoom', 'contact', 'zoomsheet'}
EXTRA = {'units', 'cycle'}


def registry():
    with open(os.path.join(KIT, 'registry.json'), encoding='utf-8') as f:
        return json.load(f)['decks']


def entry(u, l):
    for d in registry():
        if d['unit'] == u and d['lesson'] == l:
            return d
    sys.exit(f'suite.py: lesson {u}.{l} is not in registry.json')


def inside_repo(p):
    p = os.path.abspath(p)
    return p == REPO or p.startswith(REPO + os.sep)


def summary_line(text):
    """The audit's verdict line: the last line of its output that is not indented."""
    lines = [x for x in text.splitlines() if x.strip() and not x[:1].isspace()]
    return lines[-1] if lines else ''


def run_deck(d, o, out_root):
    lesson = f"{d['unit']}.{d['lesson']}"
    deck = os.path.abspath(o.deck) if o.deck else os.path.join(REPO, d['file'])
    if not os.path.exists(deck):
        sys.exit(f'suite.py: {deck} does not exist (build it first: python3 build.py {d["unit"]} {d["lesson"]})')
    with open(deck, encoding='utf-8') as f:
        scratch = '<!-- part: scratch-' in f.read()
    out = os.path.join(out_root, f"{d['unit']}-{d['lesson']}")
    logs = os.path.join(out, 'logs')
    os.makedirs(logs, exist_ok=True)
    themes = ['light', 'dark'] if o.theme == 'both' else [o.theme]
    matrix = o.matrix or os.environ.get('MATRIX') == '1'
    env = dict(os.environ,
               DECK=deck, OUT=out, DECKNAME=os.path.basename(deck), LESSON='' if scratch else lesson,
               BUDGET=os.path.join(KIT, d['budget']), KEYS_CFG=json.dumps(d['keys_cfg']), EXTRAS_CFG=json.dumps(d['extras_cfg']),
               MATRIX='1' if matrix else '0')
    if d.get('extra_slides'):
        env['SLIDES'] = '%d,%d' % tuple(d['extra_slides'])
    env['XCHECK'] = json.dumps([{
        'lesson': lesson, 'deck': deck, 'blueprint': os.path.join(REPO, f"unit{d['unit']}", 'blueprint.html'),
        'section': d['blueprint']['section'], 'next': d['blueprint']['next'], 'objectives': d['matrix'],
        'mentions': d['mentions'], 'walk': os.path.join(out, 'walk-light.json')}], ensure_ascii=False)

    jobs = []
    for name in ORDER:
        if o.only and name not in o.only:
            continue
        if name in EXTRA and name not in d.get('extra_audits', []):
            continue
        if name == 'xcheck' and o.deck:
            print(f'  skip  xcheck            (--deck: the cross-check reads the repo deck {d["file"]})')
            continue
        script = os.path.join(KIT, d['chem']) if name == 'chem' else os.path.join(AUD, name + '.js')
        if name in THEMED:
            jobs += [(name, t, ['node', script, t]) for t in themes]
        elif name == 'fonts':
            jobs.append((name, themes[0], ['node', script, themes[0]]))
        elif name == 'units':
            jobs.append((name, '', ['node', script, deck, os.path.join(out, 'units.json')]))
        elif name == 'cycle':
            jobs.append((name, '', ['node', script, deck]))
        else:
            jobs.append((name, '', ['node', script]))

    print(f"== {lesson}{' (scratch deck)' if scratch else ''}: {os.path.relpath(deck, REPO) if inside_repo(deck) else deck}")
    print(f"   out {out}, theme {o.theme}, matrix {'on' if matrix else 'off'}")
    results, t0 = [], time.time()
    for name, theme, cmd in jobs:
        t = time.time()
        r = subprocess.run(cmd, env=env, cwd=KIT, capture_output=True, text=True)
        sec = round(time.time() - t, 1)
        label = name + (' ' + theme if theme else '')
        log = os.path.join(logs, label.replace(' ', '-') + '.log')
        with open(log, 'w', encoding='utf-8') as f:
            f.write(r.stdout + (('\n--- stderr ---\n' + r.stderr) if r.stderr.strip() else ''))
        ok = r.returncode == 0
        line = summary_line(r.stdout) or summary_line(r.stderr)
        results.append({'audit': name, 'theme': theme, 'pass': ok, 'seconds': sec, 'summary': line,
                        'log': os.path.relpath(log, out)})
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<17} {sec:7.1f} s  {line}", flush=True)
    total = round(time.time() - t0, 1)
    failed = [r for r in results if not r['pass']]
    with open(os.path.join(out, 'suite.json'), 'w', encoding='utf-8') as f:
        json.dump({'lesson': lesson, 'deck': deck if not inside_repo(deck) else os.path.relpath(deck, REPO), 'scratch': scratch,
                   'theme': o.theme, 'matrix': matrix, 'audits': len(results), 'failed': len(failed), 'seconds': total,
                   'results': results}, f, indent=1, ensure_ascii=False)
    print(f"== {lesson}: {len(results) - len(failed)} of {len(results)} pass, {len(failed)} fail, {total} s")
    return results


def main():
    a = argparse.ArgumentParser(description="Run a deck's audits.")
    a.add_argument('unit', nargs='?', type=int)
    a.add_argument('lesson', nargs='?', type=int)
    a.add_argument('--all', action='store_true', help='every registered deck')
    a.add_argument('--matrix', action='store_true', help='run the zoom viewport matrix (once per workshop)')
    a.add_argument('--theme', choices=['light', 'dark', 'both'], default='both')
    a.add_argument('--out', help='output folder (outside the repo)')
    a.add_argument('--only', help='comma-separated audit names')
    a.add_argument('--deck', help='audit this deck file instead of the registry file')
    o = a.parse_args()
    if o.only:
        o.only = [x.strip() for x in o.only.split(',') if x.strip()]
        bad = [x for x in o.only if x not in ORDER]
        if bad:
            a.error(f"unknown audit(s) {', '.join(bad)}; known: {', '.join(ORDER)}")
    out_root = os.path.abspath(o.out or os.environ.get('SLIDES_KIT_OUT') or os.path.join(tempfile.gettempdir(), 'slides-kit-out'))
    if inside_repo(out_root):
        a.error(f'--out {out_root} is inside the repo; write outside it and copy logs and sheets into workshop/artifacts/NN/')
    if o.all:
        if o.unit is not None or o.deck:
            a.error('--all takes no lesson and no --deck')
        decks = registry()
    else:
        if o.unit is None or o.lesson is None:
            a.error('give <U> <L>, or --all')
        decks = [entry(o.unit, o.lesson)]
    allres = {}
    for d in decks:
        allres[f"{d['unit']}.{d['lesson']}"] = run_deck(d, o, out_root)
    if len(decks) > 1:
        print('== all decks')
        for k, rs in allres.items():
            f = [r['audit'] + (' ' + r['theme'] if r['theme'] else '') for r in rs if not r['pass']]
            print(f"  {k}: {len(rs) - len(f)} of {len(rs)} pass, {round(sum(r['seconds'] for r in rs), 1)} s{', FAIL: ' + ', '.join(f) if f else ''}")
    sys.exit(1 if any(not r['pass'] for rs in allres.values() for r in rs) else 0)


if __name__ == '__main__':
    main()
