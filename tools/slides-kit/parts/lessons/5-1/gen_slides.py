# Generates slides.html: the 28 slides of Lesson 5.1 (workshop/plan/5-1.md section 5). Run by build.py 5 1.
import json, os, re, html as H
OUT = os.path.join(os.path.dirname(__file__), 'slides.html')
def js(v): return json.dumps(v, ensure_ascii=False)
# minutes per frame (RULES 9: 0.25 per reveal, 1 per check, 1 per rule card, timers at least their minutes); budget.json holds the sums
TIMES = {
 's01':[0.5], 's02':[0.5,0.5,0.5,0.25,0.25,0.5], 's03':[0.5,0.5,0.5,0.5,1], 's04':[0.75,0.5,0.75], 's05':[1,1,0.5],
 's06':[0.25,0.5,0.5,0.25,0.25,1,1,0.25], 's07':[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,0.75,0.25], 's08':[0.25,0.25,0.25,0.25,0.25,0.25,1,0.75,0.25],
 's09':[0.25,0.25,0.25,0.25,0.75,0.25,0.25,1,0.75,0.25], 's10':[0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,0.75,0.25],
 's11':[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,0.75,0.25], 's12':[0.25,0.25,0.25,0.25,0.25,0.25,0.25,1], 's13':[0.25,0.25,0.25,0.25,0.25,0.25,1,0.75,0.25],
 's14':[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1.5],
 's15':[0.25,1.5,0.25,0.25,0.25], 's16':[0.25,0.25,0.25,0.25,0.25,1,0.75,0.25], 's17':[0.25,0.25,0.25,0.25,0.25,0.25,1,0.75,0.25],
 's18':[0.25,0.25,0.25,0.25,0.25,1,0.75,0.25], 's19':[0.25,0.25,0.25,0.25,0.25,0.25,1,0.75,0.25], 's20':[0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,3,0.25,0.25,0.25],
 's21':[0.25,0.25,0.25,0.25,1], 's22':[0.5,0.1,0.1,0.1,0.1,0.1], 's23':[0.25,0.5,1,1.5,0.5,0.75], 's24':[0.25,0.5,1,1.5,0.5,0.75], 's25':[0.25,0.5,1,1.5,0.5,0.75],
 's26':[0.5,0.25,0.25,0.5,0.25,3,0.25,0.5], 's27':[0.5,0.25,0.25,0.25,0.25], 's28':[0.5]}
def frames(sid, fr):
    assert len(TIMES[sid]) == len(fr), (sid, len(TIMES[sid]), len(fr))
    for f, t in zip(fr, TIMES[sid]): f['t'] = t
    rows = ['{' + ','.join(f"{k}:{js(f[k])}" for k in ['show','hide','stage','cls','timer','focus','label','cue','t','note'] if k in f) + '}' for f in fr]
    return f"<script>Deck.frames('{sid}',[\n    " + ',\n    '.join(rows) + "\n  ]);</script>"
def slide(sid, cls, title, sec, ref, body, notes, fr):
    per = '1' if int(sid[1:]) <= 14 else '2'
    return f'''<section class="slide {cls}" id="{sid}" data-period="{per}" data-title="{title}" data-sec="{sec}" data-ref="{ref}">
  <h2>{title}</h2>
  <div class="body">
{body}
  </div>
  <aside class="notes">{notes}</aside>
  {frames(sid, fr)}
</section>
'''
def nwords(t): return len(re.sub(r'<[^>]+>', '', t).split())
def lay(opts, col=None):
    # one row when every option is two words or fewer, else stacked; the plan's mark wins where it says "one row" (col=False)
    return 'col' if (col if col is not None else max(nwords(o) for o in opts) > 2) else 'row'
def optli(p, opts, right, fb):
    out = ''
    for l, t, f in zip('ABC', opts, fb or [None] * 3):
        g = f' data-ok="{1 if l == right else 0}" data-fb="{H.escape(f, quote=True)}"' if f is not None else ''
        out += f'<li class="opt" id="{p}-{l.lower()}"{g}><b>{l}</b><span>{t}</span></li>'
    return out
def check(p, q, opts, col=None, ans='', right=None, fb=None, pre=''):
    # fb: one feedback line per option (the right option gets its reason); a mouse click shows it under the options
    L = lay(opts, col)
    return f'''      <div class="card check" id="{p}-check" data-label="check">
        <p class="tag">Check</p>{pre}
        <p class="q">{q}</p>
        <ol class="opts{' col1' if L == 'col' else ''}" data-lay="{L}">{optli(p, opts, right, fb)}</ol>
        <div class="af"><p class="ans" id="{p}-ans" data-label="answer">{ans}</p><p class="fb" aria-live="polite"></p></div>
      </div>'''
def chips(label, items):
    # a value list with its meaning: a label line, then one chip per value (class g, mol or n: the quantity's color)
    return f'<span class="enrow"><span class="enl lbl">{label}</span><span class="chips">' + ''.join(f'<span class="chip {c}">{x}</span>' for x, c in items) + '</span></span>'
def use(i, label, cls='', vb='0 0 100 100'):
    return f'<svg class="{cls}" viewBox="{vb}" role="img" aria-label="{label}"><use href="#{i}"/></svg>'
def card(i, tag, text, lab, cls=''):
    return f'      <div class="card{(" " + cls) if cls else ""}" id="{i}" data-label="{lab}"><p class="tag">{tag}</p><p>{text}</p></div>'
def rail(p, names=('Think','Talk','Write','Self-check','Compare')):
    return '<ol class="rail">' + ''.join(f'<li id="{p}-r{k+1}">{t}</li>' for k, t in enumerate(names)) + '</ol>'
NA = '6.022&nbsp;×&nbsp;10<sup>23</sup>'
NAX = '6.02214076&nbsp;×&nbsp;10<sup>23</sup>'
CAP = 'Atom colors show the element, not the charge.'

SPRITE = '''<svg class="sprite" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden"><defs>
<symbol id="ic-next" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M48 30v40l32-20Z" class="f-acc"/></symbol>
<symbol id="ic-back" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M72 30v40L40 50Z" class="f-acc"/></symbol>
<symbol id="ic-blank" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><rect x="34" y="30" width="52" height="34" rx="4" class="f-ink"/><path d="M52 74h16" class="k-ink" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-start" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M30 34v-8h10M90 34v-8H80M30 66v8h10M90 66v8H80" fill="none" class="k-acc" stroke-width="5" stroke-linecap="round"/><path d="M52 38v24l20-12Z" class="f-acc"/></symbol>
<symbol id="ic-bag" viewBox="0 0 100 100"><path d="M24 34h52l10 52a8 8 0 0 1-8 10H22a8 8 0 0 1-8-10Z" class="f-tan k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M36 34l-6-18h40l-6 18" class="f-tan k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M30 34h40" class="k-ink" stroke-width="6" stroke-linecap="round"/><circle cx="50" cy="66" r="14" class="f-nickel k-ink" stroke-width="3"/></symbol>
<symbol id="ic-spoonful" viewBox="0 0 100 100"><path d="M52 62 94 38" class="k-ink" stroke-width="9" stroke-linecap="round"/><ellipse cx="34" cy="66" rx="30" ry="20" class="f-metal k-ink" stroke-width="3"/><ellipse cx="34" cy="64" rx="22" ry="12" class="f-water"/></symbol>
<symbol id="ic-dots" viewBox="0 0 100 100"><g class="f-e"><circle cx="20" cy="30" r="5"/><circle cx="38" cy="22" r="5"/><circle cx="58" cy="30" r="5"/><circle cx="78" cy="24" r="5"/><circle cx="26" cy="50" r="5"/><circle cx="46" cy="44" r="5"/><circle cx="66" cy="52" r="5"/><circle cx="86" cy="46" r="5"/><circle cx="16" cy="72" r="5"/><circle cx="36" cy="68" r="5"/><circle cx="56" cy="74" r="5"/><circle cx="76" cy="70" r="5"/><circle cx="46" cy="88" r="5"/><circle cx="66" cy="90" r="5"/></g></symbol>
<symbol id="ic-mole" viewBox="0 0 100 100"><rect x="39" y="2" width="22" height="26" rx="4" class="f-sea k-ink" stroke-width="3"/><circle cx="50" cy="62" r="36" class="f-sea k-ink" stroke-width="3"/><g class="f-e"><circle cx="34" cy="44" r="4"/><circle cx="50" cy="38" r="4"/><circle cx="66" cy="44" r="4"/></g><text x="50" y="80" text-anchor="middle" font-size="34" class="f-e">mol</text></symbol>
<symbol id="ic-number" viewBox="0 0 100 100"><text x="50" y="38" text-anchor="middle" font-size="34" class="f-e">6.022</text><rect x="3" y="50" width="94" height="46" rx="12" class="f-card2 k-ink" stroke-width="3"/><text x="50" y="85" text-anchor="middle" font-size="34" class="f-ink">×10²³</text></symbol>
<symbol id="ic-constant" viewBox="0 0 100 100"><text x="50" y="38" text-anchor="middle" font-size="34" class="f-e">6.022</text><rect x="8" y="50" width="84" height="46" rx="12" class="f-card2 k-acc" stroke-width="4"/><text x="50" y="85" text-anchor="middle" font-size="34" class="f-acc">/mol</text></symbol>
<symbol id="ic-amount" viewBox="0 0 100 100"><path d="M8 70h62l-8 14H16Z" class="f-metal k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M39 84v8M22 94h34" class="k-ink" stroke-width="5" stroke-linecap="round"/><g class="f-e"><circle cx="26" cy="62" r="7"/><circle cx="40" cy="62" r="7"/><circle cx="54" cy="62" r="7"/><circle cx="33" cy="50" r="7"/><circle cx="47" cy="50" r="7"/></g><circle cx="76" cy="28" r="23" class="f-acc"/><text x="76" y="40" text-anchor="middle" font-size="34" class="f-on">n</text></symbol>
<symbol id="ic-molecule" viewBox="0 0 100 100"><path d="M50 46 22 70M50 46l28 24" class="k-ink" stroke-width="7" stroke-linecap="round"/><circle cx="50" cy="44" r="24" class="f-nm"/><circle cx="20" cy="72" r="14" class="f-nms k-nm" stroke-width="3"/><circle cx="80" cy="72" r="14" class="f-nms k-nm" stroke-width="3"/></symbol>
<symbol id="ic-funit" viewBox="0 0 100 100"><circle cx="30" cy="52" r="22" class="f-cat"/><circle cx="68" cy="52" r="30" class="f-an"/><path d="M20 52h20M30 42v20M56 52h24" class="k-on" stroke-width="6" stroke-linecap="round"/></symbol>
<symbol id="ic-formula" viewBox="0 0 100 100"><text x="2" y="62" font-size="40" class="f-ink">H</text><circle cx="48" cy="66" r="16" fill="none" class="k-warm" stroke-width="4"/><text x="48" y="78" text-anchor="middle" font-size="34" class="f-warm">2</text><text x="66" y="62" font-size="40" class="f-ink">O</text></symbol>
<symbol id="ic-subscript" viewBox="0 0 100 100"><text x="4" y="66" font-size="62" class="f-ink">O</text><circle cx="72" cy="70" r="20" fill="none" class="k-warm" stroke-width="5"/><text x="72" y="82" text-anchor="middle" font-size="34" class="f-warm">2</text></symbol>
<symbol id="ic-avgmass" viewBox="0 0 100 100"><circle cx="27" cy="46" r="20" class="f-rope"/><circle cx="73" cy="46" r="20" style="fill:color-mix(in srgb,var(--rope) 60%,#000)"/><path d="M8 80h84" class="k-ink" stroke-width="5" stroke-linecap="round"/><path d="M50 70v20" class="k-acc" stroke-width="6" stroke-linecap="round"/></symbol>
<symbol id="ic-nickel" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" class="f-nickel k-ink" stroke-width="4"/><circle cx="50" cy="50" r="28" fill="none" class="k-ink" stroke-width="2"/></symbol>
<symbol id="ic-cents" viewBox="0 0 100 100"><circle cx="32" cy="44" r="26" class="f-rope k-ink" stroke-width="3"/><circle cx="68" cy="58" r="26" class="f-cent k-ink" stroke-width="3"/><circle cx="68" cy="58" r="18" class="f-zinc"/></symbol>
<symbol id="ic-flask" viewBox="0 0 100 100"><rect x="39" y="2" width="22" height="26" rx="4" class="f-sea k-ink" stroke-width="3"/><circle cx="50" cy="62" r="36" class="f-sea k-ink" stroke-width="3"/><g class="f-e"><circle cx="34" cy="50" r="5"/><circle cx="52" cy="44" r="5"/><circle cx="68" cy="56" r="5"/><circle cx="40" cy="70" r="5"/><circle cx="60" cy="76" r="5"/><circle cx="28" cy="64" r="5"/><circle cx="72" cy="72" r="5"/><circle cx="50" cy="60" r="5"/><circle cx="50" cy="88" r="5"/></g></symbol>
<symbol id="ic-scale" viewBox="0 0 100 100"><rect x="10" y="60" width="80" height="32" rx="8" class="f-card2 k-ink" stroke-width="3"/><rect x="26" y="68" width="48" height="16" rx="4" class="f-card k-ink" stroke-width="2"/><path d="M8 56h84" class="k-ink" stroke-width="6" stroke-linecap="round"/><g class="f-nickel k-ink" stroke-width="2"><circle cx="38" cy="44" r="10"/><circle cx="58" cy="44" r="10"/><circle cx="48" cy="28" r="10"/></g></symbol>
<symbol id="ic-swap" viewBox="0 0 100 100"><circle cx="24" cy="50" r="18" class="f-acc"/><g class="f-e"><circle cx="72" cy="38" r="6"/><circle cx="86" cy="50" r="6"/><circle cx="72" cy="62" r="6"/><circle cx="62" cy="50" r="6"/></g><path d="M40 36h22m-8-8 8 8-8 8M60 64H38m8 8-8-8 8-8" fill="none" class="k-muted" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="ic-jar" viewBox="0 0 100 100"><rect x="26" y="6" width="48" height="12" rx="4" class="f-metal k-ink" stroke-width="3"/><rect x="18" y="18" width="64" height="76" rx="16" class="f-water k-ink" stroke-width="3" fill-opacity=".5"/><g class="k-ink" stroke-width="2"><circle cx="36" cy="80" r="10" class="f-rope"/><circle cx="58" cy="80" r="10" class="f-cent"/><circle cx="47" cy="62" r="10" class="f-nickel"/><circle cx="66" cy="60" r="10" class="f-rope"/></g></symbol>
</defs></svg>'''

