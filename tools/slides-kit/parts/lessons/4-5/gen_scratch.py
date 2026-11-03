# Writes scratch.html: scratch slides for the Lesson 4.5 animations (workshop steps 02 and 03). Run by build.py 4 5 --scratch;
# never part of a repo build. One slide per animation instance, in the template and host size the deck will use (plan section 5):
# brickBag in t-hook (slide 2), meltScale in t-launch (slide 3), threeSolids in t-concept cw (slide 6), attractions in t-concept cw
# (slides 7, 8, 9; one instance per family), bpPlot in t-concept cw (slides 7 and 9), forceDecider in t-cer (slide 10).
# One frame per stage, labelled with the stage name. The bench captions are not content: data-zoom="none" keeps them out of the zoom cycle,
# so a zoom audit on the bench measures the animations only.
import os

# (host id, animation, template, stages, extra host attributes, extra frames after the stages)
SIMS = [
    ('bb', 'brickBag', 't-hook', ['models', 'shake', 'pour', 'words'], ''),
    ('ms', 'meltScale', 't-launch', ['three', 'melt', 'numbers'], ''),
    ('ts', 'threeSolids', 't-concept cw', ['chlorine', 'within', 'between', 'salt', 'copper'], ''),
    ('ad', 'attractions', 't-concept cw', ['cloud', 'flicker', 'neighbor', 'attract'], ''),
    ('aq', 'attractions', 't-concept cw', ['F2', 'HCl', 'turn', 'face', 'compare'], ''),
    ('ah', 'attractions', 't-concept cw', ['water', 'hbond', 'ammonia', 'methane', 'four'], ''),
    ('bp', 'bpPlot', 't-concept cw', ['axes', 'F2', 'Cl2', 'Br2', 'I2', 'trend', 'trio', 'reveal', 'HCl'], ''),
    ('fd', 'forceDecider', 't-cer', ['NH3/polar', 'NH3/H', 'NH3/lone', 'NH3/strongest', 'CO2/polar', 'CO2/H', 'CO2/strongest',
                                     'HBr/EN', 'HBr/polar', 'HBr/H', 'HBr/strongest'], ''),
]
FAMILY = {'ad': 'dispersion family', 'aq': 'dipole family', 'ah': 'hydrogen family'}


def frames(sid, stages, extra=()):
    rows = ["{stage:'%s-sim:%s',label:'%s'}" % (sid, s, s) for s in stages] + list(extra)
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
        body = (f'<div class="sim" id="{sid}-sim" data-sim="{typ}" style="flex:1 1 auto;min-height:0" aria-label="{typ} animation"></div>\n'
                f'    <p class="line small" data-zoom="none">{cap}</p>\n'
                f'    <div class="card dq reg" id="{sid}-dq" data-label="driving question"><p>How do the forces within and between particles explain the melting point, conductivity and hardness of a substance?</p></div>')
        more = ("{show:'%s-dq',label:'numbers, with the driving question below'}" % sid,)
    elif tpl == 't-cer':
        body = (f'<div class="stack"><p class="hdr" data-zoom="none">{cap}</p></div>\n'
                f'    <div class="stack">{host}</div>')
    else:
        body = f'{host}\n    <div class="col"><div class="card" id="x-{sid}-card" data-zoom="none"><p class="tag">{typ}</p><p class="small">{cap}</p></div></div>'
    out.append(f'''<section class="slide {tpl}" id="x-{sid}" data-title="Scratch: {name}" data-sec="Step 02 scratch" data-ref="{typ}">
  <h2>Scratch: {name}</h2>
  <div class="body">
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
