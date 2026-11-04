# Writes scratch.html: scratch slides for the Lesson 4.5 animations (workshop steps 02 and 03). Run by build.py 4 5 --scratch;
# never part of a repo build. One slide per animation instance, in the template and host size the deck will use (plan section 5):
# brickBag in t-hook (slide 2), meltScale in t-launch (slide 3), threeSolids in t-concept cw (slide 6), attractions in t-concept cw
# (slides 7, 8, 9; one instance per family), bpPlot in t-concept cw (slides 7 and 9), forceDecider in t-cer (slide 10);
# heating (slide 11) and iceLattice (slide 12) in t-concept cw; conductTester in t-concept wide (slide 15, with the 236 px text band
# of .ptrow kept free), in t-example cb (slide 16, the 58/42 split 4.2 uses) and in t-concept cw (slide 17, the dissolve family);
# hammerBlow in t-concept wide (slide 18); networkVsMolecules in t-concept cw (slide 19).
# One frame per stage, labelled with the stage name. The bench captions are not content: data-zoom="none" keeps them out of the zoom cycle,
# so a zoom audit on the bench measures the animations only. The iceLattice slide reveals one caption line on its second frame, for the
# extras audit's reduced-motion block check.
import os

SAMPLES15 = ['NaCl-s', 'NaCl-l', 'NaCl-aq', 'Cu', 'sugar', 'water']
SAMPLES16 = ['KCl-l', 'CaCl2-s']
# (host id, animation, template, stages, extra host attributes)
SIMS = [
    ('bb', 'brickBag', 't-hook', ['models', 'shake', 'pour', 'words'], ''),
    ('ms', 'meltScale', 't-launch', ['snow', 'salt', 'sand', 'melt', 'numbers'], ''),
    ('ts', 'threeSolids', 't-concept cw', ['chlorine', 'within', 'between', 'salt', 'copper'], ''),
    ('ad', 'attractions', 't-concept cw', ['cloud', 'flicker', 'neighbor', 'attract'], ''),
    ('aq', 'attractions', 't-concept cw', ['F2', 'HCl', 'turn', 'face', 'compare'], ''),
    ('ah', 'attractions', 't-concept cw', ['water', 'hbond', 'ammonia', 'methane', 'four'], ''),
    ('bp', 'bpPlot', 't-concept cw', ['axes', 'F2', 'Cl2', 'Br2', 'I2', 'trend', 'trio', 'reveal', 'HCl'], ''),
    ('fd', 'forceDecider', 't-cer', ['empty', 'NH3/polar', 'NH3/H', 'NH3/lone', 'NH3/strongest', 'CO2/polar', 'CO2/H', 'CO2/strongest',
                                     'HBr/EN', 'HBr/polar', 'HBr/H', 'HBr/strongest'], ''),
    ('he', 'heating', 't-concept cw', ['CH4/solid', 'CH4/melt', 'CH4/liquid', 'CH4/boil', 'CH4/gas', 'H2O/solid', 'H2O/boil', 'H2O/gas', 'energy'], ''),
    ('il', 'iceLattice', 't-concept cw', ['molecules', 'hbonds', 'neighbors', 'rings', 'float'], ''),
    ('ct', 'conductTester', 't-concept wide', ['tester'] + [f'{x}/{s}' for x in SAMPLES15 for s in ('predict', 'close', 'zoom')], 'data-reserve="236" '),
    ('cu', 'conductTester', 't-example cb', [f'{x}/{s}' for x in SAMPLES16 for s in ('predict', 'close', 'zoom')], ''),
    ('cd', 'conductTester', 't-concept cw', ['dis/NaCl', 'dis/sucrose', 'dis/CaCO3', 'dis/I2', 'dis/SiO2', 'dis/Cu'], ''),
    ('hb', 'hammerBlow', 't-concept wide', ['before', 'blow', 'shift', 'result'], 'data-reserve="236" '),
    ('nv', 'networkVsMolecules', 't-concept cw', ['co2', 'sublime', 'quartz', 'heat', 'diamond'], ''),
]
FAMILY = {'ad': 'dispersion family', 'aq': 'dipole family', 'ah': 'hydrogen family', 'ct': 'slide 15 samples', 'cu': 'slide 16 samples',
          'cd': 'dissolve family'}


def frames(sid, stages, extra=()):
    rows = ["{stage:'%s-sim:%s',label:'%s'%s}" % (sid, s, s, ",show:'il-note'" if sid == 'il' and i == 1 else '') for i, s in enumerate(stages)] + list(extra)
    return ',\n    '.join(rows)


out = ['<main id="stage">\n<div id="prog"><i></i></div>\n']
for sid, typ, tpl, stages, extra in SIMS:
    name = typ + (' (' + FAMILY[sid] + ')' if sid in FAMILY else '')
    cap = f'{name} · {len(stages)} stages'
    host = f'<div class="sim" id="{sid}-sim" data-sim="{typ}" {extra}aria-label="{typ} animation"></div>'
    more = ()
    if tpl == 't-hook':
        body = f'{host}\n    <div class="stack card band" data-zoom="none"><p class="line" data-zoom="none">{cap}</p></div>'
    elif tpl == 't-launch':
        # the deck shows the driving question under the animation after the last stage: the host shrinks, the drawing refits
        # no bench caption under the host: the deck's slide 3 has none before the driving question, so the host keeps the deck's height
        body = (f'<div class="sim" id="{sid}-sim" data-sim="{typ}" style="flex:1 1 auto;min-height:0" aria-label="{typ} animation"></div>\n'
                f'    <div class="card dq reg" id="{sid}-dq" data-label="driving question"><p>How do the forces within and between particles explain the melting point, conductivity and hardness of a substance?</p></div>')
        more = ("{show:'%s-dq',label:'numbers, with the driving question below'}" % sid,)
    elif tpl == 't-cer':
        body = (f'<div class="stack"><p class="hdr" data-zoom="none">{cap}</p></div>\n'
                f'    <div class="stack">{host}</div>')
    elif tpl == 't-concept wide':
        body = f'{host}\n    <div class="ptrow"><div class="stack"><p class="caprow" data-zoom="none">{cap}</p></div></div>'
    else:
        note = f'<p class="small" id="{sid}-note" data-zoom="none">The lattice turns slowly while the slide shows.</p>' if sid == 'il' else ''
        body = f'{host}\n    <div class="col"><div class="card" id="x-{sid}-card" data-zoom="none"><p class="tag">{typ}</p><p class="small">{cap}</p>{note}</div></div>'
    if sid == 'il':
        more = ()
    style = ' style="grid-template-columns:minmax(0,58fr) minmax(0,42fr)"' if tpl == 't-example cb' else ''
    out.append(f'''<section class="slide {tpl}" id="x-{sid}" data-title="Scratch: {name}" data-sec="Steps 02 and 03 scratch" data-ref="{typ}">
  <h2>Scratch: {name}</h2>
  <div class="body"{style}>
    {body}
  </div>
  <script>Deck.frames('x-{sid}',[
    {frames(sid, stages, more)}
  ]);</script>
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
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratch.html'), 'w', encoding='utf-8', newline='').write('\n'.join(out))
print('scratch slides', len(SIMS), 'stages', sum(len(x[3]) for x in SIMS))
