# Generates slides.html: the 25 slides of Lesson 4.1 (plan section 5). Run by build.py 4 1.
import json, os, re, html as H
OUT = os.path.join(os.path.dirname(__file__), 'slides.html')

def js(v): return json.dumps(v, ensure_ascii=False)
TIMES = {
 's01':[0.5], 's02':[0.5,0.75,0.5,0.75,0.75,0.75], 's03':[0.75,0.5,0.75,0.5,1.5], 's04':[0.75,0.75,1], 's05':[1,1.5,0.5],
 's06':[1,0.75,1.25,1,0.5,0.5], 's07':[0.5,0.5,1,1,0.5,0.5], 's08':[0.25,0.75,1,1,0.5,0.5], 's09':[0.5,1,0.5,0.75,0.5,0.75,0.5,0.5],
 's10':[0.75,0.25,0.5,0.75,0.25,0.25,0.5,0.75,0.5,0.5], 's11':[0.5,0.25,0.25,0.25,0.25,0.25,0.5,0.25,0.5], 's12':[1,0.5,0.5,0.5,0.5,0.5,0.5], 's13':[0.5,2,0.5],
 's14':[0.5,1.5,0.25,0.25,0.5], 's15':[0.25,0.5,0.25,0.5,0.5,1,0.5,0.5], 's16':[0.25,0.25,0.25,0.5,0.5,0.25,1,0.5,0.5], 's17':[0.5,0.25,0.25,0.5,0.5,0.5,0.5],
 's18':[0.25,0.25,0.5,0.5,0.25,0.5,0.5,0.75,0.5,0.5,0.5], 's19':[0.5,3,0.5,0.5,0.5], 's20':[0.5,0.1,0.1,0.1,0.1,0.1],
 's21':[0.25,0.5,1,1.5,0.5,0.75], 's22':[0.25,0.5,1,1.5,0.5,0.75], 's23':[0.25,0.5,1,1.5,0.5,0.75],
 's24':[0.5,0.5,1,0.5,0.5,3,0.5,0.5], 's25':[0.25,0.25,0.25,0.25,0.25,0.25]}
def frames(sid, fr):
    if sid in TIMES:
        assert len(TIMES[sid]) == len(fr), (sid, len(TIMES[sid]), len(fr))
        for f, t in zip(fr, TIMES[sid]): f['t'] = t
    rows = []
    for f in fr:
        parts = []
        for k in ['show','hide','stage','cls','timer','focus','label','cue','t','note']:
            if k in f: parts.append(f"{k}:{js(f[k])}")
        rows.append('{' + ','.join(parts) + '}')
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
    # options: one row when every option is two words or fewer, else stacked; the runtime stacks a row that does not fit
    return 'col' if (col if col is not None else max(nwords(o) for o in opts) > 2) else 'row'
def optli(p, opts, right, fb):
    out = ''
    for l, t, f in zip('ABC', opts, fb or [None] * 3):
        g = f' data-ok="{1 if l == right else 0}" data-fb="{H.escape(f, quote=True)}"' if f is not None else ''
        out += f'<li class="opt" id="{p}-{l.lower()}"{g}><b>{l}</b><span>{t}</span></li>'
    return out
def check(p, q, opts, label='check', col=None, tag='Check', ans='', right=None, fb=None, pre=''):
    # fb: one feedback line per option (the right option gets its reason); a mouse click shows it under the options
    L = lay(opts, col)
    return f'''      <div class="card check" id="{p}-check" data-label="{label}">
        <p class="tag">{tag}</p>{pre}
        <p class="q">{q}</p>
        <ol class="opts{' col1' if L == 'col' else ''}" data-lay="{L}">{optli(p, opts, right, fb)}</ol>
        <div class="af"><p class="ans" id="{p}-ans" data-label="answer">{ans}</p><p class="fb" aria-live="polite"></p></div>
      </div>'''
def en(*pairs, label='Electronegativity (pull on electrons)'):
    # electronegativity values with their meaning: a label line, then one chip per element on one line
    chips = ''.join(f'<span class="chip"><b>{a}</b><span class="mono">{v}</span></span>' for a, v in pairs)
    return f'<span class="enrow"><span class="enl lbl">{label}</span><span class="chips">{chips}</span></span>'
def use(i, label, cls=''):
    return f'<svg class="{cls}" viewBox="0 0 100 100" role="img" aria-label="{label}"><use href="#{i}"/></svg>'

SPRITE = '''<svg class="sprite" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden"><defs>
<symbol id="ic-ionic" viewBox="0 0 100 100"><circle cx="30" cy="30" r="18" class="f-cat"/><circle cx="70" cy="30" r="22" class="f-an"/><circle cx="30" cy="70" r="22" class="f-an"/><circle cx="70" cy="70" r="18" class="f-cat"/><path d="M22 30h16M30 22v16M62 30h16M22 70h16M62 70h16M70 62v16" class="k-on" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-covalent" viewBox="0 0 100 100"><circle cx="34" cy="50" r="28" class="f-nm k-nm" fill-opacity=".28" stroke-width="3"/><circle cx="66" cy="50" r="28" class="f-nm k-nm" fill-opacity=".28" stroke-width="3"/><circle cx="50" cy="40" r="7" class="f-e"/><circle cx="50" cy="60" r="7" class="f-e"/></symbol>
<symbol id="ic-metallic" viewBox="0 0 100 100"><rect x="4" y="12" width="92" height="76" rx="14" class="f-sea"/><circle cx="30" cy="34" r="14" class="f-metal"/><circle cx="70" cy="34" r="14" class="f-metal"/><circle cx="30" cy="68" r="14" class="f-metal"/><circle cx="70" cy="68" r="14" class="f-metal"/><path d="M24 34h12M30 28v12M64 34h12M70 28v12M24 68h12M30 62v12M64 68h12M70 62v12" class="k-on" stroke-width="4" stroke-linecap="round"/><g class="f-e"><circle cx="50" cy="51" r="8"/><circle cx="12" cy="51" r="8"/><circle cx="88" cy="51" r="8"/><circle cx="50" cy="16" r="8"/><circle cx="50" cy="86" r="8"/></g><path d="M46 51h8M8 51h8M84 51h8M46 16h8M46 86h8" class="k-on" stroke-width="3" stroke-linecap="round"/></symbol>
<symbol id="ic-wire" viewBox="0 0 200 100"><path d="M6 70C40 70 52 50 92 50" fill="none" stroke="#3a3f44" stroke-width="26" stroke-linecap="round"/><path d="M6 70C40 70 52 50 92 50" fill="none" stroke="#6b737a" stroke-width="8" stroke-linecap="round" opacity=".6"/><rect x="86" y="36" width="14" height="28" rx="4" fill="#2b2f33"/><g fill="none" stroke-linecap="round"><path d="M98 44c30-2 52-14 90-26M98 48c34 0 58-6 92-8M98 52c34 2 58 8 92 12M98 56c30 4 52 14 90 28" stroke="#9a4f1f" stroke-width="7"/><path d="M98 44c30-2 52-14 90-26M98 48c34 0 58-6 92-8M98 52c34 2 58 8 92 12M98 56c30 4 52 14 90 28" stroke="#e8955a" stroke-width="3"/></g><circle cx="150" cy="40" r="3" fill="#fff2d8"/><circle cx="168" cy="60" r="2.5" fill="#fff2d8"/></symbol>
<symbol id="ic-en" viewBox="0 0 100 100"><path d="M8 56h84" class="k-rope" stroke-width="7" stroke-linecap="round"/><circle cx="66" cy="49" r="6" class="f-e"/><circle cx="66" cy="63" r="6" class="f-e"/><path d="M40 26h44m-12-10 12 10-12 10" fill="none" class="k-acc" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="ic-partial" viewBox="0 0 100 100"><circle cx="34" cy="58" r="24" class="f-dp"/><circle cx="66" cy="58" r="28" class="f-dm"/><path d="M22 18h16M30 10v16M62 18h16" class="k-ink" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-crystal" viewBox="0 0 100 100"><rect x="6" y="6" width="88" height="88" rx="14" class="f-card2 k-acc" stroke-width="3"/><circle cx="30" cy="30" r="12" class="f-cat"/><circle cx="70" cy="30" r="15" class="f-an"/><circle cx="30" cy="70" r="15" class="f-an"/><circle cx="70" cy="70" r="12" class="f-cat"/></symbol>
<symbol id="ic-molecule" viewBox="0 0 100 100"><path d="M50 46 22 70M50 46l28 24" class="k-ink" stroke-width="7" stroke-linecap="round"/><circle cx="50" cy="44" r="24" class="f-nm"/><circle cx="20" cy="72" r="14" class="f-nms k-nm" stroke-width="3"/><circle cx="80" cy="72" r="14" class="f-nms k-nm" stroke-width="3"/></symbol>
<symbol id="ic-sodium" viewBox="0 0 100 100"><path d="M10 52 46 40l44 12v26L54 90 10 78Z" class="f-metal k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M10 52l36 12 44-12" fill="none" class="k-ink" stroke-width="3"/><path d="M46 64v26" class="k-ink" stroke-width="3"/><path d="M60 14 34 50l6 4 26-36Z" class="f-white k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M62 12l12-10 6 5-12 10Z" class="f-ink"/></symbol>
<symbol id="ic-chlorine" viewBox="0 0 100 100"><path d="M36 8h28v22l20 52a8 8 0 0 1-8 10H24a8 8 0 0 1-8-10l20-52Z" class="f-card k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M28 50h44l12 32a8 8 0 0 1-8 10H24a8 8 0 0 1-8-10Z" class="f-gas"/><circle cx="40" cy="44" r="8" class="f-gas"/><circle cx="58" cy="38" r="7" class="f-gas"/><path d="M36 8h28v22l20 52a8 8 0 0 1-8 10H24a8 8 0 0 1-8-10l20-52Z" fill="none" class="k-ink" stroke-width="3" stroke-linejoin="round"/></symbol>
<symbol id="ic-salt" viewBox="0 0 100 100"><rect x="8" y="56" width="30" height="30" class="f-white k-ink" stroke-width="3"/><rect x="40" y="50" width="34" height="34" class="f-white k-ink" stroke-width="3"/><rect x="20" y="24" width="26" height="26" class="f-white k-ink" stroke-width="3"/><path d="M86 14v52" class="k-ink" stroke-width="10" stroke-linecap="round"/><path d="M86 30v36" class="k-cat" stroke-width="5" stroke-linecap="round"/><circle cx="86" cy="76" r="10" class="f-cat k-ink" stroke-width="3"/></symbol>
<symbol id="ic-saltpack" viewBox="0 0 100 100"><path d="M22 18h56l-4 8 4 8v52H22V34l4-8Z" class="f-white k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M22 34h56" class="k-ink" stroke-width="3"/><rect x="36" y="52" width="8" height="8" class="f-ink"/><rect x="52" y="60" width="8" height="8" class="f-ink"/><rect x="42" y="70" width="8" height="8" class="f-ink"/></symbol>
<symbol id="ic-bottle" viewBox="0 0 100 100"><rect x="40" y="6" width="20" height="10" rx="3" class="f-an"/><path d="M38 16h24v10l8 12v50a6 6 0 0 1-6 6H36a6 6 0 0 1-6-6V38l8-12Z" class="f-water k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M30 52h40" class="k-ink" stroke-width="3"/></symbol>
<symbol id="ic-cable" viewBox="0 0 100 100"><rect x="56" y="8" width="28" height="30" rx="5" class="f-card2 k-ink" stroke-width="3"/><path d="M62 8V0m16 8V0" class="k-ink" stroke-width="4"/><path d="M70 38c0 24-52 8-52 34 0 10 8 16 18 16" fill="none" class="k-ink" stroke-width="10" stroke-linecap="round"/><path d="M36 88h14" class="k-copper" stroke-width="10" stroke-linecap="round" style="stroke:#c8763a"/></symbol>
<symbol id="ic-can" viewBox="0 0 100 100"><path d="M26 18h48v68a6 6 0 0 1-6 6H32a6 6 0 0 1-6-6Z" class="f-red2 k-ink" stroke-width="3"/><ellipse cx="50" cy="18" rx="24" ry="8" class="f-metal k-ink" stroke-width="3"/><path d="M26 40h48M26 72h48" class="k-on" stroke-width="4"/></symbol>
<symbol id="ic-pencil" viewBox="0 0 100 100"><path d="M18 70 66 22l14 14-48 48Z" class="f-wood k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M18 70 10 92l22-8Z" class="f-card k-ink" stroke-width="3" stroke-linejoin="round"/><path d="M10 92l4-12 8 8Z" class="f-lead"/><path d="M66 22l8-8a6 6 0 0 1 8 0l6 6a6 6 0 0 1 0 8l-8 8Z" class="f-pink k-ink" stroke-width="3"/></symbol>
<symbol id="ic-air" viewBox="0 0 100 100"><path d="M6 24h50a10 10 0 1 0-10-10M6 42h70a10 10 0 1 1-10 10" fill="none" class="k-muted" stroke-width="5" stroke-linecap="round"/><path d="M40 74h20" class="k-ink" stroke-width="6"/><circle cx="34" cy="74" r="16" class="f-nm"/><circle cx="66" cy="74" r="16" class="f-nm"/></symbol>
<symbol id="ic-next" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M48 30v40l32-20Z" class="f-acc"/></symbol>
<symbol id="ic-back" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M72 30v40L40 50Z" class="f-acc"/></symbol>
<symbol id="ic-blank" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><rect x="34" y="30" width="52" height="34" rx="4" class="f-ink"/><path d="M52 74h16" class="k-ink" stroke-width="5" stroke-linecap="round"/></symbol>
<symbol id="ic-start" viewBox="0 0 120 100"><rect x="6" y="10" width="108" height="80" rx="22" class="f-card2 k-ink" stroke-width="3"/><path d="M30 34v-8h10M90 34v-8H80M30 66v8h10M90 66v8H80" fill="none" class="k-acc" stroke-width="5" stroke-linecap="round"/><path d="M52 38v24l20-12Z" class="f-acc"/></symbol>
</defs></svg>'''

