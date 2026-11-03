# Generates 08-slides-42.html: the 26 slides of Lesson 4.2 (plan section 6). Scratch tool, not part of the repo.
import json, os, re, html as H
OUT = os.path.join(os.path.dirname(__file__), '08-slides-42.html')
def js(v): return json.dumps(v, ensure_ascii=False)
TIMES = {
 's01':[0.5], 's02':[0.5,0.75,0.75,0.75,0.75], 's03':[0.5,0.5,0.5,0.5,1.5], 's04':[0.75,0.75,1], 's05':[1,1.5,0.5],
 's06':[0.25,0.5,0.25,0.25,0.75,0.25,0.75,1,0.5,0.5], 's07':[0.5,0.75,0.5,0.5,0.75,0.5,0.5],
 's08':[0.5,0.5,0.5,0.25,0.25,0.25,0.5,0.25,1,0.5,0.5], 's09':[1,0.25,0.25,0.25,0.75,1.5,0.5,0.5],
 's10':[0.25,0.5,0.5,0.25,0.5,1,0.5,0.5], 's11':[0.25,0.5,0.75,1,0.5,0.5], 's12':[0.75,0.5,0.25,0.5,0.25,0.25,0.25,0.25,0.25,0.5,0.25,0.5,0.5],
 's13':[0.5,0.5,0.5,0.25,0.5,0.25],
 's14':[0.5,1.5,0.25,0.25,0.5], 's15':[0.5,0.25,0.25,0.25,0.25,0.5,0.5,1,0.5,0.5], 's16':[0.5,0.5,0.5,0.5,0.25,0.25,1,0.5,0.5],
 's17':[0.5,0.5,0.5,0.25,0.5,0.5,0.75,0.5,0.5], 's18':[0.25,3,0.125,0.125,0.125,0.125,0.125,0.125], 's19':[0.5,0.5,0.5,0.5,0.25,0.5,0.25],
 's20':[0.5,0.1,0.1,0.1,0.1,0.1], 's21':[0.25,0.5,1,1.5,0.5,0.75], 's22':[0.25,0.5,1,1.5,0.5,0.75], 's23':[0.25,0.5,1,1.5,0.5,0.75],
 's24':[0.5,0.5,0.5,0.5,0.5,3,0.5,0.5], 's25':[0.25,0.25,0.25,0.25,0.25,0.25], 's26':[0.5]}
def frames(sid, fr):
    assert len(TIMES[sid]) == len(fr), (sid, len(TIMES[sid]), len(fr))
    for f, t in zip(fr, TIMES[sid]): f['t'] = t
    rows = []
    for f in fr:
        rows.append('{' + ','.join(f"{k}:{js(f[k])}" for k in ['show','hide','stage','cls','timer','focus','label','cue','t','note'] if k in f) + '}')
    return f"<script>Deck.frames('{sid}',[\n    " + ',\n    '.join(rows) + "\n  ]);</script>"
def slide(sid, cls, title, sec, ref, body, notes, fr):
    per = '1' if int(sid[1:]) <= 13 else '2'
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
    # the question stays; the answer or a mouse feedback line shows under the options
    return f'''      <div class="checkrow" id="{p}-check" data-label="check">
        <p class="q" id="{p}-q"><span class="tag">Check:</span> {q}</p>
        <ol class="opts" data-lay="{lay(opts)}">{optli(p, opts, right, fb)}</ol>
        <div class="af"><p class="ans" id="{p}-ans" data-label="answer">{ans}</p><p class="fb" aria-live="polite"></p></div>
      </div>'''
def chips(label, items):
    # a value list with its meaning: a label line, then one chip per value
    return f'<span class="enrow"><span class="enl lbl">{label}</span><span class="chips">' + ''.join(f'<span class="chip">{x}</span>' for x in items) + '</span></span>'
def use(i, label, cls=''):
    return f'<svg class="{cls}" viewBox="0 0 100 100" role="img" aria-label="{label}"><use href="#{i}"/></svg>'
def rail(p, names=('Think','Talk','Write','Self-check','Compare')):
    return '<ol class="rail">' + ''.join(f'<li id="{p}-r{k+1}">{t}</li>' for k, t in enumerate(names)) + '</ol>'

SPRITE = '''<svg class="sprite" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden"><defs>
<symbol id="ic-next" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M48 30v40l32-20Z" class="f-acc"/></symbol>
<symbol id="ic-back" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M72 30v40L40 50Z" class="f-acc"/></symbol>
<symbol id="ic-blank" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><rect x="34" y="30" width="52" height="34" rx="4" class="f-ink"/><path d="M52 74h16" class="k-ink" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-start" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M30 34v-8h10M90 34v-8H80M30 66v8h10M90 66v8H80" fill="none" class="k-acc" stroke-width="5" stroke-linecap="round"/><path d="M52 38v24l20-12Z" class="f-acc"/></symbol>
<symbol id="ic-redpowder" viewBox="0 0 100 100"><ellipse cx="50" cy="74" rx="44" ry="14" class="f-dish k-ink" stroke-width="3"/><path d="M18 72q32-46 64 0Z" class="f-redp k-ink" stroke-width="3"/><path d="M58 18h30l-6 14H62Z" class="f-boat k-ink" stroke-width="3"/><path d="M73 6v12" class="k-ink" stroke-width="3"/></symbol>
<symbol id="ic-blackpowder" viewBox="0 0 100 100"><ellipse cx="50" cy="74" rx="44" ry="14" class="f-dish k-ink" stroke-width="3"/><path d="M18 72q32-46 64 0Z" class="f-black k-ink" stroke-width="3"/><path d="M66 8h20l-2 6q8 10 0 20H68q-8-10 0-20Z" class="f-pot k-ink" stroke-width="3"/></symbol>
<symbol id="ic-cuo" viewBox="0 0 100 100"><circle cx="32" cy="50" r="26" class="f-cat"/><circle cx="74" cy="50" r="20" class="f-an"/><path d="M20 50h24M32 38v24M66 50h16" class="k-on" stroke-width="6" stroke-linecap="round"/></symbol>
<symbol id="ic-cation" viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" class="f-cat"/><path d="M32 50h36M50 32v36" class="k-on" stroke-width="8" stroke-linecap="round"/></symbol>
<symbol id="ic-anion" viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" class="f-an"/><path d="M32 50h36" class="k-on" stroke-width="8" stroke-linecap="round"/></symbol>
<symbol id="ic-charge" viewBox="0 0 100 100"><circle cx="34" cy="56" r="26" class="f-cat"/><circle cx="72" cy="30" r="20" class="f-card2 k-cat" stroke-width="4"/><path d="M24 56h20M34 46v20M64 30h16M72 22v16" class="k-on" stroke-width="5" stroke-linecap="round"/><path d="M64 30h16M72 22v16" class="k-cat" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-formula" viewBox="0 0 100 100"><rect x="6" y="20" width="40" height="56" rx="8" class="f-cat"/><rect x="52" y="20" width="30" height="56" rx="8" class="f-an"/><rect x="84" y="62" width="12" height="20" rx="3" class="f-ink"/><path d="M16 48h20M26 38v20M59 48h16" class="k-on" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-subscript" viewBox="0 0 100 100"><rect x="10" y="12" width="50" height="64" rx="8" class="f-card2 k-ink" stroke-width="4"/><rect x="66" y="60" width="24" height="30" rx="5" class="f-acc"/></symbol>
<symbol id="ic-poly" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" class="k-muted" stroke-width="4" stroke-dasharray="8 6"/><circle cx="50" cy="50" r="15" class="f-ink"/><circle cx="50" cy="20" r="11" class="f-redp"/><circle cx="76" cy="64" r="11" class="f-redp"/><circle cx="24" cy="64" r="11" class="f-redp"/><circle cx="84" cy="16" r="13" class="f-an"/><path d="M78 16h12" class="k-on" stroke-width="4" stroke-linecap="round"/></symbol>
<symbol id="ic-roman" viewBox="0 0 100 100"><rect x="8" y="14" width="84" height="72" rx="12" class="f-card2 k-acc" stroke-width="4"/><path d="M34 30v40M50 30v40M66 30v40M26 30h48M26 70h48" class="k-ink" stroke-width="6" stroke-linecap="round"/></symbol>
<symbol id="ic-paren" viewBox="0 0 100 100"><path d="M26 12q-18 38 0 76M74 12q18 38 0 76" fill="none" class="k-acc" stroke-width="7" stroke-linecap="round"/><circle cx="42" cy="50" r="12" class="f-redp"/><circle cx="60" cy="50" r="8" class="f-white k-ink" stroke-width="2"/><rect x="84" y="70" width="12" height="20" rx="3" class="f-ink"/></symbol>
<symbol id="ic-tag" viewBox="0 0 100 100"><path d="M10 50 40 18h50v64H40Z" class="f-card2 k-acc" stroke-width="5" stroke-linejoin="round"/><circle cx="34" cy="50" r="7" class="f-acc"/><path d="M52 40h28M52 58h20" class="k-ink" stroke-width="6" stroke-linecap="round"/></symbol>
<symbol id="ic-tiles" viewBox="0 0 100 100"><rect x="8" y="54" width="84" height="30" rx="6" class="f-cat"/><rect x="18" y="46" width="14" height="10" rx="2" class="f-cat"/><rect x="68" y="46" width="14" height="10" rx="2" class="f-cat"/><rect x="8" y="16" width="40" height="28" rx="6" class="f-an"/><rect x="52" y="16" width="40" height="28" rx="6" class="f-an"/><path d="M41 69h18M50 60v18M20 30h16M64 30h16" class="k-on" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-magnify" viewBox="0 0 100 100"><circle cx="42" cy="42" r="28" class="f-card2 k-acc" stroke-width="7"/><path d="M62 62l26 26" class="k-acc" stroke-width="10" stroke-linecap="round"/><path d="M30 34l24 16M54 34 30 50" class="k-bad" stroke-width="6" stroke-linecap="round" style="stroke:var(--bad)"/></symbol>
</defs></svg>'''

