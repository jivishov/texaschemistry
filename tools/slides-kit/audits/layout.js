// Layout audit (teacher round, A3 and A4; RULES.md sections 3 and 11): on every frame, no option list wraps 2 + 1 (one row, stacked,
// or 2 x 2 for four), at most one third of the slide body is empty, no visible text is clipped or ellipsized (slide and footer), and
// nothing overlaps (the overlap check; README "The overlap check"):
//   DOM boxes   block-level text boxes, cards, chips, badges and the three footer spans on the current slide: no two intersect by more
//               than 2 px (1600 x 900 canvas px) in both directions; a box inside another (within 2 px) and ancestor pairs are not
//               intersections. Inline text (sup, sub, b, span, .es, inline formulas) is part of its nearest block, not a box of its own.
//   canvas      the label boxes the painter draws (text, chem, badge, fit) intersect no other label by more than 2 px, and no label
//               cuts a shape: circle, electron and badge are discs (inside: all four corners within r - 2 px of the centre; cut: the
//               box's nearest point within r - 2 px and not inside; a badge's own label is not tested against it), rrect a rectangle
//               (a label fully inside it is its label).
//               Inside one D.spheres scene nothing is tested (the depth order draws it); a label fully under an opaque shape drawn
//               after it is hidden (counted as a covered label, not tested). Recorded by test-time instrumentation of Deck.canvasSim
//               and Deck.spheres (instrument() below); the runtime is not changed.
// Measured after the frame settles (reduced motion: stages at their end state; 100 ms, then until the .acc compaction is stable), and
// for every frame whose visible animation reports a live stage, again with motion on at two moments (1.4 s and 2.4 s after Deck.go;
// tagged s<N>f<F>@live1 and @live2).
// A reference deck's accepted intersections are listed in its registry overlap_baseline file (frame, A and B strings); a hit that
// matches an entry is baselined and does not fail; entries no hit matches are printed as stale. A deck without a baseline fails on
// any intersection.
// Usage: node audits/layout.js [light|dark] (default light). Writes layout-<theme>.json, overlap-<theme>.txt (every frame with
// intersections, its boxes, and the covered labels, spheres scenes and live frames; or "no intersections, N frames, M boxes") and
// cropped JPEGs of up to six failing frames in overlap-<theme>/.
const L=require('./lib'),fs=require('fs'),path=require('path');
const EMAX=process.env.EMPTY_MAX?+process.env.EMPTY_MAX:1/3;
const TOL=2,SHOTS=6,LIVE1=1400,LIVE2=1000;
const KIT=path.join(__dirname,'..'),REPO=path.join(KIT,'..','..');

/* Runs in the page before the deck's scripts (page.addInitScript). The runtime assigns window.Deck first and Deck.canvasSim and
   Deck.spheres after it: a setter on window.Deck installs setters on the Deck object's canvasSim and spheres.
   The wrapped canvasSim(host, spec) replaces spec.draw so the animation paints through a proxy of the painter g. Every on-screen paint
   stores host.__boxes = {labels, shapes, stage, scenes} in host px (cleared at the start of the paint) and host.__live (the spec's
   live(stage)); off-screen renders (bounds() measures on a detached canvas) are not recorded.
   The wrapped spheres(g, scene, view) numbers its call within the paint: every label and shape recorded during it carries that scene.
   label box: x from the call's x and align, width from ctx.measureText with the font the painter set (chem: the width it returns;
   fit: the drawn width), y from y and the baseline (middle: centred), height the font size. shape: circle r (+ half the stroke),
   electron the dot (r, default 13, + its 3 px stroke; not the faint halo) and badge its circle are discs (centre and radius, and their
   box); rrect x, y, w, h (+ half the stroke) is a rectangle. Each record carries its paint order i; a shape is opaque when its fill
   alpha (a colour string as the canvas reads it back; a gradient its least opaque stop) and globalAlpha are both 0.9 or more.
   Calls drawn with globalAlpha at or below 0.01 are invisible and not recorded. */
