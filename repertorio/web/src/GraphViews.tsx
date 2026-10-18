import {useEffect,useId,useRef,useState} from 'react';
import {Check,Network} from 'lucide-react';
import {graphViews,type GraphView} from './graphViewOptions';
import {GraphPreview} from './GraphPreview';

export function GraphViews({value,theme,onChange}:{value:GraphView;theme:'dark'|'light';onChange:(view:GraphView)=>void}){
 const [open,setOpen]=useState(false),root=useRef<HTMLDivElement>(null),trigger=useRef<HTMLButtonElement>(null),menu=useRef<HTMLDivElement>(null),id=useId();
 const current=graphViews.find(view=>view.id===value)!;
 useEffect(()=>{
  if(!open)return;
  const selected=menu.current?.querySelector<HTMLButtonElement>('[aria-checked="true"]');selected?.focus();selected?.scrollIntoView({block:'nearest'});
  const outside=(event:PointerEvent)=>{if(!root.current?.contains(event.target as Node))setOpen(false);};
  document.addEventListener('pointerdown',outside);return()=>document.removeEventListener('pointerdown',outside);
 },[open]);
 const close=()=>{setOpen(false);trigger.current?.focus();};
 return <div className="graph-view-control" ref={root}>
  <button ref={trigger} className="graph-view-toggle" aria-label="Visualização do grafo" title={'Visualização: '+current.name} aria-haspopup="menu" aria-expanded={open} aria-controls={open?id:undefined} onClick={()=>setOpen(!open)} onKeyDown={event=>{if(event.key==='ArrowDown'||event.key==='ArrowUp'){event.preventDefault();setOpen(true);}}}><Network size={18}/></button>
  {open&&<div className="graph-view-menu" ref={menu} id={id} role="menu" aria-label="Visualização do grafo" onKeyDown={event=>{
   if(event.key==='Escape'){event.preventDefault();event.stopPropagation();close();}
   else if(['ArrowDown','ArrowUp','Home','End'].includes(event.key)){
    event.preventDefault();const options=Array.from(menu.current!.querySelectorAll<HTMLButtonElement>('[role="menuitemradio"]')),index=options.indexOf(document.activeElement as HTMLButtonElement);
    options[event.key==='Home'?0:event.key==='End'?options.length-1:(index+(event.key==='ArrowDown'?1:-1)+options.length)%options.length]?.focus();
   }else if(event.key==='Tab'){trigger.current?.focus();setOpen(false);}
  }}><div className="graph-view-heading">Visualização do grafo<small>Um repertório, {graphViews.length} maneiras de explorar.</small></div>{graphViews.map(view=><button key={view.id} role="menuitemradio" aria-checked={view.id===value} tabIndex={view.id===value?0:-1} aria-labelledby={id+'-'+view.id} aria-describedby={id+'-'+view.id+'-description'} onClick={()=>{onChange(view.id);close();}}><GraphPreview view={view.id} theme={theme}/><span><strong id={id+'-'+view.id}>{view.name}</strong><small id={id+'-'+view.id+'-description'}>{view.description}</small></span>{view.id===value&&<Check size={16}/>}</button>)}</div>}
 </div>;
}