S = []
DQ = 'How do the charges of ions decide the formula and the name of an ionic compound?'
# ---------- 1 cover
S.append(slide('s01','t-cover','Ionic formulas and names','Lesson 4.2','Reading §4.2',f'''    <div class="card dq reg"><p class="tag">Driving question</p><p>{DQ}</p></div>
    <div class="r800">
      <div class="key"><svg viewBox="0 0 120 100" role="img" aria-label="Next button"><use href="#ic-next"/></svg><b>Next</b><span>next step</span></div>
      <div class="key"><svg viewBox="0 0 120 100" role="img" aria-label="Back button"><use href="#ic-back"/></svg><b>Back</b><span>one step back</span></div>
      <div class="key"><svg viewBox="0 0 120 100" role="img" aria-label="Blank button"><use href="#ic-blank"/></svg><b>Blank</b><span>zoom part by part<br>twice fast: blank</span></div>
      <div class="key"><svg viewBox="0 0 120 100" role="img" aria-label="Start button"><use href="#ic-start"/></svg><b>Start</b><span>full screen</span></div>
    </div>''',
 '<b>Safety.</b> No demonstration in this lesson. If real samples are shown (the two copper oxides, a fertilizer bag, an antacid), keep them sealed and out of reach: copper compounds are harmful if swallowed. <b>Data and sources.</b> Names follow IUPAC, <i>Nomenclature of Inorganic Chemistry: Recommendations 2005</i> (the Red Book), IR-5 compositional names; common names leave out prefixes because the charges fix the ratio. Ion charges from group number as in the reading §4.2.1; the four transition-metal ions Fe²⁺, Fe³⁺, Cu⁺, Cu²⁺, Ag⁺, Zn²⁺. Copper(I) oxide in antifouling paint and copper(II) oxide in glazes as in the reading opener; hematite is iron(III) oxide (Mindat). OpenStax Chemistry 2e, 2.7 Chemical Nomenclature. <b>Clicker.</b> Logitech R800: Next = PageDown, Back = PageUp (while zoomed: exit the zoom), Start/stop = F5 then Escape, Blank = period. Blank zooms one part of the slide per press, animation first; the press after the last part exits; two fast presses on an unzoomed slide blank the screen. Mouse: click an option to mark it right or wrong; click the slide number or the section label for the slide list. Laptop: N notes, O overview, T theme, Ctrl+P run-sheet.',
 [dict(note='Two periods. Read the driving question aloud; students copy it. Show the four clicker buttons once so students know a zoom or a blank screen is on purpose.')]))
# ---------- 2 hook
S.append(slide('s02','t-hook','Read the label','Hook','Reading §4.2 opener','''    <div class="sim" id="s02-sim" data-sim="labelRead" aria-label="A store shelf with toothpaste, an antacid and lawn food; each label has a chemical name."></div>
    <div class="stack card band">
      <p class="line" id="s02-l0">Each product has a chemical name on its label.</p>
      <p class="line" id="s02-l1" data-label="toothpaste">Toothpaste protects teeth with sodium fluoride.</p>
      <p class="line" id="s02-l2" data-label="antacid">An antacid calms the stomach with calcium carbonate.</p>
      <p class="line" id="s02-l3" data-label="lawn food">Lawn food feeds grass with ammonium sulfate.</p>
      <p class="line" id="s02-l4" data-label="the code">Each name tells you the ions inside.</p>
    </div>''',
 'Narrative thread for 4.2: the code. Store labels are a code; the letters are ions and charges; the rule is zero total charge; the name is the code read aloud. The three names return on slide 18.',
 [dict(show='s02-l0',stage='s02-sim:shelf',note='Ask: who has read the small print on a toothpaste tube? Collect two guesses about what the names mean.'),
  dict(hide='s02-l0',show='s02-l1',stage='s02-sim:focus0',note='Sodium fluoride: sodium ions and fluoride ions. Do not explain yet; students only notice two words.'),
  dict(hide='s02-l1',show='s02-l2',stage='s02-sim:focus1',note='Calcium carbonate: calcium ions and carbonate ions, a group of atoms. Ask: what do the two names have in common? (metal first).'),
  dict(hide='s02-l2',show='s02-l3',stage='s02-sim:focus2',note='Ammonium sulfate: two groups of atoms. Misconception to listen for: "the name lists every atom".'),
  dict(hide='s02-l3',show='s02-l4',stage='s02-sim:code',note='The code line. Promise: by slide 18 students write the formula of each of these three.')]))
# ---------- 3 two copper oxides
S.append(slide('s03','t-launch','Two copper oxides','Launch','Reading §4.2 opener',f'''    <div class="trio" id="s03-trio">
      <div class="card pcard slot"><div data-b="s03-red" data-label="red powder">{use('ic-redpowder','Icon: a dish of red powder and a boat')}<p class="nm">red powder</p><p class="cap">used in boat paint</p></div></div>
      <div class="card pcard slot"><div data-b="s03-black" data-label="black powder">{use('ic-blackpowder','Icon: a dish of black powder and a pot')}<p class="nm">black powder</p><p class="cap">used in pottery glaze</p></div></div>
      <div class="card pcard slot"><div data-b="s03-both" data-label="what is inside">{use('ic-cuo','Icon: a copper atom and an oxygen atom')}<p class="nm">both</p><p class="cap">only copper ions and oxide ions</p></div></div>
    </div>
    <div class="card dq reg" id="s03-dq" data-label="driving question"><p>{DQ}</p></div>
    <div class="qrow" id="s03-st" data-label="write 60 s"><ol class="frames"><li>I think the two powders have different formulas because <span class="gap"></span>.</li></ol><div class="timer"></div></div>''',
 'Copper(I) oxide is the red powder in antifouling boat paint; copper(II) oxide is the black powder in pottery glazes. Do not name them yet: the names are the answer of slide 12.',
 [dict(show='s03-red',note='Red powder in boat paint. It keeps barnacles off the hull.'),
  dict(show='s03-black',note='Black powder used to color glazes.'),
  dict(show='s03-both',note='Both contain only copper and oxygen. Ask: how can two compounds of the same two elements differ?'),
  dict(show='s03-dq',cls={'s03-trio':'small'},note='Read the driving question; students copy it.'),
  dict(show='s03-st',timer=60,note='Sixty seconds with the starter. Collect two answers; listen for "different numbers of atoms" and for "copper has different charges".')]))
# ---------- 4 predict now
def pq(p, n, q, opts, lab):
    o = ''.join(f'<li class="opt"><b>{l}</b><span>{t}</span></li>' for l, t in zip('ABC', opts))
    return f'      <div class="card check" id="{p}" data-label="{lab}" data-mode="pick"><p class="tag">Question {n}</p><p class="q">{q}</p><ol class="opts col1" data-lay="col">{o}</ol></div>'
S.append(slide('s04','t-routine','Predict now','Predict','Reading §4.2 Before you read',f'''    <div class="card prompt"><p>Hands up: one finger for A, two for B, three for C. Write your letter.</p></div>
    <div class="stack top">
{pq('s04-q1',1,'Mg<sup>2+</sup> with O<sup>2−</sup> gives…',['MgO','Mg<sub>2</sub>O<sub>2</sub>','MgO<sub>2</sub>'],'question 1')}
{pq('s04-q2',2,'The III in iron(III) chloride means…',['a charge of 3+','three iron atoms','three electrons gained'],'question 2')}
{pq('s04-q3',3,'Calcium hydroxide is…',['Ca(OH)<sub>2</sub>','CaOH<sub>2</sub>','CaO<sub>2</sub>H<sub>2</sub>'],'question 3')}
    </div>''',
 'No answers on this slide. Students keep their letters; slide 24 returns all three answers.',
 [dict(show='s04-q1',note='Count hands for A, B, C and write the counts on the board. Do not react to the choices. A mouse click on an option only highlights it; there is no grading on this slide.'),
  dict(hide='s04-q1',show='s04-q2',note='Count hands. Many choose "three iron atoms": the numeral read as a count.'),
  dict(hide='s04-q2',show='s04-q3',note='Count hands. CaOH₂ is the common wrong idea. Keep the counts for slide 24.')]))
# ---------- 5 targets and words
W = [('ic-cation','cation','catión','a + ion; a metal atom lost electrons'),('ic-anion','anion','anión','a − ion; a nonmetal atom gained electrons'),
     ('ic-charge','charge','carga','the + or − number on an ion: charge 2+'),('ic-formula','formula','fórmula','symbols and small numbers for a compound'),
     ('ic-subscript','subscript','subíndice','the small number: how many of each'),('ic-poly','polyatomic ion','ion poliatómico','a group of atoms with one charge'),
     ('ic-roman','Roman numeral','número romano','the charge of an iron or copper ion'),('ic-paren','parentheses','paréntesis','marks around a group that repeats')]