function instrument(){
  let deck=null,sx=null;
  const alpha=c=>{
    if(typeof c==='string'&&c){if(!sx)sx=document.createElement('canvas').getContext('2d');sx.fillStyle='rgba(0,0,0,0)';sx.fillStyle=c;const v=sx.fillStyle;
      if(v[0]==='#')return 1;const m=v.match(/\(([^)]*)\)/),a=m&&m[1].split(',')[3];return a==null?1:parseFloat(a)}
    if(typeof CanvasGradient!=='undefined'&&c instanceof CanvasGradient)return c.__ovlA==null?0:c.__ovlA;
    return 0};
  if(typeof CanvasGradient!=='undefined'){const acs=CanvasGradient.prototype.addColorStop;
    CanvasGradient.prototype.addColorStop=function(o,col){const a=alpha(String(col));this.__ovlA=this.__ovlA==null?a:Math.min(this.__ovlA,a);return acs.call(this,o,col)}}
  const wrap=cs=>function(host,spec){
    if(host&&spec&&typeof spec.draw==='function'){const draw=spec.draw;host.__ovlWrapped=1;
      spec.draw=function(g,p,info){
        const ctx=g&&g.ctx;
        if(!ctx||!ctx.canvas||ctx.canvas.parentNode!==host)return draw.apply(this,arguments);
        const rec={labels:[],shapes:[],stage:info&&info.stage,n:0,sc:0,scenes:0};host.__boxes=rec;
        host.__live=!!(spec.live&&spec.live(info&&info.stage));
        const base=ctx.getTransform().inverse(),M=()=>base.multiply(ctx.getTransform());
        const box=(x0,y0,x1,y1)=>{const m=M();let a=Infinity,b=Infinity,c=-Infinity,d=-Infinity;
          for(const [x,y] of [[x0,y0],[x1,y0],[x0,y1],[x1,y1]]){const q=m.transformPoint(new DOMPoint(x,y));a=Math.min(a,q.x);b=Math.min(b,q.y);c=Math.max(c,q.x);d=Math.max(d,q.y)}
          return {x0:a,y0:b,x1:c,y1:d}};
        const seen=()=>ctx.globalAlpha>.01;
        const label=(kind,s,x0,y0,w,h,own)=>{s=String(s);if(seen()&&w>0&&h>0&&s.trim())rec.labels.push(Object.assign({kind,text:s,i:rec.n++,scene:rec.sc,own},box(x0,y0,x0+w,y0+h)))};
        const shape=(kind,x0,y0,x1,y1,fill,disc)=>{if(!seen()||!(x1>x0&&y1>y0))return null;
          const s=Object.assign({kind,i:rec.n++,scene:rec.sc,opaque:alpha(fill)>=.9&&ctx.globalAlpha>=.9},box(x0,y0,x1,y1));
          if(disc){const m=M(),c=m.transformPoint(new DOMPoint(disc[0],disc[1]));s.disc={cx:c.x,cy:c.y,r:disc[2]*Math.sqrt(Math.abs(m.a*m.d-m.b*m.c))}}
          rec.shapes.push(s);return s.i};
        const ax=(x,w,al)=>al==='left'||al==='start'?x:al==='right'||al==='end'?x-w:x-w/2;
        const ay=(y,h,b)=>b==='top'||b==='hanging'?y:b==='bottom'||b==='ideographic'?y-h:b==='alphabetic'?y-.8*h:y-h/2;
        const W={
          text(s,x,y,px,o){const r=g.text(s,x,y,px,o);o=o||{};const w=ctx.measureText(String(s)).width;label('text',s,ax(x,w,o.align||'center'),ay(y,px,o.base||'middle'),w,px);return r},
          chem(s,x,y,px,o){const w=g.chem(s,x,y,px,o);o=o||{};label('chem',s,o.align==='left'?x:o.align==='right'?x-w:x-w/2,y-px/2,w,px);return w},
          /* the painter draws the badge's circle, then its text: the shape is recorded first, and the label is its own (never tested
             against that disc: one call draws both, and the label box is the font's em box, taller than the glyphs) */
          badge(x,y,txt,col,r){const out=g.badge(x,y,txt,col,r);const R=r||36,px=Math.max(36,R*1.1),w=ctx.measureText(String(txt)).width;
            const own=shape('badge',x-R,y-R,x+R,y+R,col,[x,y,R]);label('badge',txt,x-w/2,y+2-px/2,w,px,own);return out},
          fit(s,x,y,px,maxW,o){const ok=g.fit(s,x,y,px,maxW,o);if(ok){const w=Math.min(ctx.measureText(String(s)).width,maxW);label('fit',s,x-w/2,y-px/2,w,px)}return ok},
          circle(x,y,r,fill,stroke,lw){const out=g.circle(x,y,r,fill,stroke,lw);if((fill||stroke)&&r>0){const R=r+(stroke?(lw||3)/2:0);shape('circle',x-R,y-R,x+R,y+R,fill,[x,y,R])}return out},
          rrect(x,y,w,h,r,fill,stroke,lw){const out=g.rrect(x,y,w,h,r,fill,stroke,lw);if(fill||stroke){const e=stroke?(lw||3)/2:0;shape('rrect',Math.min(x,x+w)-e,Math.min(y,y+h)-e,Math.max(x,x+w)+e,Math.max(y,y+h)+e,fill,null)}return out},
          electron(x,y,r){const out=g.electron(x,y,r);const R=(r||13)+1.5;shape('electron',x-R,y-R,x+R,y+R,deck&&deck.tok?deck.tok('e'):null,[x,y,R]);return out}};
        return draw.call(this,new Proxy(g,{get:(t,k)=>k==='__ovlRec'?rec:Object.prototype.hasOwnProperty.call(W,k)?W[k]:t[k]}),p,info)};
    }
    return cs.call(this,host,spec)};
  /* a spheres call on an instrumented painter is one scene: its records carry the scene number */
  const wrapS=sp=>function(g){const r=g&&g.__ovlRec;if(!r||r.sc)return sp.apply(this,arguments);
    r.sc=++r.scenes;try{return sp.apply(this,arguments)}finally{r.sc=0}};
  const hook=(v,name,w)=>{let f=typeof v[name]==='function'?w(v[name]):v[name];
    Object.defineProperty(v,name,{configurable:true,enumerable:true,get:()=>f,set(x){f=typeof x==='function'?w(x):x}})};
  Object.defineProperty(window,'Deck',{configurable:true,enumerable:true,get:()=>deck,set(v){deck=v;if(!v||typeof v!=='object')return;
    hook(v,'canvasSim',wrap);hook(v,'spheres',wrapS)}});
}