S = []
DQ1 = 'Particles are far too small and too many to count one by one.'
DQ2 = 'How can chemists count them?'
# ---------- 1 cover
S.append(slide('s01','t-cover','Counting particles with the mole','Lesson 5.1','Reading §5.1',f'''    <div class="card dq reg"><p class="tag">Driving question</p><p>{DQ1} {DQ2}</p></div>
    <div class="r800">
      <div class="key">{use('ic-next','Next button','','0 0 120 100')}<b>Next</b><span>next step</span></div>
      <div class="key">{use('ic-back','Back button','','0 0 120 100')}<b>Back</b><span>one step back</span></div>
      <div class="key">{use('ic-blank','Blank button','','0 0 120 100')}<b>Blank</b><span>zoom part by part<br>twice fast: blank</span></div>
      <div class="key">{use('ic-start','Start button','','0 0 120 100')}<b>Start</b><span>full screen</span></div>
    </div>''',
 '<b>Safety.</b> Nothing dangerous in this lesson. A real bag of nickels and a balance may be used live as the hook, and are recommended; nothing in the deck depends on it. <b>Data and sources.</b> U.S. Mint coin specifications: nickel 5.000 g, cent made after 1982 2.500 g (zinc coated with copper); the cent made before 1982, 3.11 g (95% copper), from secondary sources. The Mint struck its last circulating cent on November 12, 2025, so the deck says "cents made after 1982", never "today\'s cents". BIPM: the 2019 definition of the mole (exactly 6.02214076 × 10²³, voted November 16, 2018, in force May 20, 2019) and the 1971 resolution (12 g of carbon-12). NIST: the silicon spheres of the Avogadro project, lattice parameter 543.102 pm. NobelPrize.org: Jean Perrin, Physics 1926. NASA JPL: the universe 13.8 billion years old. USGS: Earth 4.54 billion years (the deck says about 4.5 billion). OpenStax Chemistry 2e, section 3.1. CIAAW masses: Al 26.982, Cu 63.546, Si 28.085 (g for one mole). Shannon 1976 ionic radii (Na⁺ 102 pm, Cl⁻ 181 pm); Cordero 2008 covalent radii; NIST CCCBDB geometries (H₂O 104.5°, CO₂ 180°, NH₃ 106.7°); NaCl cell 564 pm (the value Unit 4 used). <b>Clicker.</b> Logitech R800: Next = PageDown, Back = PageUp (while zoomed: exit the zoom), Start/stop = F5 then Escape, Blank = period. Blank zooms one part of the slide per press, animation first; the press after the last part exits; two fast presses on an unzoomed slide blank the screen. Mouse: click an option to mark it right or wrong; click the slide number or the section label for the slide list. Laptop: N notes, O overview, T theme, Ctrl+P run-sheet.',
 [dict(note='Two periods. Read the driving question aloud; students copy it. Show the four clicker buttons once, so a zoom or a blank screen is on purpose.')]))
# ---------- 2 hook
S.append(slide('s02','t-hook','The coin jar','Hook','Reading §5.1.1','''    <div class="sim" id="s02-sim" data-sim="coinScale" aria-label="A jar of nickels on a kitchen table; then the jar on a kitchen scale."></div>
    <div class="stack card band">
      <p class="line" id="s02-l0">A jar of nickels on the kitchen table. How many?</p>
      <p class="line" id="s02-l1" data-label="predict">Predict: guess the number. Then say how you would count them.</p>
      <p class="line" id="s02-l2" data-label="count one by one">Counting one by one is slow. It is easy to lose count.</p>
      <p class="line" id="s02-l3" data-label="the scale">Put the jar on a scale. Every nickel has the same mass.</p>
      <p class="line" id="s02-l4" data-label="divide">Divide the mass of the coins by the mass of one coin.</p>
      <p class="line" id="s02-l5" data-label="the thread">Too many to count? Weigh them.</p>
    </div>''',
 'Narrative thread for 5.1: too many to count? weigh them, then think in moles. An everyday jar, no chemistry yet. The bank\'s bag comes next (slide 3), and the bank\'s scale returns on slide 6.',
 [dict(show='s02-l0',stage='s02-sim:jar',note='Ask: who has a jar of coins at home? How would you find out how many are in it?'),
  dict(hide='s02-l0',show='s02-l1',stage='s02-sim:guess',note='Prediction: each table writes one guess and one way to count. Collect the guesses on the board. Do not judge them.'),
  dict(hide='s02-l1',show='s02-l2',stage='s02-sim:tally',note='The counter climbs one coin a second, then "lost count". Ask: how long would a jar of 400 take? Listen for "too long".'),
  dict(hide='s02-l2',show='s02-l3',stage='s02-sim:scale',note='The scale reads the coins: 2,000.0 g. Every nickel has a mass of 5.000 g. The scale was zeroed with the empty jar; slide 6 teaches zeroing.'),
  dict(hide='s02-l3',show='s02-l4',stage='s02-sim:reveal',note='2,000.0 g ÷ 5.000 g = 400 nickels. Compare with the guesses. Misconception to listen for: "multiply the two masses".'),
  dict(hide='s02-l4',show='s02-l5',note='The thread line. Students write it at the top of the page: too many to count? Weigh them.')]))
# ---------- 3 launch
S.append(slide('s03','t-launch','A bag of nickels at the bank','Launch','Reading §5.1 opener',f'''    <div class="trio" id="s03-trio">
      <div class="card pcard slot"><div data-b="s03-bag" data-label="the bank bag">{use('ic-bag','Icon: a sealed bank bag of nickels')}<p class="nm lbl">bank bag</p><p class="cap">1,250.0 g of nickels. The bank says 250, without opening it.</p></div></div>
      <div class="card pcard slot"><div data-b="s03-spoon" data-label="a spoonful of water">{use('ic-spoonful','Icon: a spoonful of water')}<p class="nm lbl">spoonful of water</p><p class="cap">About 18 g of water. More molecules than anyone can count.</p></div></div>
      <div class="card pcard slot"><div data-b="s03-dots" data-label="atoms">{use('ic-dots','Icon: a cloud of tiny dots')}<p class="nm lbl">atoms</p><p class="cap">Atoms: too small to see, too many to count.</p></div></div>
    </div>
    <div class="card dq reg" id="s03-dq" data-label="driving question"><p>{DQ1} {DQ2}</p></div>
    <div class="qrow" id="s03-st" data-label="write 60 s"><ol class="frames"><li>I think chemists count tiny particles by <span class="gap"></span>.</li></ol><div class="timer"></div></div>''',
 'The reading\'s opener: a bank teller counts a sealed bag of nickels by weighing it. A few grams of any substance hold more atoms than anyone could count one by one.',
 [dict(show='s03-bag',note='The bank never opens the bag. Ask: how can it know there are 250?'),
  dict(show='s03-spoon',note='About 18 g of water, a little more than a spoonful. Ask: could anyone count its molecules?'),
  dict(show='s03-dots',note='Atoms are far too small to see, and far too many to count.'),
  dict(show='s03-dq',cls={'s03-trio':'small'},note='Read the driving question. Students copy it at the top of the notebook page.'),
  dict(show='s03-st',timer=60,note='Sixty seconds with the starter. Collect two answers; do not correct yet. Listen for "a microscope" and "a very big number".')]))
# ---------- 4 predict now
def pq(p, n, q, opts, lab, row=False):
    o = ''.join(f'<li class="opt"><b>{l}</b><span>{t}</span></li>' for l, t in zip('ABC', opts))
    return f'      <div class="card check" id="{p}" data-label="{lab}" data-mode="pick"><p class="tag">Question {n}</p><p class="q">{q}</p><ol class="opts{"" if row else " col1"}" data-lay="{"row" if row else "col"}">{o}</ol></div>'
S.append(slide('s04','t-routine pn','Predict now','Predict','Reading §5.1 Before you read',f'''    <div class="card prompt"><p>Hands up: one finger for A, two for B, three for C.</p></div>
    <div class="stack top">
{pq('s04-q1',1,'One mole of copper and one mole of aluminum have…',['the same mass','the same number of atoms','the same mass and number'],'question 1')}
{pq('s04-q2',2,'One mole of sodium chloride, NaCl, holds 6.022&nbsp;×&nbsp;10<sup>23</sup>…',['molecules','formula units','atoms'],'question 2',True)}
{pq('s04-q3',3,'One mole of water, H<sub>2</sub>O, holds how many moles of hydrogen atoms?',['1 mol','2 mol',NA+' mol'],'question 3',True)}
    </div>''',
 'No answers on this slide. Students keep their letters; slide 26 returns all three answers.',
 [dict(show='s04-q1',note='Count hands for A, B, C and write the counts on the board. Do not react. A mouse click on an option only highlights it; there is no grading on this slide.'),
  dict(hide='s04-q1',show='s04-q2',note='Count hands. Many choose "molecules" for salt (the particle is a formula unit).'),
  dict(hide='s04-q2',show='s04-q3',note='Count hands. "1 mol" is the common idea: one water, one hydrogen. Keep the counts for slide 26.')]))
# ---------- 5 targets and words
W = [('ic-mole','mole','mol','the counting unit: '+NA+' particles'),
     ('ic-number','Avogadro\'s number','número de Avogadro','the number in one mole, no unit'),
     ('ic-constant','Avogadro constant','constante de Avogadro','the same number per mole, mol<sup>−1</sup>'),
     ('ic-amount','amount of substance','cantidad de sustancia','what moles measure'),
     ('ic-molecule','molecule','molécula','atoms joined by covalent bonds'),
     ('ic-funit','formula unit','unidad fórmula','one set of ions: Na<sup>+</sup> and Cl<sup>−</sup>'),
     ('ic-formula','chemical formula','fórmula química','which atoms, how many of each'),
     ('ic-subscript','subscript','subíndice','the small number after a symbol')]