S = []
# ---------- 1 cover
S.append(slide('s01','t-cover','Predicting bond type','Lesson 4.1','Reading §4.1',f'''    <div class="card dq reg"><p class="tag">Driving question</p><p>How can the periodic table predict the kind of bond two elements form?</p></div>
    <div class="r800">
      <div class="key">{use('ic-next','Next button')}<b>Next</b><span>next step</span></div>
      <div class="key">{use('ic-back','Back button')}<b>Back</b><span>one step back</span></div>
      <div class="key">{use('ic-blank','Blank button')}<b>Blank</b><span>zoom part by part<br>twice fast: blank</span></div>
      <div class="key">{use('ic-start','Start button')}<b>Start</b><span>full screen</span></div>
    </div>''',
 '<b>Safety.</b> Sodium reacting with chlorine is shown by video only and never performed: sodium reacts violently with water and chlorine is a toxic gas. <b>Data and sources.</b> Electronegativity: Pauling values as in Lesson 3.3 (Na 0.93, Cl 3.16, H 2.20, F 3.98, O 3.44, Mg 1.31, Ca 1.00, Fe 1.83, K 0.82, Li 0.98, N 3.04, C 2.55, S 2.58). Energies: NIST (Na first ionization energy 496 kJ/mol; Cl electron affinity 349 kJ/mol); lattice energy of NaCl about 787 kJ/mol (CRC). Guide lines 0.4 and 1.8: OpenStax Chemistry 2e, "a general guide, with many exceptions". Ion sizes: Shannon 1976 (Na⁺ 102 pm, Cl⁻ 181 pm). Melting and boiling points: PubChem (NaCl 801 °C, MgCl₂ 714 °C), NIST WebBook (HF boils at 19.5 °C). Names in Lesson 4.2 follow IUPAC Red Book 2005. <b>Clicker.</b> Logitech R800: Next = PageDown, Back = PageUp (while zoomed: exit the zoom), Start/stop = F5 then Escape, Blank = period. Blank zooms one part of the slide per press, animation first; the press after the last part exits; two fast presses on an unzoomed slide blank the screen. Mouse: click an option to mark it right or wrong; click the slide number or the section label for the slide list. Laptop: N notes, O overview, T theme, Ctrl+P run-sheet.',
 [dict(t=1,note='Two periods. Read the driving question aloud; students copy it. Show the four clicker buttons once so students know a zoom or a blank screen is on purpose.')]))
# ---------- 2 hook
S.append(slide('s02','t-hook','Tug of war','Hook','Reading §4.1.2','''    <div class="sim" id="s02-sim" data-sim="tugOfWar" data-pairs="Cl-Cl,H-Cl,Na-Cl" aria-label="Two teams pull on a rope. The knot is a pair of electrons."></div>
    <div class="stack card band">
      <p class="line" id="s02-l0">Two teams pull on one rope.</p>
      <p class="line" id="s02-l1" data-label="predict">Predict: who wins the rope?</p>
      <p class="line" id="s02-l2" data-label="even pull">Same strength: the knot stays in the middle.</p>
      <p class="line" id="s02-l3" data-label="uneven pull">Cl pulls harder than H. The knot moves to Cl.</p>
      <p class="line" id="s02-l4" data-label="blowout">Na lets go. The electrons go to Cl.</p>
      <p class="line" id="s02-l5" data-label="three bonds">Atoms pull on electrons like this. That pull is electronegativity <span class="es">(electronegatividad)</span>.</p>
    </div>''',
 'Narrative thread for 4.1: the rope. Team strength is the Pauling electronegativity from Lesson 3.3. Keep it light; the chemistry words come on slides 5 to 10.',
 [dict(show='s02-l0',stage='s02-sim:teams',t=1,note='Everyday scene. Ask who has played tug of war. No chemistry yet.'),
  dict(hide='s02-l0',show='s02-l1',t=1,note='Prediction: take one answer per table. Most say "the stronger team". Ask: what if both teams are equal?'),
  dict(hide='s02-l1',show='s02-l2',stage='s02-sim:even',t=1,note='Two chlorine atoms, 3.16 and 3.16. The label above the teams says what the numbers are: the pull on electrons (electronegativity). The knot is the shared pair of electrons; it stays centered.'),
  dict(hide='s02-l2',show='s02-l3',stage='s02-sim:uneven',t=1,note='H 2.20, Cl 3.16. The knot slides toward Cl in proportion to the difference; both teams still hold. Misconception to listen for: "Cl takes the electrons" (not yet: still shared).'),
  dict(hide='s02-l3',show='s02-l4',stage='s02-sim:blowout',t=1,note='Na 0.93, Cl 3.16. The knot is pulled all the way; the rope fades; the teams gain + and − and slide together. Say: the pull between + and − is now the bond.'),
  dict(hide='s02-l4',show='s02-l5',stage='s02-sim:labels',t=1,note='Three mini-frames: nonpolar covalent, polar covalent, ionic. Students write the word and the Spanish cognate.')]))