wc = '\n'.join(f'        <div class="wcard">{use(i,"Icon: "+t)}<p class="t">{t} <span class="es">({es})</span></p><p class="m">{m}</p></div>' for i,t,es,m in W)
S.append(slide('s05','t-words','Targets and words','Targets','Reading §4.2 Vocabulary',f'''    <div class="stack">
      <div class="card" id="s05-ican" data-label="targets"><p class="tag">I can…</p><ul class="ican">
        <li><b>4.2.1</b>predict an ion's charge from its group.</li>
        <li><b>4.2.2</b>write a formula with zero total charge.</li>
        <li><b>4.2.3</b>name compounds, with numerals for Fe and Cu.</li>
        <li><b>4.2.4</b>use polyatomic ions and parentheses.</li>
        <li><b>4.2.5</b>go from name to formula and back.</li></ul></div>
      <div class="words" id="s05-words" data-label="words">
{wc}
      </div>
    </div>
    <div class="legend" id="s05-leg" data-label="color code"><span><i class="i-cat">+</i>cation</span><span><i class="i-an">−</i>anion</span><span><i class="e"></i>electron</span><span><i class="i-metal"> </i>metal</span><span><i class="i-nm"> </i>nonmetal</span><span><i class="i-dp">δ+</i>small +</span><span><i class="i-dm">δ−</i>small −</span></div>''',
 'The color code is the same as in Lesson 4.1: cation red with +, anion blue with −. Shapes also carry a sign, so color-blind students can read every drawing.',
 [dict(show='s05-ican',note='Read the five targets. Students copy 4.2.1 to 4.2.5; they rate themselves on slide 25.'),
  dict(hide='s05-ican',show='s05-words',note='Choral reading: English term, then the Spanish cognate. Students add the words to the glossary with the icon.'),
  dict(show='s05-leg',note='Same color code as Lesson 4.1. Polyatomic ions appear later with a dashed outline: one unit.')]))
# ---------- 6 charges from the group (wide)
S.append(slide('s06','t-concept wide','Charges from the group','Ion charges','Reading §4.2.1',f'''    <div class="sim" id="s06-sim" data-sim="ionTable" data-fblock="0" data-reserve="214" aria-label="The periodic table with the charge of each group's ion."></div>
    <div class="ptrow"><div class="stack">
      <p class="caprow" id="s06-p0">Where are the metals? Where are the nonmetals?</p>
      <p class="caprow" id="s06-p1" data-label="group 1">Group 1 metals lose 1 electron: charge 1+.</p>
      <p class="caprow" id="s06-p2" data-label="group 2">Group 2 metals lose 2 electrons: charge 2+.</p>
      <p class="caprow" id="s06-p3" data-label="aluminum">Aluminum loses 3 electrons: charge 3+.</p>
      <p class="caprow" id="s06-p4" data-label="group 17">Group 17 gains 1 electron: charge 1−. The name ends in -ide.</p>
      <p class="caprow" id="s06-p5" data-label="group 16">Group 16 gains 2 electrons: charge 2−.</p>
      <p class="caprow" id="s06-p6" data-label="group 15">Nitrogen gains 3 electrons: charge 3−.</p>
      <div class="rulerow reg" id="s06-rule" data-label="rule"><p>Metal atoms lose 1, 2 or 3 valence electrons.</p><p>Nonmetal atoms gain electrons to reach eight.</p><p>A monatomic anion name ends in -ide.</p></div>
{checkrow('s06','Which ion does magnesium form?',['Mg<sup>+</sup>','Mg<sup>2+</sup>','Mg<sup>2−</sup>'],'B. Magnesium is in group 2. It loses 2 electrons.',right='B',fb=['Mg<sup>+</sup> lost only one electron. Group 2 loses two.','Magnesium is in group 2. It loses 2 electrons.','A minus charge means gained electrons. Metals lose electrons.'])}
    </div></div>''',
 'Group number gives the charge for groups 1, 2, 13 (aluminum), 15, 16 and 17. Groups 14 and 18 form no simple ions in this course. Monatomic anions take -ide: fluoride, chloride, bromide, iodide, oxide, sulfide, nitride.',
 [dict(show='s06-p0',stage='s06-sim:outline',focus='s06-sim',note='Students point: metals left and middle, nonmetals upper right.'),
  dict(hide='s06-p0',show='s06-p1',stage='s06-sim:g1',note='Group 1: one valence electron lost, 1+ (Lesson 4.1: Na⁺).'),
  dict(hide='s06-p1',show='s06-p2',stage='s06-sim:g2',note='Group 2: 2+. Ask: Ca? (Ca²⁺).'),
  dict(hide='s06-p2',show='s06-p3',stage='s06-sim:g13',note='Only aluminum is lit in group 13 for this course: Al³⁺.'),
  dict(hide='s06-p3',show='s06-p4',stage='s06-sim:g17',note='Group 17 gains one electron to reach eight: 1−. Read the -ide names in the list.'),
  dict(hide='s06-p4',show='s06-p5',stage='s06-sim:g16',note='Group 16: oxide, sulfide.'),
  dict(hide='s06-p5',show='s06-p6',stage='s06-sim:g15',note='Nitride, 3−. The dash badges: groups 14 and 18 form no simple ion. Misconception: "the charge equals the group number for nonmetals" (it is 8 minus the valence electrons).'),
  dict(hide='s06-p6',show='s06-rule',cue='check (first ask aloud: K? S?)',note='Students copy the three rules. Oral calls before the press: K? (K⁺) S? (S²⁻).'),
  dict(hide='s06-rule',show='s06-check',note='Hands up for A, B or C. The table still shows group 2 with its charge.'),
  dict(show='s06-ans',cls={'s06-b':'right','s06-check':'done'},note='B is right. A (Mg⁺): that is one electron lost; group 2 loses two. C (Mg²⁻): a minus charge means electrons gained; metals lose electrons.')]))
# ---------- 7 the four to memorize (wide)
S.append(slide('s07','t-concept wide','The four to memorize','Ion charges','Reading §4.2.1',f'''    <div class="sim" id="s07-sim" data-sim="ionTable" data-fblock="0" data-reserve="214" aria-label="Iron, copper, silver and zinc lit on the periodic table with their ions."></div>
    <div class="ptrow"><div class="stack">
      <p class="caprow" id="s07-p0">Four transition metals to learn.</p>
      <div class="rulerow" id="s07-p1" data-label="two ions each"><p>Fe<sup>2+</sup> and Fe<sup>3+</sup>, Cu<sup>+</sup> and Cu<sup>2+</sup>: two ions each.</p><p>The numeral is a version number, not a count.</p></div>
      <p class="caprow" id="s07-p2" data-label="silver and zinc">Ag<sup>+</sup> and Zn<sup>2+</sup> have one ion each, so no numeral.</p>
      <p class="caprow" id="s07-p3" data-label="real life">Rust and the iron ore hematite hold Fe<sup>3+</sup>.</p>
      <div class="memrow card" id="s07-mem" data-label="memory card" data-zoom="memory card"><p class="tag">Memory card: the six ions and their charges</p><p class="memchips"><span>Fe<sup>2+</sup></span><span>Fe<sup>3+</sup></span><span>Cu<sup>+</sup></span><span>Cu<sup>2+</sup></span><span>Ag<sup>+</sup></span><span>Zn<sup>2+</sup></span></p></div>
{checkrow('s07','Which metal needs a Roman numeral in its name?',['zinc','silver','copper'],'C. Copper forms Cu<sup>+</sup> and Cu<sup>2+</sup>.',right='C',fb=['Zinc forms one ion, Zn<sup>2+</sup>, so no numeral.','Silver forms one ion, Ag<sup>+</sup>, so no numeral.','Copper forms two ions, Cu<sup>+</sup> and Cu<sup>2+</sup>.'])}
    </div></div>''',
 'Transition metals: iron and copper form two common ions each; silver and zinc form one. Rust and hematite (Fe₂O₃) contain Fe³⁺; iron(II) sulfate (a plant supplement) contains Fe²⁺. Honors box (not assessed): ferrous/ferric, cuprous/cupric, Sn²⁺/Sn⁴⁺, Pb²⁺/Pb⁴⁺.',
 [dict(show='s07-p0',stage='s07-sim:tm',focus='s07-sim',note='Fe, Cu, Ag and Zn light up. Ask: why can the group number not help here?'),
  dict(hide='s07-p0',show='s07-p1',note='Two ions each for Fe and Cu. Say: like version 2 and version 3 of an app, not two apps. Misconception: "(III) means three atoms".'),
  dict(hide='s07-p1',show='s07-p2',note='Silver and zinc have one ion each, so their names need no numeral.'),
  dict(hide='s07-p2',show='s07-p3',note='Real life: rust and hematite are iron(III) compounds.'),
  dict(hide='s07-p3',show='s07-mem',note='Memory card: students copy the six ions in large print and quiz a partner for 30 seconds.'),
  dict(hide='s07-mem',show='s07-check',note='Hands up for A, B or C. The four metals stay lit on the table.'),
  dict(show='s07-ans',cls={'s07-c':'right','s07-check':'done'},note='C is right. A (zinc): one ion, Zn²⁺, so no numeral. B (silver): one ion, Ag⁺, no numeral.')]))
