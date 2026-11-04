# Generates slides.html: the 27 slides of Lesson 4.5 (workshop plan 4-5.md section 5, brief 04). Run by build.py 4 5.
# Pattern: parts/lessons/4-1/gen_slides.py and parts/lessons/4-2/gen_slides.py (slide(), frames(), check(), checkrow(), chips(), rail(),
# checkpoint(), pq(), pa(), the TIMES table). No ellipsis character anywhere: open stems end in a gap, as the sentence frames do.
import json, os, re, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'slides.html')
def js(v): return json.dumps(v, ensure_ascii=False)
# minutes per frame (RULES 9: 0.25 per reveal or stage, 1 per rule card, 0.5 + 0.5 per check and its answer, a timed frame at least its timer)
TIMES = {
 's01':[0.5], 's02':[0.5,0.75,0.5,0.5,0.75], 's03':[0.25,0.25,0.25,0.25,0.5,0.25,0.25,0.5,1], 's04':[0.5,0.75,0.75], 's05':[1,1,0.5],
 's06':[0.5,0.5,0.5,0.5,0.25,0.25,1,0.5,0.5], 's07':[0.25,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,0.5,0.5],
 's08':[0.5,0.5,0.5,0.25,0.25,0.25,1,0.5,0.5], 's09':[0.25,0.5,0.25,0.25,0.25,0.25,0.25,0.25,1,0.5,0.5],
 's10':[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1.5,0.25,0.25,0.25],
 's11':[0.25,0.5,0.25,0.25,0.25,0.25,0.25,0.25,1,0.5,0.5], 's12':[0.25,0.25,0.25,0.5,0.25,0.25,0.25,1,0.5,0.5], 's13':[0.5,0.5,0.5,0.25,1.5],
 's14':[0.25,1.5,0.25,0.25,0.25], 's15':[0.25,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,0.5,0.5],
 's16':[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1.5,0.25,0.25], 's17':[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,0.5,0.5],
 's18':[0.5,0.25,0.25,0.5,0.5,0.25,1,0.5,0.5], 's19':[0.25,0.25,0.25,0.25,0.25,0.25,1,0.5,0.5], 's20':[0.5,0.5,0.5,0.5,0.5],
 's21':[0.5,0.1,0.1,0.1,0.1,0.1], 's22':[0.25,0.5,1,1.5,0.25,0.25], 's23':[0.25,0.5,1,1.5,0.25,0.25], 's24':[0.25,0.5,1,1.5,0.25,0.25],
 's25':[0.5,0.5,0.5,0.5,0.5,3,0.25,0.25], 's26':[0.5,0.2,0.2,0.2,0.2,0.2], 's27':[0.5]}
BUDGET = json.load(open(os.path.join(HERE, 'budget.json'), encoding='utf-8'))
for k, v in TIMES.items():
    assert abs(sum(v) - BUDGET[k]) < 1e-9, (k, sum(v), BUDGET[k])
KEEP = ('-rule', '-cap', '-sim', '-plot', '-row')
def frames(sid, fr):
    assert len(TIMES[sid]) == len(fr), (sid, len(TIMES[sid]), len(fr))
    for f, t in zip(fr, TIMES[sid]): f['t'] = t
    # the check frame of a concept slide: every earlier card leaves the column except the rule (a stacked check needs the room)
    vis = []
    for f in fr:
        if f.pop('clear', False):
            h = [x for x in (f.get('hide') or []) if isinstance(f.get('hide'), list)] or ([f['hide']] if isinstance(f.get('hide'), str) else [])
            f['hide'] = h + [x for x in vis if x not in h and not x.endswith(KEEP)]
        for x in ([f['show']] if isinstance(f.get('show'), str) else f.get('show') or []):
            if x not in vis: vis.append(x)
        for x in ([f['hide']] if isinstance(f.get('hide'), str) else f.get('hide') or []):
            if x in vis: vis.remove(x)
    rows = []
    for f in fr:
        rows.append('{' + ','.join(f"{k}:{js(f[k])}" for k in ['show','hide','stage','cls','timer','focus','label','cue','t','note'] if k in f) + '}')
    return f"<script>Deck.frames('{sid}',[\n    " + ',\n    '.join(rows) + "\n  ]);</script>"
def slide(sid, cls, title, sec, ref, body, notes, fr, pre=''):
    per = '1' if int(sid[1:]) <= 13 else '2'
    return f'''<section class="slide {cls}" id="{sid}" data-period="{per}" data-title="{title}" data-sec="{sec}" data-ref="{ref}">
  {pre}<h2>{title}</h2>
  <div class="body">
{body}
  </div>
  <aside class="notes">{notes}</aside>
  {frames(sid, fr)}
</section>
'''
def nwords(t): return len(re.sub(r'<[^>]+>', '', t).split())
def lay(opts, col=None):
    # one row when every option is two words or fewer, else stacked; the runtime stacks a row that does not fit
    return 'col' if (col if col is not None else max(nwords(o) for o in opts) > 2) else 'row'
def optli(p, opts, right, fb):
    out = ''
    for l, t, f in zip('ABC', opts, fb or [None] * 3):
        g = f' data-ok="{1 if l == right else 0}" data-fb="{H.escape(f, quote=True)}"' if f is not None else ''
        out += f'<li class="opt" id="{p}-{l.lower()}"{g}><b>{l}</b><span>{t}</span></li>'
    return out
def check(p, q, opts, label='check', col=None, ans='', right=None, fb=None, pre=''):
    L = lay(opts, col)
    return f'''      <div class="card check" id="{p}-check" data-label="{label}">
        <p class="tag">Check</p>{pre}
        <p class="q">{q}</p>
        <ol class="opts{' col1' if L == 'col' else ''}" data-lay="{L}">{optli(p, opts, right, fb)}</ol>
        <div class="af"><p class="ans" id="{p}-ans" data-label="answer">{ans}</p><p class="fb" aria-live="polite"></p></div>
      </div>'''
def checkrow(p, q, opts, ans, right=None, fb=None):
    # the check of a wide slide, in the text band under the animation: the question stays; the answer or a mouse feedback line shows
    # under the options; stacked options get the compact band layout (lesson css .checkrow.stk)
    L = lay(opts)
    return f'''      <div class="checkrow{' stk' if L == 'col' else ''}" id="{p}-check" data-label="check">
        <p class="q" id="{p}-q"><span class="tag">Check:</span> {q}</p>
        <ol class="opts{' col1' if L == 'col' else ''}" data-lay="{L}">{optli(p, opts, right, fb)}</ol>
        <div class="af"><p class="ans" id="{p}-ans" data-label="answer">{ans}</p><p class="fb" aria-live="polite"></p></div>
      </div>'''
def chips(label, items, i=''):
    # a value list with its meaning: a label line, then one chip per value
    return f'<span class="enrow"{i}><span class="enl lbl">{label}</span><span class="chips">' + ''.join(f'<span class="chip"><span>{x}</span></span>' for x in items) + '</span></span>'
def use(i, label, cls=''):
    return f'<svg class="{cls}" viewBox="0 0 100 100" role="img" aria-label="{label}"><use href="#{i}"/></svg>'
def rail(p, names=('Think','Talk','Write','Self-check','Compare')):
    return '<ol class="rail">' + ''.join(f'<li id="{p}-r{k+1}">{t}</li>' for k, t in enumerate(names)) + '</ol>'
GAP = '<span class="gap"></span>'
CAP = 'Atom colors show the element, not the charge.'

SPRITE = '''<svg class="sprite" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden"><defs>
<symbol id="ic-next" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M48 30v40l32-20Z" class="f-acc"/></symbol>
<symbol id="ic-back" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M72 30v40L40 50Z" class="f-acc"/></symbol>
<symbol id="ic-blank" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><rect x="34" y="30" width="52" height="34" rx="4" class="f-ink"/><path d="M52 74h16" class="k-ink" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-start" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M30 34v-8h10M90 34v-8H80M30 66v8h10M90 66v8H80" fill="none" class="k-acc" stroke-width="5" stroke-linecap="round"/><path d="M52 38v24l20-12Z" class="f-acc"/></symbol>
<symbol id="ic-inter" viewBox="0 0 100 100"><path d="M10 50h22M68 50h22" class="k-stick" stroke-width="9" stroke-linecap="round"/><circle cx="12" cy="50" r="10" class="f-nm k-ink" stroke-width="2"/><circle cx="32" cy="50" r="10" class="f-nm k-ink" stroke-width="2"/><circle cx="68" cy="50" r="10" class="f-nm k-ink" stroke-width="2"/><circle cx="88" cy="50" r="10" class="f-nm k-ink" stroke-width="2"/><path d="M44 50h12" class="k-muted" stroke-width="5" stroke-dasharray="4 4"/><path d="M42 72h16" class="k-muted" stroke-width="5" stroke-dasharray="4 4"/><path d="M42 28h16" class="k-muted" stroke-width="5" stroke-dasharray="4 4"/></symbol>
<symbol id="ic-disp" viewBox="0 0 100 100"><ellipse cx="50" cy="50" rx="44" ry="32" class="f-sea k-e" stroke-width="3"/><circle cx="66" cy="40" r="7" class="f-e"/><circle cx="76" cy="54" r="7" class="f-e"/><circle cx="62" cy="62" r="7" class="f-e"/><circle cx="80" cy="38" r="6" class="f-e"/><circle cx="30" cy="50" r="7" class="f-ink"/><path d="M16 20h12M22 14v12" class="k-dp" stroke-width="5" stroke-linecap="round"/><path d="M74 88h12" class="k-dm" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-dipole" viewBox="0 0 100 100"><circle cx="16" cy="50" r="12" class="f-dp"/><circle cx="38" cy="50" r="14" class="f-dm"/><circle cx="62" cy="50" r="12" class="f-dp"/><circle cx="84" cy="50" r="14" class="f-dm"/><path d="M10 50h12M16 44v12M56 50h12M62 44v12" class="k-on" stroke-width="4" stroke-linecap="round"/><path d="M32 50h12M78 50h12" class="k-on" stroke-width="4" stroke-linecap="round"/><path d="M38 76Q50 88 62 76" fill="none" class="k-dm" stroke-width="5" stroke-dasharray="5 4"/></symbol>
<symbol id="ic-hbond" viewBox="0 0 100 100"><path d="M26 40 12 64M26 40l20 18" class="k-stick" stroke-width="8" stroke-linecap="round"/><circle cx="26" cy="38" r="16" class="f-o k-ink" stroke-width="2"/><circle cx="12" cy="66" r="10" class="f-white k-ink" stroke-width="2"/><circle cx="48" cy="60" r="10" class="f-white k-ink" stroke-width="2"/><path d="M58 60h14" class="k-dm" stroke-width="6" stroke-dasharray="5 4"/><ellipse cx="78" cy="60" rx="10" ry="7" class="f-sea k-e" stroke-width="2"/><circle cx="90" cy="54" r="10" class="f-o k-ink" stroke-width="2"/></symbol>
<symbol id="ic-electrolyte" viewBox="0 0 100 100"><path d="M18 14v70a6 6 0 0 0 6 6h52a6 6 0 0 0 6-6V14" fill="none" class="k-ink" stroke-width="4"/><path d="M20 40h60v44a4 4 0 0 1-4 4H24a4 4 0 0 1-4-4Z" class="f-water"/><circle cx="36" cy="56" r="10" class="f-cat"/><circle cx="64" cy="70" r="12" class="f-an"/><circle cx="60" cy="50" r="8" class="f-cat"/><path d="M30 56h12M36 50v12M58 70h12M56 50h8M60 46v8" class="k-on" stroke-width="3" stroke-linecap="round"/></symbol>
<symbol id="ic-malleable" viewBox="0 0 100 100"><rect x="30" y="8" width="40" height="18" rx="4" class="f-metal k-ink" stroke-width="2"/><path d="M58 26l16 26" class="k-wood" stroke-width="8" stroke-linecap="round"/><path d="M8 76q42-30 84 0" fill="none" class="k-copper" stroke-width="12" stroke-linecap="round"/></symbol>
<symbol id="ic-brittle" viewBox="0 0 100 100"><rect x="14" y="20" width="72" height="66" rx="6" class="f-white k-ink" stroke-width="3"/><path d="M14 44h72M14 66h72M38 20v66M62 20v66" class="k-line" stroke-width="2"/><path d="M48 18 40 36l14 10-12 14 10 12-8 16" fill="none" class="k-bad" stroke-width="5" stroke-linejoin="round"/></symbol>
<symbol id="ic-network" viewBox="0 0 100 100"><path d="M20 20 50 32 80 20M20 20v30M50 32v30M80 20v30M20 50l30 12 30-12M20 50v30M50 62v26M80 50v30M20 80l30 8 30-8" fill="none" class="k-stick" stroke-width="5"/><g class="f-nm k-ink" stroke-width="2"><circle cx="20" cy="20" r="8"/><circle cx="50" cy="32" r="8"/><circle cx="80" cy="20" r="8"/><circle cx="20" cy="50" r="8"/><circle cx="50" cy="62" r="8"/><circle cx="80" cy="50" r="8"/><circle cx="20" cy="80" r="8"/><circle cx="50" cy="88" r="8"/><circle cx="80" cy="80" r="8"/></g></symbol>
<symbol id="ic-rank" viewBox="0 0 100 100"><rect x="10" y="64" width="18" height="24" rx="3" class="f-acc"/><rect x="36" y="44" width="18" height="44" rx="3" class="f-acc"/><rect x="62" y="20" width="18" height="68" rx="3" class="f-acc"/><path d="M90 12v58" class="k-ink" stroke-width="6" stroke-linecap="round"/><circle cx="90" cy="78" r="9" class="f-dp k-ink" stroke-width="2"/><path d="M90 30v42" class="k-dp" stroke-width="3"/></symbol>
<symbol id="ic-s-nacl" viewBox="0 0 100 100"><rect x="12" y="52" width="30" height="30" class="f-white k-ink" stroke-width="3"/><rect x="46" y="44" width="38" height="38" class="f-white k-ink" stroke-width="3"/><rect x="26" y="20" width="28" height="28" class="f-white k-ink" stroke-width="3"/></symbol>
<symbol id="ic-s-sugar" viewBox="0 0 100 100"><rect x="14" y="46" width="34" height="34" rx="4" class="f-sugar k-ink" stroke-width="3"/><rect x="52" y="46" width="34" height="34" rx="4" class="f-sugar k-ink" stroke-width="3"/><rect x="33" y="12" width="34" height="34" rx="4" class="f-sugar k-ink" stroke-width="3"/></symbol>
<symbol id="ic-s-caco3" viewBox="0 0 100 100"><path d="M50 84C26 84 10 66 12 44 22 50 30 30 50 18c20 12 28 32 38 26 2 22-14 40-38 40Z" class="f-shell k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M50 84V26M50 84 28 40M50 84l22-44" class="k-muted" stroke-width="3"/></symbol>
<symbol id="ic-s-i2" viewBox="0 0 100 100"><path d="M14 70 30 40l20 8-6 30Z" class="f-iodine k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M50 82 58 30l28 10-6 38Z" class="f-iodine k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M36 36 44 18l14 6-4 18Z" class="f-iodine k-ink" stroke-width="3" stroke-linejoin="round"/></symbol>
<symbol id="ic-s-sio2" viewBox="0 0 100 100"><path d="M36 88V34l14-24 14 24v54Z" class="f-quartz k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M50 10v78M36 34h28" class="k-line" stroke-width="2"/><path d="M14 88V54l10-16 10 16v34Z" class="f-quartz k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M66 88V58l10-16 10 16v30Z" class="f-quartz k-ink" stroke-width="3" stroke-linejoin="round"/></symbol>
<symbol id="ic-s-cu" viewBox="0 0 100 100"><path d="M16 60c0-22 18-38 38-36s34 18 30 38-22 28-40 26-28-10-28-28Z" class="f-copper k-ink" stroke-width="3"/><path d="M36 46c8-8 20-10 30-4" fill="none" class="k-on" stroke-width="5" stroke-linecap="round" opacity=".7"/></symbol>
</defs></svg>'''