# ---------- 3 launch
S.append(slide('s03','t-launch','Sodium, chlorine, salt','Launch','Reading §4.1 opener',f'''    <div class="trio" id="s03-trio">
      <div class="card pcard slot"><div data-b="s03-na" data-label="sodium">{use('ic-sodium','Icon: a block of sodium metal cut with a knife')}<p class="nm">sodium</p><p class="cap">soft metal, cut with a knife</p></div></div>
      <div class="card pcard slot"><div data-b="s03-cl" data-label="chlorine">{use('ic-chlorine','Icon: a jar of yellow-green chlorine gas')}<p class="nm">chlorine</p><p class="cap">yellow-green, poisonous gas</p></div></div>
      <div class="card pcard slot"><div data-b="s03-salt" data-label="salt">{use('ic-salt','Icon: white salt crystals and a thermometer')}<p class="nm">sodium chloride</p><p class="cap">white crystals, melts at <span class="nw">801 °C</span></p></div></div>
    </div>
    <div class="card dq reg" id="s03-dq" data-label="driving question"><p>How can the periodic table predict the kind of bond two elements form?</p></div>
    <div class="qrow" id="s03-st" data-label="write 60 s"><ol class="frames"><li>I think sodium and chlorine bond differently from two chlorine atoms because <span class="gap"></span>.</li></ol><div class="timer"></div></div>''',
 'The video of sodium burning in chlorine is the hook here; show it from a trusted source. Never perform it.',
 [dict(show='s03-na',t=1,note='Show the sodium clip or photo. Ask: what kind of element is this? (a metal).'),
  dict(show='s03-cl',t=1,note='Chlorine is a toxic gas, a nonmetal. Ask: what do you predict when they meet?'),
  dict(show='s03-salt',t=1,note='Two dangerous elements make table salt, which melts at 801 °C. Ask: why is it so different?'),
  dict(show='s03-dq',cls={'s03-trio':'small'},t=1,note='Read the driving question. Students copy it at the top of the notebook page.'),
  dict(show='s03-st',timer=60,t=1.5,note='Sixty seconds of writing with the starter. Collect two answers; do not correct yet. Listen for "they share" or "they trade".')]))
# ---------- 4 predict now
def pq(p, n, q, opts, lab):
    o = ''.join(f'<li class="opt"><b>{l}</b><span>{t}</span></li>' for l, t in zip('ABC', opts))
    return f'      <div class="card check" id="{p}" data-label="{lab}" data-mode="pick"><p class="tag">Question {n}</p><p class="q">{q}</p><ol class="opts col1" data-lay="col">{o}</ol></div>'
S.append(slide('s04','t-routine','Predict now','Predict','Reading §4.1 Before you read',f'''    <div class="card prompt"><p>Hands up: one finger for A, two for B, three for C. Write your letter.</p></div>
    <div class="stack top">
{pq('s04-q1',1,'Solid salt is made of…',['ions','NaCl molecules','atoms'],'question 1')}
{pq('s04-q2',2,'In HCl, the shared pair sits…',['closer to Cl','closer to H','in the middle'],'question 2')}
{pq('s04-q3',3,'A copper wire is held together by…',['cations in a sea of electrons','shared pairs','+ and − copper ions'],'question 3')}
    </div>''',
 'No answers on this slide. Students keep their letters; slide 24 returns all three answers.',
 [dict(show='s04-q1',t=1,note='Count hands for A, B, C and write the counts on the board. Do not react to the choices. A mouse click on an option only highlights it; there is no grading on this slide.'),
  dict(hide='s04-q1',show='s04-q2',t=1,note='Count hands again. Many choose "in the middle" because a pair is "shared".'),
  dict(hide='s04-q2',show='s04-q3',t=1,note='Count hands. Option C is a common idea: metals made of + and − ions. Keep the counts for slide 24.')]))
# ---------- 5 targets and words
W = [('ic-ionic','ionic bond','enlace iónico','the pull between + and − ions'),
     ('ic-covalent','covalent bond','enlace covalente','a pair of electrons two atoms share'),
     ('ic-metallic','metallic bond','enlace metálico','cations held in a sea of electrons'),
     ('ic-en','electronegativity','electronegatividad','how hard an atom pulls on electrons'),
     ('ic-partial','partial charge','carga parcial','δ (delta) means a little: δ+ or δ−'),
     ('ic-crystal','crystal','cristal','ions in a pattern that repeats'),
     ('ic-molecule','molecule','molécula','atoms joined by shared pairs')]
wc = '\n'.join(f'        <div class="wcard">{use(i,"Icon: "+t)}<p class="t">{t} <span class="es">({es})</span></p><p class="m">{m}</p></div>' for i,t,es,m in W)
S.append(slide('s05','t-words','Targets and words','Targets','Reading §4.1 Vocabulary',f'''    <div class="stack">
      <div class="card" id="s05-ican" data-label="targets"><p class="tag">I can…</p><ul class="ican">
        <li><b>4.1.1</b>explain how ions form and attract.</li>
        <li><b>4.1.2</b>tell polar from nonpolar bonds.</li>
        <li><b>4.1.3</b>describe the electron sea in metals.</li>
        <li><b>4.1.4</b>predict a bond type from the table.</li>
        <li><b>4.1.5</b>argue for a bond type with evidence.</li></ul></div>
      <div class="words" id="s05-words" data-label="words">
{wc}
      </div>
    </div>
    <div class="legend" id="s05-leg" data-label="color code"><span><i class="i-cat">+</i>cation</span><span><i class="i-an">−</i>anion</span><span><i class="e"></i>electron</span><span><i class="i-metal"> </i>metal</span><span><i class="i-nm"> </i>nonmetal</span><span><i class="i-dp">δ+</i>small +</span><span><i class="i-dm">δ−</i>small −</span></div>''',
 'The color code stays fixed in both lessons. Shapes also carry a sign (+, −, dots), so color-blind students can read every drawing.',
 [dict(show='s05-ican',t=2,note='Read the five targets. Students copy the numbers 4.1.1 to 4.1.5; they rate themselves on slide 25.'),
  dict(hide='s05-ican',show='s05-words',t=3,note='Choral reading: English term, then the Spanish cognate. Students add the words to the glossary with the icon. The same icons return on slide 11.'),
  dict(show='s05-leg',t=1,note='Color code: cation red with +, anion blue with −, electron dots, metal gray, nonmetal green, δ+ warm, δ− teal.')]))
# ---------- 6 forming ions
S.append(slide('s06','t-concept cw','Forming ions','Ionic bonds','Reading §4.1.1',f'''    <div class="sim" id="s06-sim" data-sim="ionHop" aria-label="A sodium atom and a chlorine atom; one electron moves from sodium to chlorine."></div>
    <div class="col acc">
      <div class="card" id="s06-pred" data-label="predict"><p class="tag">Predict</p><p>Which atom lets go of its outer electron, Na or Cl?</p></div>
      <div class="card" id="s06-what" data-label="what happened"><p class="tag">What happened</p><p>Na lost one electron. It is now Na<sup>+</sup>. Cl gained it. It is now Cl<sup>−</sup>.</p></div>
      <div class="card rule reg" id="s06-rule" data-label="rule"><p class="tag">Rule</p><p>A metal atom loses its valence electrons and becomes a + ion (cation). A nonmetal atom gains them and becomes a − ion (anion). The transfer alone costs energy.</p></div>
{check('s06','Magnesium loses two electrons. Which ion forms?',['Mg<sup>2−</sup>','Mg<sup>+</sup>','Mg<sup>2+</sup>'],ans='C. Mg keeps 12 protons and has 10 electrons: Mg<sup>2+</sup>.',right='C',
  fb=['A minus charge means extra electrons. A metal loses electrons.','Mg<sup>+</sup> lost only one electron. Magnesium loses two.','Mg keeps 12 protons and has 10 electrons: Mg<sup>2+</sup>.'])}
    </div>''',
 'Energy (Honors box, not assessed): removing Na’s electron costs 496 kJ/mol; Cl releases 349 kJ/mol; the transfer alone costs 147 kJ/mol. The attraction in the crystal (slide 7) pays it back.',
 [dict(show='s06-pred',stage='s06-sim:atoms',focus='s06-sim',t=1,note='Na has one outer electron, Cl has seven. Collect predictions: Na or Cl? Listen for "Cl takes it because it needs one" (the reason is the pull, electronegativity).'),
  dict(stage='s06-sim:hop',t=1,note='The Na electron hops to Cl. The counts change: Na 11 p, 10 e; Cl 17 p, 18 e.'),
  dict(show='s06-what',stage='s06-sim:ions',t=1.5,note='Sizes: Na⁺ is smaller than the Na atom (its outer level is gone); Cl⁻ is larger than the Cl atom. Ask: which one has more protons than electrons?'),
  dict(hide='s06-what',show='s06-rule',t=1.5,note='Students copy the rule. Stress: the transfer costs energy on its own; the bond is not the transfer (slide 7).'),
  dict(show='s06-check',t=1,note='Hands up: one finger for A, two for B, three for C. Count before the press. To tease, click a wrong option: it turns red and shows why it is wrong.'),
  dict(show='s06-ans',cls={'s06-c':'right','s06-check':'done'},t=1,note='C is right. A (Mg²⁻): a minus charge means extra electrons; a metal loses electrons. B (Mg⁺): that is one electron lost; magnesium loses two.')]))