# ---------- 8 balancing the charges
S.append(slide('s08','t-concept','Balancing the charges','Formulas','Reading §4.2.2',f'''    <div class="sim" id="s08-sim" data-sim="chargeBlocks" data-pairs="Ca-Cl,Al-O,Na-O" aria-label="Ion tiles: plus studs on cations fit minus sockets on anions."></div>
    <div class="col acc">
      <div class="card" id="s08-c0" data-label="studs"><p class="tag">Model</p><p>Every + stud needs a − socket. The total charge must be zero.</p></div>
      <div class="card" id="s08-c1" data-label="calcium chloride"><p class="tag">Ca and Cl</p><p>Ca<sup>2+</sup> has two studs, so it needs two Cl<sup>−</sup> ions. The charges 2+ and 2− add to zero.</p></div>
      <div class="card" id="s08-q2" data-label="aluminum oxide"><p class="tag">Al and O</p><p>Al<sup>3+</sup> and O<sup>2−</sup>: how many of each ion make the total charge zero?</p></div>
      <div class="card" id="s08-c2" data-label="balance"><p class="tag">Al and O</p><p>Two Al<sup>3+</sup> ions give a charge of 6+. Three O<sup>2−</sup> ions give 6−. The total charge is zero.</p></div>
      <div class="card rule reg" id="s08-rule" data-label="rule"><p class="tag">Rule</p><p>The total charge of an ionic compound is zero. The formula shows the smallest whole-number ratio of ions.</p></div>
{check('s08','Na<sup>+</sup> with O<sup>2−</sup> balances as…',['NaO','NaO<sub>2</sub>','Na<sub>2</sub>O'],ans='C. Two Na<sup>+</sup> give 2+. One O<sup>2−</sup> gives 2−.',right='C',
  fb=['One Na<sup>+</sup> and one O<sup>2−</sup> leave a charge of 1−.','NaO<sub>2</sub> gives 1+ against 4−, even further from zero.','Two Na<sup>+</sup> give 2+. One O<sup>2−</sup> gives 2−.'])}
    </div>''',
 'Ion-tile model (blueprint): a tile is as long as its charge. Studs equal sockets means the total charge is zero. Reading §4.2.2 Key idea: find the smallest numbers of cations and anions whose charges add to zero.',
 [dict(show='s08-c0',stage='s08-sim:Ca-Cl/ions',focus='s08-sim',note='One Ca²⁺ tile and one Cl⁻ tile. Ask: is this balanced? (one stud is empty).'),
  dict(stage='s08-sim:Ca-Cl/add',note='A second Cl⁻ drops in. Predict first: how many Cl⁻ does one Ca²⁺ need?'),
  dict(show='s08-c1',stage='s08-sim:Ca-Cl/balance',note='The rows snap: 2+ and 2−. Point at each + stud in a − socket.'),
  dict(stage='s08-sim:Ca-Cl/formula',note='The counts become the formula CaCl₂: one Ca, two Cl.'),
  dict(stage='s08-sim:Ca-Cl/name',note='Calcium chloride: cation name, then anion with -ide.'),
  dict(hide='s08-c1',show='s08-q2',stage='s08-sim:Al-O/ions',note='Al³⁺ and O²⁻. Ask: how many of each? Give 20 seconds of partner talk.'),
  dict(hide='s08-q2',show='s08-c2',stage='s08-sim:Al-O/balance',note='Two Al³⁺ (6+) and three O²⁻ (6−). The least common multiple is 6.'),
  dict(stage='s08-sim:Al-O/formula',note='Al₂O₃. Misconception: "Al₃O₂" (counts swapped).'),
  dict(show='s08-rule',note='Students copy the rule. "Smallest set" prepares the reduce step on slide 9.'),
  dict(hide='s08-c2',show='s08-check',stage='s08-sim:Na-O/ions',note='Hands up for A, B or C. The tiles show one Na⁺ and one O²⁻: not balanced yet.'),
  dict(show='s08-ans',cls={'s08-c':'right','s08-check':'done'},stage='s08-sim:Na-O/formula',note='C is right. A (NaO): 1+ and 2− leave 1− left over. B (NaO₂): 1+ against 4−, even further off.')]))
# ---------- 9 writing the formula
S.append(slide('s09','t-example cb','Writing the formula','Formulas','Reading §4.2.2',f'''    <div class="sim" id="s09-sim" data-sim="chargeBlocks" data-pairs="Mg-O:reduce,K-S,Ca-N" aria-label="Ion tiles for magnesium oxide, potassium sulfide and calcium nitride."></div>
    <div class="col acc">
      <div class="card stepscard" id="s09-steps"><p class="tag">Writing rules</p><ol class="steps">
        <li id="s09-1" data-label="rules"><span class="k">Order</span><span>Write the cation first.</span></li>
        <li id="s09-2" data-label="rule 2"><span class="k">Subscripts</span><span>The small numbers count the ions.</span></li>
        <li id="s09-3" data-label="rule 3"><span class="k">No 1</span><span>Write no subscript 1.</span></li>
        <li id="s09-4" data-label="lowest ratio"><span class="k">Lowest</span><span>Reduce to the lowest ratio: MgO, not Mg<sub>2</sub>O<sub>2</sub>.</span></li>
      </ol></div>
      <div class="card" id="s09-try" data-label="your turn"><p class="tag">Your turn: write each formula.</p>
        <p>potassium sulfide → <span class="formula" data-b="s09-a1" data-label="answer 1">K<sub>2</sub>S</span></p>
        <p>calcium nitride → <span class="formula" data-b="s09-a2" data-label="answer 2">Ca<sub>3</sub>N<sub>2</sub></span></p>
        <div class="timer"></div></div>
    </div>''',
 'Reading §4.2.2 Key idea: cation first, anion second; subscripts are the numbers of ions in the lowest whole-number ratio: MgO, not Mg₂O₂.',
 [dict(show=['s09-1','s09-2','s09-3'],stage='s09-sim:Mg-O/ions',note='Three writing rules. Order: cation first (NaCl, never ClNa). Subscripts count ions in the formula unit. A 1 is never written: MgO, not Mg₁O₁.'),
  dict(stage='s09-sim:Mg-O/add',note='Someone adds a second pair: two Mg²⁺ and two O²⁻.'),
  dict(stage='s09-sim:Mg-O/balance',note='4+ and 4−: balanced, but not the smallest set.'),
  dict(stage='s09-sim:Mg-O/formula',note='Mg₂O₂ is not a formula. Ask: what is wrong with it?'),
  dict(show='s09-4',stage='s09-sim:Mg-O/reduce',note='Two pairs collapse to one: 2 : 2 → 1 : 1, MgO. Misconception: "crisscross always gives the final formula".'),
  dict(show='s09-try',timer=60,note='One minute. Students write both formulas in notebooks with the tile picture in mind.'),
  dict(show='s09-a1',stage='s09-sim:K-S/formula',note='K⁺ and S²⁻: two K⁺ for one S²⁻, K₂S.'),
  dict(show='s09-a2',stage='s09-sim:Ca-N/formula',note='Ca²⁺ and N³⁻: 6+ and 6−, Ca₃N₂.')]))
# ---------- 10 crisscross
S.append(slide('s10','t-example cw','The crisscross shortcut','Formulas','Reading §4.2.2',f'''    <div class="sim" id="s10-sim" data-sim="crisscross" data-pairs="Al-O,Mg-O,Ca-O" aria-label="The charge numbers cross over to become subscripts."></div>
    <div class="col acc">
      <div class="card" id="s10-cA" data-label="start"><p class="tag">Shortcut</p><p>Crisscross is a fast way to balance the charges.</p></div>
      <div class="card" id="s10-cB" data-label="magnesium oxide"><p class="tag">Mg and O</p><p>Mg<sup>2+</sup> and O<sup>2−</sup>: cross the charge numbers again.</p></div>
      <div class="card" id="s10-c0" data-label="cross"><p class="tag">Cross</p><p>Each charge number becomes the other ion's subscript. The signs drop.</p></div>
      <div class="card" id="s10-c1" data-label="check"><p class="tag">Check</p><p>Two Al<sup>3+</sup> ions give 6+. Three O<sup>2−</sup> ions give 6−. The total charge is zero.</p></div>
      <div class="card" id="s10-c2" data-label="reduce"><p class="tag">Reduce</p><p>Crossing gives Mg<sub>2</sub>O<sub>2</sub>. Divide both counts by 2: MgO.</p></div>
      <div class="card rule reg" id="s10-rule" data-label="rule"><p class="tag">Rule</p><p>Crisscross is a shortcut, not the final formula. Always reduce the ratio, then check the total charge.</p></div>
{check('s10','Crisscross gives Ca<sub>2</sub>O<sub>2</sub>. The formula is…',['Ca<sub>2</sub>O<sub>2</sub>','CaO','CaO<sub>2</sub>'],ans='B. Reduce 2 : 2 to 1 : 1. The charges 2+ and 2− make zero.',right='B',
  fb=['Ca<sub>2</sub>O<sub>2</sub> is not reduced. Divide both counts by 2.','Reduce 2 : 2 to 1 : 1. The charges 2+ and 2− make zero.','CaO<sub>2</sub> gives 2+ against 4−, so it does not balance.'])}
    </div>''',
 'The crisscross is a shortcut for the tile picture; it must be followed by reducing and by checking the charge totals.',
 [dict(show='s10-cA',stage='s10-sim:Al-O/ions',focus='s10-sim',note='Al³⁺ and O²⁻ again, the same pair as slide 8.'),
  dict(hide='s10-cA',show='s10-c0',stage='s10-sim:Al-O/cross',note='The 3 moves under O, the 2 under Al. The signs are not written in the formula.'),
  dict(show='s10-c1',stage='s10-sim:Al-O/check',note='Check: 6+ and 6−. 3 and 2 share no factor, so Al₂O₃ stays.'),
  dict(hide=['s10-c0','s10-c1'],show='s10-cB',stage='s10-sim:Mg-O/cross',note='Mg²⁺ and O²⁻ crossed: Mg₂O₂. Ask: done?'),
  dict(show='s10-c2',stage='s10-sim:Mg-O/reduce',note='Strike the common factor 2: MgO.'),
  dict(hide='s10-cB',show='s10-rule',note='Students copy the rule. Misconception: "crisscross always gives the final formula".'),
  dict(hide='s10-c2',show='s10-check',stage='s10-sim:Ca-O/cross',note='Hands up for A, B or C. The animation shows Ca²⁺ and O²⁻ crossed, as in the question.'),
  dict(show='s10-ans',cls={'s10-b':'right','s10-check':'done'},stage='s10-sim:Ca-O/check',note='B is right. A (Ca₂O₂): not reduced. C (CaO₂): 2+ against 4−, not balanced.')]))