S = []
# the driving question on the slides (review 04, F3): two sentences with the blueprint's terms; the reading and the blueprint keep the original
DQ = 'Forces act within and between particles. How do they explain melting point, conductivity and hardness?'
SAFETY = ('<b>Safety.</b> Nothing is demonstrated in this lesson. Dry ice and molten salt are only described: dry ice (−78.5 °C) burns skin and its gas can '
          'build up in a closed space; molten salt is above 801 °C. If a real conductivity tester is used, it is a low-voltage battery tester, '
          'and the salt water stays away from wall outlets. ')
SOURCES = ('<b>Data and sources.</b> Melting and boiling points at 1 atm: NIST WebBook and PubChem (CH₄ −182.5 and −161.5 °C; F₂ −188.1, Cl₂ −34.0, '
           'Br₂ 58.8, I₂ 184.4, NH₃ −33.3, HCl −85.1, H₂O 100.0 °C; NaCl 801 °C; Cu 1085 °C; quartz near 1700 °C; CO₂ sublimes at −78.5 °C). '
           'CRC Handbook: densities at 0 °C, ice 0.9167 g/cm³, water 0.99984 g/cm³; calcium carbonate is sparingly soluble. OpenStax Chemistry 2e '
           '10.1 (intermolecular forces), 10.3 (phase transitions: 40.7 kJ to boil 18 g of water), 7.5 (bond strength: about 928 kJ to break its O–H bonds), '
           '10.5 (the solid state). Radii: covalent, Cordero 2008 (ball-and-stick); van der Waals, Alvarez 2013 (space filling); ions, Shannon 1976 '
           '(Na⁺ 102 pm, Cl⁻ 181 pm; NaCl spacing 282 pm); Cu 128 pm metallic radius. Ice: O···O 276 pm, ideal hexagonal oxygen framework, hydrogen '
           'directions simplified. Fritz London named dispersion forces in 1930. Electronegativity: Pauling values (H 2.20, Br 2.96). ')
CLICKER = ('<b>Clicker.</b> Logitech R800: Next = PageDown, Back = PageUp (while zoomed: exit the zoom), Start/stop = F5 then Escape, Blank = period. '
           'Blank zooms one part of the slide per press, animation first; the press after the last part exits; two fast presses on an unzoomed '
           'slide blank the screen. Mouse: click an option to mark it right or wrong; click the slide number or the section label for the slide list. '
           'Laptop: N notes, O overview, T theme, Ctrl+P run-sheet.')

# ---------- 1 cover
S.append(slide('s01','t-cover','Bonds, forces and properties','Lesson 4.5','Reading §4.5',f'''    <div class="card dq reg"><p class="tag">Driving question</p><p>{DQ}</p></div>
    <div class="r800">
      <div class="key"><svg viewBox="0 0 120 100" role="img" aria-label="Next button"><use href="#ic-next"/></svg><b>Next</b><span>next step</span></div>
      <div class="key"><svg viewBox="0 0 120 100" role="img" aria-label="Back button"><use href="#ic-back"/></svg><b>Back</b><span>one step back</span></div>
      <div class="key"><svg viewBox="0 0 120 100" role="img" aria-label="Blank button"><use href="#ic-blank"/></svg><b>Blank</b><span>zoom part by part<br>twice fast: blank</span></div>
      <div class="key"><svg viewBox="0 0 120 100" role="img" aria-label="Start button"><use href="#ic-start"/></svg><b>Start</b><span>full screen</span></div>
    </div>''',
 SAFETY + SOURCES + CLICKER,
 [dict(note='Two periods. Read the driving question aloud; students copy it. Show the four clicker buttons once, so a zoom or a blank screen is on purpose. Thread of the lesson: what comes apart, what stays.')]))

# ---------- 2 hook: shake the bag
S.append(slide('s02','t-hook','Shake the bag','Hook','Reading §4.5.1','''    <div class="sim" id="s02-sim" data-sim="brickBag" aria-label="Three small brick models in a clear bag; shaken, they tumble apart, but no brick comes off."></div>
    <div class="stack card band">
      <p class="line" id="s02-l0">Each model is a few bricks snapped together.</p>
      <p class="line" id="s02-l1" data-label="predict">Shake the bag. What comes apart?</p>
      <p class="line" id="s02-l2" data-label="shake">The models move apart. Every brick stays snapped on.</p>
      <p class="line" id="s02-l3" data-label="pour">Pour them out: they spread far apart, still whole.</p>
      <div id="s02-l4" data-label="the two words"><p class="line two">A snap between two bricks is a bond within a molecule.</p><p class="line two">Two models side by side feel an attraction between molecules.</p></div>
    </div>''',
 'Narrative thread for 4.5: what comes apart, what stays. The bricks are atoms, a snap is a bond within, a whole model is a molecule; models that sit side by side only touch, an attraction between. Slide 6 names both.',
 [dict(show='s02-l0',stage='s02-sim:models',note='Everyday scene: three small brick models in a bag. Ask: who has built with snap-together bricks? No chemistry yet.'),
  dict(hide='s02-l0',show='s02-l1',note='Prediction: take one answer per table. Collect "the bricks come off" and "the models separate". Do not confirm.'),
  dict(hide='s02-l1',show='s02-l2',stage='s02-sim:shake',note='The models tumble apart; the counter stays at 11 of 11. Ask: what came apart, and what stayed?'),
  dict(hide='s02-l2',show='s02-l3',stage='s02-sim:pour',note='Spread far apart, every model still whole. Misconception to listen for: "shaking breaks the models" (it only separates them).'),
  dict(hide='s02-l3',show='s02-l4',stage='s02-sim:words',note='The two ideas of the lesson in kid words: a snap is a bond within; side by side is an attraction between. Students write both lines.')]))

# ---------- 3 launch: snow day
S.append(slide('s03','t-launch','Snow day','Launch','Reading §4.5 opener',f'''    <div class="sim" id="s03-sim" data-sim="meltScale" style="flex:1 1 auto;min-height:0" aria-label="A snowman, salt on the steps and a sandbox above their particles; a melting-point scale below."></div>
    <div class="lrow" id="s03-row">
      <div class="stack">
        <p class="caprow" id="s03-c1" data-label="snow">A snowman is gone by noon.</p>
        <p class="caprow" id="s03-c2" data-label="salt">Salt on the steps is there all year.</p>
        <p class="caprow" id="s03-c3" data-label="sand">Sand in the sandbox never melts.</p>
        <p class="caprow" id="s03-c4" data-label="bonds">Bonds hold all three together.</p>
        <p class="caprow" id="s03-c5" data-label="predict">What comes apart when snow melts?</p>
      </div>
      <p class="simcap" id="s03-cap" data-zoom="caption">{CAP}</p>
    </div>
    <div class="card dq reg" id="s03-dq" data-label="driving question"><p>{DQ}</p></div>
    <div class="qrow" id="s03-st" data-label="write 60 s"><ol class="frames"><li>I think snow melts by noon but sand never melts because {GAP}.</li></ol><div class="timer"></div></div>''',
 'The reading opener: methane melts at −182.5 °C, salt stays solid until 801 °C, quartz (the main mineral in sand) melts near 1700 °C. "The difference lies in what must come apart when each solid melts." Snow is water molecules; salt is Na⁺ and Cl⁻ ions (red and blue); sand is a network of Si and O atoms (CPK colors), hence the caption.',
 [dict(show=['s03-row','s03-c1','s03-cap'],stage='s03-sim:snow',note='A snowman: water molecules. Ask: where does a snowman go on a sunny day?'),
  dict(hide='s03-c1',show='s03-c2',stage='s03-sim:salt',note='Salt on the steps: Na⁺ and Cl⁻ ions drawn to scale. It is there all year.'),
  dict(hide='s03-c2',show='s03-c3',stage='s03-sim:sand',note='Sand in the sandbox: silicon and oxygen atoms in one network. It never melts in any weather.'),
  dict(hide='s03-c3',show='s03-c4',note='Bonds hold every one of the three solids together. Yet they melt at very different temperatures.'),
  dict(hide='s03-c4',show='s03-c5',note='Prediction: what comes apart when snow melts? Collect two answers. Listen for "the water molecules break" (they do not).'),
  dict(stage='s03-sim:melt',label='melt the snow',note='The water molecules let go of each other and drift, each one whole. Salt and sand do not move.'),
  dict(stage='s03-sim:numbers',label='the numbers',note='Melting points: snow 0.0 °C, salt 801 °C, sand near 1700 °C. Ask: which forces must come apart in each?'),
  dict(hide=['s03-row'],show='s03-dq',note='Read the driving question; students copy it at the top of the notebook page.'),
  dict(show='s03-st',timer=60,note='Sixty seconds with the starter. Collect two answers; do not correct yet. Listen for "salt and sand have stronger bonds" and for "nothing breaks when snow melts".')]))

# ---------- 4 predict now
def pq(p, n, q, opts, lab):
    o = ''.join(f'<li class="opt"><b>{l}</b><span>{t}</span></li>' for l, t in zip('ABC', opts))
    return f'      <div class="card check" id="{p}" data-label="{lab}" data-mode="pick"><p class="tag">Question {n}</p><p class="q">{q}</p><ol class="opts col1" data-lay="col">{o}</ol></div>'
PQ = [('When water boils, the bubbles hold ' + GAP + '.', ['H<sub>2</sub>O molecules','H and O atoms','hydrogen gas and oxygen gas']),
      ('Solid table salt ' + GAP + '.', ['conducts, it is made of ions','does not conduct','conducts with electrons']),
      ('A hydrogen bond is ' + GAP + '.', ['a covalent bond','an attraction between molecules','an ionic bond'])]
