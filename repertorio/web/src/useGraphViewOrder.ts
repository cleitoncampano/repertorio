import {useEffect,useRef,useState,type PointerEvent as ReactPointerEvent,type RefObject} from 'react';
import {graphViewOrder,graphViews,type GraphView} from './graphViewOptions';

const storageKey='repertorio-graph-view-order';
type Drag={view:GraphView;x:number;y:number;width:number;height:number;before:GraphView|null;inside:boolean};
type Gesture={view:GraphView;pointer:number;startX:number;startY:number;x:number;y:number;offsetX:number;offsetY:number;width:number;height:number;active:boolean};

function loadOrder(){
 try{return graphViewOrder(JSON.parse(localStorage.getItem(storageKey)||'null'));}
 catch{return graphViewOrder(null);}
}

export function useGraphViewOrder(open:boolean,menu:RefObject<HTMLDivElement|null>){
 const [order,setOrder]=useState(loadOrder),[drag,setDrag]=useState<Drag|null>(null),[announcement,setAnnouncement]=useState('');
 const gesture=useRef<Gesture|null>(null),frame=useRef(0),suppressClick=useRef(false);
 const rows=()=>Array.from(menu.current?.querySelectorAll<HTMLButtonElement>('[data-graph-view]')||[]);
 const focus=(view:GraphView,reveal=false)=>requestAnimationFrame(()=>{
  const row=menu.current?.querySelector<HTMLButtonElement>('[data-graph-view="'+view+'"]');
  row?.focus({preventScroll:true});if(reveal)row?.scrollIntoView({block:'nearest'});
 });
 const save=(next:GraphView[],view:GraphView)=>{
  setOrder(next);
  try{localStorage.setItem(storageKey,JSON.stringify(next));}catch{/* A ordem continua disponível nesta visita sem armazenamento. */}
  setAnnouncement(graphViews.find(item=>item.id===view)!.name+' na posição '+(next.indexOf(view)+1)+' de '+next.length+'.');
 };
 const target=(current:Gesture)=>{
  const rect=menu.current!.getBoundingClientRect(),inside=current.x>=rect.left&&current.x<=rect.right&&current.y>=rect.top&&current.y<=rect.bottom;
  const before=rows().filter(row=>row.dataset.graphView!==current.view).find(row=>{const bounds=row.getBoundingClientRect();return current.y<bounds.top+bounds.height/2;})?.dataset.graphView as GraphView|undefined;
  return {inside,before:before??null};
 };
 const cancel=()=>{
  const active=!!gesture.current?.active;
  if(gesture.current)focus(gesture.current.view,true);
  gesture.current=null;cancelAnimationFrame(frame.current);setDrag(null);
  if(active)setAnnouncement('Reordenação cancelada.');
  return active;
 };
 useEffect(()=>{
  if(!open){gesture.current=null;setDrag(null);return;}
  const tick=()=>{
   const current=gesture.current,element=menu.current;
   if(!current?.active||!element)return;
   const rect=element.getBoundingClientRect();
   if(current.x>=rect.left&&current.x<=rect.right){
    const edge=42,top=Math.max(0,Math.min(1,(rect.top+edge-current.y)/edge)),bottom=Math.max(0,Math.min(1,(current.y-rect.bottom+edge)/edge));
    element.scrollTop+=(bottom-top)*12;
   }
   const next={view:current.view,x:current.x-current.offsetX,y:current.y-current.offsetY,width:current.width,height:current.height,...target(current)};
   setDrag(previous=>previous&&previous.x===next.x&&previous.y===next.y&&previous.before===next.before&&previous.inside===next.inside?previous:next);
   frame.current=requestAnimationFrame(tick);
  };
  const move=(event:PointerEvent)=>{
   const current=gesture.current;
   if(!current||current.pointer!==event.pointerId)return;
   current.x=event.clientX;current.y=event.clientY;
   if(!current.active&&Math.hypot(current.x-current.startX,current.y-current.startY)>=6){
    current.active=true;suppressClick.current=true;focus(current.view);tick();
   }
   if(current.active)event.preventDefault();
  };
  const finish=(event:PointerEvent)=>{
   const current=gesture.current;
   if(!current||current.pointer!==event.pointerId)return;
   current.x=event.clientX;current.y=event.clientY;
   gesture.current=null;cancelAnimationFrame(frame.current);setDrag(null);
   if(!current.active)return;
   const {inside,before}=target(current);
   if(inside){
    const next=order.filter(view=>view!==current.view);
    next.splice(before===null?next.length:next.indexOf(before),0,current.view);
    save(next,current.view);
   }else setAnnouncement('Reordenação cancelada.');
   focus(current.view,true);
  };
  const interrupted=(event:PointerEvent)=>{if(event.pointerId===gesture.current?.pointer)cancel();};
  const blurred=()=>cancel();
  document.addEventListener('pointermove',move,{passive:false});
  document.addEventListener('pointerup',finish);
  document.addEventListener('pointercancel',interrupted);
  window.addEventListener('blur',blurred);
  return()=>{
   document.removeEventListener('pointermove',move);document.removeEventListener('pointerup',finish);document.removeEventListener('pointercancel',interrupted);window.removeEventListener('blur',blurred);
   cancelAnimationFrame(frame.current);gesture.current=null;
  };
 },[open,order]);
 const start=(event:ReactPointerEvent<HTMLButtonElement>,view:GraphView)=>{
  if(event.button!==0||!event.isPrimary||gesture.current)return;
  suppressClick.current=false;
  if(event.pointerType!=='mouse'&&!(event.target as Element).closest('.graph-view-grip'))return;
  const rect=event.currentTarget.getBoundingClientRect();
  event.currentTarget.setPointerCapture(event.pointerId);
  gesture.current={view,pointer:event.pointerId,startX:event.clientX,startY:event.clientY,x:event.clientX,y:event.clientY,offsetX:event.clientX-rect.left,offsetY:event.clientY-rect.top,width:rect.width,height:rect.height,active:false};
 };
 const moveByKey=(view:GraphView,direction:number)=>{
  if(gesture.current)cancel();
  const index=order.indexOf(view),destination=index+direction;
  if(destination<0||destination>=order.length)return;
  const next=[...order];next.splice(index,1);next.splice(destination,0,view);save(next,view);
  requestAnimationFrame(()=>{const row=menu.current?.querySelector<HTMLButtonElement>('[data-graph-view="'+view+'"]');row?.focus({preventScroll:true});row?.scrollIntoView({block:'nearest'});});
 };
 return {order,drag,announcement,start,cancel,moveByKey,suppressClick};
}
