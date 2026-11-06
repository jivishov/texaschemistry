// Layout audit (teacher round, A3 and A4; RULES.md sections 3 and 11): on every frame, no option list wraps 2 + 1 (one row, stacked,
// or 2 x 2 for four), at most one third of the slide body is empty, no visible text is clipped or ellipsized (slide and footer), and
// nothing overlaps (the overlap check; README "The overlap check"):
//   DOM boxes   text lines, cards, chips, badges and the three footer spans on the current slide: no two intersect by more than 2 px
//               (1600 x 900 canvas px) in both directions; a box inside another (within 2 px) and ancestor pairs are not intersections.
//   canvas      the label boxes the painter draws (text, chem, badge, fit) intersect no other label by more than 2 px, and no label
//               partly cuts a shape (circle, rrect, electron, badge): a label fully inside one shape is that shape's label. Recorded
//               by test-time instrumentation of Deck.canvasSim (instrument() below); the runtime is not changed.
// Measured after the frame settles (reduced motion: stages at their end state; 100 ms, then until the .acc compaction is stable).
// Usage: node audits/layout.js [light|dark] (default light). Writes layout-<theme>.json, overlap-<theme>.txt (every failing frame with
// its boxes, or "no intersections, N frames, M boxes") and cropped JPEGs of up to six failing frames in overlap-<theme>/.
const L=require('./lib'),fs=require('fs'),path=require('path');
const EMAX=process.env.EMPTY_MAX?+process.env.EMPTY_MAX:1/3;
const TOL=2,SHOTS=6;

/* Runs in the page before the deck's scripts (page.addInitScript). The runtime assigns window.Deck first and Deck.canvasSim after it:
   a setter on window.Deck installs a setter on the Deck object's canvasSim, and the wrapped canvasSim(host, spec) replaces spec.draw
   so the animation paints through a proxy of the painter g. Every on-screen paint stores host.__boxes = {labels, shapes, stage} in
   host px (cleared at the start of the paint); off-screen renders (bounds() measures on a detached canvas) are not recorded.
   label box: x from the call's x and align, width from ctx.measureText with the font the painter set (chem: the width it returns;
   fit: the drawn width), y from y and the baseline (middle: centred), height the font size. shape box: circle r (+ half the stroke),
   rrect x, y, w, h (+ half the stroke), electron the dot (r, default 13, + its 3 px stroke; not the faint halo), badge its circle.
   Calls drawn with globalAlpha at or below 0.01 are invisible and not recorded. D.spheres draws through the same g, so it is covered. */