S.append(slide('s04','t-routine','Predict now','Predict','Reading §4.5 Before you read',f'''    <div class="card prompt"><p>Hands up: one finger for A, two for B, three for C. Write your letter.</p></div>
    <div class="stack top">
{pq('s04-q1',1,PQ[0][0],PQ[0][1],'question 1')}
{pq('s04-q2',2,PQ[1][0],PQ[1][1],'question 2')}
{pq('s04-q3',3,PQ[2][0],PQ[2][1],'question 3')}
    </div>''',
 'No answers on this slide. Students keep their letters; slide 25 returns all three answers.',
 [dict(show='s04-q1',note='Count hands for A, B, C and write the counts on the board. Do not react to the choices. A mouse click on an option only highlights it; there is no grading on this slide.'),
  dict(hide='s04-q1',show='s04-q2',note='Count hands. Many choose A: "it is made of ions, so it conducts".'),
  dict(hide='s04-q2',show='s04-q3',note='Count hands. Many choose A: the word "bond" in the name. Keep the counts for slide 25.')]))

# ---------- 5 targets and words
W = [('ic-inter','intermolecular force','fuerza intermolecular','a pull between separate molecules'),
     ('ic-disp','dispersion forces','fuerzas de dispersión','weak pulls between all molecules'),
     ('ic-dipole','dipole-dipole forces','fuerzas dipolo-dipolo','δ+ of one pulls δ− of the next'),
     ('ic-hbond','hydrogen bonding','enlace de hidrógeno','H on N, O or F pulled to a lone pair'),
     ('ic-electrolyte','electrolyte','electrolito','forms ions in water'),
     ('ic-malleable','malleable','maleable','bends under a hammer'),
     ('ic-brittle','brittle','frágil','splits under a sharp blow'),
     ('ic-network','covalent network solid','sólido de red covalente','one giant network of bonds')]
wc = '\n'.join(f'        <div class="wcard">{use(i,"Icon: "+t)}<p class="t">{t} <span class="es">({es})</span></p><p class="m">{m}</p></div>' for i,t,es,m in W)
ICAN = [('4.5.1','tell bonds within from attractions between molecules.'),('4.5.2','name the strongest attraction between molecules.'),
        ('4.5.3','explain melting and boiling, and why ice floats.'),('4.5.4','explain what conducts and what dissolves.'),
        ('4.5.5','explain what bends, splits or is very hard.')]
S.append(slide('s05','t-words','Targets and words','Targets','Reading §4.5 Vocabulary',f'''    <div class="stack">
      <div class="card" id="s05-ican" data-label="targets"><p class="tag">I can</p><ul class="ican">
''' + '\n'.join(f'        <li><b>{a}</b>{b}</li>' for a, b in ICAN) + f'''</ul></div>
      <div class="words" id="s05-words" data-label="words">
{wc}
      </div>
    </div>
    <div class="legend" id="s05-leg" data-label="color code"><span><i class="i-cat">+</i>cation</span><span><i class="i-an">−</i>anion</span><span><i class="e"></i>electron</span><span><i class="i-metal"> </i>metal</span><span><i class="i-nm"> </i>nonmetal</span><span><i class="i-dp">δ+</i>small +</span><span><i class="i-dm">δ−</i>small −</span><span><i class="stk"></i>solid stick = bond within</span><span><i class="dsh"></i>dashed line = attraction between</span></div>''',
 'The color code is the unit code of Lessons 4.1 and 4.2, plus two marks for this lesson: a solid gray stick is a bond within a molecule, a dashed line is an attraction between molecules. Dispersion lines are gray, dipole-dipole lines run from δ+ (warm) to δ− (teal), hydrogen bonds are teal and heavier. Ball-and-stick atoms use CPK colors with the symbol on every sphere.',
 [dict(show='s05-ican',note='Read the five targets. Students copy 4.5.1 to 4.5.5; they rate themselves on slide 26.'),
  dict(hide='s05-ican',show='s05-words',note='Choral reading: English term, then the Spanish cognate. Students add the words to the glossary with the icon. "Intermolecular" means between molecules.'),
  dict(show='s05-leg',note='Same color code as Lessons 4.1 and 4.2. New: the solid stick (bond within) and the dashed line (attraction between).')]))

# ---------- 6 bonds within, attractions between
S.append(slide('s06','t-concept cw','Bonds within, attractions between','Bonds and attractions','Reading §4.5.1',f'''    <div class="sim" id="s06-sim" data-sim="threeSolids" aria-label="Chlorine molecules, a salt crystal and a layer of copper."></div>
    <div class="rcol"><div class="col acc">
      <div class="card" id="s06-c0" data-label="chlorine"><p class="tag">Chlorine</p><p>Chlorine is made of Cl<sub>2</sub> molecules.</p></div>
      <div class="card" id="s06-pred" data-label="predict"><p class="tag">Predict</p><p>Which pull is stronger: inside a molecule, or between two?</p></div>
      <div class="card" id="s06-c1" data-label="bond within"><p class="tag">Bond within</p><p>A covalent bond joins the two atoms. That is a bond within.</p></div>
      <div class="card" id="s06-c2" data-label="attraction between"><p class="tag">Attraction between</p><p>Weak attractions hold neighboring molecules close, much weaker than the bond.</p></div>
      <div class="card" id="s06-c3" data-label="salt"><p class="tag">Salt</p><p>Salt has no molecules. Ionic bonds run through the whole crystal.</p></div>
      <div class="card" id="s06-c4" data-label="copper"><p class="tag">Copper</p><p>Copper has no molecules. Metallic bonds run through the whole metal.</p></div>
      <div class="card rule reg" id="s06-rule" data-label="rule"><p class="tag">Rule</p><p>Bonds hold atoms or ions together in a substance. Much weaker attractions act between molecules.</p></div>
{check('s06','In liquid chlorine, what holds neighboring Cl<sub>2</sub> molecules near each other?',['weak attractions between molecules','covalent bonds between molecules','ionic bonds'],ans='A. The Cl–Cl bond is inside each molecule. Only weak attractions act between molecules.',right='A',
  fb=['Between molecules there are only weak attractions.','A covalent bond joins the two atoms inside one molecule, not two molecules.','Chlorine is neutral molecules, not ions. It has no ionic bonds.'])}
    </div><p class="simcap" id="s06-cap" data-label="colors" data-zoom="caption">{CAP}</p></div>''',
 'The TEKS call bonds "intramolecular forces", even though ionic and metallic crystals contain no molecules; the reading says "bonds within a substance" for that reason. Attractions between molecules are the "intermolecular forces" of slide 5. Atom colors are CPK (Cl green); the salt ions keep the unit code (Na⁺ red, Cl⁻ blue), hence the caption.',
 [dict(show=['s06-c0','s06-cap'],stage='s06-sim:chlorine',focus='s06-sim',note='Cl₂ molecules, ball-and-stick, Cl green. Ask: how many atoms in each molecule? (two).'),
  dict(show='s06-pred',note='Prediction: hands up for "inside" or "between". Most say inside; ask why.'),
  dict(hide='s06-pred',show='s06-c1',stage='s06-sim:within',note='The stick inside each molecule glows: a covalent bond, a bond within.'),
  dict(show='s06-c2',stage='s06-sim:between',note='Dashed gray lines between neighbors flicker: attractions between, much weaker. Thread: in liquid chlorine these let go; the bonds stay.'),
  dict(show='s06-c3',stage='s06-sim:salt',note='Salt: Na⁺ 102 pm and Cl⁻ 181 pm at 282 pm. No molecules: ionic bonds run through the whole crystal.'),
  dict(show='s06-c4',stage='s06-sim:copper',note='Copper: gray + cations in a sea of violet − electrons (Lesson 4.1). Metallic bonds through the whole metal.'),
  dict(show='s06-rule',note='Students copy the rule. Misconception to listen for: "molecules are held to each other by bonds" (only by much weaker attractions).'),
  dict(clear=True,hide=['s06-cap','s06-rule'],show='s06-check',stage='s06-sim:between',note='Hands up for A, B or C. The chlorine picture with the dashed attractions is back on screen: the check\'s subject.'),
  dict(show='s06-ans',cls={'s06-a':'right','s06-check':'done'},note='A is right. B (covalent bonds between the molecules): a covalent bond joins the two atoms inside one molecule. C (ionic bonds): chlorine is neutral molecules, not ions.')]))

# ---------- 7 dispersion forces (two hosts in a stack: attractions, then bpPlot)
S.append(slide('s07','t-concept cw','Dispersion forces','Dispersion forces','Reading §4.5.1',f'''    <div class="stack">
      <div class="sim" id="s07-sim" data-sim="attractions" aria-label="Two nonpolar molecules as electron clouds; for an instant the electrons crowd to one end."></div>
      <div class="sim" id="s07-plot" data-sim="bpPlot" aria-label="Boiling point against electrons per molecule for the halogens."></div>
    </div>
    <div class="col acc">
      <div class="card" id="s07-c0" data-label="electrons move"><p class="tag">Electrons</p><p>Electrons in a molecule always move.</p></div>
      <div class="card" id="s07-pred" data-label="predict"><p class="tag">Predict</p><p>For an instant, where could more electrons sit?</p></div>
      <div class="card" id="s07-c1" data-label="flicker"><p class="tag">For an instant</p><p>One end is δ− for an instant. The other end is δ+.</p></div>
      <div class="card" id="s07-c2" data-label="attract"><p class="tag">Attraction</p><p>The brief charges pull a neighbor. New ones keep forming: dispersion forces.</p></div>
      <div class="card" id="s07-c3" data-label="the plot"><p class="tag">Evidence</p><p>Boiling point against electrons per molecule.</p></div>
      <div class="card rule reg" id="s07-rule" data-label="rule"><p class="tag">Rule</p><p>Dispersion forces act between all molecules. More electrons make stronger dispersion forces. Stronger forces mean a higher boiling point.</p></div>
{check('s07','Why does bromine boil higher than chlorine?',['Br<sub>2</sub> has more electrons, so stronger dispersion forces.','Br<sub>2</sub> is polar.','Boiling must break the Br–Br bond.'],ans='A. Br<sub>2</sub> has 70 electrons and Cl<sub>2</sub> has 34. Both are nonpolar.',right='A',col=True,
  fb=['More electrons give stronger dispersion forces.','Both atoms in Br<sub>2</sub> are the same, so it is nonpolar.','Boiling separates whole Br<sub>2</sub> molecules. The Br–Br bond stays.'])}
    </div>''',
 'Fritz London explained these forces in 1930, so they are also called London dispersion forces. Halogens at 25 °C: F₂ and Cl₂ are gases, Br₂ is a liquid, I₂ is a solid; the plot shows why. The δ signs here last only an instant, unlike the lasting δ signs of a polar bond (slide 8).',
 [dict(show='s07-c0',stage='s07-sim:cloud',focus='s07-sim',note='Two nonpolar molecules drawn as electron clouds with moving violet dots. Ask: are electrons ever still?'),
  dict(show='s07-pred',note='Prediction: point to where the electrons could crowd. Collect two answers.'),
  dict(hide='s07-pred',show='s07-c1',stage='s07-sim:flicker',note='For an instant the dots crowd to one end: δ− there, δ+ at the other end. Say: "a small negative charge, for an instant".'),
  dict(stage='s07-sim:neighbor',label='the neighbor',note='The neighbor\'s cloud shifts the same way. Ask: which end of the neighbor faces the δ− end? (its δ+ end).'),
  dict(show='s07-c2',stage='s07-sim:attract',note='The dashed gray line forms, fades and forms again: dispersion forces act between all molecules.'),
  dict(hide=['s07-sim','s07-c0','s07-c1'],show=['s07-plot','s07-c3'],stage='s07-plot:axes',focus='s07-plot',note='Evidence: boiling point against electrons per molecule. Read the two axes with the class.'),
  dict(stage='s07-plot:F2',label='F₂',note='F₂: 18 electrons, boils at −188.1 °C. A gas at room temperature.'),
  dict(stage='s07-plot:Cl2',label='Cl₂',note='Cl₂: 34 electrons, −34.0 °C. Still a gas at 25 °C.'),
  dict(stage='s07-plot:Br2',label='Br₂',note='Br₂: 70 electrons, 58.8 °C: a liquid at room temperature.'),
  dict(stage='s07-plot:I2',label='I₂',note='I₂: 106 electrons, 184.4 °C: a solid at room temperature.'),
  dict(stage='s07-plot:trend',label='the trend',note='The dashed line: more electrons, higher boiling point. All four are nonpolar, so only dispersion forces differ.'),
  dict(show='s07-rule',note='Students copy the rule. Misconception to listen for: "the I–I bond is stronger, so iodine boils higher" (boiling does not break the bond).'),
  dict(clear=True,hide='s07-c3',show='s07-check',note='Hands up for A, B or C. The plot with Cl₂ and Br₂ is on screen.'),
  dict(show='s07-ans',cls={'s07-a':'right','s07-check':'done'},note='A is right. B (Br₂ is polar): both atoms are the same, so Br₂ is nonpolar. C (boiling breaks the Br–Br bond): boiling separates whole Br₂ molecules; the bond stays.')]))

