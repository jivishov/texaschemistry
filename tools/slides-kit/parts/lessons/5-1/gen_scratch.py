# Writes scratch.html: the Lesson 5.1 animation bench, one scratch slide per stage of every animation (plan section 4, in its order).
# Each slide holds one host in the template the deck uses for that stage, a label naming the animation and the stage, and sets the
# stage on frame 0. Run by build.py 5 1 --scratch; never part of a repo build.
import os

CAP = 'Atom colors show the element, not the charge.'
# (animation, template, stages, extra host attributes); templates: hook, cw, cwcap (with the caption under the host), wide, example
SIMS = [
    ('coinScale', 'hook', ['jar', 'guess', 'tally', 'scale', 'reveal'], ''),
    ('coinScale', 'cw', ['bag', 'zero', 'read', 'divide', 'count', 'roll'], ''),
    ('centJar', 'cw', ['jar', 'wrong', 'sample', 'average', 'count', 'isotopes'], ''),
    ('countingUnits', 'cw', ['dozen', 'ream', 'mole', 'exact', 'constant'], ''),
    ('howMany', 'cw', ['one', 'dozen', 'thousand', 'zoom', 'mole', 'spoon'], ''),
    ('moleKinds', 'cwcap', ['al', 'cu', 'compare', 'oxygen', 'four'], ''),
    ('secondsLine', 'wide', ['line', 'year', 'earth', 'universe', 'mole', 'times', 'spoon'], 'data-band="214"'),
    ('moleHistory', 'wide', ['avogadro', 'loschmidt', 'ostwald', 'perrin', 'si', 'exact'], 'data-band="214"'),
    ('siliconSphere', 'cw', ['sphere', 'crystal', 'cube', 'atom', 'divide'], ''),
    ('moleMap', 'cw', ['map', 'Cu/setup', 'Cu/cancel', 'Cu/result', 'Fe/setup', 'Fe/cancel', 'Fe/result', 'half'], ''),
    ('moleMap', 'example', ['CO2m/setup', 'CO2m/cancel', 'CO2m/result', 'H2Om/setup', 'H2Om/cancel', 'H2Om/result'], ''),
    ('moleMap', 'cw', ['energy/mole', 'energy/one', 'energy/why'], ''),
    ('naclCrystal', 'cw', ['crystal', 'unit', 'count', 'wrong'], ''),
    ('atomCounter', 'cwcap', ['H2O/one', 'H2O/mol', 'CO2/mol', 'CO2/atoms', 'NaCl/mol'], ''),
    ('atomCounter', 'example', ['NH3/mol'], ''),
]
TPL = {'hook': 't-hook', 'cw': 't-concept cw', 'cwcap': 't-concept cw', 'wide': 't-concept wide', 'example': 't-example'}

out = ['<main id="stage">\n<div id="prog"><i></i></div>\n']
n = 0
for typ, tpl, stages, extra in SIMS:
    for stage in stages:
        n += 1
        sid = 'x%02d' % n
        label = f'{typ} · {stage}'
        host = f'<div class="sim" id="{sid}-sim" data-sim="{typ}" {extra} aria-label="{typ} at the stage {stage}"></div>'
        lab = f'<p class="tag">Bench</p><p id="{sid}-lab">{label}</p>'
        if tpl == 'hook':
            body = f'{host}\n    <div class="stack card band" data-zoom="none"><p class="line" data-zoom="none" id="{sid}-lab">{label}</p></div>'
        elif tpl == 'cw':
            body = f'{host}\n    <div class="col acc"><div class="card" data-zoom="none">{lab}</div></div>'
        elif tpl == 'cwcap':
            body = (f'<div class="leftcol">{host}<p class="simcap" data-zoom="caption">{CAP}</p></div>\n'
                    f'    <div class="col acc"><div class="card" data-zoom="none">{lab}</div></div>')
        elif tpl == 'wide':
            body = (f'{host}\n    <div class="ptrow"><div class="stack"><p class="caprow" data-zoom="none" id="{sid}-lab">{label}</p></div></div>')
        else:
            body = f'{host}\n    <div class="acc"><div class="card" data-zoom="none">{lab}</div></div>'
        out.append(f'''<section class="slide {TPL[tpl]}" id="{sid}" data-title="Bench: {label}" data-sec="Step 02 bench" data-ref="{typ}">
  <h2>{typ}: {stage}</h2>
  <div class="body">
    {body}
  </div>
  <script>Deck.frames('{sid}',[{{stage:'{sid}-sim:{stage}',label:'{stage}',t:0.1}}]);</script>
</section>
''')
out.append('''<footer id="foot"><span id="sec"></span><span id="cue"></span><span id="count"></span></footer>
</main>
<div id="notes" hidden></div>
<div id="overview" hidden></div>
<div id="blank" hidden></div>
<div id="runsheet"></div>
<script>Deck.start()</script>
</body>
</html>
''')
open(os.path.join(os.path.dirname(__file__), 'scratch.html'), 'w', encoding='utf-8').write('\n'.join(out))
print('scratch slides', n, 'animations', len({s[0] for s in SIMS}))