wc = '\n'.join(f'        <div class="wcard" id="s05-w{k+1}">{use(i,"Icon: "+H.unescape(re.sub("<[^>]+>","",t)))}<p class="t">{t} <span class="es">({es})</span></p><p class="m">{m}</p></div>' for k,(i,t,es,m) in enumerate(W))
S.append(slide('s05','t-words','Targets and words','Targets','Reading §5.1 Vocabulary',f'''    <div class="stack">
      <div class="card" id="s05-ican" data-label="targets"><p class="tag">I can…</p><ul class="ican">
        <li><b>5.1.1</b>count objects by weighing, with one mass or an average.</li>
        <li><b>5.1.2</b>define the mole and use Avogadro's number.</li>
        <li><b>5.1.3</b>change moles to particles and back, naming the particle.</li>
        <li><b>5.1.4</b>use a formula to count atoms in a sample.</li></ul></div>
      <div class="words" id="s05-words" data-label="words">
{wc}
      </div>
    </div>
    <div class="legend" id="s05-leg" data-label="color code"><span><i class="i-g">g</i>grams (mass)</span><span><i class="i-mol">mol</i>moles (amount)</span><span><i class="i-n">#</i>particles (number)</span><span><i class="i-cat">+</i>cation</span><span><i class="i-an">−</i>anion</span><span><i class="i-atom">O</i>atom (CPK color = element)</span></div>''',
 'Unit 5 color code (plan section 3), the same in every Unit 5 deck: mass in grams amber, amount in moles teal, number of particles violet; a conversion factor is a gray bridge; ions keep Unit 4\'s red "+" and blue "−"; atoms keep CPK colors with the symbol on every sphere. Shapes carry a sign or a symbol, so color-blind students can read every drawing.',
 [dict(show='s05-ican',note='Read the four targets. Students copy 5.1.1 to 5.1.4; they rate themselves on slide 27.'),
  dict(hide='s05-ican',show='s05-words',note='Choral reading: English term, then the Spanish cognate. Students add the words to the glossary with the icon. Stress: Avogadro\'s number has no unit; the Avogadro constant is per mole.'),
  dict(show='s05-leg',note='Color code: grams amber, moles teal, particles violet; cation red with +, anion blue with −; atoms in CPK colors.')]))
# ---------- 6 counting by weighing
S.append(slide('s06','t-concept cw','Counting by weighing','Counting by weighing','Reading §5.1.1',f'''    <div class="sim" id="s06-sim" data-sim="coinScale" aria-label="A bank bag of nickels on a scale; the scale is zeroed; the mass is divided by the mass of one nickel."></div>
    <div class="col acc">
{card('s06-c0','The bank','A sealed bag of nickels on the bank\'s scale.','the bag')}
{card('s06-c1','Zero the scale','First, zero the scale with the empty bag. Now it reads the coins alone.','zero')}
{card('s06-pred','Predict','The scale reads 1,250.0&nbsp;g. How many nickels?','predict')}
      <div class="card" id="s06-c2" data-label="divide"><p class="tag">Divide</p>{chips('Mass of one nickel',[('5.000&nbsp;g','g')])}<p>1,250.0&nbsp;g ÷ 5.000&nbsp;g per nickel. The grams cancel.</p></div>
{card('s06-c3','Count','250 nickels. Check: 250 × 5.000&nbsp;g = 1,250.0&nbsp;g.','count')}
{card('s06-rule','Rule','If every object has the same mass, divide the total by one object\'s mass. The grams cancel. A pure number is left.','rule','rule reg')}
{check('s06','A roll of nickels has a mass of 200.0&nbsp;g. How many nickels is that?',['40','1,000','200'],ans='A. 200.0&nbsp;g ÷ 5.000&nbsp;g per nickel = 40 nickels.',right='A',
  fb=['Divide: 200.0 g ÷ 5.000 g = 40.','That multiplies the two masses. Divide by the mass of one nickel.','200 is the mass in grams, not the count. Divide by 5.000 g.'])}
    </div>''',
 'Zeroing (taring) in words: the scale reads 0.0 g with the empty bag on it, so it then shows the mass of the coins alone. The grams cancel, leaving a pure number of nickels.',
 [dict(show='s06-c0',stage='s06-sim:bag',focus='s06-sim',note='A bank bag of nickels on the bank\'s scale. Ask: what would the scale show?'),
  dict(show='s06-c1',stage='s06-sim:zero',note='The empty bag on the scale, then zero: the reading is 0.0 g. Say "zero", the word "tare" once.'),
  dict(hide=['s06-c0','s06-c1'],show='s06-pred',stage='s06-sim:read',note='Prediction: 1,250.0 g of nickels. How many? Collect answers on whiteboards. Listen for "multiply".'),
  dict(hide='s06-pred',show='s06-c2',stage='s06-sim:divide',note='1,250.0 g × 1 nickel / 5.000 g: the grams cancel (struck in red).'),
  dict(show='s06-c3',stage='s06-sim:count',note='250 nickels. The check multiplies back: 250 × 5.000 g = 1,250.0 g.'),
  dict(hide='s06-c2',show='s06-rule',note='Students copy the rule card (reading §5.1.1 Key idea).'),
  dict(hide='s06-c3',show='s06-check',stage='s06-sim:roll',note='Hands up for A, B or C. The animation shows the roll: 200.0 g on the scale. The answer is not drawn.'),
  dict(show='s06-ans',cls={'s06-a':'right','s06-check':'done'},note='A is right: 200.0 g ÷ 5.000 g = 40. B (1,000): that multiplies the two masses; divide by the mass of one nickel. C (200): 200 is the mass in grams, not the count; divide by 5.000 g.')]))
# ---------- 7 counting a mixed jar
S.append(slide('s07','t-concept cw','Counting a mixed jar','Counting by weighing','Reading §5.1.1',f'''    <div class="sim" id="s07-sim" data-sim="centJar" aria-label="A jar of pennies with two kinds of cents; a sample of 100 cents gives the average mass."></div>
    <div class="col acc">
      <div class="card" id="s07-c0" data-label="the jar"><p class="tag">A jar of pennies</p><p>Two kinds of cents, two masses.</p>{chips('Mass of one cent',[('before 1982: 3.11&nbsp;g','g'),('after 1982: 2.500&nbsp;g','g')])}</div>
{card('s07-pred','Predict','Divide the jar\'s 1,017.1&nbsp;g by 2.500&nbsp;g? Thumbs up or down.','predict')}
{card('s07-c1','Wrong divisors','÷ 2.500&nbsp;g counts too many. ÷ 3.11&nbsp;g counts too few.','wrong divisors')}
{card('s07-c2','Sample','Weigh a sample of 100 cents: 267.69&nbsp;g.','sample')}
{card('s07-c3','Average','267.69&nbsp;g ÷ 100 = 2.6769&nbsp;g per cent in this jar.','average')}
{card('s07-c4','Count','1,017.1&nbsp;g ÷ 2.6769&nbsp;g = about 380 cents.','count')}
      <div class="card word" id="s07-word" data-label="new word">{use('ic-avgmass','Icon: two isotopes of one size and different mass, and their average','ic')}<p class="term">average atomic mass <span class="es">(masa atómica promedio)</span></p><p class="mean">the table's mass, an average over isotopes</p></div>
{card('s07-c5','Isotopes','Most elements are a mix of isotopes. The table gives the average mass.','isotopes')}
{card('s07-rule','Rule','A mix of objects is counted with the average mass of one object. Average atomic masses let chemists count atoms the same way.','rule','rule reg')}
{check('s07','A jar holds both kinds. Which mass do you divide by?',['this jar\'s own average','the average of 2.500&nbsp;g and 3.11&nbsp;g','2.500&nbsp;g, a newer cent'],col=True,ans='A. Divide a sample\'s mass by its count.',right='A',
  fb=['The jar\'s own average is the right divisor.','That works only if the jar holds equal numbers of each kind.','Dividing by the lighter cent counts too many coins.'])}
    </div>''',
 'Lesson 2.3 link: the average atomic mass on the periodic table is the average over an element\'s isotopes, just as 2.6769 g is the average cent of this jar. "About 407" (1,017.1 g ÷ 2.500 g) and "about 327" (1,017.1 g ÷ 3.11 g) are computed from the reading\'s data; the reading says "too many" and "too few". The isotope picture draws every copper atom at one size in two shades: the shades stand for two masses, and isotopes of one element have the same size.',
 [dict(show='s07-c0',stage='s07-sim:jar',focus='s07-sim',note='Two kinds of cents: made before 1982 (95% copper, 3.11 g) and made after 1982 (zinc coated with copper, 2.500 g). The jar of pennies has a mass of 1,017.1 g.'),
  dict(show='s07-pred',note='Prediction: thumbs up or down for dividing by 2.500 g. Most say up.'),
  dict(hide='s07-pred',show='s07-c1',stage='s07-sim:wrong',note='÷ 2.500 g gives about 407: too many, because some cents are heavier. ÷ 3.11 g gives about 327: too few.'),
  dict(hide='s07-c0',show='s07-c2',stage='s07-sim:sample',note='A sample of 100 cents from this jar has a mass of 267.69 g.'),
  dict(show='s07-c3',stage='s07-sim:average',note='267.69 g ÷ 100 = 2.6769 g per cent. Misconception: "average 2.500 and 3.11" (works only with equal numbers of each).'),
  dict(hide=['s07-c1','s07-c2'],show='s07-c4',stage='s07-sim:count',note='1,017.1 g ÷ 2.6769 g = about 380 cents. Check: 2.6769 lies between 2.500 and 3.11.'),
  dict(hide='s07-c3',show='s07-word',note='Read the word card; students repeat "average atomic mass, masa atómica promedio".'),
  dict(show='s07-c5',stage='s07-sim:isotopes',note='The coins become atoms: one element, a mix of isotopes. The two shades stand for two masses. Isotopes of one element have the same size. The periodic table gives the average mass: copper 63.546. No isotope masses are needed.'),
  dict(hide=['s07-c4','s07-word'],show='s07-rule',note='Students copy the rule card (reading §5.1.1 Key idea).'),
  dict(hide=['s07-c5','s07-rule'],show='s07-check',stage='s07-sim:sample',note='Hands up for A, B or C. The animation returns to the sample of 100 cents.'),
  dict(show='s07-ans',cls={'s07-a':'right','s07-check':'done'},note='A is right: weigh a sample of this jar and divide its mass by its count. B (the average of 2.500 g and 3.11 g): that works only if the jar holds equal numbers of each kind. C (2.500 g): dividing by the lighter cent counts too many coins.')]))
# ---------- 8 the mole
S.append(slide('s08','t-concept cw','The mole','The mole','Reading §5.1.2',f'''    <div class="sim" id="s08-sim" data-sim="countingUnits" aria-label="A dozen eggs, a ream of paper and a flask holding one mole of particles."></div>
    <div class="col acc">
{card('s08-c0','A dozen','A baker counts eggs by the dozen: 12.','a dozen')}
{card('s08-c1','A ream','A ream of paper: 500 sheets.','a ream')}
{card('s08-pred','Predict','Atoms are tiny. How big must the chemist\'s counting unit be?','predict')}
{card('s08-c2','The mole','One mole: '+NA+' particles. The symbol is mol.','the mole')}
{card('s08-c3','Exactly','Since May 20, 2019: exactly '+NAX+'. We round it to '+NA+'.','exactly')}
{card('s08-c4','Number or constant','Avogadro\'s number has no unit. The Avogadro constant is the same number per mole: '+NA+'&nbsp;mol<sup>−1</sup>.','the constant')}
{card('s08-rule','Rule','One mole contains exactly '+NAX+' particles. In calculations we round it to '+NA+'. A mole is a count, not a mass.','rule','rule reg')}
{check('s08','A mole is a…',['count of particles: '+NA+' of them','mass of a substance in grams','volume of a substance'],ans='A. Like a dozen, a mole is a number of things. A very large one.',right='A',
  fb=['A mole counts particles, like a dozen counts eggs.','A mole is a count. One mole of different substances has different masses.','A mole is a count. One mole of different substances fills different volumes.'])}
    </div>''',
 '"Amount of substance" is the SI quantity; the mole is its unit. The rounded value 6.022 × 10²³ is the exact number written with fewer digits, not a measurement. N_A is read "N sub A".',
 [dict(show='s08-c0',stage='s08-sim:dozen',focus='s08-sim',note='A counting unit: the baker counts eggs by the dozen. Ask for other counting units (a pair, a ream).'),
  dict(show='s08-c1',stage='s08-sim:ream',note='A ream of paper is 500 sheets. Paper is thin, so the unit is bigger.'),
  dict(hide=['s08-c0','s08-c1'],show='s08-pred',note='Prediction: how big must the counting unit be for atoms? Collect guesses: a thousand? a million?'),
  dict(hide='s08-pred',show='s08-c2',stage='s08-sim:mole',note='One mole is 6.022 × 10²³ particles. Say it: six point oh two two times ten to the twenty-third. The symbol is mol.'),
  dict(show='s08-c3',stage='s08-sim:exact',note='Since May 20, 2019 the number is exact: 6.02214076 × 10²³. In calculations we round it.'),
  dict(hide='s08-c2',show='s08-c4',stage='s08-sim:constant',note='Avogadro\'s number has no unit; the Avogadro constant, N_A, is the same number per mole.'),
  dict(hide='s08-c3',show='s08-rule',note='Students copy the rule card. Misconception: "a mole is a mass".'),
  dict(hide=['s08-c4','s08-rule'],show='s08-check',note='Hands up for A, B or C. The figure of the three counting units stays on screen.'),
  dict(show='s08-ans',cls={'s08-a':'right','s08-check':'done'},note='A is right. B (a mass in grams): a mole is a count; one mole of different substances has different masses. C (a volume): one mole of different substances fills different volumes.')]))