# ---------- 8 dipole-dipole forces
S.append(slide('s08','t-concept cw','Dipole-dipole forces','Dipole-dipole forces','Reading §4.5.2',f'''    <div class="sim" id="s08-sim" data-sim="attractions" aria-label="Two F2 molecules, then two HCl molecules that turn so the δ+ end of one faces the δ− end of the next."></div>
    <div class="col acc">
      <div class="card" id="s08-c0" data-label="F₂"><p class="tag">F<sub>2</sub></p><p>F<sub>2</sub> is nonpolar. It has dispersion forces only.</p></div>
      <div class="card" id="s08-c1" data-label="HCl"><p class="tag">HCl</p><p>HCl is polar: δ+ on H, δ− on Cl (Lesson 4.4).</p></div>
      <div class="card" id="s08-pred" data-label="predict"><p class="tag">Predict</p><p>How will two HCl molecules line up?</p></div>
      <div class="card" id="s08-c2" data-label="face"><p class="tag">Dipole-dipole forces</p><p>The δ+ end of one pulls the δ− end of the next: dipole-dipole forces.</p></div>
      <div class="card" id="s08-c3" data-label="compare"><p class="tag">Compare</p><p>Both have 18 electrons. HCl boils about 100 °C higher.</p></div>
      <div class="card rule reg" id="s08-rule" data-label="rule"><p class="tag">Rule</p><p>Polar molecules pull each other. These pulls are dipole-dipole forces. They keep dispersion forces too.</p></div>
{check('s08','Which substance has dipole-dipole forces between its molecules?',['hydrogen chloride, HCl','carbon dioxide, CO<sub>2</sub>','methane, CH<sub>4</sub>'],ans='A. HCl is polar, so dipole-dipole forces add to its dispersion forces.',right='A',
  fb=['HCl is polar. The δ+ end of one pulls the δ− end of the next.','CO<sub>2</sub> is linear. Its two polar bonds cancel, so it is nonpolar.','Methane is nonpolar. It has dispersion forces only.'])}
    </div>''',
 'F₂ and HCl both have 18 electrons, so their dispersion forces are about equal. F₂ boils at −188.1 °C and HCl at −85.1 °C, about 100 °C higher: the extra pull is the dipole-dipole force. Polarity comes from Lesson 4.4 (shape and bond polarity).',
 [dict(show='s08-c0',stage='s08-sim:F2',focus='s08-sim',note='Two F₂ molecules, dashed gray lines only. Ask: polar or nonpolar? (nonpolar: same atoms).'),
  dict(show='s08-c1',stage='s08-sim:HCl',note='HCl: δ+ on H (warm), δ− on Cl (teal), from Lesson 4.4.'),
  dict(show='s08-pred',note='Prediction: students turn their hands like two molecules. Collect "δ+ toward δ−".'),
  dict(hide='s08-pred',stage='s08-sim:turn',label='turn',note='The molecules turn so the δ+ end of one faces the δ− end of the next.'),
  dict(show='s08-c2',stage='s08-sim:face',note='The dashed warm-to-teal line: dipole-dipole forces.'),
  dict(show='s08-c3',stage='s08-sim:compare',note='Electrons per molecule: F₂ 18, HCl 18. Boiling point: F₂ −188.1 °C, HCl −85.1 °C.'),
  dict(show='s08-rule',note='Students copy the rule. Polar molecules have both: dipole-dipole forces and dispersion forces.'),
  dict(clear=True,hide=['s08-c0','s08-c1','s08-c2'],show='s08-check',note='Hands up for A, B or C. HCl with its δ signs is on screen.'),
  dict(show='s08-ans',cls={'s08-a':'right','s08-check':'done'},note='A is right. B (CO₂): linear, its two polar bonds cancel, so it is nonpolar. C (CH₄): nonpolar, dispersion forces only.')]))

# ---------- 9 hydrogen bonding (two hosts in a stack: bpPlot first, then attractions)
S.append(slide('s09','t-concept cw','Hydrogen bonding','Hydrogen bonding','Reading §4.5.2',f'''    <div class="stack">
      <div class="sim" id="s09-plot" data-sim="bpPlot" aria-label="Boiling points of methane, ammonia and water, all with 10 electrons."></div>
      <div class="sim" id="s09-sim" data-sim="attractions" aria-label="Two water molecules joined by a hydrogen bond from an H to a lone pair."></div>
    </div>
    <div class="col acc">
      <div class="card" id="s09-c0" data-label="10 electrons"><p class="tag">Same electrons</p><p>CH<sub>4</sub>, NH<sub>3</sub> and H<sub>2</sub>O all have 10 electrons.</p></div>
      <div class="card" id="s09-pred" data-label="predict"><p class="tag">Predict</p><p>Which two boil far above methane?</p></div>
      <div class="card" id="s09-c1" data-label="hydrogen bond"><p class="tag">Hydrogen bond</p><p>An H on O is pulled to a lone pair on the next O. A hydrogen bond.</p></div>
      <div class="card" id="s09-c2" data-label="not a bond within"><p class="tag">How strong?</p><p>Not a covalent bond. About 5 to 10% as strong.</p></div>
      <div class="card" id="s09-c3" data-label="methane"><p class="tag">Methane</p><p>H on C: no hydrogen bonds. Dispersion forces only.</p></div>
      <div class="card" id="s09-c4" data-label="four"><p class="tag">Water</p><p>Each water molecule can form up to four.</p></div>
      <div class="card rule reg" id="s09-rule" data-label="rule"><p class="tag">Rule</p><p>Hydrogen bonding needs an H atom bonded to N, O or F. The next molecule needs a lone pair on N, O or F.</p></div>
{check('s09','Which substance has hydrogen bonding between its molecules?',['water, H<sub>2</sub>O','methane, CH<sub>4</sub>','hydrogen chloride, HCl'],ans='A. Each H is bonded to O, and O has two lone pairs.',right='A',
  fb=['Each H is on O, and O has lone pairs for the next molecule\'s H.','Methane\'s H atoms are bonded to carbon, not to N, O or F.','HCl is polar, but its H is on Cl. It forms no hydrogen bonds.'])}
    </div>''',
 'A hydrogen bond is an especially strong dipole-dipole attraction, not a covalent bond: only about 5 to 10% as strong. The 10-electron trio (CH₄ −161.5 °C, NH₃ −33.3 °C, H₂O 100.0 °C) has equal dispersion forces, so the difference is the hydrogen bonding. The reading\'s "all eight" view of the plot is not shown.',
 [dict(show='s09-c0',stage='s09-plot:trio',focus='s09-plot',note='Three points on the 10-electron line, unlabeled. Same number of electrons, so about the same dispersion forces.'),
  dict(show='s09-pred',note='Prediction: which two boil far above methane? Collect answers with a reason.'),
  dict(stage='s09-plot:reveal',label='reveal',note='CH₄ −161.5 °C, NH₃ −33.3 °C, H₂O 100.0 °C. Ask: what do NH₃ and H₂O have that CH₄ lacks? (H on N or O, a lone pair).'),
  dict(hide=['s09-plot','s09-c0','s09-pred'],show=['s09-sim','s09-c1'],stage='s09-sim:hbond',focus='s09-sim',note='Two water molecules, 104.5°, the lone pairs as violet lobes. The dashed teal line runs from an H of one molecule to a lone pair on the O of the next. It is longer than the O–H stick.'),
  dict(show='s09-c2',note='Not a covalent bond: about 5 to 10% as strong. Misconception to listen for: "a hydrogen bond is a bond within the molecule".'),
  dict(stage='s09-sim:ammonia',label='ammonia',note='Two NH₃ molecules: H on N, a lone pair on N, the same kind of line.'),
  dict(hide='s09-c1',show='s09-c3',stage='s09-sim:methane',note='Two CH₄: the crossed-out line. H on C, no lone pair: dispersion forces only.'),
  dict(show='s09-c4',stage='s09-sim:four',note='One water molecule with four neighbors: two through its H atoms, two through its lone pairs.'),
  dict(show='s09-rule',note='Students copy the rule. Misconception to listen for: "HCl forms hydrogen bonds" (H on Cl, not N, O or F).'),
  dict(clear=True,hide=['s09-c2','s09-c3'],show='s09-check',note='Hands up for A, B or C. Water with its four hydrogen bonds is on screen.'),
  dict(show='s09-ans',cls={'s09-a':'right','s09-check':'done'},note='A is right. B (methane): its H atoms are on carbon, not on N, O or F. C (HCl): polar, but its H is on Cl; no hydrogen bonds.')]))

# ---------- 10 name the attraction: I do, we do, you do (t-cer with forceDecider)
S.append(slide('s10','t-cer','Name the attraction: I do, we do, you do','Strongest attraction','Reading §4.5.2','''    <div class="hrow">
      <div class="stack">
        <p class="hdr" id="s10-steps" data-label="three questions">Three questions: Polar? H on N, O or F? Lone pair on N, O or F?</p>
        <p class="hdr" id="s10-h1" data-label="I do">I do: ammonia, NH<sub>3</sub>. Watch each box fill.</p>
        <p class="hdr" id="s10-h2" data-label="we do">We do: carbon dioxide, CO<sub>2</sub>. Call each box first.</p>
        <p class="hdr" id="s10-h3" data-label="you do">You do: find the difference. Name the strongest attraction.</p>
      </div>
    </div>
    <div class="stack">
      <div class="sim" id="s10-sim" data-sim="forceDecider" aria-label="Four boxes: Polar? H on N, O or F? Lone pair on N, O or F? Strongest attraction."></div>
    </div>''',
 'Reading §4.5.2, triplet 1. Watch NH₃ (polar, trigonal pyramidal, Lesson 4.4; H on N; a lone pair: hydrogen bonding, with dipole-dipole and dispersion forces). Finish it CO₂ (linear, the pulls cancel; no H: dispersion forces only). On your own HBr (2.96 − 2.20 = 0.76, polar; H on Br, not N, O or F: dipole-dipole forces). Honors (notes only, never assessed): for molecules of similar size the ranking is hydrogen bonding, then dipole-dipole, then dispersion (CH₄ −161.5, HCl −85.1, H₂O 100.0 °C). It fails across sizes: Br₂, 70 electrons and dispersion forces only, boils at 58.8 °C, far above polar HCl. Slide 13 builds the ladder of attractions.',
 [dict(show='s10-steps',stage='s10-sim:empty',focus='s10-sim',note='The three questions come first; the boxes on screen are empty. Read each title aloud.'),
  dict(hide='s10-steps',show='s10-h1',stage='s10-sim:NH3/polar',note='I do, thinking aloud: NH₃ is trigonal pyramidal (Lesson 4.4), so it is polar.'),
  dict(stage='s10-sim:NH3/H',label='H on N, O or F?',note='Its H atoms are on N: yes.'),
  dict(stage='s10-sim:NH3/lone',label='lone pair?',note='N has one lone pair: yes.'),
  dict(stage='s10-sim:NH3/strongest',label='strongest',note='Hydrogen bonding, along with dipole-dipole and dispersion forces.'),
  dict(hide='s10-h1',show='s10-h2',stage='s10-sim:CO2/polar',note='We do: students call "polar?" before the press. CO₂ is linear; the pulls cancel: no.'),
  dict(stage='s10-sim:CO2/H',label='H on N, O or F?',note='Students call it first: CO₂ has no H at all.'),
  dict(stage='s10-sim:CO2/strongest',label='strongest',note='A nonpolar molecule has only dispersion forces. Misconception: "CO₂ has polar bonds, so dipole-dipole forces" (the pulls cancel).'),
  dict(hide='s10-h2',show='s10-h3',stage='s10-sim:HBr/EN',note='You do: the chips give Br 2.96 and H 2.20. Students find the difference and the strongest attraction alone.'),
  dict(timer=90,label='timer 90 s',note='Ninety seconds, silent, in notebooks. Circulate; look for "hydrogen bonding" (H on Br is not H on N, O or F).'),
  dict(stage='s10-sim:HBr/polar',label='polar?',note='2.96 − 2.20 = 0.76: a polar bond, and HBr is polar.'),
  dict(stage='s10-sim:HBr/H',label='H on N, O or F?',note='H is on Br, not on N, O or F: no hydrogen bonding.'),
  dict(stage='s10-sim:HBr/strongest',label='strongest',note='Dipole-dipole forces. Students fix their notebook answer.')],pre='<div class="timer tr"></div>'))