# ---------- 11 naming binary compounds
ANI = [('F^−','F<sup>−</sup>','fluoride'),('Cl','Cl<sup>−</sup>','chloride'),('Br','Br<sup>−</sup>','bromide'),('I','I<sup>−</sup>','iodide'),('O','O<sup>2−</sup>','oxide'),('S','S<sup>2−</sup>','sulfide'),('N','N<sup>3−</sup>','nitride')]
rows = ''.join(f'<tr><td>{h}</td><td>{n}</td></tr>' for _,h,n in ANI)
S.append(slide('s11','t-concept cw','Naming binary compounds','Names','Reading §4.2.3',f'''    <div class="sim" id="s11-sim" data-sim="nameBuilder" data-cases="K2S,CaBr2" data-ask="CaBr2" aria-label="Name tiles slide together into one name."></div>
    <div class="col acc">
      <div class="card" id="s11-c0" data-label="two parts"><p class="tag">Two parts</p><p>A name has two parts: the cation first, then the anion.</p></div>
      <table class="tbl compact fill" id="s11-tbl" data-label="anion names" data-zoom="anion names"><thead><tr><th>Anion</th><th>Name</th></tr></thead><tbody>{rows}</tbody></table>
      <div class="card rule reg" id="s11-rule" data-label="rule"><p class="tag">Rule</p><p>Name the cation first, then the anion root plus -ide. Common names omit prefixes because the ion charges determine the ratio.</p></div>
{check('s11','Name CaBr<sub>2</sub>.',['calcium bromine','calcium bromide','calcium dibromide'],ans='B. The anion takes -ide. No prefix is needed.',right='B',
  fb=['Bromine is the element. The ion is bromide.','The anion takes -ide. No prefix is needed.','Common names use no prefix: calcium bromide.'])}
    </div>''',
 'A binary compound has exactly two elements. Common names use no prefixes (di-, tri-) because the charges fix the ratio. IUPAC also accepts a compositional name with prefixes (calcium dibromide), but the common name is calcium bromide.',
 [dict(show='s11-c0',stage='s11-sim:K2S/parts',focus='s11-sim',note='Three tiles: potassium, sulf, -ide. Ask: which part names the cation?'),
  dict(stage='s11-sim:K2S/join',note='One name: potassium sulfide. The formula K₂S has two K, but the name has no "di".'),
  dict(hide='s11-c0',show='s11-tbl',note='Choral reading of the seven anion names. Nitride is N³⁻, not nitrate (slide 15).'),
  dict(hide='s11-tbl',show='s11-rule',cue='check (first ask aloud: MgO? Na₂S?)',note='Students copy the rule. Oral calls before the press: MgO? (magnesium oxide) Na₂S? (sodium sulfide).'),
  dict(show='s11-check',stage='s11-sim:CaBr2/ask',note='Hands up for A, B or C. The animation shows only the formula CaBr₂.'),
  dict(show='s11-ans',cls={'s11-b':'right','s11-check':'done'},stage='s11-sim:CaBr2/join',note='B is right. A (calcium bromine): bromine is the element; the ion is bromide. C (calcium dibromide): IUPAC accepts this compositional name, but the common name uses no prefix; accept it orally and write calcium bromide.')]))
# ---------- 12 the Stock system
S.append(slide('s12','t-concept cw','The Stock system','Names','Reading §4.2.3',f'''    <div class="stack">
      <div class="sim" id="s12-nb" data-sim="nameBuilder" data-cases="FeCl3,FeCl2,AgCl,ZnO" aria-label="Name tiles with a Roman numeral for iron."></div>
      <div class="sim" id="s12-sd" data-sim="stockDetective" data-cases="CuO,Cu2O,FeCl2" data-ask="FeCl2" aria-label="Working back from a copper oxide formula to its name."></div>
    </div>
    <div class="col acc">
      <div class="card" id="s12-c0" data-label="version numbers"><p class="tag">Two irons</p><p>Iron(II) and iron(III) are two different ions, like version numbers.</p></div>
      <div class="card" id="s12-c1" data-label="iron(II)"><p class="tag">Same anion</p><p>A different numeral gives a different formula: FeCl<sub>3</sub> and FeCl<sub>2</sub>.</p></div>
      <div class="card" id="s12-c2" data-label="silver and zinc"><p class="tag">One ion only</p><p>Silver and zinc have one ion each. Their names have no numeral.</p></div>
      <div class="card" id="s12-c3" data-label="copper oxides"><p class="tag">Work back</p><p>Start from the anion's charge. The metal must cancel it.</p></div>
      <div class="card reg" id="s12-c4" data-label="the driving question"><p class="tag">Driving question</p><p>The copper ion's charge determines the formula. The Roman numeral records that charge in the name.</p></div>
{check('s12','Name FeCl<sub>2</sub>.',['iron(I) chloride','iron(II) chloride','iron chloride'],ans='B. Two Cl<sup>−</sup> ions give 2−, so iron is 2+.',right='B',
  fb=['Fe<sup>+</sup> cannot cancel two Cl<sup>−</sup> ions, a total of 2−.','Two Cl<sup>−</sup> ions give 2−, so iron is 2+.','Iron has two ions, so its name needs the numeral.'])}
    </div>''',
 'Stock system (Alfred Stock, 1919): the Roman numeral is the charge of the metal ion, found by working back from the anion. Only metals with more than one common ion take one. Red Cu₂O is copper(I) oxide; black CuO is copper(II) oxide: this answers slide 3.',
 [dict(show='s12-c0',stage='s12-nb:FeCl3/parts',focus='s12-nb',note='Iron(III) chloride, FeCl₃. Ask: what does the numeral count? (nothing: it is the charge).'),
  dict(stage='s12-nb:FeCl3/numeral',label='numeral',note='Fe³⁺ gives the numeral (III). Misconception: "Roman numerals count atoms".'),
  dict(stage='s12-nb:FeCl3/join',label='one name',note='Iron(III) chloride, no space before the parenthesis.'),
  dict(hide='s12-c0',show='s12-c1',stage='s12-nb:FeCl2/join',note='Iron(II) chloride, FeCl₂: same anion, different numeral and formula.'),
  dict(hide='s12-c1',show='s12-c2',stage='s12-nb:AgCl/join',note='Silver chloride: Ag⁺ is the only silver ion.'),
  dict(stage='s12-nb:ZnO/join',label='zinc oxide',note='Zinc oxide (sunscreen): Zn²⁺ only.'),
  dict(hide=['s12-c2','s12-nb'],show=['s12-sd','s12-c3'],stage='s12-sd:CuO/anion',note='Now backward: black CuO. O is oxide, 2−.'),
  dict(stage='s12-sd:CuO/name',label='name CuO',note='One Cu cancels 2−, so Cu²⁺: copper(II) oxide.'),
  dict(stage='s12-sd:Cu2O/anion',label='red Cu₂O',note='Red Cu₂O. The anion is still 2−.'),
  dict(stage='s12-sd:Cu2O/metal',note='Two coppers share 2+, so each is 1+.'),
  dict(hide='s12-c3',show='s12-c4',stage='s12-sd:Cu2O/name',note='Copper(I) oxide. This answers the driving question for the two powders of slide 3.'),
  dict(show='s12-check',stage='s12-sd:FeCl2/ask',note='Hands up for A, B or C. The animation shows only the formula FeCl₂.'),
  dict(show='s12-ans',cls={'s12-b':'right','s12-check':'done'},stage='s12-sd:FeCl2/name',note='B is right. A (iron(I)): the numeral would mean Fe⁺, which cannot cancel 2−. C (iron chloride): iron has two ions, so the name needs the numeral.')]))
# ---------- 13 summary
S.append(slide('s13','t-summary tfill','Formula in 3 steps, name in 2 parts','Summary','Reading §4.2.2 and §4.2.3','''    <div class="flowrow" id="s13-f" data-label="formula steps"><b>Formula</b><span class="fbox">1 Ions</span><span class="arw">→</span><span class="fbox">2 Balance</span><span class="arw">→</span><span class="fbox">3 Write</span></div>
    <div class="flowrow" id="s13-n" data-label="name parts"><b>Name</b><span class="fbox">cation (numeral for Fe, Cu)</span><span class="arw">+</span><span class="fbox">anion with -ide</span></div>
    <table class="tbl compact fill">
      <thead><tr><th>Question</th><th>Answer</th></tr></thead>
      <tbody>
        <tr><td>Name AlCl<sub>3</sub>.</td><td class="slot"><span data-b="s13-a1" data-label="answer 1">aluminum chloride</span></td></tr>
        <tr><td>Name K<sub>2</sub>O.</td><td class="slot"><span data-b="s13-a2" data-label="answer 2">potassium oxide</span></td></tr>
        <tr><td>Write calcium sulfide.</td><td class="slot"><span data-b="s13-a3" data-label="answer 3">CaS</span></td></tr>
        <tr><td>Name FeO.</td><td class="slot"><span data-b="s13-a4" data-label="answer 4">iron(II) oxide</span></td></tr>
      </tbody>
    </table>''',
 'One picture closes period 1. Students copy the two rows as a flow chart. Period 1 ends here.',
 [dict(show='s13-f',note='Formula: ions, balance, write. The four retrieval items are on screen; students start them in notebooks.'),
  dict(show='s13-n',note='Name: cation (numeral only for Fe and Cu), then anion with -ide.'),
  dict(show='s13-a1',note='Al³⁺ is the only aluminum ion: no numeral.'),
  dict(show='s13-a2',note='Two K⁺ for one O²⁻; the name has no prefix.'),
  dict(show='s13-a3',note='Ca²⁺ and S²⁻: 1 : 1.'),
  dict(show='s13-a4',note='O is 2−, so Fe is 2+: iron(II) oxide. End of period 1.')]))