# ---------- 7 the crystal
S.append(slide('s07','t-concept cw','The crystal','Ionic bonds','Reading §4.1.1',f'''    <div class="sim" id="cr-sim" data-sim="ionHop" aria-label="Sodium ions and chloride ions packed in a crystal."></div>
    <div class="col acc">
      <div class="card" id="cr-pred" data-label="predict"><p class="tag">Predict</p><p>Do the ions stay in pairs? Show thumbs up or down.</p></div>
      <div class="card word" id="cr-word" data-label="new word">{use('ic-crystal','Icon: a crystal, ions in a repeating pattern','ic')}<p class="term">crystal <span class="es">(cristal)</span></p><p class="mean">ions in a pattern that repeats in every direction</p></div>
      <div class="card rule reg" id="cr-rule" data-label="rule"><p class="tag">Rule</p><p>The pull (attraction) between <span class="nw">+ ions</span> and <span class="nw">− ions</span> is the ionic bond. The formula NaCl gives a ratio, not a molecule.</p></div>
{check('cr','How many Cl<sup>−</sup> ions touch each Na<sup>+</sup> ion?',['1','6','8'],ans='B. Each Na<sup>+</sup> touches six Cl<sup>−</sup>.',right='B',
  fb=['One is the pair picture. Count the lit neighbors.','Each Na<sup>+</sup> touches six Cl<sup>−</sup> ions.','Eight fits a different crystal (CsCl), not salt.'])}
    </div>''',
 'Misconception: "the transfer is the ionic bond". The transfer makes the ions; the attraction in the lattice is the bond. Building the crystal releases about 787 kJ/mol (lattice energy), far more than the transfer costs. Shannon radii: Na⁺ 102 pm, Cl⁻ 181 pm; the lattice model shrinks both so the center ion stays visible.',
 [dict(show='cr-pred',stage='cr-sim:attract',focus='cr-sim',t=1,note='The + and − ions attract and touch. Thumbs: do they stay in pairs?'),
  dict(show='cr-word',stage='cr-sim:grow',label='build the crystal',t=1,note='The lattice builds from the center out. Read the word card; students repeat "crystal, cristal".'),
  dict(stage='cr-sim:turn',label='six neighbors',t=1.5,note='The center Na⁺ lights with its six Cl⁻ neighbors while the crystal turns. Count them aloud together.'),
  dict(hide='cr-word',show='cr-rule',t=1.5,note='Students copy the rule. NaCl is a formula unit: one Na⁺ for every Cl⁻, no NaCl molecules.'),
  dict(show='cr-check',t=1,note='Hands up: one finger for A, two for B, three for C.'),
  dict(show='cr-ans',cls={'cr-b':'right','cr-check':'done'},t=1,note='B is right. A (1): the "pair" picture; point at the six lit neighbors. C (8): eight is the count in a different lattice (CsCl), not in salt.')]))
# ---------- 8 covalent bonds
S.append(slide('s08','t-concept cw','Covalent bonds','Covalent bonds','Reading §4.1.2',f'''    <div class="stack">
      <div class="sim" id="s08-tug" data-sim="tugOfWar" data-pairs="Cl-Cl,H-Cl,Na-Cl" aria-label="Two equal teams hold the knot in the middle."></div>
      <div class="sim" id="s08-sim" data-sim="sharedPair" data-bonds="H-H,Cl-Cl" aria-label="Two atoms share one pair of electrons."></div>
    </div>
    <div class="col acc">
      <div class="card" id="s08-recap" data-label="recap"><p class="tag">Recap</p><p>An even pull keeps the knot in the middle. Atoms can share electrons this way.</p></div>
      <div class="card" id="s08-h2" data-label="H2"><p class="tag">H–H</p><p>Two H atoms share one pair. Each H now has two electrons, like helium.</p></div>
      <div class="card" id="s08-cl2" data-label="Cl2"><p class="tag">Cl–Cl</p><p>Each Cl has seven outer electrons. With the shared pair, each Cl has eight around it.</p></div>
      <div class="card rule reg" id="s08-rule" data-label="rule"><p class="tag">Rule</p><p>A pair of electrons shared by two atoms is a covalent bond. Atoms joined this way form a molecule (molécula).</p></div>
{check('s08','In Cl<sub>2</sub>, how many electrons does each Cl count around itself?',['7','8','14'],ans='B. Six unshared electrons plus the shared pair make 8.',right='B',
  fb=['Seven forgets the shared pair. It counts for both atoms.','Six unshared electrons plus the shared pair make 8.','Fourteen counts the electrons of both atoms together.'])}
    </div>''',
 'Lewis (1916) proposed the shared pair; Langmuir (1919) named covalence. Lesson 4.3 draws Lewis structures for larger molecules.',
 [dict(stage='s08-tug:even',show='s08-recap',focus='s08-tug',t=1,note='Recap of the hook: equal teams, knot in the middle. Ask: what is the knot? (the shared pair).'),
  dict(hide=['s08-tug','s08-recap'],show=['s08-sim','s08-h2'],stage='s08-sim:H2',t=1.5,note='H₂: two hydrogen atoms share one pair. Ask: why does neither atom take the pair? (same pull).'),
  dict(hide='s08-h2',show='s08-cl2',stage='s08-sim:Cl2',t=1.5,note='Cl₂: each Cl has seven of its own; sharing one pair gives each eight around it. Misconception: "each Cl gets 14" (counting both atoms).'),
  dict(show='s08-rule',t=1.5,note='Students copy the rule card. A molecule is a neutral group of atoms joined by covalent bonds.'),
  dict(hide='s08-cl2',show='s08-check',t=1,note='Hands up for A, B or C.'),
  dict(show='s08-ans',cls={'s08-b':'right','s08-check':'done'},t=1,note='B is right. A (7): forgot that the shared pair counts for both atoms. C (14): counted the electrons of both atoms together.')]))
# ---------- 9 polar and nonpolar: H–H, then the rule, then the first δ drawing (H–Cl), then O–H and H–F
S.append(slide('s09','t-concept cw','Polar and nonpolar','Polar and nonpolar','Reading §4.1.2',f'''    <div class="sim" id="s09-sim" data-sim="sharedPair" data-bonds="H-H,H-Cl,H-O,H-F" aria-label="A shared pair moves toward the atom that pulls harder."></div>
    <div class="col acc">
      <div class="card" id="s09-eq" data-label="equal pull"><p class="tag">H–H</p><p>Equal pull: the pair stays in the middle. The bond is nonpolar.</p></div>
      <div class="card rule reg" id="s09-rule" data-label="rule"><p class="tag">Rule</p><p>The electrons spend more time near one atom. It is the atom with the higher electronegativity. That atom gets a small negative charge, written δ− (delta minus). The other atom gets a small positive charge, δ+.</p></div>
      <div class="card" id="s09-pred" data-label="predict"><p class="tag">Predict</p>{en(('H','2.20'),('Cl','3.16'))}<p>Which atom gets δ−?</p></div>
      <div class="card" id="s09-hcl" data-label="H–Cl"><p class="tag">H–Cl</p><p>Cl pulls harder, so the pair leans to Cl. Cl gets δ−, and H gets δ+. This bond is polar.</p></div>
      <div class="card" id="s09-more" data-label="bigger differences"><p class="tag">O–H and H–F</p><p>A bigger difference makes the pair lean more.</p></div>
{check('s09','In O–H, which atom is δ+?',['H','O','neither'],ans='A. H pulls less, so H is δ+. O is δ−.',right='A',pre=en(('O','3.44'),('H','2.20')),
  fb=['H pulls less, so H is δ+. O is δ−.','O pulls harder, so O is δ−, not δ+.','The values differ by 1.24, so the bond is polar.'])}
    </div>''',
 'Differences: H–H 0.00, H–Cl 0.96, O–H 1.24, H–F 1.78 (Pauling values). C–H is only 0.35: almost equal sharing. The rule comes before the first δ drawing, so students meet the words before the badges.',
 [dict(show='s09-eq',stage='s09-sim:H2',t=1,note='H–H: same atom, same pull, pair centered: nonpolar.'),
  dict(show='s09-rule',t=1,note='Rule first: the pair spends more time near the atom that pulls harder. Say the symbols in words: "delta minus, a small negative charge". Students copy the rule.'),
  dict(hide='s09-eq',show='s09-pred',t=1,note='Prediction: the chips show each atom\'s electronegativity. Which atom gets δ−? Collect a show of hands.'),
  dict(hide='s09-pred',show='s09-hcl',stage='s09-sim:HCl',t=1.5,note='The pair leans to Cl; δ− appears on Cl, δ+ on H, as the rule said.'),
  dict(hide='s09-hcl',show='s09-more',stage='s09-sim:HO',t=1,note='O–H: difference 1.24, the pair leans more. This is the bond in water.'),
  dict(stage='s09-sim:HF',t=1,note='H–F: 1.78, the pair leans the most of the three, still shared. Misconception: "H–F is ionic" (1.78 is just under the 1.8 guide line).'),
  dict(show='s09-check',t=1,note='Hands up for A, B or C.'),
  dict(show='s09-ans',cls={'s09-a':'right','s09-check':'done'},t=1,note='A is right. B (O): O pulls harder, so O is δ−, not δ+. C (neither): the values differ by 1.24, so the bond is polar.')]))