# ---------- 11 molecules stay whole
S.append(slide('s11','t-concept cw','Molecules stay whole','Melting and boiling','Reading §4.5.3',f'''    <div class="sim" id="s11-sim" data-sim="heating" aria-label="Four methane molecules warm from solid to gas; a readout counts the covalent bonds, all intact."></div>
    <div class="col acc">
      <div class="card" id="s11-c0" data-label="solid methane"><p class="tag">Solid methane</p><p>Solid methane at −182.5 °C. Count the C–H bonds: all intact.</p></div>
      <div class="card" id="s11-pred" data-label="predict"><p class="tag">Predict</p><p>What comes apart when it melts?</p></div>
      <div class="card" id="s11-c1" data-label="melting"><p class="tag">Melting</p><p>The attractions let go. Every molecule stays whole.</p></div>
      <div class="card" id="s11-c2" data-label="boiling"><p class="tag">Boiling</p><p>At −161.5 °C the molecules spread far apart.</p></div>
      <div class="card" id="s11-c3" data-label="water"><p class="tag">Water</p><p>Water boils at 100.0 °C. Steam is still H<sub>2</sub>O.</p></div>
      <div class="card" id="s11-c4" data-label="energy"><p class="tag">Energy for 18 g of water</p><p>Boiling 18 g of water: 40.7 kJ. Breaking all its O–H bonds: about 928 kJ.</p></div>
      <div class="card rule reg" id="s11-rule" data-label="rule"><p class="tag">Rule</p><p>Melting and boiling separate molecules. They do not break the covalent bonds inside them.</p></div>
{check('s11','What happens to the water molecules when water boils?',['The molecules move far apart, still whole.','Their O–H bonds break.','They split into hydrogen and oxygen.'],ans='A. Each molecule keeps its two O–H bonds.',right='A',col=True,
  fb=['Only the attractions between molecules let go.','Boiling does not break covalent bonds. Steam is still H<sub>2</sub>O.','Boiling is a change of state, not a reaction. The molecules stay whole.'])}
    </div>''',
 'The reading\'s heating model: four methane molecules (six water molecules) from solid to gas; the readout "Covalent bonds: 16 of 16 intact" (water: 12 of 12) never changes, while "Attractions drawn" falls to 0 in the gas. Energy (OpenStax): boiling 18 g of water at 100 °C takes 40.7 kJ; breaking every O–H bond in it would take about 928 kJ, more than 20 times as much. Shown as the reading\'s comparison only; no bond-energy calculation.',
 [dict(show='s11-c0',stage='s11-sim:CH4/solid',focus='s11-sim',note='Solid methane at its melting point. Count the C–H bonds with the class: 16 of 16 intact.'),
  dict(show='s11-pred',note='Prediction: what comes apart when methane melts? Collect answers. Listen for "the C–H bonds break".'),
  dict(hide='s11-pred',show='s11-c1',stage='s11-sim:CH4/melt',note='The top row leaves its places first. The bond readout stays 16 of 16; only "Attractions drawn" falls.'),
  dict(stage='s11-sim:CH4/liquid',label='liquid',note='Liquid: the molecules move past each other; attractions still form and break.'),
  dict(show='s11-c2',stage='s11-sim:CH4/boil',note='Boiling at −161.5 °C: the molecules spread far apart.'),
  dict(stage='s11-sim:CH4/gas',label='gas',note='The gas: attractions drawn 0, covalent bonds still 16 of 16. Misconception: "methane melts low because its C–H bonds are weak" (melting leaves them intact).'),
  dict(hide=['s11-c0','s11-c1','s11-c2'],show='s11-c3',stage='s11-sim:H2O/boil',note='Water at 100.0 °C: steam is still H₂O molecules, each with its two O–H bonds, 12 of 12.'),
  dict(show='s11-c4',stage='s11-sim:energy',note='Two bars to one scale: 40.7 kJ to boil, about 928 kJ to break the bonds. More than 20 times as much.'),
  dict(show='s11-rule',note='Students copy the rule.'),
  dict(clear=True,hide=['s11-c3','s11-c4'],show='s11-check',stage='s11-sim:H2O/gas',note='Hands up for A, B or C. Steam is back on screen: water molecules far apart, 12 of 12 bonds intact.'),
  dict(show='s11-ans',cls={'s11-a':'right','s11-check':'done'},note='A is right. B (O–H bonds break): boiling does not break covalent bonds; steam is still H₂O. C (hydrogen and oxygen): boiling is a change of state, not a reaction.')]))

# ---------- 12 why ice floats
S.append(slide('s12','t-concept cw','Why ice floats','Ice','Reading §4.5.3',f'''    <div class="sim" id="s12-sim" data-sim="iceLattice" aria-label="A fragment of ice turning slowly: each water molecule hydrogen-bonded to four neighbors in open six-sided rings."></div>
    <div class="col acc">
      <div class="card" id="s12-c0" data-label="molecules"><p class="tag">Ice</p><p>Each molecule keeps its two O–H bonds.</p></div>
      <div class="card" id="s12-c1" data-label="hydrogen bonds"><p class="tag">Dashed lines</p><p>Each dashed line is a hydrogen bond.</p></div>
      <div class="card" id="s12-c2" data-label="four neighbors"><p class="tag">Neighbors</p><p>Each oxygen has four neighbors, 276 pm away.</p></div>
      <div class="card" id="s12-pred" data-label="predict"><p class="tag">Predict</p><p>When ice melts, does the water take more space or less?</p></div>
      <div class="card" id="s12-c3" data-label="open rings"><p class="tag">Open rings</p><p>Down this axis the molecules form open six-sided rings.</p></div>
      <div class="card" id="s12-c4" data-label="ice floats"><p class="tag">Ice floats</p><p>Ice is less dense, so it floats. Water grows about 9% when it freezes.</p></div>
      <div class="card" id="s12-c5" data-label="pipes"><p class="tag">A hard freeze</p><p>This can burst water pipes in a hard freeze.</p></div>
      <div class="card rule reg" id="s12-rule" data-label="rule"><p class="tag">Rule</p><p>Hydrogen bonds hold ice in open rings. So ice is less dense than liquid water, and it floats.</p></div>
{check('s12','100.0 cm<sup>3</sup> of water freezes at 0 °C. About what volume of ice forms?',['about 109 cm<sup>3</sup>','100.0 cm<sup>3</sup>','about 92 cm<sup>3</sup>'],ans='A. Ice is less dense. The same mass takes about 9% more space.',right='A',col=True,
  fb=['Ice is less dense, so the same mass takes more space.','The mass stays the same, but ice is less dense, so the volume grows.','Most solids shrink when they freeze. Ice expands instead.'])}
    </div>''',
 'Hexagonal ice (data notes: ideal oxygen framework, O···O 276 pm, hydrogen directions simplified). Densities at 0 °C (CRC): ice 0.9167 g/cm³, liquid water 0.99984 g/cm³; a floating block shows 8.3% above the surface; 100.0 cm³ of water becomes 109.1 cm³ of ice, the same 99.98 g. Melting collapses the open rings, so liquid water is denser. The Texas freeze case file uses this slide\'s model for the burst pipes of February 2021.',
 [dict(show='s12-c0',stage='s12-sim:molecules',focus='s12-sim',note='The lattice turns slowly. Point at one molecule: two O–H sticks, still there in ice.'),
  dict(show='s12-c1',stage='s12-sim:hbonds',note='The dashed teal lines: hydrogen bonds, each from an H to a lone pair on the next O.'),
  dict(show='s12-c2',stage='s12-sim:neighbors',note='One oxygen ringed with its four neighbors, 276 pm away.'),
  dict(show='s12-pred',note='Prediction: more space or less when ice melts? Most say more; collect the reasons.'),
  dict(hide='s12-pred',show='s12-c3',stage='s12-sim:rings',note='The view tips down the axis: open six-sided rings, like tunnels. Empty space inside the solid.'),
  dict(hide=['s12-c0','s12-c1','s12-c2'],show='s12-c4',stage='s12-sim:float',note='The block floats with 8.3% above the surface. Bars: 100.0 cm³ of water becomes 109.1 cm³ of ice.'),
  dict(show='s12-c5',note='Water expands as it freezes, so it can split rocks and burst pipes. The case file returns to this.'),
  dict(show='s12-rule',note='Students copy the rule. Misconception to listen for: "ice is heavier, so it should sink".'),
  dict(clear=True,hide=['s12-c3','s12-c4','s12-c5'],show='s12-check',note='Hands up for A, B or C. The volume bars are on screen.'),
  dict(show='s12-ans',cls={'s12-a':'right','s12-check':'done'},note='A is right. B (100.0 cm³): the mass stays the same, but ice is less dense, so the volume grows. C (about 92 cm³): most solids shrink when they freeze; ice expands.')]))

# ---------- 13 one picture: the ladder of attractions
LAD = [('hydrogen bonding','H on N, O or F, pulled to a lone pair','H<sub>2</sub>O 100.0 °C'),
       ('dipole-dipole forces','polar molecules','HCl −85.1 °C'),
       ('dispersion forces','all molecules; more electrons, stronger','CH<sub>4</sub> −161.5 °C')]
lad = ''.join(f'<tr><td class="slot"><span data-b="s13-r{3-k}" data-label="{a}">{a}</span></td><td class="slot"><span data-b="s13-r{3-k}">{b}</span></td><td class="slot"><span class="chip" data-b="s13-r{3-k}"><span>{c}</span></span></td></tr>' for k, (a, b, c) in enumerate(LAD))
S.append(slide('s13','t-summary tfill lad','One picture: the ladder of attractions','Summary','Reading §4.5.1 to §4.5.3',f'''    <table class="tbl compact ladder" id="s13-tbl">
      <thead><tr><th>Attraction (strongest at the top)</th><th>Acts between</th><th>Boiling point</th></tr></thead>
      <tbody>{lad}</tbody>
    </table>
    <div class="card" id="s13-line" data-label="the thread"><p>Melting and boiling let the attractions go; the bonds stay.</p></div>
    <div class="qrow" id="s13-w" data-label="write 90 s"><div class="card"><ol class="frames"><li>When a molecular substance boils, its molecules {GAP}. Its covalent bonds {GAP}.</li></ol><div class="bank"><b>Word bank:</b> <span>separate</span> <span>move far apart</span> <span>stay whole</span> <span>do not break</span></div></div><div class="timer"></div></div>''',
 'One picture closes period 1: the three attractions as rungs, built from the bottom. Students copy the ladder. Honors (notes only): the order holds for molecules of similar size; across sizes it fails (Br₂ 58.8 °C, dispersion forces only, boils far above polar HCl at −85.1 °C). Period 1 ends here.',
 [dict(show='s13-r1',note='Bottom rung: dispersion forces, between all molecules; more electrons, stronger. Methane boils at −161.5 °C.'),
  dict(show='s13-r2',note='Middle rung: dipole-dipole forces, between polar molecules. HCl boils at −85.1 °C.'),
  dict(show='s13-r3',note='Top rung: hydrogen bonding, H on N, O or F pulled to a lone pair. Water boils at 100.0 °C.'),
  dict(show='s13-line',note='The thread of period 1: what comes apart is the attractions; what stays is the bonds.'),
  dict(show='s13-w',timer=90,note='Ninety seconds of writing with the frame and the word bank. End of period 1: collect three notebooks as a quick check.')]))

# ---------- 14 warm-up
S.append(slide('s14','t-turn two','Warm-up','Warm-up, period 2','Reading §4.5.1 to §4.5.3','''    <div class="qrow">
      <div class="card"><p>Answer in your notebook. Then check each answer.</p></div>
      <div class="timer"></div>
    </div>
    <table class="tbl fill">
      <thead><tr><th>Question</th><th>Answer</th></tr></thead>
      <tbody>
        <tr><td>Which attraction acts between all molecules?</td><td class="slot"><span data-b="s14-a1" data-label="answer 1">dispersion forces</span></td></tr>
        <tr><td>Hydrogen bonding needs an H atom bonded to '''+GAP+'''.</td><td class="slot"><span data-b="s14-a2" data-label="answer 2">N, O or F</span></td></tr>
        <tr><td>When water boils, what stays whole?</td><td class="slot"><span data-b="s14-a3" data-label="answer 3">each H<sub>2</sub>O molecule,<br>with its two O–H bonds</span></td></tr>
      </tbody>
    </table>''',
 'Period 2 starts here. The three questions retrieve 4.5.1, 4.5.2 and 4.5.3.',
 [dict(note='Students read the three questions while you take attendance.'),
  dict(timer=90,label='timer 90 s',note='Ninety seconds, in notebooks.'),
  dict(show='s14-a1',note='Dispersion forces act between all molecules, polar or not.'),
  dict(show='s14-a2',note='N, O or F, with a lone pair on N, O or F in the next molecule.'),
  dict(show='s14-a3',note='Each H₂O molecule stays whole with its two O–H bonds; only the attractions let go.')]))