/* the frame has settled when the boxes of the .acc cards, the options and the footer are the same two animation frames apart */
async function settle(page){
  const sig=()=>page.evaluate(()=>{const S=document.querySelector('.slide.current');
    return [...S.querySelectorAll('.acc>*,.opts>*'),...document.querySelectorAll('#foot>span')].map(e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.width,r.height].map(v=>Math.round(v*10)).join()}).join('|')+'|'+S.scrollHeight});
  let a=await sig();
  for(let i=0;i<15;i++){await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));const b=await sig();if(a===b)return true;a=b}
  return false;
}

/* the overlap check on the current frame; boxes in 1600 x 900 canvas px */
const overlap=page=>page.evaluate(tol=>{
  const st=document.getElementById('stage').getBoundingClientRect(),k=st.width/1600,S=document.querySelector('.slide.current');
  const CARD='.card,.phase,.wcard,.item,.key,.colh,.cer-box',CHIP='.chip,.badge,.es,.rail li,.legend>span,.scale span,.opt',FOOT='#sec,#cue,#count',
    TEXT='p,li,td,th,h2,.line,.cell,.rh,.q,.ans,.fb,.tag,.term,.mean,.k,.small,.cap,.nm,.fm,.bt,.why,.big,.hdr',
    SKIP='.notes,script,style,svg,.zoomed,.timer:not(.run)';
  const memo=new Map(),css=e=>{let c=memo.get(e);if(!c){c=getComputedStyle(e);memo.set(e,c)}return c};
  const opa=e=>{let o=1;for(let x=e;x&&x.nodeType===1;x=x.parentElement)o*=parseFloat(css(x).opacity);return o};
  const vis=e=>{const c=css(e);return c.visibility==='visible'&&c.display!=='none'&&opa(e)>0};
  const sized=r=>r.width>0&&r.height>0;
  const any=e=>{const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode()))if(n.nodeValue.trim()&&vis(n.parentElement))return true;return false};
  const cv=r=>({x0:(r.left-st.left)/k,y0:(r.top-st.top)/k,x1:(r.right-st.left)/k,y1:(r.bottom-st.top)/k});
  const txt=s=>{s=String(s).replace(/\s+/g,' ').trim();return s.length>32?s.slice(0,31)+'…':s};
  const nm=e=>{const p=e.id?null:e.parentElement&&e.parentElement.closest('[id]');
    return (e.id?'#'+e.id:'<'+e.tagName.toLowerCase()+(typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/).join('.'):'')+'>')+
      (p&&p!==S&&p.id!=='stage'?' in #'+p.id:'')+' "'+txt(e.textContent)+'"'};
  const inside=(a,b)=>a.x0>=b.x0-tol&&a.x1<=b.x1+tol&&a.y0>=b.y0-tol&&a.y1<=b.y1+tol;
  const cut=(a,b)=>{const ox=Math.min(a.x1,b.x1)-Math.max(a.x0,b.x0),oy=Math.min(a.y1,b.y1)-Math.max(a.y0,b.y0);return ox>tol&&oy>tol?{ox,oy}:null};
  /* block-level boxes only: block, flex, grid, list-item, table-cell, table-row, and an inline-block (inline-flex, inline-grid) that is
     a card, chip, badge, option or footer span; the text of anything else belongs to its nearest such ancestor */
  const BLK=new Set(['block','flex','grid','list-item','table-cell','table-row']),IB=new Set(['inline-block','inline-flex','inline-grid']),NAMED=CARD+','+CHIP+','+FOOT;
  const bm=new Map(),boxy=e=>{let v=bm.get(e);if(v===undefined){const d=css(e).display;v=BLK.has(d)||IB.has(d)&&e.matches(NAMED);bm.set(e,v)}return v};
  const owners=new Set(),roots=[S,...document.querySelectorAll(FOOT)];
  for(const root of roots){const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n;
    while((n=w.nextNode())){if(!n.nodeValue.trim())continue;let e=n.parentElement;if(!e||e.closest(SKIP)||!vis(e))continue;
      const g=document.createRange();g.selectNodeContents(n);if(![...g.getClientRects()].some(sized))continue;
      while(e&&e!==root&&!boxy(e))e=e.parentElement;if(e)owners.add(e)}}
  const hits=[],boxes=[];
  for(const e of [...S.querySelectorAll('*'),...document.querySelectorAll(FOOT)]){
    if(e.closest(SKIP)||!boxy(e))continue;
    const kind=e.matches(FOOT)?'footer':e.matches(CARD)?'card':e.matches(CHIP)?'chip':(owners.has(e)||e.matches(TEXT)&&any(e))?'text':null;
    if(!kind||!vis(e))continue;
    const r=e.getBoundingClientRect();if(sized(r))boxes.push({e,kind,r:cv(r)});
  }
  for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const A=boxes[i],B=boxes[j];
    if(A.e.contains(B.e)||B.e.contains(A.e))continue;
    const c=cut(A.r,B.r);
    if(c&&!inside(A.r,B.r)&&!inside(B.r,A.r))hits.push({kind:'dom',a:A.kind+' '+nm(A.e),b:B.kind+' '+nm(B.e),ox:c.ox,oy:c.oy,ra:A.r,rb:B.r});
  }
  /* canvas: discs for circle, electron and badge; rrect a rectangle */
  const corners=l=>[[l.x0,l.y0],[l.x1,l.y0],[l.x0,l.y1],[l.x1,l.y1]];
  const inDisc=(l,d,R)=>corners(l).every(([x,y])=>Math.hypot(x-d.cx,y-d.cy)<=R);
  const discCut=(l,s)=>{const d=s.disc,R=d.r-tol;if(R<=0||inDisc(l,d,R))return null;
    const nx=Math.min(Math.max(d.cx,l.x0),l.x1),ny=Math.min(Math.max(d.cy,l.y0),l.y1);if(Math.hypot(nx-d.cx,ny-d.cy)>R)return null;
    return {ox:Math.max(0,Math.min(l.x1,s.x1)-Math.max(l.x0,s.x0)),oy:Math.max(0,Math.min(l.y1,s.y1)-Math.max(l.y0,s.y0))}};
  const under=(l,s)=>s.disc?inDisc(l,s.disc,s.disc.r+tol):inside(l,s);
  const sameScene=(a,b)=>a.scene&&a.scene===b.scene;
  let labels=0,shapes=0,dup=0,hosts=0,covered=0;const unrec=[],live=[],scenes=[],hidden=[];
  for(const h of S.querySelectorAll('.sim[data-sim]')){
    const c=h.querySelector(':scope>canvas');if(!c||!vis(h)||!sized(h.getBoundingClientRect()))continue;
    if(!h.__boxes){unrec.push(h.id);continue}hosts++;if(h.__live)live.push(h.id);
    const r=c.getBoundingClientRect(),o=cv(r),q=r.width/k/(c.clientWidth||1),T=b=>({x0:o.x0+b.x0*q,y0:o.y0+b.y0*q,x1:o.x0+b.x1*q,y1:o.y0+b.y1*q});
    const B=h.__boxes,where='canvas #'+h.id+' ['+B.stage+']';
    const labs=[];   /* one label drawn twice at the same place is one label (its last drawing counts for the paint order) */
    B.labels.forEach(l=>{const m=labs.find(m=>m.text===l.text&&Math.abs(m.x0-l.x0)<.5&&Math.abs(m.y0-l.y0)<.5&&Math.abs(m.x1-l.x1)<.5&&Math.abs(m.y1-l.y1)<.5);
      if(m){dup++;m.i=Math.max(m.i,l.i)}else labs.push(Object.assign({},l))});
    labels+=labs.length;shapes+=B.shapes.length;
    /* a label fully under an opaque shape drawn after it is hidden: counted, not tested */
    const shown=[];
    for(const l of labs){const s=B.shapes.find(s=>s.i>l.i&&s.opaque&&under(l,s));
      if(s){covered++;hidden.push(where+': label "'+txt(l.text)+'" under '+s.kind)}else shown.push(l)}
    for(let i=0;i<shown.length;i++)for(let j=i+1;j<shown.length;j++){if(sameScene(shown[i],shown[j]))continue;const x=cut(shown[i],shown[j]);
      if(x)hits.push({kind:'label',a:where+': label "'+txt(shown[i].text)+'"',b:'label "'+txt(shown[j].text)+'"',ox:x.ox,oy:x.oy,ra:T(shown[i]),rb:T(shown[j])})}
    for(const l of shown)for(const s of B.shapes){if(sameScene(l,s)||l.own!=null&&l.own===s.i)continue;const x=s.disc?discCut(l,s):(cut(l,s)&&!inside(l,s)?cut(l,s):null);
      if(x)hits.push({kind:s.disc?'disc':'rrect',a:where+': label "'+txt(l.text)+'"',b:s.kind,ox:x.ox,oy:x.oy,ra:T(l),rb:T(s)})}
    /* each spheres scene and the box of everything it drew */
    for(let n=1;n<=(B.scenes||0);n++){const m=[...labs,...B.shapes].filter(x=>x.scene===n);if(!m.length)continue;
      scenes.push({where,n,box:T({x0:Math.min(...m.map(x=>x.x0)),y0:Math.min(...m.map(x=>x.y0)),x1:Math.max(...m.map(x=>x.x1)),y1:Math.max(...m.map(x=>x.y1))})})}
  }
  const R=b=>[b.x0,b.y0,b.x1,b.y1].map(v=>Math.round(v));
  return {dom:boxes.length,labels,shapes,dup,hosts,covered,hidden,live,unrec,scenes:scenes.map(s=>Object.assign(s,{box:R(s.box)})),
    hits:hits.map(h=>Object.assign(h,{ox:Math.round(h.ox),oy:Math.round(h.oy),ra:R(h.ra),rb:R(h.rb)}))};
},TOL);