# ---------- 9 how many is a mole
S.append(slide('s09','t-concept cw','How many is a mole?','The mole','Reading §5.1.2',f'''    <div class="sim" id="s09-sim" data-sim="howMany" aria-label="One water molecule, a dozen, a thousand, then zooming out by a thousand each step to one mole."></div>
    <div class="col acc">
{card('s09-c0','One','One water molecule.','one')}
{card('s09-c1','A dozen','A dozen: 12. You can count them.','a dozen')}
{card('s09-c2','A thousand','A thousand: 10 rows, 10 across, 10 deep.','a thousand')}
{card('s09-pred','Predict','10<sup>23</sup> has 23 zeros. How many times must we zoom out by 1,000?','predict')}
{card('s09-c3','Zoom out','Every step is 1,000 times more. Watch the counter.','zoom out')}
{card('s09-c4','One mole','Seven steps, then × 602: '+NA+'. One mole.','one mole')}
{card('s09-c5','A spoonful','All of that water fits in a spoon: about 18&nbsp;g.','the spoon')}
{card('s09-rule','Rule','A mole is '+NA+' particles. Molecules are so small that a mole of water is only about 18&nbsp;g.','rule','rule reg')}
{check('s09','One mole of water molecules has a mass of about…',['18&nbsp;g, less than a large spoonful','1&nbsp;g',NA+'&nbsp;g'],col=True,ans='A. Avogadro\'s number is huge because molecules are tiny.',right='A',
  fb=['A mole of water is about 18 g, a spoonful.','A mole is a count, not one gram. One mole of water is about 18 g.','6.022 × 10²³ is the number of molecules, not the mass in grams.'])}
    </div>''',
 'The prediction\'s answer: seven zoom-outs of × 1,000 reach 10²¹ (1,000 × 1,000 × … seven times), then a last factor of 602: 10²¹ × 602.2 = 6.022 × 10²³. The step words (a million, a billion, …) are names of powers of ten. Under reduced motion the cascade shows its end state with the ladder complete.',
 [dict(show='s09-c0',stage='s09-sim:one',focus='s09-sim',note='One water molecule, drawn in CPK colors: O red, H white.'),
  dict(show='s09-c1',stage='s09-sim:dozen',note='A dozen molecules in a carton. Twelve is easy to count.'),
  dict(hide=['s09-c0','s09-c1'],show='s09-c2',stage='s09-sim:thousand',note='A thousand: the front face shows 100 cells; the cube is 10 deep. The counter says 1,000 = 10³.'),
  dict(show='s09-pred',note='Prediction: how many zoom-outs by 1,000 to reach 10²³? Collect numbers. Listen for "23".'),
  dict(hide=['s09-c2','s09-pred'],show='s09-c3',stage='s09-sim:zoom',note='Each 1.2 s the whole cube shrinks into one cell of a new face: 10⁶, 10⁹, … 10²¹. Read the words aloud with the class.'),
  dict(show='s09-c4',stage='s09-sim:mole',note='Seven steps reach 10²¹; × 602 more gives 6.022 × 10²³: one mole, the flask of slide 8.'),
  dict(hide='s09-c3',show='s09-c5',stage='s09-sim:spoon',note='One mole of water is only about 18 g, less than a large spoonful.'),
  dict(hide='s09-c4',show='s09-rule',note='Students copy the rule card. Misconception: "one mole always has a mass of 1 gram".'),
  dict(hide=['s09-c5','s09-rule'],show='s09-check',note='Hands up for A, B or C. The spoon of water stays on screen.'),
  dict(show='s09-ans',cls={'s09-a':'right','s09-check':'done'},note='A is right. B (1 g): a mole is a count, not one gram; a mole of water is about 18 g. C (6.022 × 10²³ g): that is the number of molecules, not the mass in grams.')]))
# ---------- 10 name the particle
S.append(slide('s10','t-concept cw','Name the particle','The mole','Reading §5.1.2',f'''    <div class="leftcol"><div class="sim" id="s10-sim" data-sim="moleKinds" aria-label="One mole of aluminum and one mole of copper on a balance; then the four kinds of particles."></div><p class="simcap blk" id="s10-cap" data-zoom="caption">{CAP}</p></div>
    <div class="col acc">
{card('s10-c0','Aluminum','One mole of aluminum atoms: 26.982&nbsp;g.','aluminum')}
{card('s10-c1','Copper','One mole of copper atoms: 63.546&nbsp;g.','copper')}
{card('s10-p1','Predict','Which pan holds more atoms?','predict')}
      <div class="card" id="s10-c2" data-label="same number"><p class="tag">Compare</p>{chips('Mass of one mole',[('Al 26.982&nbsp;g','g'),('Cu 63.546&nbsp;g','g')])}<p>Same number of atoms. Different mass.</p></div>
{card('s10-p2','Predict','"One mole of oxygen." Oxygen atoms, or O<sub>2</sub> molecules?','predict')}
{card('s10-c3','Oxygen','1&nbsp;mol of O<sub>2</sub> molecules holds twice the atoms of 1&nbsp;mol of O atoms.','oxygen')}
{card('s10-c4','Four kinds','Name the particle every time: atoms, molecules, formula units or ions.','four kinds')}
{card('s10-rule','Rule','Always name the particle. It can be atoms, molecules, formula units or ions.','rule','rule reg')}
{check('s10','One mole of aluminum and one mole of copper…',['hold equal numbers of atoms, different masses','have the same mass','hold different numbers; copper atoms are larger'],ans='A. Same count; copper atoms have more mass.',right='A',
  fb=['Same count; copper atoms are heavier, so the copper sample is heavier.','Each element\'s atoms have their own mass, so the moles differ in mass.','A mole always holds 6.022 × 10²³ particles, whatever their size.'])}
    </div>''',
 'Masses of one mole from the blueprint\'s misconception table (CIAAW): aluminum 26.982 g, copper 63.546 g. Atom sizes from covalent radii (Cordero 2008); ion sizes from Shannon 1976. The caption under the picture says that atom colors (CPK) show the element; ions keep Unit 4\'s red "+" and blue "−".',
 [dict(show=['s10-c0','s10-cap'],stage='s10-sim:al',focus='s10-sim',note='One mole of aluminum atoms on the left pan: 26.982 g. The beam tips toward the loaded pan.'),
  dict(show='s10-c1',stage='s10-sim:cu',note='One mole of copper atoms: 63.546 g. The beam tips toward copper.'),
  dict(hide=['s10-c0','s10-c1'],show='s10-p1',note='Prediction: which pan holds more atoms? Hands up for aluminum, copper, the same.'),
  dict(hide='s10-p1',show='s10-c2',stage='s10-sim:compare',note='Both hold 6.022 × 10²³ atoms. A copper atom has more mass. Misconception: "a mole is a mass".'),
  dict(show='s10-p2',note='Prediction: "one mole of oxygen" could mean either. Which?'),
  dict(hide=['s10-c2','s10-p2'],show='s10-c3',stage='s10-sim:oxygen',note='1 mol of O₂ molecules holds 2 mol of O atoms: twice the atoms of 1 mol of O atoms.'),
  dict(show='s10-c4',stage='s10-sim:four',note='Atoms (a Cu atom), molecules (H₂O), formula units (one Na⁺ with one Cl⁻), ions. Read the caption: atom colors show the element, not the charge.'),
  dict(hide='s10-c3',show='s10-rule',note='Students copy the rule card (reading §5.1.2: a mole must always name its particles).'),
  dict(hide=['s10-c4','s10-rule','s10-cap'],show='s10-check',stage='s10-sim:compare',note='Hands up for A, B or C. The balance returns: one mole of Al, one mole of Cu.'),
  dict(show='s10-ans',cls={'s10-a':'right','s10-check':'done'},note='A is right. B (the same mass): each element\'s atoms have their own mass, so the moles differ in mass. C (different numbers; copper atoms are larger): a mole always holds 6.022 × 10²³ particles, whatever their size.')]))
# ---------- 11 the size of a mole (wide; the check in the band)
S.append(slide('s11','t-concept wide','The size of a mole','The mole','Reading §5.1.2',f'''    <div class="sim" id="s11-sim" data-sim="secondsLine" data-band="236" aria-label="A time line in powers of ten: one year, Earth, the universe, and the time to count one mole."></div>
    <div class="ptrow tall blk" id="s11-row" data-label="time line"><div class="stack">
      <p class="caprow" id="s11-p0">Count one particle each second. Never stop.</p>
      <p class="caprow" id="s11-p1" data-label="one year">One year is about 3.156&nbsp;×&nbsp;10<sup>7</sup> seconds.</p>
      <p class="caprow" id="s11-p2" data-label="Earth">Earth is about 4.5 billion years old.</p>
      <p class="caprow" id="s11-p3" data-label="the universe">The universe is about 13.8 billion years old.</p>
      <p class="caprow" id="s11-p4" data-label="predict">Predict: where does {NA} seconds land?</p>
      <p class="caprow" id="s11-p5" data-label="the mole">{NA} s is about 1.9&nbsp;×&nbsp;10<sup>16</sup> years.</p>
      <p class="caprow" id="s11-p6" data-label="how many times">About 1.4 million times the age of the universe.</p>
      <p class="caprow" id="s11-p7" data-label="a spoonful">Yet one mole of water is about 18&nbsp;g. Less than a large spoonful.</p>
      <div class="rulerow reg" id="s11-rule" data-label="rule"><p>At one particle each second, a mole takes about 1.9&nbsp;×&nbsp;10<sup>16</sup> years.</p><p>That is 1.4 million times the age of the universe.</p><p>Yet a mole of water is only about 18&nbsp;g.</p></div>
      <div class="checkrow" id="s11-check" data-label="check">
        <p class="q" id="s11-q"><span class="tag">Check:</span> Earth is 4.5 billion years old. About how many Earth ages?</p>
        <ol class="opts" data-lay="row">{optli('s11',['4 million times','4,000 times','1.4 million times'],'A',['10¹⁶ ÷ 10⁹ = 10⁷, and 1.9 ÷ 4.5 ≈ 0.4: about 4 × 10⁶.','Divide the powers of ten carefully: 10¹⁶ ÷ 10⁹ = 10⁷.','1.4 million is for the universe. Earth is younger, so more times.'])}</ol>
        <div class="af"><p class="ans" id="s11-ans" data-label="answer">A. 1.9&nbsp;×&nbsp;10<sup>16</sup> ÷ 4.5&nbsp;×&nbsp;10<sup>9</sup> is about 4&nbsp;×&nbsp;10<sup>6</sup>.</p><p class="fb" aria-live="polite"></p></div>
      </div>
    </div></div>''',
 'The reading\'s worked example: 6.022 × 10²³ s × 1 year / 3.156 × 10⁷ s = 1.908 × 10¹⁶ years; 1.908 × 10¹⁶ ÷ 1.38 × 10¹⁰ = 1.38 × 10⁶, about 1.4 million. Each mark on the line is 10 times the one before. "Avogadro\'s number is so large because atoms are so small."',
 [dict(show=['s11-row','s11-p0'],stage='s11-sim:line',focus='s11-sim',note='The counter ticks one particle each second beside the clock. Ask: how long to count a mole this way?'),
  dict(hide='s11-p0',show='s11-p1',stage='s11-sim:year',note='One year is about 3.156 × 10⁷ seconds. Each mark of the line is ten times the one before.'),
  dict(hide='s11-p1',show='s11-p2',stage='s11-sim:earth',note='Earth: about 4.5 billion years (USGS 4.54 billion).'),
  dict(hide='s11-p2',show='s11-p3',stage='s11-sim:universe',note='The universe: about 13.8 billion years (NASA JPL).'),
  dict(hide='s11-p3',show='s11-p4',note='Prediction: point at the line. Where does 6.022 × 10²³ seconds land?'),
  dict(hide='s11-p4',show='s11-p5',stage='s11-sim:mole',note='Far to the right: 6.022 × 10²³ s is about 1.9 × 10¹⁶ years.'),
  dict(hide='s11-p5',show='s11-p6',stage='s11-sim:times',note='1.9 × 10¹⁶ ÷ 1.38 × 10¹⁰ is about 1.4 million times the age of the universe.'),
  dict(hide='s11-p6',show='s11-p7',stage='s11-sim:spoon',note='Yet one mole of water is about 18 g: less than a large spoonful.'),
  dict(hide='s11-p7',show='s11-rule',note='Students copy the three lines of the rule (reading §5.1.2 Key idea).'),
  dict(hide='s11-rule',show='s11-check',stage='s11-sim:times',note='Hands up for A, B or C. The line shows the universe bracket and, faint, the Earth bracket.'),
  dict(show='s11-ans',cls={'s11-a':'right','s11-check':'done'},note='A is right: 1.9 × 10¹⁶ ÷ 4.5 × 10⁹ is about 4 × 10⁶. B (4,000 times): divide the powers of ten carefully, 10¹⁶ ÷ 10⁹ = 10⁷. C (1.4 million times): that is for the universe; Earth is younger, so more times.')]))