# ---------- 15 does it conduct? (wide)
S.append(slide('s15','t-concept wide','Does it conduct?','Conductivity','Reading §4.5.4',f'''    <div class="sim" id="s15-sim" data-sim="conductTester" data-reserve="236" aria-label="A battery, a switch, a bulb and a beaker with two electrodes; a magnified circle shows the particles."></div>
    <div class="ptrow" style="height:236px"><div class="band2">
      <div class="stack">
      <p class="caprow" id="s15-p0" data-label="charge must move">A current is a flow of charge. Something charged must move.</p>
      <p class="caprow" id="s15-p1" data-label="solid salt">Solid salt. Lights or stays dark?</p>
      <p class="caprow" id="s15-p2" data-label="locked">The ions are locked in the crystal. They cannot move.</p>
      <p class="caprow" id="s15-p3" data-label="molten salt">Molten salt, 801 °C. Lights or stays dark?</p>
      <p class="caprow" id="s15-p4" data-label="ions move">Now the ions move. They carry the current.</p>
      <p class="caprow" id="s15-p5" data-label="salt water">Salt water: ions move among water molecules. An electrolyte.</p>
      <p class="caprow" id="s15-p6" data-label="copper">Copper: delocalized electrons move.</p>
      <p class="caprow" id="s15-p7" data-label="sugar water">Sugar water: whole molecules, no charge. Dark.</p>
      <p class="caprow" id="s15-p8" data-label="distilled water">Distilled water: very few ions. Dark.</p>
      <div class="rulerow reg" id="s15-rule" data-label="rule"><p>A substance conducts when it has charged particles that can move.</p><p>Ions in a liquid or a solution.</p><p>Delocalized electrons in a metal.</p></div>
{checkrow('s15','Why does molten NaCl conduct, but solid NaCl not?',['In the liquid, the ions can move.','Melting turns atoms into ions.','Melting frees sodium\'s electrons.'],'A. The ions were always there. Now they can move.',right='A',
  fb=['Moving ions carry the current.','Solid NaCl is already Na<sup>+</sup> and Cl<sup>−</sup>. In the solid they are locked in place.','NaCl has no electron sea. Moving ions carry its current.'])}
      </div>
      <p class="simcap" id="s15-cap" data-label="colors" data-zoom="caption">{CAP}</p>
    </div></div>''',
 'The reading\'s conductivity table: solid NaCl (Na⁺ and Cl⁻ locked: dark), molten NaCl (lights), salt water (lights), sugar water (no charged particles: dark), copper (delocalized electrons: lights), distilled water (very few ions: dark). A substance that forms ions in water, like NaCl, is an electrolyte. The magnified circle draws the ions to scale (Shannon); water molecules in CPK colors share the circle with the ions, hence the caption. Nothing is demonstrated: molten salt is above 801 °C.',
 [dict(show=['s15-p0','s15-cap'],stage='s15-sim:tester',focus='s15-sim',note='The tester: battery, switch, bulb, beaker with two electrodes. Thread for period 2: what can move?'),
  dict(hide='s15-p0',show='s15-p1',stage='s15-sim:NaCl-s/predict',note='Prediction: hands up for "lights" or "stays dark". Many say lights: "salt is made of ions".'),
  dict(stage='s15-sim:NaCl-s/close',label='close the switch',note='The switch closes. The bulb stays dark.'),
  dict(hide='s15-p1',show='s15-p2',stage='s15-sim:NaCl-s/zoom',label='look inside',note='Magnified: Na⁺ and Cl⁻ locked in the crystal. Charged, but they cannot move.'),
  dict(hide='s15-p2',show='s15-p3',stage='s15-sim:NaCl-l/predict',note='Molten salt at 801 °C. Hands up again: lights or dark?'),
  dict(stage='s15-sim:NaCl-l/close',label='close the switch',note='The bulb lights.'),
  dict(hide='s15-p3',show='s15-p4',stage='s15-sim:NaCl-l/zoom',label='look inside',note='The same ions, now free to move. Moving ions carry the current.'),
  dict(hide='s15-p4',show='s15-p5',stage='s15-sim:NaCl-aq/zoom',note='Salt water lights: Na⁺ and Cl⁻ move among water molecules. Salt is an electrolyte.'),
  dict(hide='s15-p5',show='s15-p6',stage='s15-sim:Cu/zoom',note='Copper lights: delocalized electrons stream one way; the cations stay (Lesson 4.1).'),
  dict(hide='s15-p6',show='s15-p7',stage='s15-sim:sugar/close',note='Sugar water stays dark: whole sugar molecules, no charge. Misconception: "anything dissolved conducts".'),
  dict(hide='s15-p7',show='s15-p8',stage='s15-sim:water/close',note='Distilled water stays dark: very few ions. Tap water has more ions and conducts a little.'),
  dict(hide='s15-p8',show='s15-rule',note='Students copy the three lines. Misconception to listen for: "charge alone makes it conduct" (the charges must move).'),
  dict(hide=['s15-rule','s15-cap'],show='s15-check',stage='s15-sim:NaCl-l/zoom',note='Hands up for A, B or C. Molten salt with its moving ions is back on screen.'),
  dict(show='s15-ans',cls={'s15-a':'right','s15-check':'done'},note='A is right. B (melting makes ions): solid NaCl is already Na⁺ and Cl⁻, locked in place. C (melting frees electrons): NaCl has no electron sea; moving ions carry its current.')]))

# ---------- 16 predict the bulb: I do, we do, you do (t-example cb)
STEP = [('Type','ionic','ionic'),('Particles','K<sup>+</sup> and Cl<sup>−</sup>','Ca<sup>2+</sup> and Cl<sup>−</sup>'),
        ('Free to move?','yes, in the liquid','no, locked in the crystal'),('Prediction','conducts','does not conduct')]
srows = ''.join(f'<li><span class="k">{k}</span><span class="stack"><span id="s16-k{i+1}" data-label="I do: step {i+1}">{a}</span><span id="s16-c{i+1}" data-label="we do: step {i+1}">{b}</span></span></li>' for i, (k, a, b) in enumerate(STEP))
S.append(slide('s16','t-example cb','Predict the bulb: I do, we do, you do','Conductivity','Reading §4.5.4',f'''    <div class="sim" id="s16-sim" data-sim="conductTester" aria-label="The tester with molten potassium chloride, then solid calcium chloride."></div>
    <div class="col acc">
      <div class="card stepscard" id="s16-steps" data-label="four steps"><p class="tag"><span class="stack"><span id="s16-tk">I do: molten KCl</span><span id="s16-tc">We do: solid CaCl<sub>2</sub></span></span></p><ol class="steps">{srows}</ol></div>
      <div class="card" id="s16-you" data-label="you do"><p class="tag">You do</p><p>Four samples: solid KCl, KCl in water, molten KCl, sugar water.</p><p>How many light the bulb? What carries the current?</p>
        <div class="stack ylow"><p class="ansl"><span id="s16-a1" data-label="answer 1">2 samples: KCl in water and molten KCl.</span> <span id="s16-a2" data-label="answer 2">K<sup>+</sup> and Cl<sup>−</sup> ions that can move.</span></p><div class="timer"></div></div></div>
    </div>''',
 'Reading §4.5.4, triplet 2. Watch molten KCl (ionic; K⁺ and Cl⁻; free to move in the liquid; conducts). Finish it solid CaCl₂ (ionic; Ca²⁺ and Cl⁻; locked in the crystal; does not conduct; melted or dissolved, it would). On your own: solid KCl, dissolved KCl, molten KCl, sugar water: two light the bulb, carried by K⁺ and Cl⁻ ions that can move.',
 [dict(show=['s16-steps','s16-tk'],stage='s16-sim:KCl-l/predict',focus='s16-sim',note='The four steps come first: type, particles, free to move, prediction. I do: molten KCl.'),
  dict(show='s16-k1',note='Type: K is a metal, Cl a nonmetal: ionic.'),
  dict(show='s16-k2',note='Particles: K⁺ and Cl⁻.'),
  dict(show='s16-k3',note='Free to move? Yes: it is a liquid.'),
  dict(show='s16-k4',note='Prediction: conducts.'),
  dict(stage='s16-sim:KCl-l/close',label='close the switch',note='The bulb lights, as predicted.'),
  dict(hide=['s16-tk','s16-k1','s16-k2','s16-k3','s16-k4'],show=['s16-tc','s16-c1'],stage='s16-sim:CaCl2-s/predict',note='We do: solid CaCl₂. Students call each step before the press. Type: ionic.'),
  dict(show='s16-c2',note='Particles: Ca²⁺ and Cl⁻.'),
  dict(show='s16-c3',note='Free to move? No: locked in the crystal.'),
  dict(show='s16-c4',note='Prediction: does not conduct. Melted or dissolved, it would.'),
  dict(stage='s16-sim:CaCl2-s/close',label='close the switch',note='The bulb stays dark. Misconception to listen for: "it is ionic, so it conducts".'),
  dict(show='s16-you',note='You do: four samples. Students write how many light the bulb and what carries the current.'),
  dict(timer=90,label='timer 90 s',note='Ninety seconds, alone. Circulate; look for "3 samples" (solid KCl counted) and for "electrons carry it".'),
  dict(show='s16-a1',note='Two samples: KCl in water and molten KCl. Solid KCl and sugar water stay dark.'),
  dict(show='s16-a2',stage='s16-sim:KCl-l/zoom',note='The magnified view: K⁺ and Cl⁻ free to move carry the current.')]))

# ---------- 17 does it dissolve?
SIX = [('ic-s-nacl','sodium chloride'),('ic-s-sugar','sucrose (table sugar)'),('ic-s-caco3','calcium carbonate'),('ic-s-i2','iodine'),('ic-s-sio2','quartz'),('ic-s-cu','copper')]
six = ''.join(f'<div class="samp">{use(i,"Icon: "+n)}<p>{n}</p></div>' for i, n in SIX)
DIS = [('sodium chloride, NaCl','ionic','yes',''),('sucrose (table sugar)','molecular','yes',''),('calcium carbonate, CaCO<sub>3</sub>','ionic','barely',' <span class="why">(limestone and seashells)</span>'),
       ('iodine, I<sub>2</sub>','molecular','slightly',''),('quartz, SiO<sub>2</sub>','covalent network','no',''),('copper, Cu','metallic','no','')]
drows = ''.join(f'<tr><td class="slot"><span data-b="s17-r{k+1}" data-label="{re.sub("<[^>]+>","",n).split(",")[0]}">{n}{w}</span></td><td class="slot"><span data-b="s17-r{k+1}">{t}</span></td><td class="slot"><span data-b="s17-r{k+1}">{d}</span></td></tr>' for k, (n, t, d, w) in enumerate(DIS))
S.append(slide('s17','t-concept cw','Does it dissolve?','Dissolving','Reading §4.5.4',f'''    <div class="leftcol"><div class="stack">
      <div class="card sixcard" id="s17-six" data-label="six samples"><p class="tag">Six samples</p><div class="sixgrid">{six}</div></div>
      <div class="sim" id="s17-sim" data-sim="conductTester" aria-label="A beaker of water; each sample drops in and dissolves or sits."></div>
    </div><p class="simcap" id="s17-cap" data-label="colors" data-zoom="caption">{CAP}</p></div>
    <div class="col acc">
      <div class="card" id="s17-c0" data-label="dissolve"><p class="tag">In water</p><p>Many substances dissolve in water. Many do not.</p></div>
      <div class="card" id="s17-pred" data-label="predict"><p class="tag">Predict</p><p>Which of these six dissolve?</p></div>
      <table class="tbl compact dis" id="s17-tab" data-label="the table" data-zoom="dissolving table"><thead><tr><th>Substance</th><th>Type</th><th>Dissolves in water?</th></tr></thead><tbody>{drows}</tbody></table>
      <div class="card rule reg" id="s17-rule" data-label="rule"><p class="tag">Rule</p><p>Some ionic and some molecular substances dissolve in water. Some do not. The type of bond alone does not predict it.</p></div>
{check('s17','Which statement fits the data?',['Some ionic compounds, such as CaCO<sub>3</sub>, barely dissolve.','Every ionic compound dissolves in water.','No molecular substance dissolves in water.'],ans='A. Ionic does not mean it dissolves. Check the data.',right='A',col=True,
  fb=['The type of bond alone does not predict it.','Calcium carbonate is ionic, yet it barely dissolves.','Sugar is molecular, and it dissolves easily.'])}
    </div>''',
 'The reading describes which substances dissolve and does not explain why; neither does this slide. Calcium carbonate is sparingly soluble (data notes): limestone, marble and seashells. Iodine dissolves slightly and tints the water pale yellow-brown. About 360 g of NaCl dissolves in 1 L of water (case file, only if asked). The beaker shows ions (unit code) and I₂ molecules (CPK), hence the caption.',
 [dict(show=['s17-six','s17-c0','s17-cap'],note='Six samples from the kitchen, the beach and the hardware store. Ask: which have you seen disappear in water?'),
  dict(show='s17-pred',note='Prediction: students list the ones they think dissolve. Collect counts for each.'),
  dict(hide=['s17-six','s17-pred','s17-c0'],show=['s17-sim','s17-tab','s17-r1'],stage='s17-sim:dis/NaCl',focus='s17-sim',note='Sodium chloride: ionic, dissolves. The ions spread out: an electrolyte.'),
  dict(show='s17-r2',stage='s17-sim:dis/sucrose',note='Sucrose: molecular, dissolves. Whole molecules spread out; no ions.'),
  dict(show='s17-r3',stage='s17-sim:dis/CaCO3',note='Calcium carbonate: ionic, yet it barely dissolves. Limestone and seashells last for years in water.'),
  dict(show='s17-r4',stage='s17-sim:dis/I2',note='Iodine: molecular, dissolves slightly. The water turns pale yellow-brown.'),
  dict(show='s17-r5',stage='s17-sim:dis/SiO2',note='Quartz: a covalent network, does not dissolve. Sand stays sand.'),
  dict(show='s17-r6',stage='s17-sim:dis/Cu',note='Copper: metallic, does not dissolve.'),
  dict(hide='s17-tab',show='s17-rule',note='Students copy the rule. Misconception to listen for: "every ionic compound dissolves" (CaCO₃ barely does).'),
  dict(clear=True,hide='s17-cap',show='s17-check',stage='s17-sim:dis/CaCO3',note='Hands up for A, B or C. Calcium carbonate is back in the beaker.'),
  dict(show='s17-ans',cls={'s17-a':'right','s17-check':'done'},note='A is right. B (every ionic compound dissolves): calcium carbonate is ionic, yet it barely dissolves. C (no molecular substance dissolves): sugar is molecular and dissolves easily.')]))

