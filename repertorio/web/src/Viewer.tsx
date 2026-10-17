import {useEffect,useRef,useState} from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import {ChevronLeft,ChevronRight,Minus,Plus,X} from 'lucide-react';
import {sized} from './api';

export type ViewerItem={url:string;label:string;short?:string};
type View={s:number;x:number;y:number};
const FIT:View={s:1,x:0,y:0};
type GestureLike=Event&{scale:number;clientX:number;clientY:number};

// Em destaque: a imagem ocupa a tela e as setas passam pelos slides.
// Zoom de visualizador: rodinha ou pinça aproximam no ponto do cursor, arrastar move, duplo clique alterna.
// Mostra já a versão leve (2048 px) e troca pelo original assim que ele chega.
export function Viewer({title,items,start,open,onOpenChange,returnFocus}:{title:string;items:ViewerItem[];start:number;open:boolean;onOpenChange:(open:boolean)=>void;returnFocus?:React.RefObject<HTMLElement|null>}){
 const [index,setIndex]=useState(start),[full,setFull]=useState<string|null>(null);
 const [view,setView]=useState<View>(FIT),[smooth,setSmooth]=useState(false),[dragging,setDragging]=useState(false);
 const stage=useRef<HTMLDivElement|null>(null),picture=useRef<HTMLImageElement>(null),strip=useRef<HTMLDivElement>(null);
 // o palco só existe depois que o diálogo monta: guardar em estado liga a rodinha e a pinça na hora certa
 const [stageNode,setStageNode]=useState<HTMLDivElement|null>(null);
 const current=useRef(view);current.current=view;
 const drag=useRef<{x:number;y:number;vx:number;vy:number}|null>(null);
 useEffect(()=>{if(open)setIndex(Math.min(start,Math.max(0,items.length-1)));},[open,start,items.length]);
 const item=open?items[index]:undefined;
 useEffect(()=>{
  setView(FIT);setFull(null);if(!item)return;
  const img=new Image();img.onload=()=>setFull(item.url);img.src=item.url;
  strip.current?.querySelector(`[data-index="${index}"]`)?.scrollIntoView({block:'nearest',inline:'center'});
  return()=>{img.onload=null;};
 },[item?.url,index]);

 // Medidas no tamanho "imagem inteira": a caixa do <img>, a parte ocupada pela foto e a área visível do palco.
 const frame=()=>{
  const img=picture.current,box=stage.current;if(!img||!box)return null;
  const r=box.getBoundingClientRect(),W=img.offsetWidth,H=img.offsetHeight,ratio=img.naturalWidth/img.naturalHeight||16/9;
  const cw=Math.min(W,H*ratio),ch=cw/ratio;
  return {left:r.left+img.offsetLeft,top:r.top+img.offsetTop,W,H,cw,ch,ox:(W-cw)/2,oy:(H-ch)/2,
   vx:[-img.offsetLeft,box.clientWidth-img.offsetLeft],vy:[-img.offsetTop,box.clientHeight-img.offsetTop],
   // até 4 vezes, ou mais quando o original tem pixels para mostrar (limite de 12)
   max:Math.min(12,Math.max(4,2*img.naturalWidth/(window.devicePixelRatio||1)/cw))};
 };
 const clamp=(s:number,x:number,y:number):View=>{
  const f=frame();if(!f)return FIT;
  s=Math.min(f.max,Math.max(1,s));if(s<=1.001)return FIT;
  // menor que o palco: fica centralizada; maior: as bordas da foto não descolam das bordas do palco
  const axis=(t:number,content:number,offset:number,size:number,[v0,v1]:number[])=>s*content<=v1-v0?(size-s*content)/2-s*offset:Math.min(v0-s*offset,Math.max(v1-s*(offset+content),t));
  return {s,x:axis(x,f.cw,f.ox,f.W,f.vx),y:axis(y,f.ch,f.oy,f.H,f.vy)};
 };
 const zoomTo=(next:number,cx?:number,cy?:number,animated=false)=>{
  const f=frame();if(!f)return;const v=current.current;
  const px=(cx??f.left+f.W/2)-f.left,py=(cy??f.top+f.H/2)-f.top,s=Math.min(f.max,Math.max(1,next));
  setSmooth(animated);setView(clamp(s,px-(s/v.s)*(px-v.x),py-(s/v.s)*(py-v.y)));
 };
 const zoomRef=useRef(zoomTo);zoomRef.current=zoomTo;
 const clampRef=useRef(clamp);clampRef.current=clamp;

 useEffect(()=>{
  const box=stageNode;if(!box)return;
  let gesture=false,base=1;
  // Como nos apps do Mac: rodinha do mouse aproxima, pinça aproxima, dois dedos no trackpad movem a imagem.
  // A pinça chega como gesture no Safari e no app do Mac; nos outros navegadores, como wheel com ctrl.
  const wheel=(e:WheelEvent)=>{
   e.preventDefault();if(gesture)return;
   const legacy=(e as WheelEvent&{wheelDeltaY?:number}).wheelDeltaY;
   const notch=e.deltaMode===1||(!!legacy&&legacy%120===0); // rodinha de mouse anda em degraus de 120
   if(e.ctrlKey)zoomRef.current(current.current.s*Math.exp(-e.deltaY*.01),e.clientX,e.clientY);
   else if(notch)zoomRef.current(current.current.s*Math.pow(1.2,-Math.sign(e.deltaY)),e.clientX,e.clientY);
   else if(current.current.s>1){const v=current.current;setSmooth(false);setView(clampRef.current(v.s,v.x-e.deltaX,v.y-e.deltaY));}
  };
  const gestureStart=(e:Event)=>{e.preventDefault();gesture=true;base=current.current.s;};
  const gestureChange=(e:Event)=>{e.preventDefault();const g=e as GestureLike;zoomRef.current(base*g.scale,g.clientX,g.clientY);};
  const gestureEnd=(e:Event)=>{e.preventDefault();gesture=false;};
  const resize=()=>setView(FIT);
  box.addEventListener('wheel',wheel,{passive:false});
  box.addEventListener('gesturestart',gestureStart);box.addEventListener('gesturechange',gestureChange);box.addEventListener('gestureend',gestureEnd);
  window.addEventListener('resize',resize);
  return()=>{box.removeEventListener('wheel',wheel);box.removeEventListener('gesturestart',gestureStart);box.removeEventListener('gesturechange',gestureChange);box.removeEventListener('gestureend',gestureEnd);window.removeEventListener('resize',resize);};
 },[stageNode]);

 const go=(step:number)=>setIndex(i=>Math.min(items.length-1,Math.max(0,i+step)));
 const fit=()=>{setSmooth(true);setView(FIT);};
 const onKey=(e:React.KeyboardEvent)=>{
  e.stopPropagation(); // atalhos do app (busca, Esc do painel) ficam parados enquanto a peça está em destaque
  if(e.key==='ArrowRight'){go(1);e.preventDefault();}
  else if(e.key==='ArrowLeft'){go(-1);e.preventDefault();}
  else if(e.key==='+'||e.key==='='){zoomTo(view.s*1.5,undefined,undefined,true);e.preventDefault();}
  else if(e.key==='-'){zoomTo(view.s/1.5,undefined,undefined,true);e.preventDefault();}
  else if(e.key==='0'){fit();e.preventDefault();}
 };
 if(!item)return null;
 const zoomed=view.s>1;
 return <Dialog.Root open={open} onOpenChange={onOpenChange}><Dialog.Portal><Dialog.Overlay className="viewer-overlay"/>
  <Dialog.Content className="viewer" aria-describedby={undefined} onKeyDown={onKey} onEscapeKeyDown={e=>e.stopPropagation()} onCloseAutoFocus={e=>{e.preventDefault();returnFocus?.current?.focus();}}>
   <header className="viewer-bar"><div><Dialog.Title>{title}</Dialog.Title><span>{item.label}{items.length>1&&` · ${index+1} de ${items.length}`}</span></div>
    <div className="viewer-zoom">
     <button onClick={()=>zoomTo(view.s/1.5,undefined,undefined,true)} disabled={!zoomed} aria-label="Diminuir zoom" title="Diminuir (−)"><Minus size={16}/></button>
     <button className="viewer-percent" onClick={fit} aria-label="Ajustar à tela" title="Ajustar à tela (0)">{Math.round(view.s*100)}%</button>
     <button onClick={()=>zoomTo(view.s*1.5,undefined,undefined,true)} aria-label="Aumentar zoom" title="Aumentar (+)"><Plus size={16}/></button>
    </div>
    <Dialog.Close aria-label="Fechar e voltar" title="Fechar (Esc)"><X size={21}/></Dialog.Close></header>
   <div ref={node=>{stage.current=node;setStageNode(node);}} className={'viewer-stage'+(dragging?' dragging':'')}
    onClick={e=>{if(e.target===e.currentTarget&&!zoomed)onOpenChange(false);}}
    onDoubleClick={e=>zoomTo(zoomed?1:2.5,e.clientX,e.clientY,true)}
    onPointerDown={e=>{if(!zoomed||e.button!==0)return;drag.current={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y};setDragging(true);e.currentTarget.setPointerCapture(e.pointerId);}}
    onPointerMove={e=>{const d=drag.current;if(!d)return;setSmooth(false);setView(clamp(current.current.s,d.vx+e.clientX-d.x,d.vy+e.clientY-d.y));}}
    onPointerUp={()=>{drag.current=null;setDragging(false);}} onPointerCancel={()=>{drag.current=null;setDragging(false);}}>
    <img ref={picture} src={full||sized(item.url,2048)} alt={item.label} draggable={false}
     style={{transform:`translate(${view.x}px,${view.y}px) scale(${view.s})`,transition:smooth?'transform 180ms ease-out':'none'}}/>
   </div>
   {items.length>1&&<>
    <button className="viewer-arrow previous" disabled={!index} onClick={()=>go(-1)} aria-label="Anterior"><ChevronLeft size={28}/></button>
    <button className="viewer-arrow next" disabled={index===items.length-1} onClick={()=>go(1)} aria-label="Próxima"><ChevronRight size={28}/></button>
    <div className="viewer-strip" ref={strip}>{items.map((x,i)=><button key={x.url} data-index={i} className={i===index?'current':''} onClick={()=>setIndex(i)} aria-label={x.label} aria-current={i===index}><img src={sized(x.url,256)} alt="" loading="lazy"/><span>{x.short??i+1}</span></button>)}</div>
   </>}
  </Dialog.Content></Dialog.Portal></Dialog.Root>;
}