# ---------- 12 who found the number (wide, no check)
S.append(slide('s12','t-concept wide','Who found the number','The mole','Reading §5.1.2',f'''    <div class="sim" id="s12-sim" data-sim="moleHistory" data-band="214" aria-label="A time ruler from 1800 to 2020 with the people and dates behind the mole."></div>
    <div class="ptrow blk" id="s12-row" data-label="history"><div class="stack">
      <p class="caprow" id="s12-p0">1811: Avogadro's idea. At one temperature and pressure, equal gas volumes hold equal numbers of particles. He never knew the number.</p>
      <p class="caprow" id="s12-p1" data-label="1865">1865: Loschmidt made the first estimate of the size of molecules.</p>
      <p class="caprow" id="s12-p2" data-label="1890s">1890s: Ostwald made the word Mol a unit.</p>
      <p class="caprow" id="s12-p3" data-label="1909">1909: Jean Perrin measured it several ways and named it after Avogadro. Nobel Prize, 1926.</p>
      <p class="caprow" id="s12-p4" data-label="1971">1971: the mole became an SI base unit. Old definition: the atoms in exactly 12&nbsp;g of carbon-12.</p>
      <p class="caprow" id="s12-p5" data-label="predict">Predict: today, is the number measured, or fixed by definition?</p>
      <p class="caprow" id="s12-p6" data-label="2018 and 2019">Voted November 16, 2018. Exact since May 20, 2019. No longer measured.</p>
      <div class="card rule reg" id="s12-rule" data-label="rule"><p class="tag">Rule</p><p>Since May 20, 2019 the number is exact: {NAX}. It is no longer measured.</p></div>
    </div></div>''',
 'The reading\'s section "How the number was found". The 1971 definition (the atoms in exactly 12 g of carbon-12) is "a definition that older books still print". The silicon spheres of the Avogadro project come next, on slide 13.',
 [dict(show=['s12-row','s12-p0'],stage='s12-sim:avogadro',focus='s12-sim',note='1811, Amedeo Avogadro: equal volumes of gases at the same temperature and pressure hold equal numbers of particles. The condition matters: both gases at one temperature and one pressure. He never knew how large that number was. Misconception: "Avogadro measured the number".'),
  dict(hide='s12-p0',show='s12-p1',stage='s12-sim:loschmidt',note='1865, Josef Loschmidt: the first estimate of the size of molecules, and so of the number.'),
  dict(hide='s12-p1',show='s12-p2',stage='s12-sim:ostwald',note='1890s, Wilhelm Ostwald: the word Mol as a unit.'),
  dict(hide='s12-p2',show='s12-p3',stage='s12-sim:perrin',note='Around 1909, Jean Perrin measured the number by several independent methods and proposed naming it after Avogadro; Nobel Prize in Physics, 1926.'),
  dict(hide='s12-p3',show='s12-p4',stage='s12-sim:si',note='1971: the mole became an SI base unit, defined by 12 g of carbon-12.'),
  dict(hide='s12-p4',show='s12-p5',note='Prediction: is the number still measured today? Hands up for "measured" and for "fixed".'),
  dict(hide='s12-p5',show='s12-p6',stage='s12-sim:exact',note='The vote of November 16, 2018; in force May 20, 2019. The number is now exact and is no longer measured.'),
  dict(hide='s12-p6',show='s12-rule',note='Students copy the rule card. No check on this slide.')]))
# ---------- 13 the silicon sphere
S.append(slide('s13','t-concept cw','Counting the atoms in a silicon sphere','The mole','Reading §5.1.2',f'''    <div class="sim" id="s13-sim" data-sim="siliconSphere" aria-label="A silicon sphere; its crystal of identical cubes, turning; one cube with its edge measured."></div>
    <div class="col acc">
{card('s13-c0','The sphere','The Avogadro project: a nearly perfect sphere of silicon.','the sphere')}
{card('s13-pred','Predict','How could anyone count the atoms in this ball?','predict')}
{card('s13-c1','One crystal','The sphere is one crystal. Its atoms repeat in identical cubes.','one crystal')}
{card('s13-cube','One cube','X-rays measure one cube\'s edge: 543.102&nbsp;pm. Corner and face atoms are shared: 8 atoms per cube.','one cube')}
{card('s13-c2','One atom','The density gives the mass of one cube, so of one atom.','one atom')}
{card('s13-c3','The count','Mass of one mole of silicon ÷ mass of one atom = '+NA+'.','the count')}
{card('s13-rule','Rule','The atoms of a crystal repeat in identical cubes. Count one cube and measure its size. Then the whole sphere is counted.','rule','rule reg')}
{check('s13','In the Avogadro project, a silicon sphere was used to…',['count atoms: mass, density, atom spacing','define the kilogram by its size','compare silicon and carbon atoms'],ans='A. Those measurements gave the value fixed in 2019.',right='A',
  fb=['Volume, density and atom spacing give the count.','The spheres counted atoms. Since 2019 the kilogram is defined by the Planck constant.','The project counted atoms. It did not compare their sizes.'])}
    </div>''',
 '<b>Honors (notes only, never assessed).</b> The real spheres were enriched to more than 99.99% silicon-28: natural silicon is a mix of silicon-28, -29 and -30, and every uncertainty in those abundances becomes an uncertainty in the count; the other isotopes were measured with a mass spectrometer. <b>The model\'s arithmetic</b> with natural silicon: one cube has an edge of 543.102 pm, so a volume of (5.43102 × 10⁻⁸ cm)³ = 1.6019 × 10⁻²² cm³; × 2.329 g/cm³ = 3.7308 × 10⁻²² g per cube; ÷ 8 atoms = 4.6635 × 10⁻²³ g per atom; 28.085 g ÷ 4.6635 × 10⁻²³ g = 6.022 × 10²³ atoms per mole. The real spheres used their own measured values. "Molar mass" is Lesson 5.2\'s word; here say "the mass of one mole of silicon".',
 [dict(show='s13-c0',stage='s13-sim:sphere',focus='s13-sim',note='The international Avogadro project polished nearly perfect spheres of silicon. Ask: what could you measure about this ball?'),
  dict(show='s13-pred',stage='s13-sim:sphere',note='Prediction: how could anyone count its atoms? Collect ideas. Misconception: "they weighed one atom".'),
  dict(hide=['s13-c0','s13-pred'],show='s13-c1',stage='s13-sim:crystal',note='The sphere is a single crystal: the atoms repeat in identical cubes. The model turns slowly.'),
  dict(show='s13-cube',stage='s13-sim:cube',note='X-rays measure the edge of one cube: 543.102 pm. The picture rings the 18 atoms that touch the cube; corner and face atoms are shared with the next cubes. Each cube holds the equivalent of 8 atoms: 8 corners × 1/8 + 6 faces × 1/2 + 4 inside = 8.'),
  dict(hide='s13-c1',show='s13-c2',stage='s13-sim:atom',note='The density gives the mass of one cube; divide by 8 for the mass of one atom.'),
  dict(show='s13-c3',stage='s13-sim:divide',note='The mass of one mole of silicon ÷ the mass of one atom = the number of atoms in one mole: 6.022 × 10²³.'),
  dict(hide=['s13-cube','s13-c2'],show='s13-rule',note='Students copy the rule card. The project counted atoms; it did not weigh one atom directly.'),
  dict(hide=['s13-c3','s13-rule'],show='s13-check',stage='s13-sim:cube',note='Hands up for A, B or C. The lit cube with its edge returns to the screen.'),
  dict(show='s13-ans',cls={'s13-a':'right','s13-check':'done'},note='A is right. B (define the kilogram by its size): the spheres counted atoms; since 2019 the kilogram is defined by the Planck constant. C (compare silicon and carbon atoms): the project counted atoms; it did not compare their sizes.')]))
# ---------- 14 one picture
def colh(n, ic, name, label):
    return f'      <div class="colh slot"><div class="colin" data-b="s14-c{n}" data-label="{name}">{use(ic,label)}<p>{name}</p></div></div>'
rows = [('The problem',['same mass, too many','two masses','too small, too many'],'s14-r1','the problem'),
        ('The trick',['divide by 5.000&nbsp;g','divide by the average','count in moles of '+NA],'s14-r2','the trick'),
        ('Name it',['nickels','cents','atoms, molecules, formula units or ions'],'s14-r3','name it')]
rh = ''
for name, cells, b, lab in rows:
    rh += f'      <p class="rh">{name}</p>\n' + ''.join(f'      <p class="cell slot lbl"><span data-b="{b}"{" data-label=%s" % js(lab) if i==0 else ""}>{c}</span></p>\n' for i, c in enumerate(cells))
S.append(slide('s14','t-summary s3','One picture: three ways to count','Summary','Reading §5.1.1 and §5.1.2',f'''    <div class="g3">
      <span></span>
{colh(1,'ic-nickel','nickels','Icon: a nickel')}
{colh(2,'ic-cents','cents','Icon: two kinds of cents')}
{colh(3,'ic-flask','atoms','Icon: a flask of particles')}
{rh}    </div>
    <div class="acc s3b">
      <p class="line" id="s14-thread" data-label="the thread">Too many to count? Weigh them. Then think in moles.</p>
      <div class="qrow" id="s14-w" data-label="write 90 s"><div><ol class="frames"><li>A bank counts nickels by weighing because <span class="gap"></span>.</li><li>Chemists count particles in moles, where one mole is <span class="gap"></span>.</li></ol><p class="bank"><b>Word bank:</b> <span>the same mass</span> <span>divide</span> <span>6.022&nbsp;×&nbsp;10<sup>23</sup></span> <span>particles</span> <span>named</span></p></div><div class="timer"></div></div>
    </div>''',
 'One picture closes period 1. Students copy the three columns as one diagram. Period 1 ends here: collect three notebooks as a quick check before period 2.',
 [dict(note='The empty table. Ask: what were the three things we counted today?'),
  dict(show='s14-c1',note='Nickels: every nickel has the same mass.'),
  dict(show='s14-c2',note='Cents: two kinds, two masses.'),
  dict(show='s14-c3',note='Atoms: far too small and far too many.'),
  dict(show='s14-r1',note='The problem in each column.'),
  dict(show='s14-r2',note='The trick: divide by one mass, by the average mass, or count in moles of 6.022 × 10²³.'),
  dict(show='s14-r3',note='Name it: a mole always names its particles.'),
  dict(show='s14-thread',note='The thread line, said together: too many to count? Weigh them. Then think in moles.'),
  dict(hide='s14-thread',show='s14-w',timer=90,note='Ninety seconds of writing with the frames and the word bank. End of period 1.')]))