# ---------- 14 warm-up
S.append(slide('s14','t-turn two','Warm-up','Warm-up, period 2','Reading §4.2.1 to §4.2.3','''    <div class="qrow">
      <div class="card"><p>Answer in your notebook. Then check each answer.</p></div>
      <div class="timer"></div>
    </div>
    <table class="tbl fill">
      <thead><tr><th>Question</th><th>Answer</th></tr></thead>
      <tbody>
        <tr><td>What charge does a group 16 ion have?</td><td class="slot"><span data-b="s14-a1" data-label="answer 1">charge 2−</span></td></tr>
        <tr><td>Write magnesium chloride.</td><td class="slot"><span data-b="s14-a2" data-label="answer 2">MgCl<sub>2</sub></span></td></tr>
        <tr><td>What does (III) mean in iron(III)?</td><td class="slot"><span data-b="s14-a3" data-label="answer 3">the iron ion has a charge of 3+</span></td></tr>
      </tbody>
    </table>''',
 'Period 2 starts here. The three questions retrieve 4.2.1, 4.2.2 and 4.2.3.',
 [dict(note='Students write while you take attendance.'),
  dict(timer=90,label='timer 90 s',note='Ninety seconds.'),
  dict(show='s14-a1',note='Group 16 gains two electrons: 2−.'),
  dict(show='s14-a2',note='Mg²⁺ needs two Cl⁻: MgCl₂.'),
  dict(show='s14-a3',note='The numeral is the charge, not a count.')]))
# ---------- 15 polyatomic ions
PI = [('NH4','ammonium','NH<sub>4</sub><sup>+</sup>'),('OH','hydroxide','OH<sup>−</sup>'),('NO3','nitrate','NO<sub>3</sub><sup>−</sup>'),('CO3','carbonate','CO<sub>3</sub><sup>2−</sup>'),('SO4','sulfate','SO<sub>4</sub><sup>2−</sup>'),('PO4','phosphate','PO<sub>4</sub><sup>3−</sup>')]
prow = ''.join(f'<div class="pchip slot"><span data-b="s15-r{k+1}">{n}</span><span class="pf" data-b="s15-r{k+1}">{f}</span></div>' for k,(_,n,f) in enumerate(PI))
S.append(slide('s15','t-concept cw','Polyatomic ions','Polyatomic ions','Reading §4.2.4',f'''    <div class="leftcol"><div class="sim" id="s15-sim" data-sim="polyIons" aria-label="A polyatomic ion turning slowly in 3D."></div><p class="simcap" id="s15-cap" data-label="colors">Atom colors show the element, not the charge.</p></div>
    <div class="col acc">
      <div class="card" id="s15-c0" data-label="squad"><p class="tag">A squad</p><p>A polyatomic ion is a group of atoms with one shared charge.</p></div>
      <div class="card" id="s15-A" data-zoom="six ions"><p class="tag">Six polyatomic ions</p><div class="pgrid">{prow}</div></div>
      <div class="card" id="s15-c1" data-label="pattern"><p class="tag">Pattern</p><p>An -ate ion contains oxygen. Nitrate is not nitride. Sulfate is not sulfide.</p></div>
      <div class="card" id="s15-c2" data-label="memory card"><p class="tag">Memory card</p><p class="mem">Nick the Camel ate Supper in Phoenix.</p><p class="small">Consonants count O atoms. Vowels give the charge.</p></div>
{check('s15','Sulfate, SO<sub>4</sub><sup>2−</sup>: which statement is right?',['Each O is an oxide ion.','It is the same as sulfide.','The whole group carries 2−.'],ans='C. The charge belongs to the whole group.',right='C',
  fb=['The atoms share electrons. There are no O<sup>2−</sup> ions inside.','Sulfide is S<sup>2−</sup>, one atom. Sulfate has one S and four O.','The charge belongs to the whole group.'])}
    </div>''',
 'Six core polyatomic ions. Memory sentence: Nick = NO₃⁻ (3 consonants N, c, k; 1 vowel), Camel = CO₃²⁻ (3 consonants, 2 vowels), Supper = SO₄²⁻ (4 consonants, 2 vowels), Phoenix = PO₄³⁻ (4 consonants, 3 vowels). Ammonium NH₄⁺ is the only common positive one; hydroxide OH⁻.',
 [dict(show=['s15-A','s15-c0','s15-r1','s15-cap'],stage='s15-sim:NH4',note='Ammonium, NH₄⁺, the only positive one; the badge is on the whole group. Atom colors are CPK colors and show the element: H white, C dark gray, N blue, O red, S yellow, P orange. They are not the ion colors.'),
  dict(show='s15-r2',stage='s15-sim:OH',label='next ion',note='Hydroxide, OH⁻: two atoms, one charge.'),
  dict(show='s15-r3',stage='s15-sim:NO3',label='next ion',note='Nitrate, NO₃⁻: flat triangle. Watch it turn edge-on.'),
  dict(show='s15-r4',stage='s15-sim:CO3',label='next ion',note='Carbonate, CO₃²⁻: same shape as nitrate, different charge. Limestone is calcium carbonate.'),
  dict(show='s15-r5',stage='s15-sim:SO4',label='next ion',note='Sulfate, SO₄²⁻: a tetrahedron, not flat.'),
  dict(show='s15-r6',stage='s15-sim:PO4',label='next ion',note='Phosphate, PO₄³⁻: tetrahedron like sulfate, charge 3−.'),
  dict(show='s15-c1',note='The -ate ending signals oxygen. Misconception: "nitrate = nitride".'),
  dict(hide='s15-c0',show='s15-c2',note='Read the sentence together. Count with students: Nick has N, c, k (3 O) and i (1−).'),
  dict(hide=['s15-c1','s15-c2','s15-cap'],show='s15-check',stage='s15-sim:SO4',note='Hands up for A, B or C. The model turns back to sulfate, the ion in the question.'),
  dict(show='s15-ans',cls={'s15-c':'right','s15-check':'done'},note='C is right. A (each O an oxide ion): the atoms are joined by covalent bonds; there are no O²⁻ ions inside. B (same as sulfide): sulfide is S²⁻, a single atom.')]))
# ---------- 16 parentheses
S.append(slide('s16','t-concept','Parentheses','Polyatomic ions','Reading §4.2.4',f'''    <div class="stack">
      <div class="sim" id="s16-pb" data-sim="parenBus" aria-label="One hydroxide squad, then two squads in parentheses."></div>
      <div class="sim" id="s16-cb" data-sim="chargeBlocks" data-pairs="NH4-SO4,Na-NO3,Mg-NO3" aria-label="Ion tiles with polyatomic ions."></div>
    </div>
    <div class="col acc">
      <div class="card" id="s16-c0" data-label="squad"><p class="tag">Squad</p><p>OH<sup>−</sup> is one squad: one O and one H with one charge.</p></div>
      <div class="card" id="s16-c1" data-label="two squads"><p class="tag">Two squads</p><p>Two ammonium squads ride in parentheses. One sulfate squad needs none.</p></div>
      <div class="card" id="s16-c2" data-label="one squad"><p class="tag">One squad</p><p>One nitrate squad, so no parentheses.</p></div>
      <div class="card rule reg" id="s16-rule" data-label="rule"><p class="tag">Rule</p><p>Treat a polyatomic ion as one unit. Never change the subscripts inside a polyatomic ion.</p></div>
{check('s16','Write the formula of magnesium nitrate.',['MgNO<sub>3</sub>','Mg(NO<sub>3</sub>)<sub>2</sub>','MgN<sub>2</sub>O<sub>6</sub>'],ans='B. Mg<sup>2+</sup> needs two NO<sub>3</sub><sup>−</sup> squads.',right='B',
  fb=['One NO<sub>3</sub><sup>−</sup> gives 1−. That cannot cancel 2+.','Mg<sup>2+</sup> needs two NO<sub>3</sub><sup>−</sup> squads.','The squads were broken up. Keep each NO<sub>3</sub><sup>−</sup> whole.'])}
    </div>''',
 'Reading §4.2.4 Key idea: treat a polyatomic ion as one unit; put it in parentheses when the formula needs more than one of it; never change the subscripts inside it (SO₃²⁻ is a different ion, sulfite).',
 [dict(show='s16-c0',stage='s16-pb:one',focus='s16-pb',note='NaOH: one squad, no parentheses.'),
  dict(stage='s16-pb:two',note='Ca²⁺ needs two OH⁻ squads: they ride in parentheses, the 2 outside: Ca(OH)₂.'),
  dict(stage='s16-pb:wrong',note='CaOH₂ would mean one O and two H. Misconception: "parentheses change an ion".'),
  dict(hide=['s16-c0','s16-pb'],show=['s16-cb','s16-c1'],stage='s16-cb:NH4-SO4/balance',note='Two NH₄⁺ (2+) and one SO₄²⁻ (2−).'),
  dict(stage='s16-cb:NH4-SO4/formula',note='(NH₄)₂SO₄, the lawn food of slide 2.'),
  dict(hide='s16-c1',show='s16-c2',stage='s16-cb:Na-NO3/formula',label='sodium nitrate',note='Na⁺ and NO₃⁻: 1 : 1, NaNO₃, no parentheses.'),
  dict(show='s16-rule',note='Students copy the rule.'),
  dict(hide='s16-c2',show='s16-check',stage='s16-cb:Mg-NO3/ions',note='Hands up for A, B or C. The tiles show Mg²⁺ and one NO₃⁻: not balanced yet.'),
  dict(show='s16-ans',cls={'s16-b':'right','s16-check':'done'},stage='s16-cb:Mg-NO3/formula',note='B is right. A (MgNO₃): 2+ against 1−, not balanced. C (MgN₂O₆): the squads were broken up; the numbers inside a squad never change.')]))
