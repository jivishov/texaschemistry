// Shared helpers for the audit scripts (RULES.md section 11).
// DECK (the deck to audit) and OUT (the folder for logs, JSON and screenshots) come from the environment; suite.py sets both.
const {chromium}=require('playwright');
const path=require('path'),fs=require('fs');
if(!process.env.DECK||!process.env.OUT)throw new Error('set DECK (the deck to audit) and OUT (the output folder); suite.py sets both');
const DECK=path.resolve(process.env.DECK);
const OUT=path.resolve(process.env.OUT);fs.mkdirSync(OUT,{recursive:true});
async function open(opts={}){
  const browser=opts.browser||await chromium.launch();
  const ctx=await browser.newContext({viewport:opts.viewport||{width:1920,height:1080},deviceScaleFactor:opts.dsf||1,reducedMotion:opts.reduced?'reduce':'no-preference'});
  const page=await ctx.newPage();
  const errors=[];
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
  page.on('pageerror',e=>errors.push('pageerror: '+e.message));
  await page.goto('file://'+DECK+(opts.theme?'?theme='+opts.theme:'')+(opts.hash||''));
  await page.waitForFunction(()=>window.Deck&&Deck.slides.length>0);
  await page.waitForTimeout(500);
  return {browser,page,errors};
}
const wait=(page,ms)=>page.waitForTimeout(ms);
const state=page=>page.evaluate(()=>Deck.state());
// Blocks visible and managed classes on the current slide: the full "frame state" for exact Back comparison.
const frameState=page=>page.evaluate(()=>{
  const S=document.querySelector('.slide.current'),st=Deck.state();
  const on=[...S.querySelectorAll('.blk.on')].map(e=>e.id||e.dataset.b).filter(Boolean);
  const cls=[...S.querySelectorAll('[id]')].filter(e=>e._dc&&e._dc.length).map(e=>e.id+':'+e._dc.join('.'));
  return {s:st.s,f:st.f,sims:st.sims,on:[...new Set(on)].sort(),cls:cls.sort(),timer:st.timer?st.timer.sec:0};
});
// Overflow: anything visible that leaves the slide box, or leaves its container (card, column, cell), by more than 1 canvas px.
const overflow=page=>page.evaluate(()=>{
  const S=document.querySelector('.slide.current'),sr=S.getBoundingClientRect(),k=sr.width/1600,tol=1.01*k,bad=[];
  const vis=e=>{const cs=getComputedStyle(e);return cs.visibility!=='hidden'&&cs.display!=='none'&&parseFloat(cs.opacity)>0};
  const name=e=>(e.id?'#'+e.id:'')+(e.dataset&&e.dataset.b?'['+e.dataset.b+']':'')+'<'+e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\s+/).join('.'):'')+'>';
  const out=(r,c)=>r.left<c.left-tol||r.top<c.top-tol||r.right>c.right+tol||r.bottom>c.bottom+tol;
  const all=[...S.querySelectorAll('*')].filter(e=>!e.closest('.notes')&&e.tagName!=='SCRIPT'&&!e.closest('.zoomed'));
  for(const e of all){if(!vis(e))continue;const r=e.getBoundingClientRect();if(!r.width&&!r.height)continue;
    if(out(r,sr))bad.push({el:name(e),why:'leaves the slide',px:Math.round(Math.max(sr.left-r.left,sr.top-r.top,r.right-sr.right,r.bottom-sr.bottom)/k)})}
  const containers=[...S.querySelectorAll('.body>*,.card,.col>*,.stack>*,.phase,.steps li,.opt,.tbl td,.g3>*,.rail li,.timer,.cer-box')].filter(vis);
  for(const c of containers){const cr=c.getBoundingClientRect();
    for(const e of c.querySelectorAll('*')){if(!vis(e)||e.closest('.zoomed'))continue;const r=e.getBoundingClientRect();if(!r.width&&!r.height)continue;
      // inline boxes: a fallback glyph's ascent can exceed the line height without any visible overflow; allow 0.3 em vertically
      const cs=getComputedStyle(e),vt=cs.display==='inline'?.3*parseFloat(cs.fontSize)*k:tol;
      if(r.left<cr.left-tol||r.right>cr.right+tol||r.top<cr.top-vt||r.bottom>cr.bottom+vt)bad.push({el:name(e),why:'leaves its container '+name(c),px:Math.round(Math.max(cr.left-r.left,cr.top-r.top,r.right-cr.right,r.bottom-cr.bottom)/k)})}}
  return bad;
});
// Emptiness: the share of the slide body (below the title, above the footer) that no visible object covers, on a 20 px grid.
// Objects: cards, chips, steps, table cells, slots, timers, pictures, text lines, and each animation's drawn bounds().
const emptiness=page=>page.evaluate(()=>{
  const S=document.querySelector('.slide.current'),B=S.querySelector('.body'),k=S.getBoundingClientRect().width/1600,br=B.getBoundingClientRect();
  const W=Math.ceil(br.width/k/20),H=Math.ceil(br.height/k/20),grid=new Uint8Array(W*H);
  const mark=r=>{const x0=Math.max(0,Math.floor((r.left-br.left)/k/20)),x1=Math.min(W,Math.ceil((r.right-br.left)/k/20)),y0=Math.max(0,Math.floor((r.top-br.top)/k/20)),y1=Math.min(H,Math.ceil((r.bottom-br.top)/k/20));
    for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++)grid[y*W+x]=1};
  const vis=e=>{const cs=getComputedStyle(e);return cs.visibility!=='hidden'&&cs.display!=='none'&&parseFloat(cs.opacity)>0.05};
  B.querySelectorAll('.card,.opt,.rail li,.steps li,.slot,.timer.run,.pic svg,.cer-box,.colh,td,th,.item,.key,.wcard,.legend>span,.rate li,.steprows li,.ican li,.caprow,.rulerow p,.checkrow,.scale span').forEach(e=>{if(vis(e))mark(e.getBoundingClientRect())});
  const w=document.createTreeWalker(B,NodeFilter.SHOW_TEXT);let n;
  while((n=w.nextNode())){if(!n.nodeValue.trim())continue;const e=n.parentElement;if(e.closest('svg')||!vis(e))continue;const rg=document.createRange();rg.selectNodeContents(n);[...rg.getClientRects()].forEach(mark)}
  B.querySelectorAll('.sim[data-sim]').forEach(h=>{const x=Deck.sims[h.id];if(!x||!vis(h))return;const b=x.bounds&&x.bounds();const hr=h.getBoundingClientRect();
    if(b)mark({left:hr.left+b.x*k,top:hr.top+b.y*k,right:hr.left+(b.x+b.w)*k,bottom:hr.top+(b.y+b.h)*k})});
  let c=0;grid.forEach(v=>{c+=v});return +(1-c/grid.length).toFixed(3);
});
// Clipped text (teacher round, R1): no visible text may be cut off or ellipsized, on the slide or in the footer.
// An element that hides overflow (or ellipsizes) and whose content is larger than its box, with visible text inside, is clipped.
const clipped=page=>page.evaluate(()=>{
  const S=document.querySelector('.slide.current'),out=[];
  const vis=e=>{const cs=getComputedStyle(e);return cs.visibility!=='hidden'&&cs.display!=='none'&&parseFloat(cs.opacity)>0};
  const hasText=e=>{const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){if(n.nodeValue.trim()&&vis(n.parentElement))return true}return false};
  [...S.querySelectorAll('*'),...document.querySelectorAll('#foot,#foot *')].forEach(e=>{if(e.closest('.notes,script,.sim')||!vis(e))return;const cs=getComputedStyle(e);
    const hides=/hidden|clip|scroll|auto/.test(cs.overflowX+cs.overflowY)||cs.textOverflow==='ellipsis'||cs.webkitLineClamp&&cs.webkitLineClamp!=='none';
    if(!hides||!hasText(e))return;
    if(e.scrollWidth>e.clientWidth+1||e.scrollHeight>e.clientHeight+1)out.push({el:(e.id?'#'+e.id:'')+'<'+e.tagName.toLowerCase()+'.'+String(e.className).trim().split(/\s+/).join('.')+'>',sw:e.scrollWidth,cw:e.clientWidth,sh:e.scrollHeight,ch:e.clientHeight})});
  return out;
});
function ensure(d){fs.mkdirSync(d,{recursive:true});return d}
function save(name,obj){fs.writeFileSync(path.join(OUT,name),JSON.stringify(obj,null,2))}
module.exports={open,wait,state,frameState,overflow,emptiness,clipped,ensure,save,OUT,DECK};