# ---------- 15 warm-up
S.append(slide('s15','t-turn two','Warm-up','Warm-up, period 2','Reading §5.1.1 and §5.1.2','''    <div class="qrow">
      <div class="card"><p>Answer in your notebook.</p></div>
      <div class="timer"></div>
    </div>
    <table class="tbl fill" id="s15-tbl">
      <thead><tr><th>Question</th><th>Answer</th></tr></thead>
      <tbody>
        <tr><td>A bag of nickels has a mass of 1,000.0&nbsp;g.<br>How many nickels?</td><td class="slot"><span data-b="s15-a1" data-label="answer 1">200<br>(1,000.0&nbsp;g ÷ 5.000&nbsp;g)</span></td></tr>
        <tr><td>How many particles are in one mole?</td><td class="slot"><span data-b="s15-a2" data-label="answer 2">6.022&nbsp;×&nbsp;10<sup>23</sup><br>(exactly 6.02214076&nbsp;×&nbsp;10<sup>23</sup>)</span></td></tr>
        <tr><td>Name the four kinds of particles<br>a mole can count.</td><td class="slot"><span data-b="s15-a3" data-label="answer 3">atoms, molecules,<br>formula units, ions</span></td></tr>
      </tbody>
    </table>''',
 'Period 2 starts here. The three questions retrieve 5.1.1 and 5.1.2. 1,000.0 g ÷ 5.000 g = 200 is arithmetic on the reading\'s data.',
 [dict(note='Students read the questions while you take attendance.'),
  dict(timer=90,label='timer 90 s',note='Ninety seconds. Students answer in the notebook.'),
  dict(show='s15-a1',note='1,000.0 g ÷ 5.000 g = 200 nickels. Misconception: "multiply".'),
  dict(show='s15-a2',note='6.022 × 10²³, exactly 6.02214076 × 10²³ since 2019.'),
  dict(show='s15-a3',note='Atoms, molecules, formula units, ions. A mole always names its particle.')]))
# ---------- 16 moles to particles
S.append(slide('s16','t-concept cw','Moles to particles','Moles and particles','Reading §5.1.3',f'''    <div class="sim" id="s16-sim" data-sim="moleMap" aria-label="A map with moles on the left, particles on the right and a bridge of 6.022 times ten to the 23 per mole."></div>
    <div class="col acc">
{card('s16-c0','The map','Moles on the left. Particles on the right. The bridge is '+NA+' per mole.','the map')}
{card('s16-pred','Predict','2.00&nbsp;mol of copper. More or fewer than '+NA+' atoms?','predict')}
{card('s16-c1','Setup','2.00&nbsp;mol × '+NA+' atoms per mol.','setup')}
{card('s16-c2','Cancel','The unit mol cancels. Atoms remain.','cancel')}
{card('s16-c3','Result','1.20&nbsp;×&nbsp;10<sup>24</sup> Cu atoms. More than one mole, so more than '+NA+'.','result')}
{card('s16-rule','Rule','Particles = moles × '+NA+'. The unit mol cancels. Always name the particle.','rule','rule reg')}
{check('s16','To change moles into a number of particles, you…',['multiply by '+NA+' particles per mole','divide by '+NA+' particles per mole','multiply by the mass of one particle'],ans='A. The unit mol cancels, and particles remain.',right='A',
  fb=['mol × (particles / mol) = particles.','Dividing gives a tiny number, smaller than one particle. Check the units.','That would give a mass. To count particles, use the Avogadro constant.'])}
    </div>''',
 'Reading §5.1.3: the Avogadro constant is a conversion factor; multiply by 6.022 × 10²³ particles/mol so that mol cancels. Copper and other metals are counted as atoms.',
 [dict(show='s16-c0',stage='s16-sim:map',focus='s16-sim',note='The map: moles (teal) on the left, particles (violet) on the right, the gray bridge 6.022 × 10²³ per mole.'),
  dict(hide='s16-c0',show='s16-pred',stage='s16-sim:map',note='Prediction: 2.00 mol of copper atoms. More or fewer than 6.022 × 10²³? Listen for "fewer" (dividing).'),
  dict(hide='s16-pred',show='s16-c1',stage='s16-sim:Cu/setup',note='Write the factor with its units: 6.022 × 10²³ atoms over 1 mol.'),
  dict(show='s16-c2',stage='s16-sim:Cu/cancel',note='mol cancels (struck in red); atoms remain (circled).'),
  dict(show='s16-c3',stage='s16-sim:Cu/result',note='1.20 × 10²⁴ Cu atoms. Check: more than one mole, so more than 6.022 × 10²³.'),
  dict(hide=['s16-c1','s16-c2'],show='s16-rule',note='Students copy the rule card. Misconception: "divide to get particles".'),
  dict(hide=['s16-c3','s16-rule'],show='s16-check',note='Hands up for A, B or C. The copper example stays on the map.'),
  dict(show='s16-ans',cls={'s16-a':'right','s16-check':'done'},note='A is right. B (divide): dividing gives a tiny number, smaller than one particle; check the units. C (the mass of one particle): that would give a mass; to count particles, use the Avogadro constant.')]))
# ---------- 17 particles to moles
S.append(slide('s17','t-concept cw','Particles to moles','Moles and particles','Reading §5.1.3',f'''    <div class="sim" id="s17-sim" data-sim="moleMap" aria-label="The map again: from a number of iron atoms back to moles."></div>
    <div class="col acc">
{card('s17-c0','Iron','9.03&nbsp;×&nbsp;10<sup>23</sup> iron atoms. How many moles?','iron atoms')}
      <div class="card" id="s17-pred" data-label="predict"><p class="tag">Predict</p><p>Multiply, or divide?</p>{chips('Across the bridge',[('× '+NA+' per mol','n'),('÷ '+NA+' per mol','mol')])}</div>
{card('s17-c1','Cancel','× 1&nbsp;mol per '+NA+' atoms. The atoms cancel.','cancel')}
{card('s17-c2','Result','1.50&nbsp;mol of Fe atoms. 9.03 is 1.5 times 6.022.','result')}
{card('s17-c3','Half a mole','3.011&nbsp;×&nbsp;10<sup>23</sup> molecules is 0.5000&nbsp;mol. Moles can be fractions.','half a mole')}
{card('s17-c4','Small and huge','A sample you can see is a small number of moles. But an enormous number of particles.','small and huge')}
{card('s17-rule','Rule','Moles = particles ÷ '+NA+'. A visible sample is a small number of moles.','rule','rule reg')}
{check('s17','How many moles of carbon dioxide molecules are 3.011&nbsp;×&nbsp;10<sup>23</sup> molecules?',['0.5000&nbsp;mol','2.000&nbsp;mol','1.813&nbsp;×&nbsp;10<sup>47</sup>&nbsp;mol'],col=False,ans='A. 3.011&nbsp;×&nbsp;10<sup>23</sup> ÷ '+NA+' = 0.5000&nbsp;mol.',right='A',
  fb=['Half of 6.022 × 10²³ is half a mole.','That divides 6.022 × 10²³ by 3.011 × 10²³, the wrong way around.','That multiplies by Avogadro\'s number. Particles to moles means dividing.'])}
    </div>''',
 'Reading §5.1.3: particles to moles divides, "the same as multiplying by 1 mol / 6.022 × 10²³ particles". Scientific notation: a number from 1 to less than 10 times a power of ten; Lesson 5.3 shows the calculator. 9.03 × 10²³ and 6.022 × 10²³ have equal powers of ten, so compare 9.03 with 6.022.',
 [dict(show='s17-c0',stage='s17-sim:Fe/setup',focus='s17-sim',note='9.03 × 10²³ iron atoms on the particle side. The arrow points to moles.'),
  dict(show='s17-pred',stage='s17-sim:Fe/setup',note='Prediction: multiply or divide? Hands up. Listen for "multiply" (more moles?).'),
  dict(hide=['s17-c0','s17-pred'],show='s17-c1',stage='s17-sim:Fe/cancel',note='The factor flips: 1 mol over 6.022 × 10²³ atoms; atoms cancel, mol remains.'),
  dict(show='s17-c2',stage='s17-sim:Fe/result',note='1.50 mol of Fe atoms. Check: 9.03 is 1.5 times 6.022; equal powers of ten.'),
  dict(hide='s17-c1',show='s17-c3',stage='s17-sim:half',note='3.011 × 10²³ molecules is half of 6.022 × 10²³: 0.5000 mol. Misconception: "a count below 6.022 × 10²³ cannot be moles".'),
  dict(hide='s17-c2',show='s17-c4',note='A sample you can hold is a few moles at most, but an enormous number of particles.'),
  dict(hide='s17-c3',show='s17-rule',note='Students copy the rule card (reading §5.1.3 Key idea).'),
  dict(hide='s17-c4',show='s17-check',stage='s17-sim:half',note='Hands up for A, B or C. The half mole stays on the map.'),
  dict(show='s17-ans',cls={'s17-a':'right','s17-check':'done'},note='A is right: 3.011 × 10²³ ÷ 6.022 × 10²³ = 0.5000 mol. B (2.000 mol): that divides 6.022 × 10²³ by 3.011 × 10²³, the wrong way around. C (1.813 × 10⁴⁷ mol): that multiplies by Avogadro\'s number; particles to moles means dividing.')]))
# ---------- 18 formula units
S.append(slide('s18','t-concept cw','Formula units','Moles and particles','Reading §5.1.3',f'''    <div class="sim" id="s18-sim" data-sim="naclCrystal" aria-label="A crystal of sodium ions and chloride ions turning slowly; one sodium ion and one chloride ion lit."></div>
    <div class="col acc">
{card('s18-c0','Sodium chloride','Sodium chloride is a crystal of ions. It has no molecules.','a crystal of ions')}
{card('s18-c1','One formula unit','One formula unit: one Na<sup>+</sup> and one Cl<sup>−</sup>.','one formula unit')}
{card('s18-pred','Predict','4.50&nbsp;mol of NaCl makes 2.71&nbsp;×&nbsp;10<sup>24</sup> of what?','predict')}
{card('s18-c2','Count','4.50&nbsp;mol × '+NA+' = 2.71&nbsp;×&nbsp;10<sup>24</sup> formula units.','count')}
{card('s18-c3','Wrong particle','"1.51&nbsp;×&nbsp;10<sup>24</sup> molecules of NaCl": right number, wrong particle.','wrong particle')}
{card('s18-rule','Rule','Count a metal in atoms. Count a molecular compound in molecules. Count an ionic compound in formula units.','rule','rule reg')}
{check('s18','Which particles are counted in 1&nbsp;mol of NaCl?',['formula units: one Na<sup>+</sup> and one Cl<sup>−</sup> each','NaCl molecules','sodium atoms and chlorine atoms'],ans='A. NaCl has no molecules. Its formula gives the ratio of ions.',right='A',
  fb=['Count formula units, or count the ions.','Sodium chloride is a crystal of ions with no separate molecules.','In the crystal, sodium and chlorine are ions, not neutral atoms.'])}
    </div>''',
 'Unit 4\'s formula unit: the group of ions given by the formula of an ionic compound; it states a ratio and is not a molecule. The blueprint\'s misconception: "2.50 mol of sodium chloride contains 1.51 × 10²⁴ molecules" has the right number (2.50 × 6.022 × 10²³ = 1.51 × 10²⁴) and the wrong particle. Ion sizes from Shannon 1976 (Na⁺ 102 pm, Cl⁻ 181 pm) on the 564 pm cell.',
 [dict(show='s18-c0',stage='s18-sim:crystal',focus='s18-sim',note='The NaCl crystal of Unit 4: red + ions and blue − ions, turning slowly. No molecules anywhere.'),
  dict(show='s18-c1',stage='s18-sim:unit',note='One Na⁺ and one neighboring Cl⁻ lit: one formula unit.'),
  dict(hide='s18-c0',show='s18-pred',stage='s18-sim:unit',note='Prediction: 2.71 × 10²⁴ of what? Listen for "molecules".'),
  dict(hide=['s18-c1','s18-pred'],show='s18-c2',stage='s18-sim:count',note='4.50 mol × 6.022 × 10²³ = 2.71 × 10²⁴ formula units (the reading\'s "On your own").'),
  dict(show='s18-c3',stage='s18-sim:wrong',note='"1.51 × 10²⁴ molecules of NaCl": the number is right, the particle is wrong.'),
  dict(hide='s18-c2',show='s18-rule',note='Students copy the rule card: metals in atoms, molecular compounds in molecules, ionic compounds in formula units.'),
  dict(hide=['s18-c3','s18-rule'],show='s18-check',stage='s18-sim:unit',note='Hands up for A, B or C. One formula unit is lit again.'),
  dict(show='s18-ans',cls={'s18-a':'right','s18-check':'done'},note='A is right. B (NaCl molecules): sodium chloride is a crystal of ions with no separate molecules. C (sodium atoms and chlorine atoms): in the crystal, sodium and chlorine are ions, not neutral atoms.')]))