# ---------- 17 the two-way road
S.append(slide('s17','t-example cb','The two-way road','Translating','Reading §4.2.5',f'''    <div class="stack">
      <div class="sim" id="s17-cb" data-sim="chargeBlocks" data-pairs="Al-SO4" aria-label="Ion tiles for aluminum sulfate."></div>
      <div class="sim" id="s17-sd" data-sim="stockDetective" data-cases="Cu2S,Fe2SO43" data-ask="Fe2SO43" aria-label="Working back from Cu2S to its name."></div>
    </div>
    <div class="col acc">
      <div class="card stepscard k1" id="s17-A"><p class="tag">Name → formula: aluminum sulfate</p>
        <ol class="steps">
          <li><span class="k">Ions</span><span id="s17-a1">Al<sup>3+</sup> and SO<sub>4</sub><sup>2−</sup></span></li>
          <li><span class="k">Balance</span><span id="s17-a2" data-label="balance">two Al<sup>3+</sup>: 2 × 3+ = 6+<br>three SO<sub>4</sub><sup>2−</sup>: 3 × 2− = 6−</span></li>
          <li><span class="k">Write</span><span class="formula" id="s17-a3" data-label="write">Al<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub></span></li>
        </ol>
      </div>
      <div class="card" id="s17-B" data-label="formula to name"><p class="tag">Formula → name: Cu<sub>2</sub>S</p><p>Work back: start from the anion. The copper ions must cancel its charge.</p></div>
      <div class="card" id="s17-both" data-label="check both ways"><p class="tag">Check both ways</p><p>Name your formula again. Write your name again. Both must agree.</p></div>
{check('s17','Name Fe<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub>.',['iron(II) sulfate','iron(III) sulfate','iron sulfide'],ans='B. Three SO<sub>4</sub><sup>2−</sup> give 6−. Two Fe share 6+, so each is 3+.',right='B',
  fb=['Two Fe<sup>2+</sup> give 4+ against 6−.','Three SO<sub>4</sub><sup>2−</sup> give 6−. Two Fe share 6+, so each is 3+.','Sulfate is not sulfide, and iron needs its numeral.'])}
    </div>''',
 'Reading §4.2.5 Key idea: name to formula: ions, balance, write. Formula to name: find the anion charge, work back to the metal charge if it needs a numeral, then name both ions.',
 [dict(show=['s17-A','s17-a1'],stage='s17-cb:Al-SO4/ions',focus='s17-cb',note='Name to formula. Identify both ions first; sulfate is a squad.'),
  dict(show='s17-a2',stage='s17-cb:Al-SO4/balance',note='Least common multiple 6: two Al³⁺ and three SO₄²⁻.'),
  dict(show='s17-a3',stage='s17-cb:Al-SO4/formula',note='Al₂(SO₄)₃: parentheses because sulfate repeats.'),
  dict(hide='s17-cb',show=['s17-B','s17-sd'],stage='s17-sd:Cu2S/anion',label='formula to name',note='Formula to name: Cu₂S. Start with the anion: sulfide, 2−.'),
  dict(stage='s17-sd:Cu2S/metal',label='the metal',note='Two copper ions share 2+: each is Cu⁺.'),
  dict(stage='s17-sd:Cu2S/name',label='the name',note='Copper(I) sulfide. Misconception: "the 2 in Cu₂S means copper(II)".'),
  dict(hide='s17-A',show='s17-both',note='Check both ways: write the formula from your name; it must match.'),
  dict(hide='s17-B',show='s17-check',stage='s17-sd:Fe2SO43/ask',note='Hands up for A, B or C. The animation shows only the formula Fe₂(SO₄)₃.'),
  dict(show='s17-ans',cls={'s17-b':'right','s17-check':'done'},stage='s17-sd:Fe2SO43/name',note='B is right. A (iron(II)): would give 4+ against 6−. C (iron sulfide): sulfate is not sulfide, and iron needs its numeral.')]))
# ---------- 18 six compounds
SIX = [('sodium fluoride','toothpaste','NaF',1),('calcium carbonate','antacid','CaCO<sub>3</sub>',1),('ammonium sulfate','lawn food','(NH<sub>4</sub>)<sub>2</sub>SO<sub>4</sub>',1),
       ('MgBr<sub>2</sub>','','magnesium bromide',0),('FeO','','iron(II) oxide',0),('Zn(OH)<sub>2</sub>','','zinc hydroxide',0)]
srow = ''.join(f'<tr><td>{g}{" <span class=\"why\">("+p+")</span>" if p else ""}</td><td>{"formula" if f else "name"}</td><td class="slot"><span data-b="s18-a{k+1}" data-label="answer {k+1}">{a}</span></td></tr>' for k,(g,p,a,f) in enumerate(SIX))
S.append(slide('s18','t-turn two','You do: six compounds','Translating','Reading §4.2.5',f'''    <div class="qrow">
      <div class="card"><p>Write each formula or name. The first three are the shelf labels.</p></div>
      <div class="timer"></div>
    </div>
    <table class="tbl compact fill">
      <thead><tr><th>Given</th><th>Write</th><th>Answer</th></tr></thead>
      <tbody>{srow}</tbody>
    </table>''',
 'You do. The first three names come from the shelf on slide 2. Circulate during the timer; look for missing parentheses and for missing numerals.',
 [dict(note='Read the task. Students work alone in notebooks.'),
  dict(timer=180,label='timer 3 min',note='Three minutes. Early finishers check both ways.'),
  dict(show='s18-a1',note='Na⁺ and F⁻: NaF.'),
  dict(show='s18-a2',note='Ca²⁺ and CO₃²⁻: CaCO₃, one squad, no parentheses.'),
  dict(show='s18-a3',note='NH₄⁺ and SO₄²⁻: (NH₄)₂SO₄.'),
  dict(show='s18-a4',note='Magnesium bromide: no prefix.'),
  dict(show='s18-a5',note='O is 2−, so Fe is 2+: iron(II) oxide.'),
  dict(show='s18-a6',note='Zinc hydroxide: zinc needs no numeral.')]))
# ---------- 19 spot the error
ERR = [('NaSO<sub>4</sub>','Na<sub>2</sub>SO<sub>4</sub>','charges must total zero',1),('Mg<sub>2</sub>O<sub>2</sub>','MgO','lowest ratio',1),('CaOH<sub>2</sub>','Ca(OH)<sub>2</sub>','keep the squad',1),
       ('Cu<sub>2</sub>O: copper(II) oxide','copper(I) oxide','each Cu is 1+',0),('FeCl<sub>3</sub>: iron chloride','iron(III) chloride','iron needs its numeral',0),('NaNO<sub>3</sub>: sodium nitride','sodium nitrate','-ate has oxygen',0)]
erow = ''.join(f'<tr><td>{w}</td><td class="slot"><span data-b="s19-a{k+1}" data-label="fix {k+1}">{fx}</span> <span class="why" data-b="s19-a{k+1}">{why}</span></td></tr>' for k,(w,fx,why,f) in enumerate(ERR))
S.append(slide('s19','t-turn two','Spot the error','Translating','Reading §4.2.5',f'''    <div class="card"><p>Each item has one error. Call out the fix.</p></div>
    <table class="tbl compact fill">
      <thead><tr><th>Wrong</th><th>Fix</th></tr></thead>
      <tbody>{erow}</tbody>
    </table>''',
 'Six errors from the reading’s Find the error mission. Ask a student to name the error before each press.',
 [dict(note='Students study the six items with a partner for 30 seconds.'),
  dict(show='s19-a1',note='Na⁺ and SO₄²⁻ need two Na⁺: Na₂SO₄.'),
  dict(show='s19-a2',note='Reduce 2 : 2 to MgO.'),
  dict(show='s19-a3',note='Two OH⁻ squads ride in parentheses.'),
  dict(show='s19-a4',note='O is 2−, two Cu share it: each Cu is 1+.'),
  dict(show='s19-a5',note='Iron has two ions; three Cl⁻ mean Fe³⁺.'),
  dict(show='s19-a6',note='NO₃⁻ is nitrate; nitride is N³⁻.')]))
# ---------- 20 checkpoint routine
steps = [('Think · 30 s','alone, no talking'),('Talk · 60 s','tell your partner, then listen'),('Write · 90 s','use the sentence frames'),('Self-check','tick each success criterion'),('Compare','read the sample and fix one line')]
sr = '\n'.join(f'        <li id="s20-s{k+1}"><b class="lbl">{a}</b><span>{b}</span></li>' for k,(a,b) in enumerate(steps))
S.append(slide('s20','t-routine','Checkpoint routine','Checkpoint','Objectives 4.2.2 to 4.2.4',f'''    <div class="card prompt"><p>Each checkpoint uses the same five steps.</p></div>
    {rail('s20')}
    <ol class="steprows">
{sr}
    </ol>''',
 'Routine for slides 21 to 23: think 30 s, talk 60 s, write 90 s, self-check 30 s, compare 45 s.',
 [dict(note='Explain that the routine repeats for each question.')]+
 [dict(cls=dict([(f's20-r{j+1}','done') for j in range(k)]+[(f's20-s{j+1}','') for j in range(k)]+[(f's20-r{k+1}','now'),(f's20-s{k+1}','now')]),label=['think','talk','write','self-check','compare'][k],note=n) for k,n in enumerate(['Think: silent, no pencils.','Talk: partner A first, then partner B.','Write: the sentence frames and word bank stay on screen.','Self-check: tick each criterion you met.','Compare: read the sample answer and fix one line.'])]))
# ---------- 21 to 23 checkpoints
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
        <div class="card phase" id="{p}-check" data-label="self-check"><p class="tag">Self-check: did you write…</p><ul class="crit">{cr}</ul></div>
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
    return slide(sid,'t-routine',title,title,ref,body,'Routine: think 30 s, talk 60 s, write 90 s, self-check 30 s, compare 45 s. The question stays on screen on every frame.',fr)
S.append(checkpoint('s21','Checkpoint 1','Objective 4.2.2',
  'Write the formula of aluminum oxide from Al<sup>3+</sup> and O<sup>2−</sup>. Explain why the ratio is correct.',
  'Read the question. Which ions do you have?',
  ['The formula is <span class="gap"></span>.','Two Al<sup>3+</sup> ions give a charge of <span class="gap"></span>, and three O<sup>2−</sup> ions give <span class="gap"></span>.','The ratio is right because <span class="gap"></span>.'],
  ['6+ and 6−','total charge','zero','lowest ratio'],
  ['the formula Al<sub>2</sub>O<sub>3</sub>?','the totals 6+ and 6−?','zero total charge?'],
  'The formula is Al<sub>2</sub>O<sub>3</sub>. Two aluminum ions provide 6+, and three oxide ions provide 6−. The total charge equals zero.',
  ['Read the prompt aloud. Ask: which numbers will you balance? (3+ and 2−).','Compare with the sample. Reading §4.2.2: the total charge is zero, in the lowest whole-number ratio.'],
  '"Al₃O₂" (counts swapped) and "AlO" (charges ignored).'))
