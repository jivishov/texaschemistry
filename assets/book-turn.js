/* Shared, dependency-free page turns for all reading chapters. */
(function(){
  'use strict';
  let snapshotId=0;

  function snapshot(page){
    const node=page.cloneNode(true),prefix='book-turn-'+(++snapshotId)+'-',ids=new Map();
    const source=[page,...page.querySelectorAll('*')],copy=[node,...node.querySelectorAll('*')];
    const scroll=[];
    copy.forEach((el,i)=>{
      if(el.id){ids.set(el.id,prefix+el.id);el.id=prefix+el.id}
      const original=source[i];
      if(original.scrollTop||original.scrollLeft)scroll.push([el,original.scrollTop,original.scrollLeft]);
      if(el.matches('input,textarea,select'))el.value=original.value;
      if(el.matches('input'))el.checked=original.checked;
      if(el.matches('canvas')){
        // cloneNode does not copy the bitmap of a chemistry simulation.
        try{el.getContext('2d').drawImage(original,0,0)}catch(e){}
      }
    });
    copy.forEach(el=>{
      [...el.attributes].forEach(attr=>{
        if(attr.name==='id')return;
        let value=attr.value.replace(/url\(#([^\)]+)\)/g,(all,id)=>ids.has(id)?'url(#'+ids.get(id)+')':all);
        if((attr.name==='href'||attr.name==='xlink:href')&&value[0]==='#'&&ids.has(value.slice(1)))value='#'+ids.get(value.slice(1));
        if(['for','aria-labelledby','aria-describedby','aria-controls'].includes(attr.name))value=value.split(' ').map(id=>ids.get(id)||id).join(' ');
        if(value!==attr.value)el.setAttribute(attr.name,value);
      });
    });
    return {node,restore(){scroll.forEach(([el,top,left])=>{el.scrollTop=top;el.scrollLeft=left})}};
  }

  window.BookTurn={create(book){
    const reduced=matchMedia('(prefers-reduced-motion: reduce)');
    let active=null;
    function cancel(){
      if(!active)return;
      const turn=active;active=null;
      turn.animations.forEach(animation=>animation.cancel());
      turn.layer.remove();book.classList.remove('is-turning');
    }
    // Layout changes and printing can rebuild the reader while a sheet is in flight.
    addEventListener('resize',cancel);
    addEventListener('scroll',()=>{if(active&&(scrollX!==active.x||scrollY!==active.y))cancel()},{passive:true,capture:true});
    reduced.addEventListener('change',cancel);
    document.addEventListener('visibilitychange',()=>{if(document.hidden)cancel()});

    return {cancel,capture(direction,single){
      cancel();
      if(reduced.matches||!Element.prototype.animate)return null;
      const visible=[...book.querySelectorAll('.page.on')];
      if(!visible.length)return null;
      return {direction,single,pages:visible.map(snapshot),height:visible[0].getBoundingClientRect().height};
    },play(turn,incoming){
      cancel();
      if(reduced.matches||!incoming.length)return;
      const forward=turn.direction>0,single=turn.single;
      const rect=incoming[0].getBoundingClientRect();
      const layer=document.createElement('main');
      layer.className='book book-turn-layer '+(single?'single ':'')+(forward?'forward':'backward');
      layer.setAttribute('aria-hidden','true');layer.inert=true;
      layer.style.left=rect.left+'px';layer.style.top=rect.top+'px';
      layer.style.setProperty('--turn-width',(rect.width*(single?1:2))+'px');
      layer.style.setProperty('--turn-height',(single&&forward?turn.height:rect.height)+'px');
      const animations=[],snapshots=[];
      const add=(className,parent=layer)=>{const el=document.createElement('div');el.className=className;parent.append(el);return el};
      const place=(el,left,width)=>{el.style.left=left;el.style.width=width};
      const put=(parent,shot)=>{if(shot){parent.append(shot.node);snapshots.push(shot)}};
      const leaf=add('book-turn-leaf');
      const front=add('book-turn-face book-turn-front',leaf);
      const back=add('book-turn-face book-turn-back',leaf);
      const shadow=add('book-turn-shadow');
      if(single){
        place(leaf,'0','100%');place(shadow,'0','100%');leaf.style.transformOrigin='left center';
        if(forward)put(front,turn.pages[0]);
        else{
          const still=add('book-turn-still');place(still,'0','100%');put(still,turn.pages[0]);
          put(front,snapshot(incoming[0]));
        }
      }else{
        place(leaf,forward?'50%':'0','50%');place(shadow,forward?'50%':'0','50%');
        leaf.style.transformOrigin=forward?'left center':'right center';
        const still=add('book-turn-still');place(still,forward?'0':'50%','50%');
        put(still,turn.pages[forward?0:1]);
        put(front,turn.pages[forward?1:0]);
        put(back,incoming[forward?0:1]?snapshot(incoming[forward?0:1]):null);
      }
      const shades=[front,back].map(face=>add('book-turn-shade',face));
      document.body.append(layer);snapshots.forEach(shot=>shot.restore());
      const duration=single?540:700,easing='cubic-bezier(.32,.08,.2,1)';
      const animate=(element,frames,options={})=>{
        const animation=element.animate(frames,{duration,easing,fill:'both',...options});animations.push(animation);return animation;
      };
      active={layer,animations,x:scrollX,y:scrollY};book.classList.add('is-turning');
      let motion;
      if(single){
        const frames=[{transform:'rotateY(0deg)',opacity:1},{transform:'rotateY(-55deg)',opacity:1,offset:.6},{transform:'rotateY(-105deg)',opacity:0}];
        motion=animate(leaf,frames,{direction:forward?'normal':'reverse'});
      }else motion=animate(leaf,[{transform:'rotateY(0deg)'},{transform:'rotateY('+(forward?-180:180)+'deg)'}]);
      animate(leaf,[{boxShadow:'0 0 0 rgba(0,0,0,0)'},{boxShadow:'0 14px 36px rgba(0,0,0,.22)',offset:.5},{boxShadow:'0 0 0 rgba(0,0,0,0)'}]);
      animate(shadow,[{opacity:0,transform:'scaleX(.15)'},{opacity:.85,transform:'scaleX(.9)',offset:.45},{opacity:0,transform:'scaleX(.15)'}]);
      // Light travels across both faces as the sheet passes the spine.
      shades.forEach(shade=>animate(shade,[{opacity:0},{opacity:.9,offset:.48},{opacity:0}]));
      motion.finished.then(()=>{if(active&&active.layer===layer)cancel()},()=>{});
    }};
  }};
})();