/* the registry's overlap_baseline for the deck under audit (matched by its path), or null; a named file that cannot be read is an error */
function baseline(){
  let d=null;try{d=JSON.parse(fs.readFileSync(path.join(KIT,'registry.json'),'utf8')).decks.find(x=>x.file&&path.resolve(REPO,x.file)===L.DECK)}catch(e){}
  if(!d||!d.overlap_baseline)return null;
  try{const j=JSON.parse(fs.readFileSync(path.join(KIT,d.overlap_baseline),'utf8')),list=Array.isArray(j)?j:j.entries;
    if(!Array.isArray(list))throw new Error('no entries list');return {name:d.overlap_baseline,list,used:new Set()}}
  catch(e){return {name:d.overlap_baseline,list:[],used:new Set(),error:e.message}}
}
const bkey=(frame,a,b)=>frame+'\n'+a+'\n'+b;

module.exports={instrument,settle,overlap,baseline,TOL};
if(require.main===module)(async()=>{
  const theme=process.argv[2]||'light';
  const {browser,page,errors}=await L.open({reduced:true,theme,init:instrument});
  const nf=await page.evaluate(()=>Deck.slides.map(S=>S.frames.length));
  const rec=[],fails=[];let lists=0;
  const base=baseline(),keys=new Set(base?base.list.map(e=>bkey(e.frame,e.a,e.b)):[]);
  if(base&&base.error)fails.push(`overlap: baseline ${base.name} cannot be read (${base.error})`);
  const ov={dom:0,labels:0,shapes:0,dup:0,covered:0,unsettled:[],frames:[],hidden:[],scenes:[],live:[],moments:[]};
  /* one overlap measurement: fails for every hit the baseline does not list */
  const take=(tag,s,f,x)=>{
    x.unrec.forEach(id=>fails.push(`${tag}: overlap: canvas #${id} has no recorded paint (instrumentation)`));
    x.hits.forEach(h=>{h.frame=tag;const kk=bkey(tag,h.a,h.b);h.baselined=keys.has(kk);if(h.baselined)base.used.add(kk);
      else fails.push(`${tag}: ${h.a} ∩ ${h.b} (${h.ox} × ${h.oy} px)`)});
    ov.covered+=x.covered;x.hidden.forEach(t=>ov.hidden.push(tag+' '+t));x.scenes.forEach(c=>ov.scenes.push({frame:tag,where:c.where,n:c.n,box:c.box}));
    if(x.hits.length)ov.frames.push({tag,s,f,hits:x.hits});
  };
  for(let s=0;s<nf.length;s++)for(let f=0;f<nf[s];f++){
    await page.evaluate(([s,f])=>Deck.go(s,f),[s,f]);await L.wait(page,100);
    const o=await page.evaluate(()=>[...document.querySelectorAll('.slide.current .opts')].filter(x=>x.getClientRects().length&&getComputedStyle(x).visibility==='visible').map(x=>{
      const r=[...x.children].map(c=>c.getBoundingClientRect()),tops=[...new Set(r.map(q=>Math.round(q.top/4)))],lefts=[...new Set(r.map(q=>Math.round(q.left/4)))];
      const per=tops.map(t=>r.filter(q=>Math.round(q.top/4)===t).length);
      return {id:x.closest('[id]').id,n:r.length,rows:tops.length,per,shape:tops.length===1?'row':tops.length===r.length&&lefts.length===1?'stacked':r.length===4&&per.join()==='2,2'?'2x2':'wrap '+per.join('+')}}));
    const em=await L.emptiness(page),cl=await L.clipped(page);lists+=o.length;
    /* canvas text drawn past the edge of its animation would be cut off too */
    const ct=await page.evaluate(()=>Deck.slides[Deck.cur.s].sims.filter(x=>x.outText>0).map(x=>x.id+' '+x.outText));
    ct.forEach(c=>fails.push(`s${s+1}f${f}: canvas text cut at the edge in ${c}`));
    cl.forEach(c=>fails.push(`s${s+1}f${f}: clipped text in ${c.el} (${c.sw}x${c.sh} in ${c.cw}x${c.ch})`));
    o.forEach(x=>{if(x.shape.startsWith('wrap'))fails.push(`s${s+1}f${f} ${x.id}: options ${x.shape}`)});
    if(em>EMAX)fails.push(`s${s+1}f${f}: ${Math.round(em*100)}% of the slide body is empty (gate ${Math.round(EMAX*100)}%)`);
    /* the overlap check, after the frame settles */
    if(!await settle(page))ov.unsettled.push(`s${s+1}f${f}`);
    const x=await overlap(page);
    ov.dom+=x.dom;ov.labels+=x.labels;ov.shapes+=x.shapes;ov.dup+=x.dup;
    take(`s${s+1}f${f}`,s+1,f,x);
    if(x.live.length)ov.live.push({s:s+1,f,ids:x.live});
    rec.push({s:s+1,f,empty:em,opts:o,overlap:{dom:x.dom,labels:x.labels,shapes:x.shapes,canvases:x.hosts,covered:x.covered,scenes:x.scenes.length,live:x.live,hits:x.hits.length}});
  }
  /* every canvas animation of the deck must have been wrapped, or its labels were never measured */
  const wr=await page.evaluate(()=>{const h=[...document.querySelectorAll('.sim[data-sim]')].filter(x=>x.querySelector(':scope>canvas'));return {n:h.length,miss:h.filter(x=>!x.__ovlWrapped).map(x=>x.id)}});
  if(wr.miss.length)fails.push(`overlap: canvas instrumentation missed ${wr.miss.length} of ${wr.n} canvas animations (${wr.miss.join(', ')})`);
  if(ov.unsettled.length)console.log(`  (layout did not settle within 15 animation frames on ${ov.unsettled.join(', ')}; measured anyway)`);
  /* the motion-on pass: every frame whose visible animation reported a live stage, in a second context with motion on, at two moments */
  let lv=null;
  if(ov.live.length){lv=await L.open({browser,reduced:false,theme,init:instrument});
    for(const fr of ov.live){await lv.page.evaluate(([s,f])=>Deck.go(s,f),[fr.s-1,fr.f]);
      for(const [m,ms] of [[1,LIVE1],[2,LIVE2]]){await L.wait(lv.page,ms);const x=await overlap(lv.page),tag=`s${fr.s}f${fr.f}@live${m}`;
        take(tag,fr.s,fr.f,x);ov.moments.push({frame:tag,dom:x.dom,labels:x.labels,shapes:x.shapes,canvases:x.hosts,covered:x.covered,scenes:x.scenes.length,hits:x.hits.length})}}}
  /* crops of up to six frames with failing intersections, one per slide first, both boxes outlined (A red, B blue); a live moment is
     cropped in the motion-on context at the same delay, so moving shapes may sit a little off their outlines */
  const shots=[],bad=ov.frames.map(fr=>Object.assign({},fr,{hits:fr.hits.filter(h=>!h.baselined)})).filter(fr=>fr.hits.length);
  if(bad.length){const dir=L.ensure(path.join(L.OUT,'overlap-'+theme));fs.readdirSync(dir).forEach(f=>fs.unlinkSync(path.join(dir,f)));
    const pick=[];bad.forEach(fr=>{if(pick.length<SHOTS&&!pick.some(p=>p.s===fr.s))pick.push(fr)});
    bad.forEach(fr=>{if(pick.length<SHOTS&&!pick.includes(fr))pick.push(fr)});
    for(const fr of pick){const m=fr.tag.match(/@live(\d)$/),pg=m?lv.page:page;
      await pg.evaluate(([s,f])=>Deck.go(s,f),[fr.s-1,fr.f]);
      if(m)await L.wait(pg,m[1]==='1'?LIVE1:LIVE1+LIVE2);else{await L.wait(pg,100);await settle(pg)}
      const clip=await pg.evaluate(hits=>{const st=document.getElementById('stage').getBoundingClientRect(),k=st.width/1600;
        const h0=hits[0],x0=Math.max(0,Math.min(h0.ra[0],h0.rb[0])-120),y0=Math.max(0,Math.min(h0.ra[1],h0.rb[1])-120),x1=Math.min(1600,Math.max(h0.ra[2],h0.rb[2])+120),y1=Math.min(900,Math.max(h0.ra[3],h0.rb[3])+120);
        hits.slice(0,8).forEach(h=>[[h.ra,'#e0182d'],[h.rb,'#1f5fff']].forEach(([r,c])=>{const d=document.createElement('div');d.className='ovl-mark';
          d.style.cssText=`position:fixed;z-index:2147483647;pointer-events:none;box-sizing:border-box;border:3px solid ${c};left:${st.left+r[0]*k}px;top:${st.top+r[1]*k}px;width:${(r[2]-r[0])*k}px;height:${(r[3]-r[1])*k}px`;
          document.body.appendChild(d)}));
        return {x:st.left+x0*k,y:st.top+y0*k,width:(x1-x0)*k,height:(y1-y0)*k}},fr.hits);
      const file=`${fr.tag.replace('@','-')}.jpg`;await pg.screenshot({path:path.join(dir,file),type:'jpeg',quality:80,clip});
      await pg.evaluate(()=>document.querySelectorAll('.ovl-mark').forEach(d=>d.remove()));
      shots.push('overlap-'+theme+'/'+file);
    }
  }
  if(lv)errors.push(...lv.errors.map(e=>'(motion on) '+e));
  if(errors.length)fails.push('console errors: '+errors.join(' | '));
  const all=ov.frames.flatMap(fr=>fr.hits),nh=all.length,nbl=all.filter(h=>h.baselined).length,nb=ov.dom+ov.labels+ov.shapes;
  const stale=base?base.list.filter(e=>!base.used.has(bkey(e.frame,e.a,e.b))):[];
  const byKind={};all.forEach(h=>{byKind[h.kind]=(byKind[h.kind]||0)+1});
  const boxesTxt=`${nb} boxes (${ov.dom} DOM boxes, ${ov.labels} canvas labels, ${ov.shapes} canvas shapes${ov.dup?', '+ov.dup+' repeated canvas labels counted once':''})`;
  const extraTxt=`${ov.covered} covered canvas labels, ${ov.scenes.length} spheres scenes (live moments included)`;
  const liveTxt=`live: ${ov.live.length} frames at two moments`;
  const baseTxt=base?`${nbl} baselined (${base.name}, ${base.list.length} entries, ${stale.length} stale), ${nh-nbl} not in the baseline`:'no baseline';
  const kindTxt=Object.entries(byKind).map(([k,v])=>k+' '+v).join(', ');
  const sec=(title,lines)=>lines.length?`${title}\n${lines.map(l=>'  - '+l).join('\n')}\n`:'';
  fs.writeFileSync(path.join(L.OUT,'overlap-'+theme+'.txt'),
    (!nh?`no intersections, ${rec.length} frames, ${boxesTxt}; ${extraTxt}; ${liveTxt}${base?'; '+baseTxt:''}\n`:
    `${process.env.DECKNAME||path.basename(L.DECK)} ${theme}: ${nh} intersections on ${ov.frames.length} frames (${rec.length} frames and ${ov.moments.length} live moments measured; ${kindTxt}); ${baseTxt}; ${boxesTxt}; ${extraTxt}; ${liveTxt}; boxes as [x0, y0, x1, y1] in 1600 x 900 canvas px\n`+
    ov.frames.map(fr=>`${fr.tag}: ${fr.hits.length} intersection${fr.hits.length>1?'s':''}\n`+fr.hits.map(h=>`  - ${h.a} ∩ ${h.b} (${h.ox} × ${h.oy} px)  A [${h.ra.join(', ')}]  B [${h.rb.join(', ')}]${h.baselined?'  [baselined]':''}`).join('\n')).join('\n')+'\n')+
    sec(`stale baseline entries (${stale.length}; listed in ${base?base.name:''}, matched by no hit; not a failure):`,stale.map(e=>`${e.frame}: ${e.a} ∩ ${e.b}`))+
    sec(`live frames (${ov.live.length}; measured with motion on 1.4 s and 2.4 s after Deck.go):`,ov.live.map(fr=>`s${fr.s}f${fr.f}: ${fr.ids.map(i=>'#'+i).join(', ')}; `+ov.moments.filter(m=>m.frame.startsWith(`s${fr.s}f${fr.f}@`)).map(m=>`${m.frame.split('@')[1]} ${m.hits} intersection${m.hits===1?'':'s'}`).join(', ')))+
    sec(`covered canvas labels (${ov.hidden.length}; fully under an opaque shape drawn later, so hidden; not tested, not a failure):`,ov.hidden)+
    sec(`spheres scenes (${ov.scenes.length}; nothing inside one scene is tested against the same scene):`,ov.scenes.map(c=>`${c.frame} ${c.where}: scene ${c.n} [${c.box.join(', ')}]`))+
    (shots.length?`crops (A red, B blue): ${shots.join(', ')}\n`:''));
  const sh={};rec.forEach(r=>r.opts.forEach(x=>{sh[x.shape]=(sh[x.shape]||0)+1}));
  const worst=rec.reduce((a,r)=>r.empty>a.empty?r:a,rec[0]);
  L.save('layout-'+theme+'.json',{theme,frames:rec.length,fails,overlap:{intersections:nh,frames:ov.frames.length,kinds:byKind,baselined:nbl,
    baseline:base?{file:base.name,entries:base.list.length,stale}:null,dom:ov.dom,labels:ov.labels,shapes:ov.shapes,repeated:ov.dup,covered:ov.covered,
    hidden:ov.hidden,scenes:ov.scenes,live:ov.live,moments:ov.moments,canvases:wr.n,unsettled:ov.unsettled,failing:ov.frames,shots},rec});
  console.log(`layout ${theme}: ${rec.length} frames, ${lists} visible option lists (${Object.entries(sh).map(([k,v])=>k+' '+v).join(', ')}), max empty ${Math.round(worst.empty*100)}% (s${worst.s}f${worst.f}), gate ${Math.round(EMAX*100)}%, clipped or ellipsized text: ${fails.filter(f=>/clipped text/.test(f)).length}, overlap: ${nh} intersections on ${ov.frames.length} frames, ${baseTxt} (${boxesTxt}, ${extraTxt}, ${wr.n-wr.miss.length} of ${wr.n} canvas animations instrumented), ${liveTxt}, ${fails.length?'FAIL':'PASS'}`);fails.forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
