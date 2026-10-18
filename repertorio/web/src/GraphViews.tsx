import {useEffect,useId,useRef,useState,type KeyboardEvent} from 'react';
import {createPortal} from 'react-dom';
import {Check,GripVertical,Network} from 'lucide-react';
import {graphViews,type GraphView} from './graphViewOptions';
import {GraphPreview} from './GraphPreview';
import {useGraphViewOrder} from './useGraphViewOrder';

function GraphViewCard({view,theme,selected,labelId}:{view:typeof graphViews[number];theme:'dark'|'light';selected:boolean;labelId?:string}){
 return <>
  <span className="graph-view-grip" aria-hidden="true" title="Arrastar para reordenar"><GripVertical size={14}/></span>
  <GraphPreview view={view.id} theme={theme}/>
  <span className="graph-view-copy">
   <strong id={labelId}>{view.name}</strong>
   <small id={labelId?labelId+'-description':undefined}>{view.description}</small>
  </span>
  {selected&&<Check size={16}/>}
 </>;
}

export function GraphViews({value,theme,onChange}:{value:GraphView;theme:'dark'|'light';onChange:(view:GraphView)=>void}){
 const [open,setOpen]=useState(false),root=useRef<HTMLDivElement>(null),trigger=useRef<HTMLButtonElement>(null),menu=useRef<HTMLDivElement>(null),id=useId();
 const {order,drag,announcement,start,cancel,moveByKey,suppressClick}=useGraphViewOrder(open,menu);
 const displayOrder=order.filter(view=>!drag?.inside||view!==drag.view);
 if(drag?.inside)displayOrder.splice(drag.before===null?displayOrder.length:displayOrder.indexOf(drag.before),0,drag.view);
 const options=displayOrder.map(view=>graphViews.find(option=>option.id===view)!);
 const current=graphViews.find(view=>view.id===value)!;
 useEffect(()=>{
  if(!open)return;
  const selected=menu.current?.querySelector<HTMLButtonElement>('[aria-checked="true"]');selected?.focus();selected?.scrollIntoView({block:'nearest'});
  const outside=(event:PointerEvent)=>{if(!root.current?.contains(event.target as Node))setOpen(false);};
  document.addEventListener('pointerdown',outside);return()=>document.removeEventListener('pointerdown',outside);
 },[open]);
 const close=()=>{setOpen(false);trigger.current?.focus();};
 const handleKeyDown=(event:KeyboardEvent<HTMLDivElement>)=>{
  if(event.key==='Escape'){
   event.preventDefault();event.stopPropagation();if(!cancel())close();
  }else if(event.altKey&&['ArrowDown','ArrowUp'].includes(event.key)){
   event.preventDefault();event.stopPropagation();const view=(document.activeElement as HTMLElement)?.dataset.graphView as GraphView|undefined;
   if(view)moveByKey(view,event.key==='ArrowDown'?1:-1);
  }else if(['ArrowDown','ArrowUp','Home','End'].includes(event.key)){
   event.preventDefault();const buttons=Array.from(menu.current!.querySelectorAll<HTMLButtonElement>('[role="menuitemradio"]')),index=buttons.indexOf(document.activeElement as HTMLButtonElement);
   buttons[event.key==='Home'?0:event.key==='End'?buttons.length-1:(index+(event.key==='ArrowDown'?1:-1)+buttons.length)%buttons.length]?.focus();
  }else if(event.key==='Tab'){
   trigger.current?.focus();setOpen(false);
  }
 };
 return <div className="graph-view-control" ref={root}>
  <button ref={trigger} className="graph-view-toggle" aria-label="Visualização do grafo" title={'Visualização: '+current.name} aria-haspopup="menu" aria-expanded={open} aria-controls={open?id:undefined} onClick={()=>setOpen(!open)} onKeyDown={event=>{if(event.key==='ArrowDown'||event.key==='ArrowUp'){event.preventDefault();setOpen(true);}}}><Network size={18}/></button>
  {open&&<div className="graph-view-menu" ref={menu} id={id} role="menu" aria-label="Visualização do grafo" onKeyDown={handleKeyDown}>
   <div className="graph-view-heading">
    Visualização do grafo
    <small>Um repertório, {graphViews.length} maneiras de explorar.</small>
    <small id={id+'-reorder'}>Arraste para reordenar.<span className="graph-view-sr"> Pelo teclado, use Alt e as setas para cima ou para baixo.</span></small>
   </div>
   {options.map(view=><button
    key={view.id} className="graph-view-card" data-graph-view={view.id}
    data-dragging={drag?.view===view.id||undefined}
    data-drop-before={drag?.inside&&drag.before===view.id||undefined}
    data-drop-after={drag?.inside&&drag.before===null&&view.id===order.filter(item=>item!==drag.view).at(-1)||undefined}
    role="menuitemradio" aria-checked={view.id===value} tabIndex={view.id===value?0:-1}
    aria-labelledby={id+'-'+view.id} aria-describedby={id+'-'+view.id+'-description '+id+'-reorder'}
    onPointerDown={event=>start(event,view.id)} onDragStart={event=>event.preventDefault()}
    onClick={event=>{
     if(suppressClick.current&&event.detail>0){event.preventDefault();event.stopPropagation();return;}
     onChange(view.id);close();
    }}
   ><GraphViewCard view={view} theme={theme} selected={view.id===value} labelId={id+'-'+view.id}/></button>)}
  </div>}
  <span className="graph-view-sr" role="status">{announcement}</span>
  {drag&&createPortal(<div className="graph-view-card graph-view-drag-preview" aria-hidden="true" style={{left:drag.x,top:drag.y,width:drag.width,minHeight:drag.height}}>
   <GraphViewCard view={graphViews.find(view=>view.id===drag.view)!} theme={theme} selected={drag.view===value}/>
  </div>,document.body)}
 </div>;
}
