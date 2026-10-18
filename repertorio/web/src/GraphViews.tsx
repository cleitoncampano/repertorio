import {useEffect,useId,useRef,useState} from 'react';
import {Check,Network} from 'lucide-react';
import {graphViews,type GraphView} from './graphViewOptions';

function Preview({view}:{view:GraphView}){
 const points=view==='free'
  ?[[46,32],[23,19],[66,18],[27,46],[69,46],[9,30],[83,32],[44,9],[45,55]]
  :view==='grouped'
   ?[[23,18],[10,10],[36,9],[11,29],[36,28],[68,45],[56,35],[81,35],[56,55],[82,56]]
   :[[12,32],[43,16],[43,48],[79,8],[79,24],[79,40],[79,56]];
 const paths=view==='free'?[[0,1],[0,2],[0,3],[0,4],[1,5],[2,6],[1,7],[3,8],[4,6]]:view==='grouped'?[[0,1],[0,2],[0,3],[0,4],[5,6],[5,7],[5,8],[5,9]]:[[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]];
 return <svg className="graph-view-preview" viewBox="0 0 92 64" aria-hidden="true"><g fill="none" stroke="currentColor" strokeWidth="1" opacity=".4">{paths.map(([a,b],i)=><path key={i} d={view==='hierarchy'?`M${points[a][0]},${points[a][1]}H${(points[a][0]+points[b][0])/2}V${points[b][1]}H${points[b][0]}`:`M${points[a].join(',')}L${points[b].join(',')}`}/>)}</g>{points.map(([x,y],i)=>view==='hierarchy'&&i>2?<rect key={i} x={x-4} y={y-3} width={8} height={6} rx={1} fill="currentColor"/>:<circle key={i} cx={x} cy={y} r={i===0||view==='grouped'&&i===5?5:3} fill={i===0?'#FF5A3C':view==='grouped'&&i>=5?'#3E7BFF':'currentColor'} opacity={i===0?1:.8}/>)}</svg>;
}

export function GraphViews({value,onChange}:{value:GraphView;onChange:(view:GraphView)=>void}){
 const [open,setOpen]=useState(false),root=useRef<HTMLDivElement>(null),trigger=useRef<HTMLButtonElement>(null),menu=useRef<HTMLDivElement>(null),id=useId();
 const current=graphViews.find(view=>view.id===value)!;
 useEffect(()=>{
  if(!open)return;
  menu.current?.querySelector<HTMLButtonElement>('[aria-checked="true"]')?.focus();
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
   }else if(event.key==='Tab')setOpen(false);
  }}><div className="graph-view-heading">Visualização do grafo<small>Um repertório, três maneiras de explorar.</small></div>{graphViews.map(view=><button key={view.id} role="menuitemradio" aria-checked={view.id===value} tabIndex={view.id===value?0:-1} aria-labelledby={id+'-'+view.id} aria-describedby={id+'-'+view.id+'-description'} onClick={()=>{onChange(view.id);close();}}><Preview view={view.id}/><span><strong id={id+'-'+view.id}>{view.name}</strong><small id={id+'-'+view.id+'-description'}>{view.description}</small></span>{view.id===value&&<Check size={16}/>}</button>)}</div>}
 </div>;
}
