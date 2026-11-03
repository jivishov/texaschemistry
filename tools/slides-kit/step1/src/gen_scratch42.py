# Scratch slides for the Lesson 4.2 animations (step 5). Never part of a repo build.
import os
PAIRS='Ca-Cl,Al-O,Mg-O:reduce,Na-O,K-S,Ca-N,Fe2-Cl,Fe3-Cl,Ag-Cl,Zn-O,Ca-OH,NH4-SO4,Na-NO3,Al-SO4,Ca-PO4'
def cb_stages():
    out=[]
    for t in PAIRS.split(','):
        k,_,fl=t.partition(':')
        one = k in ('Ag-Cl','Zn-O','Na-NO3')
        out+= [k+'/'+s for s in (['ions','add','balance','formula','reduce','name'] if fl=='reduce' else ['ions','add','balance','formula','name']) if not (one and s=='add')]
    return out
SIMS=[
 ('lr','labelRead','t-hook','',['shelf','focus0','focus1','focus2','code']),
 ('it','ionTable','t-concept wide','data-fblock="0" data-reserve="180"',['outline','g1','g2','g13','g17','g16','g15','tm']),
 ('cb','chargeBlocks','t-concept','data-pairs="%s"'%PAIRS,cb_stages()),
 ('cc','crisscross','t-concept','data-pairs="Al-O,Mg-O"',[p+'/'+s for p in ['Al-O','Mg-O'] for s in ['ions','cross','reduce','check']]),
 ('nb','nameBuilder','t-concept','data-cases="K2S,FeCl3,FeCl2,AgCl,ZnO"',['K2S/parts','K2S/join','FeCl3/parts','FeCl3/numeral','FeCl3/join','FeCl2/parts','FeCl2/numeral','FeCl2/join','AgCl/parts','AgCl/join','ZnO/parts','ZnO/join']),
 ('sd','stockDetective','t-concept','data-cases="CuO,Cu2O,FeCl2"',[c+'/'+s for c in ['CuO','Cu2O','FeCl2'] for s in ['anion','total','metal','name']]),
 ('pi','polyIons','t-concept','',['NH4','OH','NO3','CO3','SO4','PO4']),
 ('pb','parenBus','t-concept','',['one','two','wrong']),
]
out=['<main id="stage">\n<div id="prog"><i></i></div>\n']
for sid,typ,tpl,extra,stages in SIMS:
    host=f'<div class="sim" id="{sid}-sim" data-sim="{typ}" {extra} aria-label="{typ} animation"></div>'
    if tpl=='t-concept':
        body=f'{host}\n    <div class="col"><div class="card"><p class="tag">{typ}</p><p class="small">{len(stages)} stages</p></div></div>'
    elif tpl=='t-concept wide':
        body=f'{host}\n    <div class="ptrow" style="border-top:3px dashed var(--line)"><p class="caprow" style="color:var(--muted)">band kept free for the rule or the check</p></div>'
    else:
        body=f'{host}\n    <p class="line small">{typ} · {len(stages)} stages</p>'
    fr=',\n    '.join("{stage:'%s-sim:%s',label:'%s'}"%(sid,s,s) for s in stages)
    out.append(f'''<section class="slide {tpl}" id="x-{sid}" data-title="Scratch: {typ}" data-sec="Step 5 scratch" data-ref="{typ}">
  <h2>Scratch: {typ}</h2>
  <div class="body">
    {body}
  </div>
  <script>Deck.frames('x-{sid}',[
    {fr}
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
open(os.path.join(os.path.dirname(__file__),'07-scratch-42.html'),'w').write('\n'.join(out))
print('scratch slides',len(SIMS),'stages',sum(len(x[4]) for x in SIMS))
