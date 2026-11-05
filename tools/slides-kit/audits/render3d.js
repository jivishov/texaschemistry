// 3D sphere renderer test: Deck.spheres is reusable outside the demo animation.
// Draws ball-and-stick nitrate (flat triangle) and sulfate (tetrahedron) at three-quarter views, then asserts depth order by pixels.
const L=require('./lib');
(async()=>{
  const res=[];
  for(const theme of ['light','dark']){
    const {browser,page,errors}=await L.open({theme});
    const r=await page.evaluate(()=>{
      const host=document.createElement('div');host.style.cssText='position:fixed;inset:0;z-index:200;background:var(--slide)';document.body.appendChild(host);
      const cv=document.createElement('canvas');cv.width=1600;cv.height=900;cv.style.cssText='width:1600px;height:900px';host.appendChild(cv);
      const ctx=cv.getContext('2d'),g=Deck.painter(ctx),c=n=>Deck.tok(n);
      const O=c('cat'),S=c('warm'),N=c('an');
      // nitrate: N at center, 3 O in a plane (120 degrees)
      const no3={atoms:[{p:[0,0,0],r:.42,color:N,label:'N'}],bonds:[]};
      for(let i=0;i<3;i++){const a=i*2*Math.PI/3;no3.atoms.push({p:[1.3*Math.cos(a),1.3*Math.sin(a),0],r:.48,color:O,label:'O'});no3.bonds.push({a:0,b:i+1,w:.16})}
      // sulfate: S at center, 4 O at tetrahedral corners
      const t=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],so4={atoms:[{p:[0,0,0],r:.5,color:S,label:'S'}],bonds:[]};
      t.forEach((v,i)=>{const k=1.45/Math.sqrt(3);so4.atoms.push({p:[v[0]*k,v[1]*k,v[2]*k],r:.48,color:O,label:'O'});so4.bonds.push({a:0,b:i+1,w:.16})});
      g.text('nitrate: flat',400,90,44);g.text('sulfate: tetrahedron',1200,90,44);
      Deck.spheres(g,no3,{cx:400,cy:480,scale:150,yaw:-.6,pitch:.9,dist:7});
      const P=Deck.spheres(g,so4,{cx:1200,cy:480,scale:150,yaw:.5,pitch:.35,dist:7});
      // depth test: two overlapping spheres, the near one (z=+1) must cover the far one (z=-1) where they overlap
      const near=c('an'),far=c('cat');
      ctx.save();ctx.translate(0,0);
      const Q=Deck.spheres(g,{atoms:[{p:[.15,0,1],r:.5,color:near},{p:[-.15,0,-1],r:.5,color:far}]},{cx:800,cy:800,scale:80,yaw:0,pitch:0,dist:7});
      ctx.restore();
      const px=ctx.getImageData(800,800,1,1).data;
      const hex=s=>s[0]==='#'?[parseInt(s.slice(1,3),16),parseInt(s.slice(3,5),16),parseInt(s.slice(5,7),16)]:s.match(/\d+/g).slice(0,3).map(Number);
      const d=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1],a[2]-b[2]),pc=[px[0],px[1],px[2]];
      return {nearCloser:d(pc,hex(near))<d(pc,hex(far)),pixel:pc,minFont:g.minFont,projected:P.map(p=>Math.round(p.r))};
    });
    await page.screenshot({path:L.OUT+'/render3d-'+theme+'.png'});
    res.push({theme,...r,errors:errors.slice()});
    await browser.close();
  }
  const pass=res.every(r=>r.nearCloser&&r.minFont>=36&&!r.errors.length);
  L.save('render3d.json',res);
  res.forEach(r=>console.log(`  ${r.theme}: depth order ${r.nearCloser?'ok':'WRONG'} (pixel ${r.pixel}), min label ${r.minFont}px, sphere radii ${r.projected.join(',')}`));
  console.log('render3d: '+(pass?'PASS':'FAIL'));process.exitCode=pass?0:1;
})();