# ---------- 10 metallic bonds: a concert crowd, then cations in an electron sea; copper before the check
S.append(slide('s10','t-concept cw','Metallic bonds','Metallic bonds','Reading §4.1.3',f'''    <div class="sim" id="s10-sim" data-sim="electronSea" aria-label="A concert crowd shares beach balls; then metal cations sit in a sea of electrons."></div>
    <div class="col acc">
      <div class="card" id="s10-c0" data-label="crowd"><p class="tag">A concert crowd</p><p>Beach balls bounce over everyone. No one owns a ball; the crowd shares them all.</p></div>
      <div class="card" id="s10-c1" data-label="cores"><p class="tag">Cations</p><p>Each head is now a + ion: a metal cation.</p></div>
      <div class="card" id="s10-c2" data-label="sea"><p class="tag">Electron sea</p><p>In a metal, the outer electrons are the balls. They belong to the whole metal.</p></div>
      <div class="card" id="s10-c3" data-label="current"><p class="tag">Current</p><p>A battery pushes the electrons one way. That flow is a current.</p></div>
      <div class="card" id="s10-c4" data-label="Mg"><p class="tag">Magnesium</p><p>Each Mg atom gives two electrons to the sea.</p></div>
      <div class="card" id="s10-c5" data-label="Al"><p class="tag">Aluminum</p><p>Each Al atom gives three electrons to the sea.</p></div>
      <div class="card wirecard" id="s10-c6" data-label="copper"><p class="tag">Copper</p><p>Each Cu atom gives one electron to the sea.</p><figure class="wire">{use('ic-wire','Drawing: a copper wire with the insulation stripped back and shiny orange-brown strands','wsvg')}<figcaption>copper wire</figcaption></figure></div>
      <div class="card rule reg" id="s10-rule" data-label="rule"><p class="tag">Rule</p><p>Metal cations sit in a sea of delocalized electrons. Their attraction is the metallic bond. Real electrons behave as waves, not dots.</p></div>
{check('s10','Why can a copper wire carry a current?',['Its electrons can move.','Its copper ions move.','Its atoms share pairs.'],ans='A. The electrons in the sea move. The cations stay in place.',right='A',
  fb=['The electrons in the sea move. The cations stay in place.','In a solid metal, the cations stay in place.','Shared pairs describe covalent bonds, not metals.'])}
    </div>''',
 'Model limits (objective 4.1.3): electrons are drawn as dots but behave as waves; the model shows one flat layer of a 3D crystal. Each electron dot carries a − wherever the cores carry a +. Copper gives one electron per core in this model. Lesson 4.5 uses the model for other metal properties.',
 [dict(show='s10-c0',stage='s10-sim:crowd',t=1,note='Background story: a concert crowd passing beach balls. Ask: who owns the balls? (No one; the crowd shares them.)'),
  dict(show='s10-c1',stage='s10-sim:cores',t=1,note='The heads become + cores: sodium cations.'),
  dict(show='s10-c2',stage='s10-sim:sea',t=1,note='The balls become drifting electrons, each with a − sign: delocalized, they belong to the whole metal.'),
  dict(show='s10-c3',stage='s10-sim:drift',t=1.5,note='Battery on: electrons stream toward +, cations stay. Ask: what moves in a wire?'),
  dict(hide='s10-c3',show='s10-c4',stage='s10-sim:Mg',t=1,note='Magnesium is in group 2: two valence electrons per atom, cores 2+.'),
  dict(hide='s10-c4',show='s10-c5',stage='s10-sim:Al',t=1,note='Aluminum, group 13: three per atom, cores 3+.'),
  dict(hide='s10-c5',show='s10-c6',stage='s10-sim:Cu',t=1,note='Copper: one electron per core in this model. Show the drawing of a stripped copper wire: this is the metal in a charger cable.'),
  dict(hide=['s10-c0','s10-c1','s10-c2'],show='s10-rule',t=1.5,note='Students copy the rule. Ask for one thing the model leaves out (electrons are waves; real metals are 3D).'),
  dict(show='s10-check',t=1,note='Hands up for A, B or C. The copper picture stays on screen, so the question matches it.'),
  dict(show='s10-ans',cls={'s10-a':'right','s10-check':'done'},t=1,note='A is right. B (ions move): in a solid metal the cations stay in the lattice; ions move in solutions, not here. C (shared pairs): that describes covalent bonds, not metals.')]))
# ---------- 11 one picture
def colh(n, ic, name):
    return f'      <div class="colh slot"><div class="colin" data-b="s11-c{n}" data-label="{name}">{use(ic,"Icon: "+name+" bond","big")}<p>{name}</p></div></div>'
rows = [('Particles',['+ and − ions','atoms','+ ions and electrons'],'s11-r1','particles',''),
        ('Electrons',['transferred','shared','delocalized, a sea'],'s11-r5','electrons',''),
        ('Held by',['pull of + and −','a shared pair','a sea of electrons'],'s11-r2','what holds them',''),
        ('Example',['NaCl','Cl<sub>2</sub>','Cu'],'s11-r3','examples',' formula'),
        ('Made of',['metal + nonmetal','two nonmetals','one metal'],'s11-r4','the rule',' hl')]
rh = ''
for name, cells, b, lab, extra in rows:
    rh += f'      <p class="rh">{name}</p>\n' + ''.join(f'      <p class="cell slot{extra}"><span data-b="{b}"{" data-label=%s" % js(lab) if i==0 else ""}>{c}</span></p>\n' for i, c in enumerate(cells))
S.append(slide('s11','t-summary','One picture for three bonds','Three bonds','Reading §4.1.1 to §4.1.4',f'''    <div class="g3">
      <span></span>
{colh(1,'ic-ionic','ionic')}
{colh(2,'ic-covalent','covalent')}
{colh(3,'ic-metallic','metallic')}
{rh}    </div>''',
 'This picture closes the teaching of period 1. Students copy it as one diagram with three columns; the icons match the word strip on slide 5.',
 [dict(t=.5,note='The empty table is on screen. Ask: what are the three kinds of bonds? Build the columns as students name them.'),
  dict(show='s11-c1',t=.5,note='Ionic: + and − ions in a grid; no shared pairs, no molecules.'),
  dict(show='s11-c2',t=.5,note='Covalent: two atoms overlap; the shared pair sits in the overlap.'),
  dict(show='s11-c3',t=.5,note='Metallic: + cores in a sea of electrons; each electron dot carries a −.'),
  dict(show='s11-r1',t=.5,note='Who: ions / atoms / cations and delocalized electrons.'),
  dict(show='s11-r5',t=.5,note='What the electrons do: transferred (ionic), shared (covalent), delocalized in a sea (metallic).'),
  dict(show='s11-r2',t=.5,note='What holds: every bond is an attraction between + and − charges.'),
  dict(show='s11-r3',t=.5,note='One example each.'),
  dict(show='s11-r4',t=1,note='The rule in one line: metal + nonmetal → ionic; nonmetal + nonmetal → covalent; metal alone → metallic.')]))
# ---------- 12 backpack sort
items = [('ic-saltpack','salt packet','NaCl','ionic','ionic','Na metal, Cl nonmetal'),
         ('ic-bottle','water bottle','H<sub>2</sub>O','polar','polar covalent','O pulls the pair'),
         ('ic-wire','charger cable','Cu','metallic','metallic','copper atoms, electron sea'),
         ('ic-can','soda can','Al','metallic','metallic','aluminum alone, electron sea'),
         ('ic-pencil','pencil','C','nonpolar','covalent','carbon atoms share pairs'),
         ('ic-air','air you breathe','O<sub>2</sub>','nonpolar','nonpolar covalent','two O, equal pull')]
bag = '\n'.join(f'''      <div class="item">{use(i,'Icon: '+n)}<p class="nm lbl">{n}</p><p class="fm lbl">{f}</p><div class="back"><div data-b="s12-i{k}"{' data-label="card %d"' % (k+1)}><p class="bt {c} lbl">{t}</p><p class="why">{w}</p></div></div></div>''' for k,(i,n,f,c,t,w) in enumerate(items))
S.append(slide('s12','t-turn','Backpack sort','Practice','Reading §4.1 Review',f'''    <div class="card prompt"><p>Call out each bond. Use the table.</p></div>
    <div class="bag">
{bag}
    </div>''',
 'Pencil "lead" is graphite: carbon atoms joined by covalent bonds in layers. Water: O 3.44, H 2.20, difference 1.24, polar covalent. O₂: same atoms, nonpolar.',
 [dict(t=1,note='Students call the bond for each item before you flip it. Allow 30 seconds of table talk.')]+
 [dict(show=f's12-i{k}',t=.5,note=n) for k,n in enumerate(['Salt: sodium (metal) with chlorine (nonmetal), ionic.','Water: two nonmetals, difference 1.24, polar covalent. Misconception: "water is ionic because it dissolves salt".','Copper wire: one metal, metallic bonding.','Aluminum can: one metal, metallic.','Pencil graphite: carbon atoms share pairs, covalent.','Oxygen gas O₂: two identical atoms, nonpolar covalent.'])]))
# ---------- 13 period 1 exit
S.append(slide('s13','t-routine two','Period 1 exit','Exit, period 1','Reading §4.1 Review','''    <div class="card prompt reg"><p>Write one sentence that compares the particles and attractions in three kinds of bonds.</p></div>
    <div class="rt-main">
      <div class="acc">
        <div class="card phase" id="s13-w" data-label="write">
          <p class="tag">Write</p>
          <ol class="frames"><li>The three bonds differ in what holds the particles: <span class="gap"></span>.</li></ol>
          <p class="bank"><b>Word bank:</b> <span>attraction</span> <span>ions</span> <span>shared pair</span> <span>electron sea</span></p>
        </div>
        <div class="card phase reg" id="s13-s" data-label="sample answer"><p class="tag">Sample answer</p><p>Ionic bonds hold oppositely charged ions. Covalent bonds share pairs of electrons. Metallic bonds hold cations in an electron sea.</p></div>
      </div>
      <div class="timer"></div>
    </div>''',
 'Period 1 ends here. Collect the notebooks of three students as a quick check before period 2.',
 [dict(show='s13-w',t=.5,note='Read the prompt. Point at the sentence frame and the word bank.'),
  dict(timer=120,label='write 2 min',t=2,note='Two minutes of silent writing in notebooks.'),
  dict(show='s13-s',t=1,note='Students compare with the sample and fix one word. End of period 1.')]))
