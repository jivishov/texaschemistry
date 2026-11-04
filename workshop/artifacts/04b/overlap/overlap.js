// Ad-hoc overlap scan (step 04b): on every frame, visible text lines and visible blocks that overlap another block they do not belong to.
// node overlap.js <deck> [theme]   prints one line per frame with an overlap, and a total
const {chromium}=require('playwright');
(async()=>{const [deck,theme,only]=process.argv.slice(2);const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:1600,height:900},reducedMotion:'reduce'})).newPage();
await p.goto('file://'+deck+'?theme='+(theme||'light'));await p.waitForFunction(()=>window.Deck&&Deck.slides.length);await p.waitForTimeout(400);
const ns=await p.evaluate(()=>Deck.slides.length);let total=0,frames=0;
for(let s=0;s<ns;s++){if(only&&!only.split(',').includes(await p.evaluate(s=>Deck.slides[s].id,s)))continue;const nf=await p.evaluate(s=>Deck.slides[s].frames.length,s);
 for(let f=0;f<nf;f++){frames++;await p.evaluate(([s,f])=>Deck.go(s,f),[s,f]);await p.waitForTimeout(950);
  const r=await p.evaluate(()=>{const S=document.querySelector('.slide.current'),k=S.getBoundingClientRect().width/1600;
   const vis=e=>{for(let x=e;x&&x!==S;x=x.parentElement){const cs=getComputedStyle(x);if(cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity)<.05)return false}return true};
   const SEL='.card,.caprow,.simcap,table,.sim,.qrow,.rulerow,.checkrow,.timer,.rail,.legend,.mission,.enrow,.handsup,.steprows,.hrow,.cer-box,.words,.lines,h2,.opt,.af';
   const rect=e=>{const r=e.getBoundingClientRect();const res=+(e.dataset&&e.dataset.reserve||0);return res?{left:r.left,right:r.right,top:r.top,bottom:r.bottom-res*k,width:r.width,height:r.height-res*k}:r};
   const blocks=[...S.querySelectorAll(SEL)].filter(e=>!e.closest('.notes')&&vis(e)).map(e=>({e,r:rect(e)})).filter(x=>x.r.width>2&&x.r.height>2);
   const ov=(a,b,m)=>Math.min(a.right,b.right)-Math.max(a.left,b.left)>m&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>m;
   const name=e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\s+/).slice(0,2).join('.'):'');
   // a box is drawn when it has a border or a background; an unboxed block only counts through its text
   const boxed=e=>{const cs=getComputedStyle(e);return parseFloat(cs.borderTopWidth)>0&&cs.borderTopStyle!=='none'||(cs.backgroundColor&&!/rgba\(0, 0, 0, 0\)|transparent/.test(cs.backgroundColor))||e.tagName==='CANVAS'||e.classList.contains('sim')};
   const out=[];
   // block against block: neither inside the other
   for(let i=0;i<blocks.length;i++)for(let j=i+1;j<blocks.length;j++){const A=blocks[i],B=blocks[j];if(A.e.contains(B.e)||B.e.contains(A.e))continue;
     if(boxed(A.e)&&boxed(B.e)&&ov(A.r,B.r,4*k))out.push('block '+name(A.e)+' x '+name(B.e))}
   // text lines against blocks they are not in
   const w=document.createTreeWalker(S,NodeFilter.SHOW_TEXT);let n;
   while((n=w.nextNode())){if(!n.nodeValue.trim())continue;const e=n.parentElement;if(e.closest('.notes,script,style,svg')||!vis(e))continue;const rg=document.createRange();rg.selectNodeContents(n);
     [...rg.getClientRects()].forEach(t0=>{if(t0.width<2)return;const t={left:t0.left,right:t0.right,top:t0.top+t0.height*.2,bottom:t0.bottom-t0.height*.2};blocks.forEach(B=>{if(B.e.contains(e)||!boxed(B.e))return;if(ov(t,B.r,3*k))out.push('text "'+n.nodeValue.trim().slice(0,30)+'" over '+name(B.e))})})}
   const T=[];const w2=document.createTreeWalker(S,NodeFilter.SHOW_TEXT);let n2;
   while((n2=w2.nextNode())){if(!n2.nodeValue.trim())continue;const e=n2.parentElement;if(e.closest('.notes,script,style,svg')||!vis(e))continue;const rg=document.createRange();rg.selectNodeContents(n2);[...rg.getClientRects()].forEach(t0=>{if(t0.width<2)return;const t={left:t0.left,right:t0.right,top:t0.top+t0.height*.2,bottom:t0.bottom-t0.height*.2};T.push({t,e,s:n2.nodeValue.trim().slice(0,24)})})}
   for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){if(T[i].e===T[j].e)continue;if(ov(T[i].t,T[j].t,4*k))out.push('text "'+T[i].s+'" x text "'+T[j].s+'"')}
   return [...new Set(out)]});
  if(r.length){total+=r.length;console.log(await p.evaluate(()=>Deck.slides[Deck.cur.s].id),'f'+f,r.length,r.slice(0,4).join(' | '))}}}
console.log(`overlap scan: ${frames} frames, ${total} overlaps`);await b.close()})();