function instrument(){
  let deck=null;
  const wrap=cs=>function(host,spec){
    if(host&&spec&&typeof spec.draw==='function'){const draw=spec.draw;host.__ovlWrapped=1;
      spec.draw=function(g,p,info){
        const ctx=g&&g.ctx;
        if(!ctx||!ctx.canvas||ctx.canvas.parentNode!==host)return draw.apply(this,arguments);
        const rec={labels:[],shapes:[],stage:info&&info.stage};host.__boxes=rec;
        const base=ctx.getTransform().inverse();
        const box=(x0,y0,x1,y1)=>{const M=base.multiply(ctx.getTransform());let a=Infinity,b=Infinity,c=-Infinity,d=-Infinity;
          for(const [x,y] of [[x0,y0],[x1,y0],[x0,y1],[x1,y1]]){const q=M.transformPoint(new DOMPoint(x,y));a=Math.min(a,q.x);b=Math.min(b,q.y);c=Math.max(c,q.x);d=Math.max(d,q.y)}
          return {x0:a,y0:b,x1:c,y1:d}};
        const seen=()=>ctx.globalAlpha>.01;
        const label=(kind,s,x0,y0,w,h)=>{s=String(s);if(seen()&&w>0&&h>0&&s.trim())rec.labels.push(Object.assign({kind,text:s},box(x0,y0,x0+w,y0+h)))};
        const shape=(kind,x0,y0,x1,y1)=>{if(seen()&&x1>x0&&y1>y0)rec.shapes.push(Object.assign({kind},box(x0,y0,x1,y1)))};
        const ax=(x,w,al)=>al==='left'||al==='start'?x:al==='right'||al==='end'?x-w:x-w/2;
        const ay=(y,h,b)=>b==='top'||b==='hanging'?y:b==='bottom'||b==='ideographic'?y-h:b==='alphabetic'?y-.8*h:y-h/2;
        const W={
          text(s,x,y,px,o){const r=g.text(s,x,y,px,o);o=o||{};const w=ctx.measureText(String(s)).width;label('text',s,ax(x,w,o.align||'center'),ay(y,px,o.base||'middle'),w,px);return r},
          chem(s,x,y,px,o){const w=g.chem(s,x,y,px,o);o=o||{};label('chem',s,o.align==='left'?x:o.align==='right'?x-w:x-w/2,y-px/2,w,px);return w},
          badge(x,y,txt,col,r){const out=g.badge(x,y,txt,col,r);const R=r||36,px=Math.max(36,R*1.1),w=ctx.measureText(String(txt)).width;
            label('badge',txt,x-w/2,y+2-px/2,w,px);shape('badge',x-R,y-R,x+R,y+R);return out},
          fit(s,x,y,px,maxW,o){const ok=g.fit(s,x,y,px,maxW,o);if(ok){const w=Math.min(ctx.measureText(String(s)).width,maxW);label('fit',s,x-w/2,y-px/2,w,px)}return ok},
          circle(x,y,r,fill,stroke,lw){const out=g.circle(x,y,r,fill,stroke,lw);if((fill||stroke)&&r>0){const R=r+(stroke?(lw||3)/2:0);shape('circle',x-R,y-R,x+R,y+R)}return out},
          rrect(x,y,w,h,r,fill,stroke,lw){const out=g.rrect(x,y,w,h,r,fill,stroke,lw);if(fill||stroke){const e=stroke?(lw||3)/2:0;shape('rrect',Math.min(x,x+w)-e,Math.min(y,y+h)-e,Math.max(x,x+w)+e,Math.max(y,y+h)+e)}return out},
          electron(x,y,r){const out=g.electron(x,y,r);const R=(r||13)+1.5;shape('electron',x-R,y-R,x+R,y+R);return out}};
        return draw.call(this,new Proxy(g,{get:(t,k)=>Object.prototype.hasOwnProperty.call(W,k)?W[k]:t[k]}),p,info)};
    }
    return cs.call(this,host,spec)};
  Object.defineProperty(window,'Deck',{configurable:true,enumerable:true,get:()=>deck,set(v){deck=v;if(!v||typeof v!=='object')return;
    let cs=typeof v.canvasSim==='function'?wrap(v.canvasSim):v.canvasSim;
    Object.defineProperty(v,'canvasSim',{configurable:true,enumerable:true,get:()=>cs,set(f){cs=typeof f==='function'?wrap(f):f}})}});
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
    TEXT='p,li,td,th,h2,.line,.cell,.rh,.q,.ans,.fb,.tag,.term,.mean,.k,.small,.cap,.nm,.fm,.bt,.why,.big,.hdr';
  const memo=new Map(),css=e=>{let c=memo.get(e);if(!c){c=getComputedStyle(e);memo.set(e,c)}return c};
  const opa=e=>{let o=1;for(let x=e;x&&x.nodeType===1;x=x.parentElement)o*=parseFloat(css(x).opacity);return o};
  const vis=e=>{const c=css(e);return c.visibility==='visible'&&c.display!=='none'&&opa(e)>0};
  const sized=r=>r.width>0&&r.height>0;
  const own=e=>[...e.childNodes].some(n=>{if(n.nodeType!==3||!n.nodeValue.trim())return false;const g=document.createRange();g.selectNodeContents(n);return [...g.getClientRects()].some(sized)});
  const any=e=>{const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode()))if(n.nodeValue.trim()&&vis(n.parentElement))return true;return false};
  const cv=r=>({x0:(r.left-st.left)/k,y0:(r.top-st.top)/k,x1:(r.right-st.left)/k,y1:(r.bottom-st.top)/k});
  const txt=s=>{s=String(s).replace(/\s+/g,' ').trim();return s.length>32?s.slice(0,31)+'…':s};
  const nm=e=>{const p=e.id?null:e.parentElement&&e.parentElement.closest('[id]');
    return (e.id?'#'+e.id:'<'+e.tagName.toLowerCase()+(typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/).join('.'):'')+'>')+
      (p&&p!==S&&p.id!=='stage'?' in #'+p.id:'')+' "'+txt(e.textContent)+'"'};
  const inside=(a,b)=>a.x0>=b.x0-tol&&a.x1<=b.x1+tol&&a.y0>=b.y0-tol&&a.y1<=b.y1+tol;
  const cut=(a,b)=>{const ox=Math.min(a.x1,b.x1)-Math.max(a.x0,b.x0),oy=Math.min(a.y1,b.y1)-Math.max(a.y0,b.y0);return ox>tol&&oy>tol?{ox,oy}:null};
  const hits=[],boxes=[];
  for(const e of [...S.querySelectorAll('*'),...document.querySelectorAll(FOOT)]){
    if(e.closest('.notes,script,style,svg,.zoomed,.timer:not(.run)'))continue;
    const kind=e.matches(FOOT)?'footer':e.matches(CARD)?'card':e.matches(CHIP)?'chip':(own(e)||e.matches(TEXT)&&any(e))?'text':null;
    if(!kind||!vis(e))continue;
    const rs=(css(e).display==='inline'?[...e.getClientRects()]:[e.getBoundingClientRect()]).filter(sized).map(cv);
    if(rs.length)boxes.push({e,kind,rs});
  }
  for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const A=boxes[i],B=boxes[j];
    if(A.e.contains(B.e)||B.e.contains(A.e))continue;
    let best=null;
    for(const a of A.rs)for(const b of B.rs){const c=cut(a,b);if(c&&!inside(a,b)&&!inside(b,a)&&(!best||c.ox*c.oy>best.ox*best.oy))best=Object.assign(c,{ra:a,rb:b})}
    if(best)hits.push({kind:'dom',a:A.kind+' '+nm(A.e),b:B.kind+' '+nm(B.e),ox:best.ox,oy:best.oy,ra:best.ra,rb:best.rb});
  }
  let labels=0,shapes=0,dup=0,hosts=0;const unrec=[];
  for(const h of S.querySelectorAll('.sim[data-sim]')){
    const c=h.querySelector(':scope>canvas');if(!c||!vis(h)||!sized(h.getBoundingClientRect()))continue;
    if(!h.__boxes){unrec.push(h.id);continue}hosts++;
    const r=c.getBoundingClientRect(),o=cv(r),q=r.width/k/(c.clientWidth||1),T=b=>({x0:o.x0+b.x0*q,y0:o.y0+b.y0*q,x1:o.x0+b.x1*q,y1:o.y0+b.y1*q});
    const B=h.__boxes,where='canvas #'+h.id+' ['+B.stage+']';
    const labs=[];   /* one label drawn twice at the same place is one label */
    B.labels.forEach(l=>{if(labs.some(m=>m.text===l.text&&Math.abs(m.x0-l.x0)<.5&&Math.abs(m.y0-l.y0)<.5&&Math.abs(m.x1-l.x1)<.5&&Math.abs(m.y1-l.y1)<.5))dup++;else labs.push(l)});
    labels+=labs.length;shapes+=B.shapes.length;
    for(let i=0;i<labs.length;i++)for(let j=i+1;j<labs.length;j++){const x=cut(labs[i],labs[j]);
      if(x)hits.push({kind:'label',a:where+': label "'+txt(labs[i].text)+'"',b:'label "'+txt(labs[j].text)+'"',ox:x.ox,oy:x.oy,ra:T(labs[i]),rb:T(labs[j])})}
    for(const l of labs)for(const s of B.shapes){const x=cut(l,s);
      if(x&&!inside(l,s))hits.push({kind:'shape',a:where+': label "'+txt(l.text)+'"',b:s.kind,ox:x.ox,oy:x.oy,ra:T(l),rb:T(s)})}
  }
  const R=b=>[b.x0,b.y0,b.x1,b.y1].map(v=>Math.round(v));
  return {dom:boxes.length,labels,shapes,dup,hosts,unrec,hits:hits.map(h=>Object.assign(h,{ox:Math.round(h.ox),oy:Math.round(h.oy),ra:R(h.ra),rb:R(h.rb)}))};
},TOL);