# ---------- 14 warm-up
S.append(slide('s14','t-turn two','Warm-up','Warm-up, period 2','Reading §4.1.1 to §4.1.3','''    <div class="qrow">
      <div class="card"><p>Answer in your notebook. Then check each answer.</p></div>
      <div class="timer"></div>
    </div>
    <table class="tbl fill">
      <thead><tr><th>Question</th><th>Answer</th></tr></thead>
      <tbody>
        <tr><td>What particles make up solid salt?</td><td class="slot"><span data-b="s14-a1" data-label="answer 1">Na<sup>+</sup> and Cl<sup>−</sup> ions in a crystal</span></td></tr>
        <tr><td>In HCl, which atom is δ−?</td><td class="slot"><span data-b="s14-a2" data-label="answer 2">Cl, because it pulls harder</span></td></tr>
        <tr><td>What moves in a copper wire?</td><td class="slot"><span data-b="s14-a3" data-label="answer 3">electrons in the electron sea</span></td></tr>
      </tbody>
    </table>''',
 'Period 2 starts here. The three questions retrieve 4.1.1, 4.1.2 and 4.1.3.',
 [dict(t=.5,note='Students write while you take attendance.'),
  dict(timer=90,label='timer 90 s',t=1.5,note='Ninety seconds.'),
  dict(show='s14-a1',t=.5,note='Ions, not molecules: NaCl is a ratio.'),
  dict(show='s14-a2',t=.5,note='Cl (3.16) pulls harder than H (2.20).'),
  dict(show='s14-a3',t=.5,note='Electrons move; the cations stay.')]))
# ---------- 15 the electronegativity difference
S.append(slide('s15','t-concept cw','The electronegativity difference','Predicting bonds','Reading §4.1.4',f'''    <div class="sim" id="s15-sim" data-sim="enMeter" data-bonds="Cl-Cl,H-Cl,Na-Cl" aria-label="A bar from 0 to 3.3 with the difference of each bond."></div>
    <div class="col acc">
      <div class="card" id="s15-def" data-label="the difference"><p class="tag">The difference</p><p>ΔEN means the difference: the larger value minus the smaller value.</p></div>
      <div class="card" id="s15-guide" data-label="guide lines"><p class="tag">Guide</p><p>The lines at 0.4 and 1.8 are a guide, not a wall. Bonds change slowly along the bar.</p></div>
      <div class="card rule reg" id="s15-rule" data-label="rule"><p class="tag">Rule</p><p>Subtract the smaller value from the larger one. Below 0.4, the bond is nonpolar covalent. From 0.4 to 1.8, it is polar covalent. Above 1.8, it is ionic.</p></div>
{check('s15','What does the guide predict for Ca–O?',['nonpolar','polar','ionic'],ans='C. 3.44 − 1.00 = 2.44, above 1.8: ionic.',right='C',pre=en(('Ca','1.00'),('O','3.44')),
  fb=['Nonpolar needs a difference below 0.4. Here it is 2.44.','Polar covers 0.4 to 1.8. The difference 2.44 is above 1.8.','3.44 − 1.00 = 2.44, above 1.8: ionic.'])}
    </div>''',
 'Guide from OpenStax Chemistry 2e: "just a general guide, however, with many exceptions". The bar colors blend at 0.4 and 1.8 on purpose.',
 [dict(show='s15-def',stage='s15-sim:bar',t=1,note='Δ (delta) means "difference". Always larger minus smaller, so ΔEN is never negative.'),
  dict(show='s15-guide',stage='s15-sim:lines',t=1,note='The lines are a guide, not a wall: bond character changes gradually.'),
  dict(stage='s15-sim:Cl-Cl',t=1,note='Ask for the subtraction first: 3.16 − 3.16 = 0.00, nonpolar.'),
  dict(stage='s15-sim:H-Cl',t=1,note='3.16 − 2.20 = 0.96, polar covalent.'),
  dict(stage='s15-sim:Na-Cl',t=1,note='3.16 − 0.93 = 2.23, ionic. Misconception: "a cutoff proves the bond type" (it does not; slide 17).'),
  dict(hide='s15-def',show='s15-rule',t=1.5,note='Students copy the rule card.'),
  dict(hide='s15-guide',show='s15-check',t=1,note='Students subtract on whiteboards first, then hands up.'),
  dict(show='s15-ans',cls={'s15-c':'right','s15-check':'done'},t=1,note='C is right (2.44). A (nonpolar): only below 0.4. B (polar): 0.4 to 1.8; 2.44 is well above. Also calcium is a metal and oxygen a nonmetal.')]))
# ---------- 16 evidence from the table (wide)
S.append(slide('s16','t-concept wide','Evidence from the table','Predicting bonds','Reading §4.1.4',f'''    <div class="sim" id="s16-sim" data-sim="ptMap" data-pairs="Na-Cl,H-Cl,Cu-Cu" data-caption="0" data-band="214" aria-label="The periodic table with metals, nonmetals and a pair of elements."></div>
    <div class="ptrow blk" id="s16-row" data-label="pairs" style="height:214px"><div class="stack">
      <p class="caprow" id="s16-p1" data-label="Na and Cl">Na and Cl: a metal and a nonmetal. The bond is ionic.</p>
      <p class="caprow" id="s16-p2" data-label="H and Cl">H and Cl: two nonmetals. They share a pair: covalent.</p>
      <p class="caprow" id="s16-p3" data-label="Cu and Cu">Cu alone: one metal. The bond is metallic.</p>
      <div class="rulerow reg" id="s16-rule" data-label="rule"><p>A metal and a nonmetal: electrons transfer. <b class="bn lbl">Ionic bond.</b></p><p>Two nonmetals: electrons are shared. <b class="bn lbl">Covalent bond.</b></p><p>A metal alone: electrons are delocalized, a sea. <b class="bn lbl">Metallic bond.</b></p></div>
      <div class="checkrow" id="s16-check" data-label="check">
        <p class="q" id="s16-q"><span class="tag">Check:</span> Which pair forms a covalent bond?</p>
        <ol class="opts" data-lay="row">{optli('s16',['K–Br','N–O','Mg–O'],'B',['K is a metal, so K–Br is ionic.','N and O are both nonmetals. They share pairs.','Mg is a metal, so Mg–O is ionic.'])}</ol>
        <div class="af"><p class="ans" id="s16-ans" data-label="answer">B. N and O are both nonmetals. They share pairs.</p><p class="fb" aria-live="polite"></p></div>
      </div>
    </div></div>''',
 'Second line of evidence. Metals (left and middle) have low ionization energies and electronegativities; nonmetals (upper right) have high ones. Metalloids along the staircase are left untinted.',
 [dict(stage='s16-sim:outline',focus='s16-sim',t=1,note='Ask: where are the metals? where are the nonmetals? Students point on their own tables.'),
  dict(stage='s16-sim:metals',t=1,note='Metals tint from the left: groups 1 and 2, the transition metals, and the lower p-block.'),
  dict(stage='s16-sim:nonmetals',t=1,note='Nonmetals tint from the right; the staircase divides them. Hydrogen is a nonmetal.'),
  dict(show=['s16-row','s16-p1'],stage='s16-sim:Na-Cl',t=1,note='Na and Cl: metal with nonmetal, ionic. Same answer as the difference (2.23).'),
  dict(hide='s16-p1',show='s16-p2',stage='s16-sim:H-Cl',t=1,note='H and Cl: two nonmetals, covalent (polar, 0.96).'),
  dict(hide='s16-p2',show='s16-p3',stage='s16-sim:Cu-Cu',t=1,note='Copper alone: metallic.'),
  dict(hide='s16-p3',show='s16-rule',stage='s16-sim:nonmetals',t=1.5,note='Students copy the three lines. They match slide 11.'),
  dict(hide='s16-rule',show='s16-check',t=1,note='Hands up for A, B or C.'),
  dict(show='s16-ans',cls={'s16-b':'right','s16-check':'done'},t=1,note='B is right. A (K and Br): potassium is a metal, so the bond is ionic. C (Mg and O): magnesium is a metal, ionic.')]))
# ---------- 17 near the line
S.append(slide('s17','t-example','Near the line','Predicting bonds','Reading §4.1.4',f'''    <div class="sim" id="s17-sim" data-sim="enMeter" data-bonds="H-F,Mg-Cl,Fe-Cl" aria-label="Three bonds placed near the 1.8 line."></div>
    <div class="acc">
      <div class="card" id="s17-pred" data-label="predict"><p class="tag">Predict</p><p>Is a difference close to 1.8 strong evidence for ionic?</p></div>
      <div class="card stepscard" id="s17-steps" data-label="H–F"><p class="tag">Close to 1.8</p><ol class="steps">
        <li id="s17-1"><span class="k">H–F</span><span>Difference 1.78: molecules. HF boils at 20 °C.</span></li>
        <li id="s17-2" data-label="Mg–Cl"><span class="k">Mg–Cl</span><span>Difference 1.85: an ionic solid. It melts at 714 °C.</span></li>
        <li id="s17-3" data-label="so what"><span class="k">So</span><span>Close numbers, very different substances. Near 1.8 the number alone is weak evidence.</span></li>
        <li id="s17-4" data-label="Fe–Cl"><span class="k">Fe–Cl</span><span>Difference 1.33, yet named like an ionic compound (Lesson 4.2).</span></li>
      </ol></div>
{check('s17','MgCl<sub>2</sub> has a difference of 1.85. How strong is that number alone as evidence for ionic?',['strong','weak','against'],ans='B. 1.85 is only 0.05 above 1.8. Use the table too.',right='B',
  fb=['1.85 is too close to the line to be strong alone.','1.85 is only 0.05 above 1.8. Use the table too.','1.85 is above 1.8, so it supports ionic, weakly.'])}
    </div>''',
 'HF boils at 19.5 °C (NIST); MgCl₂ melts at 714 °C (PubChem). FeCl₃ (1.33) and CuO (1.54) are partly covalent but are named as ionic compounds because names follow composition, metal + nonmetal.',
 [dict(show='s17-pred',stage='s17-sim:lines',t=1,note='Prediction: hands up for "strong" or "weak".'),
  dict(hide='s17-pred',show=['s17-steps','s17-1'],stage='s17-sim:H-F',t=1,note='H–F: 3.98 − 2.20 = 1.78, just below 1.8. HF is made of molecules and boils at 20 °C.'),
  dict(show='s17-2',stage='s17-sim:Mg-Cl',t=1,note='Mg–Cl: 3.16 − 1.31 = 1.85, just above. MgCl₂ is an ionic solid that melts at 714 °C.'),
  dict(show='s17-3',t=1,note='0.07 apart, very different substances. The number near 1.8 is weak evidence; add the table (metal + nonmetal) and properties.'),
  dict(show='s17-4',stage='s17-sim:Fe-Cl',t=1,note='Fe–Cl: 3.16 − 1.83 = 1.33. Partly covalent, still named as an ionic compound (Lesson 4.2).'),
  dict(show='s17-check',t=1,note='Hands up for A, B or C.'),
  dict(show='s17-ans',cls={'s17-b':'right','s17-check':'done'},t=1,note='B is right. A (strong): 1.85 is too close to the line to be strong alone. C (against): 1.85 is above 1.8 and Mg is a metal, so the evidence supports ionic, weakly.')]))