# ---------- 18 malleable or brittle (wide)
S.append(slide('s18','t-concept wide','Malleable or brittle','Hardness','Reading §4.5.5',f'''    <div class="sim" id="s18-sim" data-sim="hammerBlow" data-reserve="236" aria-label="A copper block and a salt block side by side; a hammer strikes the top layers of both."></div>
    <div class="ptrow" style="height:236px"><div class="band2">
      <div class="stack">
        <div class="lines" id="s18-l">
          <div class="stack">
            <p class="caprow" id="s18-p0" data-label="copper and salt">Copper and salt: both are hard.</p>
            <p class="caprow" id="s18-p1" data-label="predict">Which one breaks under a sharp blow?</p>
            <p class="caprow" id="s18-pb" data-label="the blow">The hammer strikes the top layers of both.</p>
            <div id="s18-p2" data-label="the layers shift"><p class="caprow">Copper: the layers slide, the electrons move with them.</p><p class="caprow">Salt: shifted layers put like charges side by side.</p></div>
            <p class="caprow" id="s18-p3" data-label="result">Copper bends: malleable. Salt splits: brittle.</p>
            <p class="caprow" id="s18-p4" data-label="molecular solids">Molecular solids, like iodine, are soft. Only weak attractions hold them.</p>
          </div>
          {chips('Ion and atom sizes',['Na<sup>+</sup> 102 pm','Cl<sup>−</sup> 181 pm','Cu 128 pm'],' id="s18-sz" data-label="sizes" data-zoom="sizes"')}
        </div>
        <div class="rulerow two reg" id="s18-rule" data-label="rule"><p>A metal bends because its electrons move with the shifting cations.</p><p>An ionic crystal splits because shifted layers put like charges side by side.</p></div>
{checkrow('s18','A sharp blow splits a salt crystal. Why?',['Shifted layers put like charges together; they repel.','Ionic bonds are weak.','Electrons flow out of the crystal.'],'A. Like charges repel and push the layers apart.',right='A',
  fb=['Like charges side by side repel, and the layers push apart.','Ionic bonds are strong, so salt is hard. Like charges repel when layers shift.','Salt has no electron sea. Its ions stay charged, and like charges repel.'])}
      </div>
      <p class="simcap" id="s18-cap" data-label="colors" data-zoom="caption">{CAP}</p>
    </div>''',
 'The reading\'s hammer model (§4.5.5): both blocks to one scale, Na⁺ 102 pm, Cl⁻ 181 pm at 282 pm, Cu 128 pm. A metal bends because its electrons move with the shifting cations; an ionic crystal splits because shifted layers put like charges side by side. Molecular solids (iodine, dry ice) are usually soft: only weak attractions hold them. Nothing is demonstrated.',
 [dict(show=['s18-p0','s18-sz','s18-cap'],stage='s18-sim:before',focus='s18-sim',note='Copper and salt, drawn to one scale. Both are hard: you cannot scratch either with a fingernail.'),
  dict(hide='s18-sz',show='s18-p1',note='Prediction: which one breaks under a sharp blow? Hands up for copper or salt; ask for a reason.'),
  dict(show='s18-pb',stage='s18-sim:blow',note='The hammer strikes the top layers of both blocks.'),
  dict(hide=['s18-p0','s18-p1','s18-pb'],show='s18-p2',stage='s18-sim:shift',note='The top layers move one spacing. Copper: the electrons flow along. Salt: each shifted ion now sits beside an ion of the same charge; three pairs flash red.'),
  dict(hide='s18-p2',show='s18-p3',stage='s18-sim:result',note='Copper bends and stays one piece: malleable. Salt\'s layers push apart along a flat face: brittle, with a red crack.'),
  dict(hide='s18-p3',show='s18-p4',note='Molecular solids such as iodine and dry ice are usually soft: only weak attractions hold their molecules.'),
  dict(hide='s18-p4',show='s18-rule',note='Students copy the rule. Misconception to listen for: "salt splits because ionic bonds are weak" (salt is hard; like charges repel).'),
  dict(hide=['s18-rule','s18-cap'],show='s18-check',note='Hands up for A, B or C. The split salt block is on screen.'),
  dict(show='s18-ans',cls={'s18-a':'right','s18-check':'done'},note='A is right. B (ionic bonds are weak): ionic bonds are strong, so salt is hard; like charges repel when layers shift. C (electrons flow out): salt has no electron sea; its ions stay charged.')]))

# ---------- 19 covalent network solids
S.append(slide('s19','t-concept cw','Covalent network solids','Network solids','Reading §4.5.5',f'''    <div class="leftcol"><div class="sim" id="s19-sim" data-sim="networkVsMolecules" aria-label="Dry ice molecules fly off whole; a quartz network stays as it heats; a diamond network."></div><p class="simcap" id="s19-cap" data-label="colors" data-zoom="caption">{CAP}</p></div>
    <div class="col acc">
      <div class="card" id="s19-c0" data-label="dry ice"><p class="tag">Dry ice</p><p>Dry ice is solid CO<sub>2</sub>: separate molecules.</p></div>
      <div class="card" id="s19-pred" data-label="predict"><p class="tag">Predict</p><p>CO<sub>2</sub> and SiO<sub>2</sub> have similar formulas. Do they behave the same?</p></div>
      <div class="card" id="s19-c1" data-label="sublimes"><p class="tag">−78.5 °C</p><p>At −78.5 °C the molecules fly off, whole. No liquid.</p></div>
      <div class="card" id="s19-c2" data-label="quartz"><p class="tag">Quartz</p><p>Quartz, SiO<sub>2</sub>: covalent bonds join every atom. No molecules.</p></div>
      <div class="card" id="s19-c3" data-label="heat"><p class="tag">Heat it</p><p>To melt it, covalent bonds must break. Near 1700 °C.</p></div>
      <div class="card" id="s19-c4" data-label="diamond"><p class="tag">Diamond</p><p>Diamond: a network of carbon atoms. The hardest natural substance.</p></div>
      <div class="card rule reg" id="s19-rule" data-label="rule"><p class="tag">Rule</p><p>In a covalent network solid, covalent bonds join every atom to its neighbors. To melt it, covalent bonds must break. So it melts only when very hot.</p></div>
{check('s19','Which substance is a covalent network solid?',['quartz, SiO<sub>2</sub>','dry ice, CO<sub>2</sub>','iodine, I<sub>2</sub>'],ans='A. Covalent bonds join every atom in quartz. It melts only near 1700 °C.',right='A',
  fb=['Covalent bonds join every atom in quartz. No molecules.','Dry ice is separate CO<sub>2</sub> molecules held by dispersion forces.','Solid iodine is separate I<sub>2</sub> molecules held by dispersion forces.'])}
    </div>''',
 'Dry ice sublimes at −78.5 °C: no liquid at 1 atm (never give CO₂ a boiling point). Quartz, SiO₂, melts near 1700 °C (sources 1710 to 1722 °C); its fragment is idealized with straight Si–O–Si. Most covalent network solids are very hard; diamond is the hardest natural substance. Teacher only, the exception: graphite conducts along its layers (one delocalized electron per carbon), and its layers are held by dispersion forces only, so it is soft. Atom colors are CPK: C dark gray, O red, Si tan.',
 [dict(show=['s19-c0','s19-cap'],stage='s19-sim:co2',focus='s19-sim',note='Dry ice: six CO₂ molecules, linear, with dashed dispersion lines between them. The thermometer reads −78.5 °C.'),
  dict(show='s19-pred',note='Prediction: CO₂ and SiO₂ look alike on paper. Do they behave the same? Hands up yes or no.'),
  dict(hide='s19-pred',show='s19-c1',stage='s19-sim:sublime',note='The molecules fly off whole; the dashed lines vanish; no liquid forms. That is sublimation.'),
  dict(show='s19-c2',stage='s19-sim:quartz',note='Quartz: every Si bonded to four O, each O bridging two Si. No molecule outline anywhere.'),
  dict(show='s19-c3',stage='s19-sim:heat',note='The thermometer passes 1000 °C and the network stays. Misconception to listen for: "all covalent solids melt low" (water melts at 0 °C, quartz near 1700 °C).'),
  dict(show='s19-c4',stage='s19-sim:diamond',note='Diamond: a network of carbon atoms, the hardest natural substance.'),
  dict(hide=['s19-c0','s19-c1','s19-c2'],show='s19-rule',note='Students copy the rule.'),
  dict(clear=True,hide=['s19-c0','s19-c1','s19-c3','s19-c4','s19-cap'],show='s19-check',stage='s19-sim:quartz',note='Hands up for A, B or C. The quartz network is back on screen.'),
  dict(show='s19-ans',cls={'s19-a':'right','s19-check':'done'},note='A is right. B (dry ice): separate CO₂ molecules held by dispersion forces. C (iodine): separate I₂ molecules held by dispersion forces.')]))

# ---------- 20 four kinds of solids
KS = [('Molecular, I<sub>2</sub>','attractions between molecules; low melting point','no','soft'),
      ('Ionic, NaCl','ionic bonds; high melting point','when molten or dissolved','hard, brittle'),
      ('Metallic, Cu','metallic bonds;<br>melting point usually high','yes, solid and liquid','malleable'),
      ('Covalent network,<br>SiO<sub>2</sub>','covalent bonds;<br>very high melting point','no<br>(except graphite)','very hard<br>(except graphite)')]
krows = ''.join(f'<tr><td class="slot"><span data-b="s20-r{k+1}" data-label="{re.sub("<[^>]+>","",a).split(",")[0].lower()} solids">{a}</span></td><td class="slot"><span data-b="s20-r{k+1}">{b}</span></td><td class="slot"><span data-b="s20-r{k+1}">{c}</span></td><td class="slot"><span data-b="s20-r{k+1}">{d}</span></td></tr>' for k, (a, b, c, d) in enumerate(KS))
S.append(slide('s20','t-summary tfill tab','Four kinds of solids','Summary','Reading §4.5 Review',f'''    <table class="tbl compact kinds" id="s20-tbl">
      <thead><tr><th>Solid</th><th>What holds it; melting point</th><th>Conducts?</th><th>Under a hammer</th></tr></thead>
      <tbody>{krows}</tbody>
    </table>
    <div class="card" id="s20-end" data-label="snow, salt, sand"><p>Snow: the attractions let go at 0 °C. Salt: ionic bonds, 801 °C. Sand: covalent bonds, near 1700 °C.</p></div>''',
 'The reading\'s Review table in one picture. The thread closes: what comes apart decides the melting point. Graphite is the exception in the last row (it conducts along its layers and is soft); teacher only.',
 [dict(show='s20-r1',note='Molecular solids, iodine: melting overcomes only the attractions between molecules, so the melting point is low. No charged particles move: no current. Soft.'),
  dict(show='s20-r2',note='Ionic solids, salt: ionic bonds, a high melting point. Conducts when molten or dissolved. Hard, but brittle.'),
  dict(show='s20-r3',note='Metallic solids, copper: metallic bonds, a melting point that is usually high. Conducts as a solid and a liquid. Malleable.'),
  dict(show='s20-r4',note='Covalent network solids, quartz: covalent bonds, a very high melting point. No current, very hard (graphite is the exception).'),
  dict(show='s20-end',note='The snow day returns: snow melts at 0 °C because only attractions let go; salt needs 801 °C for ionic bonds; sand near 1700 °C for covalent bonds.')]))

# ---------- 21 checkpoint routine
steps = [('Think · 30 s','alone, no talking'),('Talk · 60 s','tell your partner, then listen'),('Write · 90 s','use the sentence frames'),('Self-check','tick each success criterion'),('Compare','read the sample and fix one line')]
sr = '\n'.join(f'        <li id="s21-s{k+1}"><b class="lbl">{a}</b><span>{b}</span></li>' for k,(a,b) in enumerate(steps))
S.append(slide('s21','t-routine','Checkpoint routine','Checkpoint','Objectives 4.5.2, 4.5.4 and 4.5.5',f'''    <div class="card prompt"><p>Each checkpoint uses the same five steps.</p></div>
    {rail('s21')}
    <ol class="steprows">
{sr}
    </ol>''',
 'Routine for slides 22 to 24: think 30 s, talk 60 s, write 90 s, self-check, compare.',
 [dict(note='Explain that the routine repeats for each question.')]+
 [dict(cls=dict([(f's21-r{j+1}','done') for j in range(k)]+[(f's21-s{j+1}','') for j in range(k)]+[(f's21-r{k+1}','now'),(f's21-s{k+1}','now')]),label=['think','talk','write','self-check','compare'][k],note=n) for k,n in enumerate(['Think: silent, no pencils.','Talk: partner A first, then partner B.','Write: the sentence frames and word bank stay on screen.','Self-check: tick each criterion you met.','Compare: read the sample answer and fix one line.'])]))