module.exports={instrument,settle,overlap,TOL};
if(require.main===module)(async()=>{
  const theme=process.argv[2]||'light';
  const {browser,page,errors}=await L.open({reduced:true,theme,init:instrument});
  const nf=await page.evaluate(()=>Deck.slides.map(S=>S.frames.length));
  const rec=[],fails=[];let lists=0;
  const ov={dom:0,labels:0,shapes:0,dup:0,unsettled:[],frames:[]};
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
    x.unrec.forEach(id=>fails.push(`s${s+1}f${f}: overlap: canvas #${id} has no recorded paint (instrumentation)`));
    x.hits.forEach(h=>fails.push(`s${s+1}f${f}: ${h.a} ∩ ${h.b} (${h.ox} × ${h.oy} px)`));
    if(x.hits.length)ov.frames.push({s:s+1,f,hits:x.hits});
    rec.push({s:s+1,f,empty:em,opts:o,overlap:{dom:x.dom,labels:x.labels,shapes:x.shapes,canvases:x.hosts,hits:x.hits.length}});
  }
  /* every canvas animation of the deck must have been wrapped, or its labels were never measured */
  const wr=await page.evaluate(()=>{const h=[...document.querySelectorAll('.sim[data-sim]')].filter(x=>x.querySelector(':scope>canvas'));return {n:h.length,miss:h.filter(x=>!x.__ovlWrapped).map(x=>x.id)}});
  if(wr.miss.length)fails.push(`overlap: canvas instrumentation missed ${wr.miss.length} of ${wr.n} canvas animations (${wr.miss.join(', ')})`);
  if(ov.unsettled.length)console.log(`  (layout did not settle within 15 animation frames on ${ov.unsettled.join(', ')}; measured anyway)`);
  /* crops of up to six failing frames, one per slide first, both boxes of each intersection outlined (A red, B blue) */
  const shots=[];
  if(ov.frames.length){const dir=L.ensure(path.join(L.OUT,'overlap-'+theme));fs.readdirSync(dir).forEach(f=>fs.unlinkSync(path.join(dir,f)));
    const pick=[];ov.frames.forEach(fr=>{if(pick.length<SHOTS&&!pick.some(p=>p.s===fr.s))pick.push(fr)});
    ov.frames.forEach(fr=>{if(pick.length<SHOTS&&!pick.includes(fr))pick.push(fr)});
    for(const fr of pick){
      await page.evaluate(([s,f])=>Deck.go(s,f),[fr.s-1,fr.f]);await L.wait(page,100);await settle(page);
      const clip=await page.evaluate(hits=>{const st=document.getElementById('stage').getBoundingClientRect(),k=st.width/1600;
        const h0=hits[0],x0=Math.max(0,Math.min(h0.ra[0],h0.rb[0])-120),y0=Math.max(0,Math.min(h0.ra[1],h0.rb[1])-120),x1=Math.min(1600,Math.max(h0.ra[2],h0.rb[2])+120),y1=Math.min(900,Math.max(h0.ra[3],h0.rb[3])+120);
        hits.slice(0,8).forEach(h=>[[h.ra,'#e0182d'],[h.rb,'#1f5fff']].forEach(([r,c])=>{const d=document.createElement('div');d.className='ovl-mark';
          d.style.cssText=`position:fixed;z-index:2147483647;pointer-events:none;box-sizing:border-box;border:3px solid ${c};left:${st.left+r[0]*k}px;top:${st.top+r[1]*k}px;width:${(r[2]-r[0])*k}px;height:${(r[3]-r[1])*k}px`;
          document.body.appendChild(d)}));
        return {x:st.left+x0*k,y:st.top+y0*k,width:(x1-x0)*k,height:(y1-y0)*k}},fr.hits);
      const file=`s${fr.s}f${fr.f}.jpg`;await page.screenshot({path:path.join(dir,file),type:'jpeg',quality:80,clip});
      await page.evaluate(()=>document.querySelectorAll('.ovl-mark').forEach(d=>d.remove()));
      shots.push('overlap-'+theme+'/'+file);
    }
  }
  if(errors.length)fails.push('console errors: '+errors.join(' | '));
  const nh=ov.frames.reduce((a,fr)=>a+fr.hits.length,0),nb=ov.dom+ov.labels+ov.shapes;
  const boxesTxt=`${nb} boxes (${ov.dom} DOM boxes, ${ov.labels} canvas labels, ${ov.shapes} canvas shapes${ov.dup?', '+ov.dup+' repeated canvas labels counted once':''})`;
  fs.writeFileSync(path.join(L.OUT,'overlap-'+theme+'.txt'),!nh?`no intersections, ${rec.length} frames, ${boxesTxt}\n`:
    `${process.env.DECKNAME||path.basename(L.DECK)} ${theme}: ${nh} intersections on ${ov.frames.length} of ${rec.length} frames, ${boxesTxt}; boxes as [x0, y0, x1, y1] in 1600 x 900 canvas px\n`+
    ov.frames.map(fr=>`s${fr.s}f${fr.f}: ${fr.hits.length} intersection${fr.hits.length>1?'s':''}\n`+fr.hits.map(h=>`  - ${h.a} ∩ ${h.b} (${h.ox} × ${h.oy} px)  A [${h.ra.join(', ')}]  B [${h.rb.join(', ')}]`).join('\n')).join('\n')+
    (shots.length?`\ncrops (A red, B blue): ${shots.join(', ')}\n`:'\n'));
  const sh={};rec.forEach(r=>r.opts.forEach(x=>{sh[x.shape]=(sh[x.shape]||0)+1}));
  const worst=rec.reduce((a,r)=>r.empty>a.empty?r:a,rec[0]);
  L.save('layout-'+theme+'.json',{theme,frames:rec.length,fails,overlap:{intersections:nh,frames:ov.frames.length,dom:ov.dom,labels:ov.labels,shapes:ov.shapes,repeated:ov.dup,canvases:wr.n,unsettled:ov.unsettled,failing:ov.frames,shots},rec});
  console.log(`layout ${theme}: ${rec.length} frames, ${lists} visible option lists (${Object.entries(sh).map(([k,v])=>k+' '+v).join(', ')}), max empty ${Math.round(worst.empty*100)}% (s${worst.s}f${worst.f}), gate ${Math.round(EMAX*100)}%, clipped or ellipsized text: ${fails.filter(f=>/clipped text/.test(f)).length}, overlap: ${nh} intersections on ${ov.frames.length} frames (${boxesTxt}, ${wr.n-wr.miss.length} of ${wr.n} canvas animations instrumented), ${fails.length?'FAIL':'PASS'}`);fails.forEach(f=>console.log('  - '+f));
  await browser.close();process.exitCode=fails.length?1:0;
})();