# ---------- 18 bonding argument
S.append(slide('s18','t-cer','Bonding argument: I do, we do','Bonding arguments','Reading §4.1.5',f'''    <div class="stack">
      <p class="hdr" id="s18-h1" data-label="I do">I do: potassium fluoride, KF.</p>
      <p class="hdr" id="s18-h2" data-label="we do">We do: hydrogen chloride, HCl. Say each part first.</p>
    </div>
    <div class="stack">
      <div class="sim" id="s18-sim" data-sim="cerBuilder" aria-label="Four boxes: claim, evidence, reasoning, strength.">
        <div data-set="KF"><p data-part="claim">Potassium fluoride (KF) is ionic.</p>
          <p data-part="evidence">{en(('K','0.82'),('F','3.98'))}The difference is 3.16. K is a metal; F is a nonmetal.</p>
          <p data-part="reasoning">A difference above 1.8 predicts ionic. A metal gives electrons to a nonmetal.</p>
          <p data-part="strength">Strong. 3.16 is far above 1.8, and both kinds of evidence agree.</p></div>
        <div data-set="HCl"><p data-part="claim">The bond in HCl is polar covalent.</p>
          <p data-part="evidence">{en(('H','2.20'),('Cl','3.16'))}The difference is 0.96. Both are nonmetals.</p>
          <p data-part="reasoning">0.96 is between 0.4 and 1.8. Two nonmetals share the pair unequally. Cl is δ−.</p>
          <p data-part="strength">Strong. 0.96 is far from both lines, and both kinds of evidence agree.</p></div>
      </div>
{check('s18','Which evidence best supports “KF is ionic”?',['metal + nonmetal, difference 3.16','KF is a white solid.','F is a gas.'],ans='A. Values and positions are evidence. Color and state are not.',right='A',
  fb=['Values and positions are evidence. Color and state are not.','Color does not show the type of bond.','The state of fluorine says nothing about the compound KF.'])}
    </div>''',
 'Four parts: claim, evidence (both values, the difference, positions on the table), reasoning (the guide and what metals and nonmetals do), strength (distance from 0.4 and 1.8, and whether both kinds of evidence agree).',
 [dict(show='s18-h1',stage='s18-sim:empty',t=1,note='Show the four empty boxes. Name each part.'),
  dict(stage='s18-sim:KF-claim',t=.5,note='I do: think aloud. The claim names the bond type.'),
  dict(stage='s18-sim:KF-evidence',t=1,note='Both values, the difference, and the positions on the table.'),
  dict(stage='s18-sim:KF-reasoning',t=1,note='The rule that links evidence to claim.'),
  dict(stage='s18-sim:KF-strength',t=1,note='Strong: far from both lines and both kinds of evidence agree.'),
  dict(hide='s18-h1',show='s18-h2',stage='s18-sim:HCl-claim',t=1,note='We do: students say the claim before the press.'),
  dict(stage='s18-sim:HCl-evidence',t=1,note='Students supply 2.20, 3.16 and 0.96 before the press.'),
  dict(stage='s18-sim:HCl-reasoning',t=1,note='Students supply the rule: between 0.4 and 1.8, two nonmetals share unequally.'),
  dict(stage='s18-sim:HCl-strength',t=1,note='Strong because 0.96 is far from both lines.'),
  dict(hide=['s18-h2','s18-sim'],show='s18-check',label='check',t=1,note='Hands up for A, B or C.'),
  dict(show='s18-ans',cls={'s18-a':'right','s18-check':'done'},t=1,note='A is right. B (white solid): color is not evidence for a bond type. C (F is a gas): the element’s state says nothing about the compound KF.')]))
# ---------- 19 you do
S.append(slide('s19','t-turn tblmid','You do: three bonds','Bonding arguments','Reading §4.1.5','''    <div class="qrow">
      <div class="card"><p>Find each difference. Predict the bond type.</p><p class="small">Then write a full argument for one bond.</p></div>
      <div class="timer"></div>
    </div>
    <table class="tbl fill">
      <thead><tr><th>Bond</th><th>Electronegativity (pull on electrons)</th><th>Difference</th><th>Bond type</th></tr></thead>
      <tbody>
        <tr><td>Li–F</td><td><span class="chips"><span class="chip"><b>Li</b><span class="mono">0.98</span></span><span class="chip"><b>F</b><span class="mono">3.98</span></span></span></td><td class="slot"><span class="mono" data-b="yt-1" data-label="answer 1">3.00</span></td><td class="slot"><span data-b="yt-1">ionic, strong</span></td></tr>
        <tr><td>N–H</td><td><span class="chips"><span class="chip"><b>N</b><span class="mono">3.04</span></span><span class="chip"><b>H</b><span class="mono">2.20</span></span></span></td><td class="slot"><span class="mono" data-b="yt-2" data-label="answer 2">0.84</span></td><td class="slot"><span data-b="yt-2">polar, N is <span class="dm">δ−</span></span></td></tr>
        <tr><td>C–S</td><td><span class="chips"><span class="chip"><b>C</b><span class="mono">2.55</span></span><span class="chip"><b>S</b><span class="mono">2.58</span></span></span></td><td class="slot"><span class="mono" data-b="yt-3" data-label="answer 3">0.03</span></td><td class="slot"><span data-b="yt-3">nonpolar</span></td></tr>
      </tbody>
    </table>
    <p data-b="yt-2">N–H is a bond in ammonia, NH<sub>3</sub>. C–S is a bond in carbon disulfide, CS<sub>2</sub>.</p>''',
 'You do. Circulate during the timer. Look for "smaller minus larger" (negative differences) and for arguments without a strength part.',
 [dict(t=.5,note='Read the task. Students work alone in notebooks.'),
  dict(timer=180,label='timer 3 min',t=3,note='Three minutes. Early finishers write the full argument for one bond: claim, evidence, reasoning, strength.'),
  dict(show='yt-1',t=.5,note='3.98 − 0.98 = 3.00. Far above 1.8 and metal with nonmetal: strong.'),
  dict(show='yt-2',t=.5,note='3.04 − 2.20 = 0.84. N pulls harder, so N is δ− and H is δ+.'),
  dict(show='yt-3',t=.5,note='2.58 − 2.55 = 0.03. Two nonmetals sharing almost equally.')]))
# ---------- 20 checkpoint routine
steps = [('Think · 30 s','alone, no talking'),('Talk · 60 s','tell your partner, then listen'),('Write · 90 s','use the sentence frames'),('Self-check','tick each success criterion'),('Compare','read the sample and fix one line')]
sr = '\n'.join(f'        <li id="s20-s{k+1}"><b class="lbl">{a}</b><span>{b}</span></li>' for k,(a,b) in enumerate(steps))
rail = lambda p: '<ol class="rail">' + ''.join(f'<li id="{p}-r{k+1}">{t}</li>' for k,t in enumerate(['Think','Talk','Write','Self-check','Compare'])) + '</ol>'
S.append(slide('s20','t-routine','Checkpoint routine','Checkpoint','Objectives 4.1.1 to 4.1.3',f'''    <div class="card prompt"><p>Each checkpoint uses the same five steps.</p></div>
    {rail('s20')}
    <ol class="steprows">
{sr}
    </ol>''',
 'Routine for slides 21 to 23: think 30 s, talk 60 s, write 90 s, self-check 30 s, compare 60 s.',
 [dict(t=.5,note='Explain that the routine repeats for each question.')]+
 [dict(cls=dict([(f's20-r{j+1}','done') for j in range(k)]+[(f's20-s{j+1}','') for j in range(k)]+[(f's20-r{k+1}','now'),(f's20-s{k+1}','now')]),label=['think','talk','write','self-check','compare'][k],t=.3,note=n) for k,n in enumerate(['Think: silent, no pencils.','Talk: partner A first, then partner B.','Write: the sentence frames and word bank stay on screen.','Self-check: tick each criterion you met.','Compare: read the sample answer and fix one line.'])]))