# ---------- 19 atoms in a molecule
S.append(slide('s19','t-concept cw','Atoms in a molecule','Atoms in a formula','Reading §5.1.4',f'''    <div class="leftcol"><div class="sim" id="s19-sim" data-sim="atomCounter" aria-label="A water molecule and its formula with the subscript ringed; a table counts the moles of each atom."></div><p class="simcap blk" id="s19-cap" data-zoom="caption">{CAP}</p></div>
    <div class="col acc">
{card('s19-c0','Water','One water molecule: two H atoms, one O atom. The subscript says so.','water')}
{card('s19-pred','Predict','One mole of water molecules. How many moles of hydrogen atoms?','predict')}
{card('s19-c1','One mole of water','1&nbsp;mol of H<sub>2</sub>O holds 2&nbsp;mol of H atoms and 1&nbsp;mol of O atoms.','a mole of water')}
{card('s19-c2','Carbon dioxide','2.00&nbsp;mol of CO<sub>2</sub> × 2 = 4.00&nbsp;mol of O atoms.','carbon dioxide')}
{card('s19-c3','Count the atoms','4.00&nbsp;mol × '+NA+' = 2.41&nbsp;×&nbsp;10<sup>24</sup> O atoms.','count the atoms')}
{card('s19-c4','Sodium chloride','1&nbsp;mol of NaCl holds 1&nbsp;mol of Na<sup>+</sup> ions and 1&nbsp;mol of Cl<sup>−</sup> ions.','sodium chloride')}
{card('s19-rule','Rule','Moles of an element\'s atoms = moles of molecules × its subscript. Then multiply by '+NA+' to count the atoms.','rule','rule reg')}
{check('s19','How many moles of oxygen atoms are in 2.0&nbsp;mol of carbon dioxide, CO<sub>2</sub>?',['4.0&nbsp;mol','2.0&nbsp;mol','1.0&nbsp;mol'],ans='A. Each CO<sub>2</sub> molecule has two oxygen atoms: 2.0&nbsp;mol × 2.',right='A',
  fb=['Two O atoms in every molecule, so twice the moles.','That counts CO₂ molecules. Each molecule holds two oxygen atoms.','That divides by the subscript. The subscript multiplies.'])}
    </div>''',
 'Reading §5.1.4: in H₂O the subscript 2 means two hydrogen atoms; no subscript after O means one. Molecules in ball and stick: CPK colors, the symbol on every sphere, covalent radii (Cordero 2008), NIST geometries (H₂O 104.5°, CO₂ 180°). The NaCl pair uses Shannon radii; the caption under the picture says that atom colors show the element. Also: 0.50 mol of methane, CH₄, holds 2.0 mol of H atoms.',
 [dict(show=['s19-c0','s19-cap'],stage='s19-sim:H2O/one',focus='s19-sim',note='One H₂O: the subscript 2 is ringed; no subscript after O means one.'),
  dict(show='s19-pred',stage='s19-sim:H2O/one',note='Prediction: one mole of water molecules, how many moles of H atoms? Collect answers. Misconception: "one mole of water holds one mole of hydrogen atoms".'),
  dict(hide=['s19-c0','s19-pred'],show='s19-c1',stage='s19-sim:H2O/mol',note='The subscript multiplies the moles: 1 mol × 2 = 2 mol of H atoms; 1 mol × 1 = 1 mol of O atoms.'),
  dict(show='s19-c2',stage='s19-sim:CO2/mol',note='CO₂: 2.00 mol × 2 = 4.00 mol of O atoms (the reading\'s Watch example).'),
  dict(show='s19-c3',stage='s19-sim:CO2/atoms',note='Then count: 4.00 mol × 6.022 × 10²³ = 2.41 × 10²⁴ O atoms, twice the 1.20 × 10²⁴ CO₂ molecules.'),
  dict(hide=['s19-c1','s19-c2'],show='s19-c4',stage='s19-sim:NaCl/mol',note='NaCl: 1 mol holds 1 mol of Na⁺ ions and 1 mol of Cl⁻ ions. Read the caption.'),
  dict(hide='s19-c3',show='s19-rule',note='Students copy the rule card (reading §5.1.4 Key idea).'),
  dict(hide='s19-c4',show='s19-check',stage='s19-sim:CO2/mol',note='Hands up for A, B or C. The CO₂ molecule and its table return.'),
  dict(show='s19-ans',cls={'s19-a':'right','s19-check':'done'},note='A is right: two O atoms in every molecule, 2.0 mol × 2. B (2.0 mol): that counts CO₂ molecules; each holds two oxygen atoms. C (1.0 mol): that divides by the subscript; the subscript multiplies.')]))
# ---------- 20 I do, we do, you do
S.append(slide('s20','t-example','Convert: I do, we do, you do','Converting','Reading §5.1.3 and §5.1.4',f'''    <div class="stack">
      <div class="sim" id="s20-sim" data-sim="moleMap" aria-label="The moles and particles map for carbon dioxide and water."></div>
      <div class="sim blk" id="s20-ac" data-sim="atomCounter" aria-label="An ammonia molecule with its subscript 3 ringed."></div>
    </div>
    <div class="acc">
      <div class="card stepscard" id="s20-steps" data-label="steps"><p class="tag">Steps</p><ol class="steps">
        <li><span class="k">Given</span><span>the number and its unit</span></li>
        <li><span class="k">Factor</span><span>{NA} per mole</span></li>
        <li><span class="k">Setup</span><span>the unit to cancel goes below</span></li>
        <li><span class="k">Result</span><span>name the particle</span></li>
        <li><span class="k">Check</span><span>more than one mole, more particles</span></li></ol></div>
{card('s20-i','I do: 0.250 mol of CO<sub>2</sub>','1.51&nbsp;×&nbsp;10<sup>23</sup> molecules. A quarter of a mole is a quarter of '+NA+'.','I do')}
{card('s20-w','We do: 1.81 × 10<sup>24</sup> water molecules','3.01&nbsp;mol. 18.1&nbsp;×&nbsp;10<sup>23</sup> is about three times '+NA+'.','we do')}
      <div class="qrow" id="s20-yq" data-label="you do"><div class="card"><p class="tag">You do</p><p>Convert each one. Name the particle.</p></div><div class="timer"></div></div>
      <table class="tbl compact yd" id="s20-yd" data-label="you do table"><tbody>
        <tr><td>0.500&nbsp;mol of NH<sub>3</sub><br>→ moles of H atoms</td><td class="slot"><span data-b="s20-a1" data-label="answer 1">1.50&nbsp;mol of H atoms</span></td></tr>
        <tr><td>1.00&nbsp;mol of glucose,<br>C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> → H atoms</td><td class="slot"><span data-b="s20-a2" data-label="answer 2">12.0&nbsp;mol × {NA}<br>= 7.23&nbsp;×&nbsp;10<sup>24</sup> H atoms</span></td></tr>
        <tr><td>2.5&nbsp;×&nbsp;10<sup>22</sup> CO<sub>2</sub><br>molecules → moles</td><td class="slot"><span data-b="s20-a3" data-label="answer 3">0.042&nbsp;mol <span class="why">fewer than {NA},<br>so less than one mole</span></span></td></tr>
      </tbody></table>
    </div>''',
 'You do: circulate during the timer. Look for "multiply" where dividing is needed (particles to moles), and for results without a named particle. Glucose: 1.00 mol × 12 = 12.0 mol of H atoms, then × 6.022 × 10²³ = 7.23 × 10²⁴ H atoms (the reading\'s "On your own").',
 [dict(show='s20-steps',stage='s20-sim:map',focus='s20-steps',note='The steps of every conversion (the reading\'s form): Given, Factor, Setup, Result, Check.'),
  dict(show='s20-i',stage='s20-sim:CO2m/setup',focus='s20-sim',note='I do: 0.250 mol of CO₂ to molecules. Think aloud: the given is in moles, so the factor puts mol below.'),
  dict(stage='s20-sim:CO2m/cancel',label='cancel',note='mol cancels; molecules remain.'),
  dict(stage='s20-sim:CO2m/result',label='result',note='1.51 × 10²³ molecules. A quarter of a mole is a quarter of 6.022 × 10²³.'),
  dict(show='s20-w',stage='s20-sim:H2Om/setup',note='We do: 1.81 × 10²⁴ water molecules to moles. Students say the factor before the press: 1 mol over 6.022 × 10²³ molecules.'),
  dict(stage='s20-sim:H2Om/cancel',label='cancel',note='Students say which unit cancels: molecules.'),
  dict(stage='s20-sim:H2Om/result',label='result',note='3.01 mol. Check: 18.1 × 10²³ is about three times 6.022 × 10²³.'),
  dict(hide=['s20-steps','s20-i','s20-w'],show=['s20-yq','s20-yd'],note='You do: three conversions in the notebook. Read the three rows aloud.'),
  dict(timer=180,label='timer 3 min',note='Three minutes of silent work. Circulate.'),
  dict(hide='s20-sim',show=['s20-ac','s20-a1'],stage='s20-ac:NH3/mol',note='0.500 mol × 3 = 1.50 mol of H atoms: the subscript 3 multiplies.'),
  dict(show='s20-a2',note='12.0 mol of H atoms × 6.022 × 10²³ = 7.23 × 10²⁴ H atoms.'),
  dict(show='s20-a3',note='2.5 × 10²² ÷ 6.022 × 10²³ = 0.042 mol: fewer than 6.022 × 10²³ molecules, so less than one mole.')]))
# ---------- 21 the mole in earlier lessons
S.append(slide('s21','t-concept cw','The mole in earlier lessons','Per mole','Reading §5.1.2',f'''    <div class="sim" id="s21-sim" data-sim="moleMap" aria-label="One mole of sodium atoms and one sodium atom losing an electron: energy per mole and per atom."></div>
    <div class="col acc">
{card('s21-c0','Lesson 3.2','Lesson 3.2: sodium\'s first ionization energy is 496&nbsp;kJ/mol.','per mole')}
{card('s21-pred','Predict','Per mole means for how many atoms?','predict')}
{card('s21-c1','One atom','496&nbsp;kJ ÷ '+NA+' atoms = 8.24&nbsp;×&nbsp;10<sup>−19</sup>&nbsp;J for one atom.','one atom')}
{card('s21-c2','Why per mole','Tiny for one atom. Per mole, the numbers have a handy size.','why per mole')}
{card('s21-rule','Rule','A value per mole describes '+NA+' particles. Divide by that number to get one particle.','rule','rule reg')}
    </div>''',
 'The reading\'s Watch example: 496 kJ/mol × 1000 J/kJ × 1 mol / 6.022 × 10²³ atoms = 8.24 × 10⁻¹⁹ J per atom. Lesson 3.3 gave heat "per mole of metal" the same way.',
 [dict(show='s21-c0',stage='s21-sim:energy/mole',focus='s21-sim',note='Lesson 3.2: 496 kJ/mol removes the most loosely held electron from each atom in a mole of gaseous sodium atoms.'),
  dict(show='s21-pred',stage='s21-sim:energy/mole',note='Prediction: per mole means for how many atoms? (6.022 × 10²³.)'),
  dict(hide=['s21-c0','s21-pred'],show='s21-c1',stage='s21-sim:energy/one',note='Divide by 6.022 × 10²³: 8.24 × 10⁻¹⁹ J for one atom.'),
  dict(show='s21-c2',stage='s21-sim:energy/why',note='For one atom the number is tiny, so chemists give such energies per mole.'),
  dict(hide='s21-c1',show='s21-rule',note='Students copy the rule card (reading §5.1.2 Key idea). No check on this slide.')]))