# ---------- 22 to 24 checkpoints
def checkpoint(sid, title, ref, prompt, read, fr_lines, bank, crit, sample, notes, listen):
    p = sid
    fl = ''.join(f'<li>{x}</li>' for x in fr_lines); bk = ' '.join(f'<span>{b}</span>' for b in bank); cr = ''.join(f'<li>{c}</li>' for c in crit)
    body = f'''    <div class="card prompt reg"><p>{prompt}</p></div>
    {rail(p)}
    <div class="rt-main">
      <div class="acc">
        <div class="card phase" id="{p}-read" data-label="read"><p class="big">{read}</p></div>
        <div class="card phase" id="{p}-think" data-label="think 30 s"><p class="big">Think alone. Do not talk yet.</p></div>
        <div class="card phase" id="{p}-talk" data-label="talk 60 s"><p class="big">Tell your partner your answer. Then listen.</p></div>
        <div class="card phase" id="{p}-write" data-label="write 90 s"><p class="tag">Write</p><ol class="frames">{fl}</ol><div class="bank"><b>Word bank:</b> {bk}</div></div>
        <div class="card phase" id="{p}-check" data-label="self-check"><p class="tag">Self-check: did you write</p><ul class="crit">{cr}</ul></div>
        <div class="card phase reg" id="{p}-sample" data-label="sample answer"><p class="tag">Sample answer</p><p>{sample}</p></div>
      </div>
      <div class="timer"></div>
    </div>'''
    fr = [dict(show=f'{p}-read',note=notes[0]),
          dict(hide=f'{p}-read',show=f'{p}-think',cls={f'{p}-r1':'now'},timer=30,note='Silent thinking. No pencils yet.'),
          dict(hide=f'{p}-think',show=f'{p}-talk',cls={f'{p}-r1':'done',f'{p}-r2':'now'},timer=60,note='Partner A speaks first, then B. Listen for: '+listen),
          dict(hide=f'{p}-talk',show=f'{p}-write',cls={f'{p}-r2':'done',f'{p}-r3':'now'},timer=90,note='Students write in notebooks with the frames; the word bank stays up.'),
          dict(show=f'{p}-check',cls={f'{p}-r3':'done',f'{p}-r4':'now'},note='Students tick each criterion they met and fix one line.'),
          dict(show=f'{p}-sample',cls={f'{p}-r4':'done',f'{p}-r5':'now'},note=notes[1])]
    return slide(sid,'t-routine',title,title,ref,body,'Routine: think 30 s, talk 60 s, write 90 s, self-check, compare. The question stays on screen on every frame.',fr)
S.append(checkpoint('s22','Checkpoint 1','Objective 4.5.2',
  'Methane and water both have 10 electrons. Methane boils at −161.5 °C and water at 100.0 °C. Explain the difference.',
  'Read the question. What do the two molecules share?',
  [f'Water boils far above methane because {GAP}.', f'Hydrogen bonding needs {GAP} and {GAP}.'],
  ['hydrogen bonding','H on O','a lone pair','H on C','dispersion forces only','stronger attraction'],
  ['hydrogen bonding named?','H on O and a lone pair?','methane has none?'],
  'Water forms hydrogen bonds: H on O, lone pairs. Methane has only dispersion forces, so it boils lower.',
  ['Read the prompt aloud. Same electrons, so the same dispersion forces: the difference must be another attraction.','Compare with the sample. Reading §4.5.2: hydrogen bonding needs an H on N, O or F and a lone pair on N, O or F.'],
  '"water\'s bonds are stronger" (the covalent bonds do not break on boiling).'))
S.append(checkpoint('s23','Checkpoint 2','Objective 4.5.4',
  'Solid salt leaves the bulb dark. Salt water lights it. Explain both with the particles.',
  'Read the question. Which particles does salt contain?',
  [f'Solid salt does not conduct because its ions {GAP}.', f'Salt water conducts because {GAP}.'],
  ['Na<sup>+</sup> and Cl<sup>−</sup> ions','locked in the crystal','free to move','carry the current','no electrons move'],
  ['the ions named?','locked in the solid?','moving in the water?'],
  'Solid salt has Na<sup>+</sup> and Cl<sup>−</sup> ions, locked in the crystal. In salt water, ions move and carry the current.',
  ['Read the prompt aloud. The same ions are in both; what changes?','Compare with the sample. Reading §4.5.4: a substance conducts when it has charged particles that can move.'],
  '"salt water conducts through electrons".'))
S.append(checkpoint('s24','Checkpoint 3','Objective 4.5.5',
  'A hammer bends a copper sheet but splits a salt crystal. Explain both.',
  'Read the question. What happens to the layers in each?',
  [f'Copper bends because {GAP}.', f'Salt splits because {GAP}.'],
  ['layers slide','electrons move with the cations','like charges','side by side','repel'],
  ['electrons move with the cations?','like charges side by side?','they repel?'],
  'Copper\'s electrons move with the sliding cations, so it bends. In salt, shifted layers put like charges side by side; they repel.',
  ['Read the prompt aloud. Picture the hammer model of slide 18.','Compare with the sample. Reading §4.5.5: a metal bends because its electrons move with the shifting cations; an ionic crystal splits because shifted layers put like charges side by side.'],
  '"ionic bonds are weak" (salt is hard; like charges repel).'))

# ---------- 25 predictions and exit ticket
def pa(p, n, q, right, reason, lab):
    return f'''      <div class="card check done" id="{p}" data-label="{lab}" data-mode="none"><p class="tag">Question {n}</p><p class="q">{q}</p><ol class="opts" data-lay="row"><li class="opt right"><b>{right[0]}</b><span>{right[1]}</span></li></ol><p class="reason">{reason}</p></div>'''
S.append(slide('s25','t-routine t-exit','Predictions and exit ticket','Exit ticket','Objectives 4.5.1, 4.5.3 and 4.5.5',f'''    <div class="stack">
      <div class="phaseA" id="s25-A" data-label="answers">
        <div class="stack">
{pa('s25-p1',1,PQ[0][0],('A','H<sub>2</sub>O molecules'),'Boiling separates whole molecules. Each keeps its O–H bonds.','answer 1')}
{pa('s25-p2',2,PQ[1][0],('B','does not conduct'),'Its ions are locked in the crystal. Molten or dissolved salt conducts.','answer 2')}
{pa('s25-p3',3,PQ[2][0],('B','an attraction between molecules'),'A hydrogen bond is about 5 to 10% of a covalent bond.','answer 3')}
        </div>
        <p class="handsup">Hands up if you predicted this.</p>
      </div>
      <div class="phaseB" id="s25-B" data-label="exit ticket">
        <div class="card prompt dq reg"><p>{DQ}</p></div>
        <ol class="rail"><li id="s25-r1">Claim</li><li id="s25-r2">Evidence</li><li id="s25-r3">Reasoning</li><li id="s25-r4">Self-check</li><li id="s25-r5">Sample</li></ol>
        <div class="rt-main">
          <div class="acc">
            <div class="card phase" id="s25-fr" data-label="claim"><p class="tag">Write</p><ol class="frames">
              <li id="s25-f1">The forces that must come apart decide {GAP}.</li>
              <li id="s25-f2" data-label="evidence">Snow melts at {GAP} °C because only {GAP} let go. Salt needs 801 °C because {GAP} must come apart. Sand needs near 1700 °C because {GAP}.</li>
              <li id="s25-f3" data-label="reasoning">Attractions between molecules are much weaker than bonds within, so {GAP}.</li>
            </ol>
            <div class="bank"><b>Word bank:</b> <span>attractions between molecules</span> <span>bonds within</span> <span>ionic bonds</span> <span>covalent bonds</span> <span>a network</span> <span>weaker</span> <span>higher melting point</span></div></div>
            <div class="card" id="s25-check" data-label="self-check"><p class="tag">Self-check: did you write</p><ul class="crit"><li>a claim about the forces that come apart?</li><li>snow, salt and sand with their melting points?</li><li>attractions weaker than bonds in the reasoning?</li></ul></div>
            <div class="card reg" id="s25-sample" data-label="sample answer"><p class="tag">Sample answer</p><p>The forces that come apart set the melting point. Snow melts at 0 °C: only attractions between molecules let go. Salt needs 801 °C: ionic bonds. Sand needs near 1700 °C: covalent bonds. Attractions are weaker than bonds.</p></div>
          </div>
          <div class="timer"></div>
        </div>
      </div>
    </div>''',
 'Predictions from slide 4 come back first; students check their letters. Then the CER exit ticket on the driving question, with the snow day as evidence. The question stays on screen while the sample shows. Collect the exit tickets.',
 [dict(show=['s25-A','s25-p1'],note='Answer 1: H₂O molecules. Hands up if you predicted A. Compare with the counts from slide 4.'),
  dict(hide='s25-p1',show='s25-p2',note='Answer 2: does not conduct; the ions are locked. Ask a student who changed their mind to say why.'),
  dict(hide='s25-p2',show='s25-p3',note='Answer 3: an attraction between molecules, about 5 to 10% of a covalent bond.'),
  dict(hide='s25-A',show=['s25-B','s25-fr','s25-f1'],cls={'s25-r1':'now'},note='Exit ticket. Claim first: what decides the melting point?'),
  dict(show='s25-f2',cls={'s25-r1':'done','s25-r2':'now'},note='Evidence: the snow day, with the three melting points of slide 3.'),
  dict(show='s25-f3',cls={'s25-r2':'done','s25-r3':'now'},timer=180,label='write 3 min',note='Reasoning: attractions are much weaker than bonds. Three minutes of writing.'),
  dict(show='s25-check',cls={'s25-r3':'done','s25-r4':'now'},note='Self-check with the three criteria.'),
  dict(hide='s25-fr',show='s25-sample',cls={'s25-r4':'done','s25-r5':'now'},note='Compare with the sample. Collect the tickets.')]))

# ---------- 26 rate your learning
T = [('4.5.1',ICAN[0][1],'slides 6 and 7'),('4.5.2',ICAN[1][1],'slides 8 to 10'),('4.5.3',ICAN[2][1],'slides 11 and 12'),('4.5.4',ICAN[3][1],'slides 15 to 17'),('4.5.5',ICAN[4][1],'slides 18 and 19')]
rt = '\n'.join(f'        <li id="s26-t{k+1}"><span><b class="mono lbl">{a}</b> {b}</span><span class="rev">Review: {c}</span></li>' for k,(a,b,c) in enumerate(T))
S.append(slide('s26','t-routine','Rate your learning','Reflect','All objectives',f'''    <div class="scale lbl"><span>1 finger: not yet</span><span>2 fingers: almost</span><span>3 fingers: I can teach it</span></div>
    <p class="tag">I can</p>
    <ol class="rate">
{rt}
    </ol>''',
 'Fingers 1 to 3 for each target. Students below 3 revisit the review slides named on the right.',
 [dict(note='Explain the scale: 1 not yet, 2 almost, 3 I can teach it.')]+
 [dict(cls=dict([(f's26-t{j+1}','') for j in range(k)]+[(f's26-t{k+1}','now')]),label=f'target {k+1}',note=f'Fingers for target 4.5.{k+1}. Note who shows 1 and point to the review slides.') for k in range(5)]))

# ---------- 27 next
S.append(slide('s27','t-summary tnext','Next','Next','Missions 4.5 and the case file','''    <div class="mrow">
      <div class="mission card"><svg viewBox="0 0 100 100" role="img" aria-label="Icon: two molecules and a dashed attraction"><use href="#ic-dipole"/></svg><b>Name the attraction</b><span>six substances</span></div>
      <div class="mission card"><svg viewBox="0 0 100 100" role="img" aria-label="Icon: a hammer and a bent sheet"><use href="#ic-malleable"/></svg><b>Explain the property</b><span>six real materials</span></div>
      <div class="mission card"><svg viewBox="0 0 100 100" role="img" aria-label="Icon: bars from low to high and a thermometer"><use href="#ic-rank"/></svg><b>Rank the boiling points</b><span>five sets</span></div>
    </div>
    <div class="card"><p class="big">The Texas freeze case file uses this lesson. It explains why water pipes burst in February 2021.</p></div>''',
 'Missions for Lesson 4.5: Name the attraction (six substances), Explain the property (six properties of real materials), Rank the boiling points (five sets, lowest to highest). Next in Unit 4: the Texas freeze case file, why water pipes burst in the February 2021 freeze; it uses the ice model of slide 12.',
 [dict(note='Point to the three missions. Preview the case file: water expands when it freezes, so pipes burst.')]))

html = '<main id="stage">\n<div id="prog"><i></i></div>\n' + SPRITE + '\n' + '\n'.join(S) + '''
<footer id="foot"><span id="sec"></span><span id="cue"></span><span id="count"></span></footer>
</main>
<div id="notes" hidden></div>
<div id="overview" hidden></div>
<div id="blank" hidden></div>
<div id="runsheet"></div>
<script>Deck.start()</script>
</body>
</html>
'''
assert '…' not in html, 'no ellipsis character'
open(OUT, 'w', encoding='utf-8', newline='').write(html)
print('slides:', len(S))