# ---------- 21 to 23 checkpoints
def checkpoint(sid, title, ref, prompt, read, fr_lines, bank, crit, sample, notes, listen):
    p = sid
    fl = ''.join(f'<li>{x}</li>' for x in fr_lines)
    bk = ' '.join(f'<span>{b}</span>' for b in bank)
    cr = ''.join(f'<li>{c}</li>' for c in crit)
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
    fr = [dict(show=f'{p}-read',t=.5,note=notes[0]),
          dict(hide=f'{p}-read',show=f'{p}-think',cls={f'{p}-r1':'now'},timer=30,t=.5,note='Silent thinking. No pencils yet.'),
          dict(hide=f'{p}-think',show=f'{p}-talk',cls={f'{p}-r1':'done',f'{p}-r2':'now'},timer=60,t=1,note='Partner A speaks first, then B. Listen for: '+listen),
          dict(hide=f'{p}-talk',show=f'{p}-write',cls={f'{p}-r2':'done',f'{p}-r3':'now'},timer=90,t=2,note='Students write in notebooks with the frames; the word bank stays up.'),
          dict(show=f'{p}-check',cls={f'{p}-r3':'done',f'{p}-r4':'now'},t=1,note='Students tick each criterion they met and fix one line.'),
          dict(show=f'{p}-sample',cls={f'{p}-r4':'done',f'{p}-r5':'now'},t=1,note=notes[1])]
    return slide(sid,'t-routine',title,title,ref,body,'Routine: think 30 s, talk 60 s, write 90 s, self-check 30 s, compare 60 s. The question stays on screen on every frame.',fr)
S.append(checkpoint('s21','Checkpoint 1','Objective 4.1.1',
  'A student calls the transferred electron the ionic bond. Explain the error. What holds solid salt together?',
  'Read the question. What does the student claim?',
  ['The transfer only <span class="gap"></span>.','The ionic bond is <span class="gap"></span>.'],
  ['forms the ions','attraction','oppositely charged','crystal'],
  ['the transfer only forms ions?','the bond is the attraction between ions?','salt is a crystal of ions?'],
  'The transfer only forms the ions. The attraction between oppositely charged ions is the ionic bond.',
  ['Read the prompt aloud. Ask: what does the student claim? (The transferred electron is the bond.)','Compare with the sample. Reading §4.1.1 Key idea: an ionic bond is the attraction between oppositely charged ions.'],
  '"the electron is the bond".'))
S.append(checkpoint('s22','Checkpoint 2','Objective 4.1.2',
  'Cl<sub>2</sub> and HCl each contain one shared electron pair. Explain why Cl<sub>2</sub> is nonpolar, but HCl is polar. Identify the δ− atom.',
  'Read the question. What is the same in both?',
  ['Cl<sub>2</sub> is nonpolar because <span class="gap"></span>.','HCl is polar because <span class="gap"></span>.','The δ− atom is <span class="gap"></span>.'],
  ['electronegativity','equal pull','unequal sharing','pulls harder'],
  ['equal pull in Cl<sub>2</sub>?','Cl pulls harder in HCl?','Cl is δ−?'],
  'Both Cl atoms have the same electronegativity. In HCl, Cl pulls harder and is δ−.',
  ['Read the prompt aloud. Both molecules have one shared pair; the difference is the pull.','Compare with the sample. Reading §4.1.2 Key idea: unequal sharing gives partial charges and a polar bond.'],
  '"HCl is ionic" or "H is δ−".'))
S.append(checkpoint('s23','Checkpoint 3','Objective 4.1.3',
  'A copper wire carries an electric current. Use the electron-sea model to explain why. Name one limitation of the model.',
  'Read the question. It has two parts.',
  ['The electrons in copper <span class="gap"></span>.','A current flows because <span class="gap"></span>.','The model leaves out <span class="gap"></span>.'],
  ['cations','electron sea','move freely','waves'],
  ['electrons in the sea move?','cations stay in place?','one model limit?'],
  'Delocalized electrons flow through the metal, so copper conducts. Real electrons are waves.',
  ['Read the prompt aloud. Two parts: why copper conducts, and one limit of the model.','Compare with the sample. Other limits: one flat layer shown, a real metal is a 3D crystal.'],
  '"copper ions move" (they stay in the lattice).'))
# ---------- 24 predictions and exit ticket
def pa(p, n, q, right, reason, lab):
    return f'''      <div class="card check done" id="{p}" data-label="{lab}" data-mode="none"><p class="tag">Question {n}</p><p class="q">{q}</p><ol class="opts" data-lay="row"><li class="opt right"><b>A</b><span>{right}</span></li></ol><p class="reason">{reason}</p></div>'''
S.append(slide('s24','t-routine t-exit','Predictions and exit ticket','Exit ticket','Objectives 4.1.4 and 4.1.5',f'''    <div class="stack">
      <div class="phaseA" id="s24-A" data-label="answers">
        <div class="stack">
{pa('s24-p1',1,'Solid salt is made of…','ions','Salt is a crystal of Na<sup>+</sup> and Cl<sup>−</sup> ions. It has no molecules.','answer 1')}
{pa('s24-p2',2,'In HCl, the shared pair sits…','closer to Cl',en(('Cl','3.16'),('H','2.20'))+'Cl pulls harder.','answer 2')}
{pa('s24-p3',3,'A copper wire is held together by…','cations in a sea of electrons','Copper alone is a metal: a metallic bond.','answer 3')}
        </div>
        <p class="handsup">Hands up if you predicted this.</p>
      </div>
      <div class="phaseB" id="s24-B" data-label="exit ticket">
        <div class="card prompt reg"><p>How can the periodic table predict the kind of bond two elements form?</p></div>
        <ol class="rail"><li id="s24-r1">Claim</li><li id="s24-r2">Evidence</li><li id="s24-r3">Reasoning</li><li id="s24-r4">Self-check</li><li id="s24-r5">Sample</li></ol>
        <div class="rt-main">
          <div class="acc">
            <div class="card phase" id="s24-fr" data-label="claim"><p class="tag">Write</p><ol class="frames">
              <li id="s24-f1">Claim: The periodic table predicts a bond from <span class="gap"></span>.</li>
              <li id="s24-f2" data-label="evidence">Evidence: For example, <span class="gap"></span> and <span class="gap"></span> differ by <span class="gap"></span>.</li>
              <li id="s24-f3" data-label="reasoning">Reasoning: This works because <span class="gap"></span>.</li>
            </ol>
            <p class="bank" id="s24-bank"><b>Word bank:</b> <span>electronegativity</span> <span>difference</span> <span>metal</span> <span>nonmetal</span> <span>guide</span></p></div>
            <div class="card" id="s24-check" data-label="self-check"><p class="tag">Self-check: did you write…</p><ul class="crit"><li>a claim that answers the question?</li><li>two values and their difference?</li><li>reasoning from the guide and the table positions?</li></ul></div>
            <div class="card reg" id="s24-sample" data-label="sample answer"><p class="tag">Sample answer</p><p>Look up both values on the table and subtract. A metal and a nonmetal above 1.8 form ions. Two nonmetals share electrons.</p></div>
          </div>
          <div class="timer"></div>
        </div>
      </div>
    </div>''',
 'Predictions from slide 4 come back first; students check their letters. Then the CER exit ticket on the driving question; the question stays on screen while the sample shows. Collect the exit tickets.',
 [dict(show=['s24-A','s24-p1'],t=.5,note='Answer 1: ions. Hands up if you predicted A. Compare with the counts from slide 4.'),
  dict(hide='s24-p1',show='s24-p2',t=.5,note='Answer 2: closer to Cl. Ask a student who changed their mind to say why.'),
  dict(hide='s24-p2',show='s24-p3',t=.5,note='Answer 3: cations in a sea of electrons. Option C (+ and − copper ions) was the common wrong idea.'),
  dict(hide='s24-A',show=['s24-B','s24-fr','s24-f1'],cls={'s24-r1':'now'},t=1,note='Exit ticket. Claim first: what does the table give you? (electronegativity values and positions).'),
  dict(show='s24-f2',cls={'s24-r1':'done','s24-r2':'now'},t=1,note='Evidence: two values and the difference, plus positions.'),
  dict(show='s24-f3',cls={'s24-r2':'done','s24-r3':'now'},timer=180,label='write 3 min',t=3,note='Reasoning: the guide and what metals and nonmetals do. Three minutes of writing.'),
  dict(show='s24-check',cls={'s24-r3':'done','s24-r4':'now'},t=1,note='Self-check with the three criteria.'),
  dict(show='s24-sample',cls={'s24-r4':'done','s24-r5':'now'},t=1,note='Compare with the sample. Collect the tickets.')]))
# ---------- 25 rate your learning
T = [('4.1.1','explain how ions form and attract.','slides 6 and 7'),('4.1.2','tell polar from nonpolar bonds.','slides 8 and 9'),('4.1.3','describe the electron sea in metals.','slide 10'),('4.1.4','predict a bond type from the table.','slides 11, 15 to 17'),('4.1.5','argue for a bond type with evidence.','slides 18 and 19')]
rt = '\n'.join(f'        <li id="s25-t{k+1}"><span><b class="mono lbl">{a}</b> {b}</span><span class="rev">Review: {c}</span></li>' for k,(a,b,c) in enumerate(T))
S.append(slide('s25','t-routine','Rate your learning','Reflect','All objectives',f'''    <div class="scale lbl"><span>1 finger: not yet</span><span>2 fingers: almost</span><span>3 fingers: I can teach it</span></div>
    <p class="tag">I can…</p>
    <ol class="rate">
{rt}
    </ol>''',
 'Fingers 1 to 3 for each target. Students below 3 revisit the slides named on the right, then the missions: Predict the bond, Find a partner, Build the argument. Lesson 4.2 uses ion charges to write formulas and names.',
 [dict(t=.5,note='Explain the scale: 1 not yet, 2 almost, 3 I can teach it.')]+
 [dict(cls=dict([(f's25-t{j+1}','') for j in range(k)]+[(f's25-t{k+1}','now')]),label=f'target {k+1}',t=.5,note=f'Fingers for target 4.1.{k+1}. Note who shows 1 and point to the review slides.') for k in range(5)]))

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