# ---------- 22 checkpoint routine
steps = [('Think · 30 s','alone, no talking'),('Talk · 60 s','tell your partner, then listen'),('Write · 90 s','use the sentence frames'),('Self-check','tick each success criterion'),('Compare','read the sample and fix one line')]
sr = '\n'.join(f'        <li id="s22-s{k+1}"><b class="lbl">{a}</b><span>{b}</span></li>' for k,(a,b) in enumerate(steps))
S.append(slide('s22','t-routine','Checkpoint routine','Checkpoint','Objectives 5.1.2 to 5.1.4',f'''    <div class="card prompt"><p>Each checkpoint uses the same five steps.</p></div>
    {rail('s22')}
    <ol class="steprows">
{sr}
    </ol>''',
 'Routine for slides 23 to 25: think 30 s, talk 60 s, write 90 s, self-check 30 s, compare 45 s.',
 [dict(note='Explain that the routine repeats for each question.')]+
 [dict(cls=dict([(f's22-r{j+1}','done') for j in range(k)]+[(f's22-s{j+1}','') for j in range(k)]+[(f's22-r{k+1}','now'),(f's22-s{k+1}','now')]),label=['think','talk','write','self-check','compare'][k],note=n) for k,n in enumerate(['Think: silent, no pencils.','Talk: partner A first, then partner B.','Write: the sentence frames and word bank stay on screen.','Self-check: tick each criterion you met.','Compare: read the sample answer and fix one line.'])]))
# ---------- 23 to 25 checkpoints
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
        <div class="card phase" id="{p}-write" data-label="write 90 s"><p class="tag">Write</p><ol class="frames">{fl}</ol><p class="bank"><b>Word bank:</b> {bk}</p></div>
        <div class="card phase" id="{p}-check" data-label="self-check"><p class="tag">Self-check: did you write that…</p><ul class="crit">{cr}</ul></div>
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
    return slide(sid,'t-routine',title,'Checkpoint',ref,body,'Routine: think 30 s, talk 60 s, write 90 s, self-check 30 s, compare 45 s. The question stays on screen on every frame.',fr)
S.append(checkpoint('s23','Checkpoint 1','Objective 5.1.2',
  'A student says a mole of copper and of aluminum have equal mass. Explain the error.',
  'Read the question. What does the student claim?',
  ['A mole is a count of <span class="gap"></span>, not a <span class="gap"></span>.','Both samples hold <span class="gap"></span> atoms, but a copper atom <span class="gap"></span>.'],
  ['6.022&nbsp;×&nbsp;10<sup>23</sup> particles','a mass','the same number of','has more mass'],
  ['a mole is a count?','the same number of atoms?','the masses differ?'],
  'A mole is a count, not a mass. Same number of atoms; copper atoms are heavier.',
  ['Read the prompt aloud. Ask: what does the student think a mole is? (a mass).','Compare with the sample. Reading §5.1.2: a mole is a count, like a dozen; one mole of copper (63.546 g) and one mole of aluminum (26.982 g) hold the same number of atoms.'],
  '"a mole weighs one gram" or "6.022 × 10²³ grams".'))
S.append(checkpoint('s24','Checkpoint 2','Objective 5.1.3',
  'A student writes: 2.50&nbsp;mol of sodium chloride contains 1.51&nbsp;×&nbsp;10<sup>24</sup> molecules. What is right? What is wrong?',
  'Read the question. Check the number, then the particle.',
  ['The number is right because <span class="gap"></span>.','The particle is wrong because <span class="gap"></span>.'],
  ['2.50 × 6.022&nbsp;×&nbsp;10<sup>23</sup>','formula units','no molecules','Na<sup>+</sup> and Cl<sup>−</sup> ions'],
  ['multiplied by 6.022&nbsp;×&nbsp;10<sup>23</sup>?','sodium chloride has no molecules?','formula units named?'],
  'The number is right: 2.50 × 6.022&nbsp;×&nbsp;10<sup>23</sup> = 1.51&nbsp;×&nbsp;10<sup>24</sup>. The particle is wrong: NaCl has no molecules. Count formula units.',
  ['Read the prompt aloud. Two parts: the number, then the particle.','Compare with the sample. Reading §5.1.3: ionic compounds are counted in formula units, one Na⁺ ion and one Cl⁻ ion each.'],
  '"divide to get particles".'))
S.append(checkpoint('s25','Checkpoint 3','Objective 5.1.4',
  'One mole of H<sub>2</sub>O holds one mole of H atoms. True or false?',
  'Read the question. Look at the formula of water.',
  ['False, because the subscript 2 means <span class="gap"></span>.','One mole of H<sub>2</sub>O holds <span class="gap"></span> of H atoms and <span class="gap"></span> of O atoms.'],
  ['two H atoms in each molecule','2&nbsp;mol','1&nbsp;mol','the subscript multiplies'],
  ['the subscript is atoms per molecule?','2&nbsp;mol of H?','1&nbsp;mol of O?'],
  'False. The subscript 2 means two H atoms per molecule. One mole of H<sub>2</sub>O has 2&nbsp;mol of H, 1&nbsp;mol of O.',
  ['Read the prompt aloud. Ask: what does the small 2 in H₂O tell you?','Compare with the sample. Reading §5.1.4: moles of an element\'s atoms = moles of molecules × the subscript.'],
  '"the subscript divides".'))
# ---------- 26 predictions and exit ticket
def pa(p, n, q, right, reason, lab, letter='B'):
    return f'''      <div class="card check done" id="{p}" data-label="{lab}" data-mode="none"><p class="tag">Question {n}</p><p class="q">{q}</p><ol class="opts" data-lay="row"><li class="opt right"><b>{letter}</b><span>{right}</span></li></ol><p class="reason">{reason}</p></div>'''
S.append(slide('s26','t-routine t-exit','Predictions and exit ticket','Exit ticket','Objectives 5.1.1 to 5.1.4',f'''    <div class="stack">
      <div class="phaseA" id="s26-A" data-label="answers">
        <div class="stack">
{pa('s26-p1',1,'One mole of copper and one mole of aluminum have…','the same number of atoms',chips('Mass of one mole',[('Al 26.982&nbsp;g','g'),('Cu 63.546&nbsp;g','g')])+'A mole is a count. The two samples hold the same number of atoms.','answer 1')}
{pa('s26-p2',2,'One mole of sodium chloride, NaCl, holds 6.022&nbsp;×&nbsp;10<sup>23</sup>…','formula units','Sodium chloride has no molecules. One formula unit is one Na<sup>+</sup> and one Cl<sup>−</sup>.','answer 2')}
{pa('s26-p3',3,'One mole of water, H<sub>2</sub>O, holds how many moles of hydrogen atoms?','2&nbsp;mol','The subscript 2 multiplies: two H atoms in every molecule.','answer 3')}
        </div>
        <p class="handsup">Hands up if you predicted this.</p>
      </div>
      <div class="phaseB" id="s26-B" data-label="exit ticket">
        <div class="card prompt reg dq"><p>{DQ1} {DQ2}</p></div>
        <ol class="rail"><li id="s26-r1">Claim</li><li id="s26-r2">Evidence</li><li id="s26-r3">Reasoning</li><li id="s26-r4">Self-check</li><li id="s26-r5">Sample</li></ol>
        <div class="rt-main">
          <div class="acc">
            <div class="card phase" id="s26-fr" data-label="claim"><p class="tag">Write</p><ol class="frames">
              <li id="s26-f1">Claim: Chemists count particles in moles, where one mole is <span class="gap"></span>.</li>
              <li id="s26-f2" data-label="evidence">Evidence: A bank counts nickels by weighing because <span class="gap"></span>. To change moles into particles, <span class="gap"></span>.</li>
              <li id="s26-f3" data-label="reasoning">Reasoning: For a compound, the formula tells <span class="gap"></span>, so <span class="gap"></span>.</li>
            </ol>
            <p class="bank" id="s26-bank"><b>Word bank:</b> <span>6.022&nbsp;×&nbsp;10<sup>23</sup> particles</span> <span>same mass</span> <span>divide</span> <span>multiply</span> <span>subscript</span> <span>each element</span></p></div>
            <div class="card" id="s26-check" data-label="self-check"><p class="tag">Self-check: did you write…</p><ul class="crit"><li>a claim that names the mole and its number?</li><li>the bank's method and the mole-to-particle step?</li><li>the subscript's role?</li></ul></div>
            <div class="card reg" id="s26-sample" data-label="sample answer"><p class="tag">Sample answer</p><p>One mole is 6.022&nbsp;×&nbsp;10<sup>23</sup> named particles. A bank weighs nickels because each has the same mass. Moles × 6.022&nbsp;×&nbsp;10<sup>23</sup> gives particles. The formula's subscripts count the atoms.</p></div>
          </div>
          <div class="timer"></div>
        </div>
      </div>
    </div>''',
 'Predictions from slide 4 come back first; students check their letters. Then the CER exit ticket on the driving question, which stays on screen while the sample shows. Collect the exit tickets.',
 [dict(show=['s26-A','s26-p1'],note='Answer 1: the same number of atoms. Hands up if you predicted it. Compare with the counts from slide 4.'),
  dict(hide='s26-p1',show='s26-p2',note='Answer 2: formula units. Ask a student who changed their mind to say why.'),
  dict(hide='s26-p2',show='s26-p3',note='Answer 3: 2 mol. "1 mol" was the common wrong idea.'),
  dict(hide='s26-A',show=['s26-B','s26-fr','s26-f1'],cls={'s26-r1':'now'},note='Exit ticket. Claim first: what is a mole?'),
  dict(show='s26-f2',cls={'s26-r1':'done','s26-r2':'now'},note='Evidence: the bank\'s weighing and the step from moles to particles.'),
  dict(show='s26-f3',cls={'s26-r2':'done','s26-r3':'now'},timer=180,label='write 3 min',note='Reasoning: the subscripts. Three minutes of writing.'),
  dict(show='s26-check',cls={'s26-r3':'done','s26-r4':'now'},note='Self-check with the three criteria.'),
  dict(show='s26-sample',cls={'s26-r4':'done','s26-r5':'now'},note='Compare with the sample. Collect the tickets.')]))
# ---------- 27 rate your learning
T = [('5.1.1','count objects by weighing, with one mass or an average.','slides 6 and 7'),('5.1.2','define the mole and use Avogadro\'s number.','slides 8 to 13 and 21'),
     ('5.1.3','change moles to particles and back, naming the particle.','slides 16 to 18'),('5.1.4','use a formula to count atoms in a sample.','slides 19 and 20')]
rt = '\n'.join(f'        <li id="s27-t{k+1}"><span><b class="mono lbl">{a}</b> {b}</span><span class="rev">Review: {c}</span></li>' for k,(a,b,c) in enumerate(T))
S.append(slide('s27','t-routine','Rate your learning','Reflect','All objectives',f'''    <div class="scale lbl"><span>1 finger: not yet</span><span>2 fingers: almost</span><span>3 fingers: I can teach it</span></div>
    <p class="tag">I can…</p>
    <ol class="rate">
{rt}
    </ol>''',
 'Fingers 1 to 3 for each target. Students below 3 revisit the slides named on the right, then the missions: Count by weighing, Moles and particles, Jar puzzles.',
 [dict(note='Explain the scale: 1 not yet, 2 almost, 3 I can teach it.')]+
 [dict(cls=dict([(f's27-t{j+1}','') for j in range(k)]+[(f's27-t{k+1}','now')]),label=f'target {k+1}',note=f'Fingers for target 5.1.{k+1}. Note who shows 1 and point to the review slides.') for k in range(4)]))
# ---------- 28 next
S.append(slide('s28','t-summary tnext','Next','Next','Missions 5.1 and Lesson 5.2','''    <div class="mrow">
      <div class="mission card"><svg viewBox="0 0 100 100" role="img" aria-label="Icon: a scale with nickels"><use href="#ic-scale"/></svg><b>Count by weighing</b><span>4 cases</span></div>
      <div class="mission card"><svg viewBox="0 0 100 100" role="img" aria-label="Icon: moles and particles, both ways"><use href="#ic-swap"/></svg><b>Moles and particles</b><span>5 cases</span></div>
      <div class="mission card"><svg viewBox="0 0 100 100" role="img" aria-label="Icon: a jar of mixed coins"><use href="#ic-jar"/></svg><b>Jar puzzles</b><span>jars of mixed objects</span></div>
    </div>
    <div class="card"><p class="big">Lesson 5.2 finds the mass of one mole of any substance from the periodic table.</p></div>''',
 'Missions for Lesson 5.1: Count by weighing (4 cases), Moles and particles (5 cases), Jar puzzles. Lesson 5.2 finds the mass of one mole of any substance from the periodic table (molar mass).',
 [dict(note='Point to the three missions. Preview Lesson 5.2: the mass of one mole of any substance, from the periodic table.')]))

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
open(OUT, 'w', encoding='utf-8').write(html)
print('slides:', len(S))