S.append(checkpoint('s22','Checkpoint 2','Objective 4.2.3',
  'Iron forms two different chlorides, FeCl<sub>2</sub> and FeCl<sub>3</sub>. Name both compounds and explain how you determined each Roman numeral.',
  'Read the question. What is the anion?',
  ['FeCl<sub>2</sub> is <span class="gap"></span> because <span class="gap"></span>.','FeCl<sub>3</sub> is <span class="gap"></span> because <span class="gap"></span>.'],
  ['chloride is 1−','total charge','numeral = charge'],
  ['both names with numerals?','each Cl<sup>−</sup> is 1−?','the numeral is the iron charge?'],
  'FeCl<sub>2</sub> is iron(II) chloride. FeCl<sub>3</sub> is iron(III) chloride. Each chloride ion is 1−, so iron balances them.',
  ['Read the prompt aloud. Both compounds have the same anion.','Compare with the sample. Reading §4.2.3: the numeral is the charge of the metal ion, found from the anion.'],
  '"the numeral counts the chlorines" (it gives the charge; here the two agree only because Cl⁻ is 1−).'))
S.append(checkpoint('s23','Checkpoint 3','Objective 4.2.4',
  'Some antacids contain aluminum hydroxide. Write its formula. Explain why it needs parentheses but NaOH does not.',
  'Read the question. How many hydroxide ions does aluminum need?',
  ['The formula is <span class="gap"></span>.','It needs <span class="gap"></span> OH<sup>−</sup> because <span class="gap"></span>.','NaOH needs no parentheses because <span class="gap"></span>.'],
  ['squad','one charge','three','parentheses'],
  ['Al(OH)<sub>3</sub> with parentheses?','three OH<sup>−</sup> balance 3+?','one OH<sup>−</sup> needs none?'],
  'The formula is Al(OH)<sub>3</sub>. Aluminum needs three hydroxide ions, so they go in parentheses. NaOH has one.',
  ['Read the prompt aloud. Aluminum hydroxide neutralizes stomach acid in some antacids.','Compare with the sample. Reading §4.2.4: parentheses only when a polyatomic ion repeats.'],
  '"AlOH₃" (squad broken) and "Al(OH)" (charges not balanced).'))
# ---------- 24 predictions and exit ticket
def pa(p, n, q, right, reason, lab):
    return f'''      <div class="card check done" id="{p}" data-label="{lab}" data-mode="none"><p class="tag">Question {n}</p><p class="q">{q}</p><ol class="opts" data-lay="row"><li class="opt right"><b>A</b><span>{right}</span></li></ol><p class="reason">{reason}</p></div>'''
S.append(slide('s24','t-routine t-exit','Predictions and exit ticket','Exit ticket','Objectives 4.2.2 and 4.2.3',f'''    <div class="stack">
      <div class="phaseA" id="s24-A" data-label="answers">
        <div class="stack">
{pa('s24-p1',1,'Mg<sup>2+</sup> with O<sup>2−</sup> gives…','MgO','The charges 2+ and 2− cancel in a 1 : 1 ratio.','answer 1')}
{pa('s24-p2',2,'The III in iron(III) chloride means…','a charge of 3+','The numeral is the charge of the iron ion.','answer 2')}
{pa('s24-p3',3,'Calcium hydroxide is…','Ca(OH)<sub>2</sub>','Two OH<sup>−</sup> squads ride in parentheses.','answer 3')}
        </div>
        <p class="handsup">Hands up if you predicted this.</p>
      </div>
      <div class="phaseB" id="s24-B" data-label="exit ticket">
        <div class="card prompt reg dq"><p>{DQ}</p></div>
        <ol class="rail"><li id="s24-r1">Claim</li><li id="s24-r2">Evidence</li><li id="s24-r3">Reasoning</li><li id="s24-r4">Self-check</li><li id="s24-r5">Sample</li></ol>
        <div class="rt-main">
          <div class="acc">
            <div class="card phase" id="s24-fr" data-label="claim"><p class="tag">Write</p><ol class="frames">
              <li id="s24-f1">Claim: The charges decide <span class="gap"></span>.</li>
              <li id="s24-f2" data-label="evidence">Evidence: Cu<sub>2</sub>O and CuO both contain <span class="gap"></span>, but <span class="gap"></span>.</li>
              <li id="s24-f3" data-label="reasoning">Reasoning: This works because the total charge <span class="gap"></span>.</li>
            </ol>
            <p class="bank"><b>Word bank:</b> <span>zero</span> <span>ratio</span> <span>numeral</span> <span>copper(I)</span> <span>copper(II)</span></p></div>
            <div class="card" id="s24-check" data-label="self-check"><p class="tag">Self-check: did you write…</p><ul class="crit"><li>a claim about formula and name?</li><li>the two copper oxides as evidence?</li><li>zero total charge in the reasoning?</li></ul></div>
            <div class="card reg" id="s24-sample" data-label="sample answer"><p class="tag">Sample answer</p><p>The total charge must be zero, so ion charges determine the ratio. Copper(I) gives Cu<sub>2</sub>O; copper(II) gives CuO.</p></div>
          </div>
          <div class="timer"></div>
        </div>
      </div>
    </div>''',
 'Predictions from slide 4 come back first; students check their letters. Then the CER exit ticket on the driving question, with the two copper oxides as evidence. The question stays on screen while the sample shows. Collect the exit tickets.',
 [dict(show=['s24-A','s24-p1'],note='Answer 1: MgO. Hands up if you predicted A. Compare with the counts from slide 4.'),
  dict(hide='s24-p1',show='s24-p2',note='Answer 2: the charge 3+. Ask a student who changed their mind to say why.'),
  dict(hide='s24-p2',show='s24-p3',note='Answer 3: Ca(OH)₂. CaOH₂ was the common wrong idea.'),
  dict(hide='s24-A',show=['s24-B','s24-fr','s24-f1'],cls={'s24-r1':'now'},note='Exit ticket. Claim first: the charges decide both the formula and the name.'),
  dict(show='s24-f2',cls={'s24-r1':'done','s24-r2':'now'},note='Evidence: the two copper oxides of slide 3.'),
  dict(show='s24-f3',cls={'s24-r2':'done','s24-r3':'now'},timer=180,label='write 3 min',note='Reasoning: zero total charge sets the ratio; the numeral records the charge. Three minutes of writing.'),
  dict(show='s24-check',cls={'s24-r3':'done','s24-r4':'now'},note='Self-check with the three criteria.'),
  dict(show='s24-sample',cls={'s24-r4':'done','s24-r5':'now'},note='Compare with the sample. Collect the tickets.')]))
# ---------- 25 rate your learning
T = [('4.2.1',"predict an ion's charge from its group.",'slides 6 and 7'),('4.2.2','write a formula with zero total charge.','slides 8 to 10'),('4.2.3','name compounds, with numerals for Fe and Cu.','slides 11 and 12'),('4.2.4','use polyatomic ions and parentheses.','slides 15 and 16'),('4.2.5','go from name to formula and back.','slides 17 to 19')]
rt = '\n'.join(f'        <li id="s25-t{k+1}"><span><b class="mono lbl">{a}</b> {b}</span><span class="rev">Review: {c}</span></li>' for k,(a,b,c) in enumerate(T))
S.append(slide('s25','t-routine','Rate your learning','Reflect','All objectives',f'''    <div class="scale lbl"><span>1 finger: not yet</span><span>2 fingers: almost</span><span>3 fingers: I can teach it</span></div>
    <p class="tag">I can…</p>
    <ol class="rate">
{rt}
    </ol>''',
 'Fingers 1 to 3 for each target. Students below 3 revisit the slides named on the right.',
 [dict(note='Explain the scale: 1 not yet, 2 almost, 3 I can teach it.')]+
 [dict(cls=dict([(f's25-t{j+1}','') for j in range(k)]+[(f's25-t{k+1}','now')]),label=f'target {k+1}',note=f'Fingers for target 4.2.{k+1}. Note who shows 1 and point to the review slides.') for k in range(5)]))
# ---------- 26 next
S.append(slide('s26','t-summary tnext','Next','Next','Missions 4.2 and Lesson 4.3','''    <div class="mrow">
      <div class="mission card"><svg viewBox="0 0 100 100" role="img" aria-label="Icon: a name tag"><use href="#ic-tag"/></svg><b>Name the compound</b><span>six compounds</span></div>
      <div class="mission card"><svg viewBox="0 0 100 100" role="img" aria-label="Icon: ion tiles"><use href="#ic-tiles"/></svg><b>Build the formula</b><span>six formulas from tiles</span></div>
      <div class="mission card"><svg viewBox="0 0 100 100" role="img" aria-label="Icon: a magnifier over an error"><use href="#ic-magnify"/></svg><b>Find the error</b><span>six items to fix</span></div>
    </div>
    <div class="card"><p class="big">Next lesson: two nonmetals get names with prefixes. One example is carbon dioxide.</p></div>''',
 'Missions for Lesson 4.2: Name the compound, Build the formula, Find the error. Lesson 4.3 adds prefix names for compounds of two nonmetals and their Lewis structures.',
 [dict(note='Point to the three missions. Preview Lesson 4.3: two nonmetals share electrons, so their names count atoms with prefixes.')]))

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
open(OUT, 'w').write(html)
print('slides:', len(S))
