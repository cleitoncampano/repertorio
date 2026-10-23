import {useEffect,useRef,useState} from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import {ChevronLeft,ChevronRight,Copy,ExternalLink,Link,Maximize,Minimize,PanelRight,Pause,Play,RectangleHorizontal,SkipBack,SkipForward,Volume2,VolumeX,X} from 'lucide-react';
import {sized} from './api';
import {motionSummary} from './MotionParts';
import {kindName,terms,type Detail,type Reference,type Vocabulary} from './types';

// Ver uma referência em tela grande, como no YouTube: modo padrão (peça grande, ficha e parecidos ao lado),
// modo teatro (peça na largura toda, ficha abaixo) e tela cheia. Como no Prompt Motion, passa-se de uma
// referência a outra pelas setas da tela, pelas setas do teclado ou deslizando para o lado (dedo ou trackpad).
// Imagem: as setas sobre a peça, ← → e o deslize passam pelas imagens do material; os botões do canto,
// ↑ ↓, N e P trocam de material. Material de uma imagem só: ← → e o deslize já trocam de material.
// Vídeo: as setas e ← → trocam de vídeo; espaço ou K, M, Shift + ← → (5 s), J e L (10 s). T alterna o teatro e F a tela cheia.
type Mode='default'|'theater';
const MODE_KEY='repertorio-cinema-mode';
const clock=(s:number)=>!Number.isFinite(s)?'0:00':`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
type FullscreenDocument=Document&{webkitFullscreenElement?:Element;webkitExitFullscreen?:()=>void};
type FullscreenElement=HTMLElement&{webkitRequestFullscreen?:()=>void};

const ASPECT_NAMES:Record<string,string>={horizontal:'Horizontal',vertical:'Vertical',quadrado:'Quadrado ou 4:5'};

export function MotionCinema({item,detail,sequence,vocab,onClose,onOpen,onDetails,copy}:{item:Reference;detail?:Detail;sequence:Reference[];vocab?:Vocabulary;onClose:()=>void;onOpen:(id:string,workspace?:string)=>void;onDetails:()=>void;copy:(text:string)=>void}){
 const isVideo=!!item.motion?.video;
 const [mode,setMode]=useState<Mode>(()=>{try{return localStorage.getItem(MODE_KEY)==='theater'?'theater':'default';}catch{return 'default';}});
 const [playing,setPlaying]=useState(false),[time,setTime]=useState(0),[duration,setDuration]=useState(item.motion?.duration||0);
 const [muted,setMuted]=useState(false),[volume,setVolume]=useState(1),[full,setFull]=useState(false),[filled,setFilled]=useState(false),[idle,setIdle]=useState(false);
 const video=useRef<HTMLVideoElement|null>(null),stage=useRef<HTMLDivElement>(null),idleTimer=useRef(0),pointer=useRef('mouse');
 // O diálogo monta o conteúdo depois do primeiro desenho: o vídeo começa quando o elemento existe.
 const [node,setNode]=useState<HTMLVideoElement|null>(null);
 const d=detail?.id===item.id?detail:undefined;
 const related=(d?.related||[]).filter(r=>isVideo?r.motion?.video:r.thumbnail);
 // Imagem: numa apresentação, os slides em sequência; nas outras peças, as prévias.
 const slides=(d?.children||[]).filter(c=>c.thumbnail).map((c,i)=>({url:c.thumbnail!,label:`Slide ${c.number??i+1}`}));
 const previews=(d?.assets||[]).filter(a=>a.role==='preview'&&!a.missing).map((a,i,all)=>({url:a.url,label:all.length>1?`Prévia ${i+1}`:'Prévia'}));
 const frames=slides.length?slides:previews.length?previews:item.thumbnail?[{url:item.thumbnail,label:'Prévia'}]:[];
 const [frame,setFrame]=useState(0);
 useEffect(()=>setFrame(0),[item.id]);
 const shown=frames[Math.min(frame,frames.length-1)];
 const step=(delta:number)=>{const next=Math.max(0,Math.min(frames.length-1,frame+delta));if(next===frame)return;setDirection(delta);setFrame(next);};
 const multi=!isVideo&&frames.length>1;
 // Vizinhos na ordem em que o espaço está sendo visto (busca, lista ou o espaço inteiro).
 const index=sequence.findIndex(r=>r.id===item.id),previous=index>0?sequence[index-1]:undefined,following=index>=0?sequence[index+1]:sequence[0];
 const [direction,setDirection]=useState(0);
 const swipe=useRef<{x:number;y:number}|null>(null),swiped=useRef(false);
 useEffect(()=>{try{localStorage.setItem(MODE_KEY,mode);}catch{/* O modo volta ao padrão sem armazenamento. */}},[mode]);

 // Abrir é um clique do usuário: tenta tocar com som e, se o navegador recusar, toca sem som.
 useEffect(()=>{
  const v=node;if(!v)return;
  setTime(0);v.muted=muted;
  v.play().catch(()=>{v.muted=true;setMuted(true);v.play().catch(()=>{/* Fica o botão de reproduzir. */});});
 },[node]);

 useEffect(()=>{
  const sync=()=>{const doc=document as FullscreenDocument;setFull(!!(doc.fullscreenElement||doc.webkitFullscreenElement));};
  document.addEventListener('fullscreenchange',sync);document.addEventListener('webkitfullscreenchange',sync);
  return()=>{document.removeEventListener('fullscreenchange',sync);document.removeEventListener('webkitfullscreenchange',sync);clearTimeout(idleTimer.current);};
 },[]);

 const toggle=()=>{const v=video.current;if(!v)return;if(v.paused)v.play().catch(()=>{});else v.pause();};
 const seek=(to:number)=>{const v=video.current;if(v&&Number.isFinite(v.duration))v.currentTime=Math.max(0,Math.min(v.duration,to));};
 const mute=()=>{const v=video.current;if(!v)return;v.muted=!v.muted;setMuted(v.muted);if(!v.muted&&v.volume===0){v.volume=.5;setVolume(.5);}};
 const changeVolume=(value:number)=>{const v=video.current;if(!v)return;v.volume=value;v.muted=value===0;setVolume(value);setMuted(v.muted);};
 // Tela cheia de verdade quando o navegador permite; senão, o vídeo ocupa a janela inteira.
 const fullscreen=()=>{
  const doc=document as FullscreenDocument,el=stage.current as FullscreenElement|null;
  if(doc.fullscreenElement||doc.webkitFullscreenElement){(doc.exitFullscreen?doc.exitFullscreen():doc.webkitExitFullscreen?.());return;}
  if(filled){setFilled(false);return;}
  const request=el?.requestFullscreen?()=>el.requestFullscreen():el?.webkitRequestFullscreen?()=>Promise.resolve(el.webkitRequestFullscreen!()):null;
  if(!request||!(doc.fullscreenEnabled??true)){setFilled(true);return;}
  Promise.resolve(request()).catch(()=>setFilled(true));
 };
 const wake=()=>{setIdle(false);clearTimeout(idleTimer.current);idleTimer.current=window.setTimeout(()=>setIdle(true),2500);};
 // No toque, como no YouTube: o primeiro toque mostra os controles; com eles à vista, toca ou pausa.
 const tap=()=>{if(swiped.current){swiped.current=false;return;}if(pointer.current==='touch'&&idle&&playing){wake();return;}if(isVideo)toggle();};
 const go=(step:number)=>{const target=step<0?previous:following;if(!target)return;setDirection(step);onOpen(target.id,target.workspace_id);};
 // Passar para o lado: imagens do material quando há mais de uma; senão, o próximo material.
 const side=(delta:number)=>{if(multi)step(delta);else go(delta);};
 const goRef=useRef(side);goRef.current=side;
 // Dois dedos para o lado no trackpad: um gesto troca um vídeo só, mesmo com a inércia do movimento.
 const [content,setContent]=useState<HTMLDivElement|null>(null);
 useEffect(()=>{
  if(!content)return;
  let sum=0,locked=false,quiet=0;
  const wheel=(e:WheelEvent)=>{
   if(Math.abs(e.deltaX)<=Math.abs(e.deltaY)||(e.target as HTMLElement).closest('pre'))return;
   e.preventDefault();clearTimeout(quiet);quiet=window.setTimeout(()=>{locked=false;sum=0;},220);
   if(locked)return;
   sum+=e.deltaX;
   if(Math.abs(sum)>90){locked=true;goRef.current(sum>0?1:-1);sum=0;}
  };
  content.addEventListener('wheel',wheel,{passive:false});
  return()=>{content.removeEventListener('wheel',wheel);clearTimeout(quiet);};
 },[content]);

 // Os atalhos valem na página inteira enquanto o player está aberto, inclusive em tela cheia;
 // os do mapa ficam parados. Esc segue com o diálogo.
 const onKey=(e:KeyboardEvent)=>{
  if(e.key==='Escape')return;
  e.stopPropagation();
  const target=e.target as HTMLElement;
  if(target.tagName==='INPUT'&&e.key.startsWith('Arrow'))return; // a barra de tempo e o volume tratam as setas
  if(target.tagName==='BUTTON'&&(e.key===' '||e.key==='Enter'))return;
  const v=video.current,key=e.key.toLowerCase();
  const shared:Record<string,()=>void>={f:fullscreen,t:()=>setMode(m=>m==='theater'?'default':'theater'),n:()=>go(1),p:()=>go(-1)};
  const actions:Record<string,()=>void>=isVideo?{...shared,' ':toggle,k:toggle,m:mute,
   arrowleft:()=>e.shiftKey?seek((v?.currentTime||0)-5):go(-1),arrowright:()=>e.shiftKey?seek((v?.currentTime||0)+5):go(1),
   j:()=>seek((v?.currentTime||0)-10),l:()=>seek((v?.currentTime||0)+10),
   arrowup:()=>changeVolume(Math.min(1,(v?.volume||0)+.1)),arrowdown:()=>changeVolume(Math.max(0,(v?.volume||0)-.1))}
   :{...shared,arrowleft:()=>side(-1),arrowright:()=>side(1),arrowup:()=>go(-1),arrowdown:()=>go(1)};
  if(isVideo&&/^[0-9]$/.test(key)&&v){seek(v.duration*Number(key)/10);e.preventDefault();return;}
  if(actions[key]&&!e.metaKey&&!e.ctrlKey&&!e.altKey){actions[key]();wake();e.preventDefault();}
 };
 const keyRef=useRef(onKey);keyRef.current=onKey;
 useEffect(()=>{const listen=(e:KeyboardEvent)=>keyRef.current(e);document.addEventListener('keydown',listen);return()=>document.removeEventListener('keydown',listen);},[]);

 const source=d?.source;
 const progress=duration?time/duration*100:0;
 const noun=isVideo?'vídeo':'referência';
 const techniques=terms(vocab,'tecnicas');
 const meta=isVideo?motionSummary(item):[kindName[item.kind]||'Referência',ASPECT_NAMES[item.aspect||''],item.origin==='pptreta'?'PPTRETA':item.origin==='externa'?'Externa':''].filter(Boolean).join(' · ');
 return <Dialog.Root open onOpenChange={open=>{if(!open)onClose();}}><Dialog.Portal><Dialog.Overlay className="cinema-overlay"/>
  <Dialog.Content ref={setContent} className={'cinema '+mode+(filled?' filled':'')} aria-describedby={undefined}
   onEscapeKeyDown={e=>{e.stopPropagation();const doc=document as FullscreenDocument;if(doc.fullscreenElement||doc.webkitFullscreenElement){e.preventDefault();return;}if(filled){e.preventDefault();setFilled(false);}}}>
   <header className="cinema-bar"><Dialog.Title>{item.title}</Dialog.Title>{index>=0&&sequence.length>1&&<span className="cinema-count">{index+1} de {sequence.length}</span>}
    <Dialog.Close aria-label={isVideo?'Fechar vídeo':'Fechar'} title="Fechar (Esc)"><X size={21}/></Dialog.Close></header>
   <div className="cinema-body">
    <div ref={stage} className={'cinema-stage'+(idle&&playing?' idle':'')} onPointerDown={e=>{pointer.current=e.pointerType;swipe.current=e.pointerType==='touch'?{x:e.clientX,y:e.clientY}:null;}}
     onPointerUp={e=>{const start=swipe.current;swipe.current=null;if(!start)return;const dx=e.clientX-start.x,dy=e.clientY-start.y;if(Math.abs(dx)>60&&Math.abs(dx)>1.5*Math.abs(dy)){swiped.current=true;side(dx<0?1:-1);}}}
     onPointerMove={wake} onPointerLeave={()=>playing&&setIdle(true)}>
     {isVideo?<video ref={el=>{video.current=el;setNode(el);}} key={item.motion?.video} className={direction>0?'from-right':direction<0?'from-left':''} src={item.motion?.video} poster={sized(item.thumbnail,2048)} playsInline loop
      onClick={tap} onDoubleClick={fullscreen} onPlay={()=>{setPlaying(true);wake();}} onPause={()=>{setPlaying(false);setIdle(false);}}
      onTimeUpdate={e=>setTime(e.currentTarget.currentTime)} onLoadedMetadata={e=>setDuration(e.currentTarget.duration)}
      onVolumeChange={e=>{setMuted(e.currentTarget.muted);setVolume(e.currentTarget.volume);}} aria-label={'Vídeo: '+item.title}/>
     :shown&&<img key={item.id+':'+frame} className={'cinema-picture'+(direction>0?' from-right':direction<0?' from-left':'')} src={sized(shown.url,2048)} alt={item.title+', '+shown.label} onClick={tap} onDoubleClick={fullscreen} draggable={false}/>}
     {isVideo&&!playing&&<button className="cinema-big-play" onClick={toggle} aria-label="Reproduzir"><Play size={34} fill="currentColor"/></button>}
     {isVideo?<>
      {previous&&<button className="cinema-side previous" onClick={()=>go(-1)} aria-label="Vídeo anterior" title="Anterior (←)"><ChevronLeft size={30}/></button>}
      {following&&<button className="cinema-side next" onClick={()=>go(1)} aria-label="Próximo vídeo" title="Próximo (→)"><ChevronRight size={30}/></button>}
     </>:multi&&<>
      {frame>0&&<button className="cinema-side previous" onClick={()=>step(-1)} aria-label="Imagem anterior" title="Imagem anterior (←)"><ChevronLeft size={30}/></button>}
      {frame<frames.length-1&&<button className="cinema-side next" onClick={()=>step(1)} aria-label="Próxima imagem" title="Próxima imagem (→)"><ChevronRight size={30}/></button>}
     </>}
     {!isVideo&&<div className="cinema-tools">
      <button onClick={()=>setMode(mode==='theater'?'default':'theater')} aria-label={mode==='theater'?'Modo padrão':'Modo teatro'} title={mode==='theater'?'Modo padrão (T)':'Modo teatro (T)'} aria-pressed={mode==='theater'}><RectangleHorizontal size={18}/></button>
      <button onClick={fullscreen} aria-label={full||filled?'Sair da tela cheia':'Tela cheia'} title={full||filled?'Sair da tela cheia (F)':'Tela cheia (F)'}>{full||filled?<Minimize size={17}/>:<Maximize size={17}/>}</button></div>}
     {!isVideo&&frames.length>1&&<div className="cinema-strip" aria-label="Slides">{frames.map((f,i)=><button key={f.url} className={i===frame?'current':''} aria-current={i===frame} aria-label={f.label} onClick={()=>{setDirection(i>frame?1:-1);setFrame(i);}}><img src={sized(f.url,256)} alt="" loading="lazy"/></button>)}<span>Imagem {frame+1} de {frames.length}</span></div>}
     {isVideo&&<div className="cinema-controls">
      <input className="cinema-progress" type="range" min={0} max={duration||0} step={.01} value={time} aria-label="Posição do vídeo"
       style={{'--progress':progress+'%'} as React.CSSProperties} onChange={e=>seek(Number(e.target.value))}/>
      <div className="cinema-row">
       <button onClick={toggle} aria-label={playing?'Pausar':'Reproduzir'} title={playing?'Pausar (K)':'Reproduzir (K)'}>{playing?<Pause size={20} fill="currentColor"/>:<Play size={20} fill="currentColor"/>}</button>
       <button onClick={()=>go(-1)} disabled={!previous} aria-label="Voltar ao vídeo anterior" title="Anterior (P)"><SkipBack size={19} fill="currentColor"/></button>
       <button onClick={()=>go(1)} disabled={!following} aria-label="Avançar para o próximo vídeo" title="Próximo (N)"><SkipForward size={19} fill="currentColor"/></button>
       <div className="cinema-volume"><button onClick={mute} aria-label={muted?'Ativar som':'Desativar som'} title={muted?'Ativar som (M)':'Desativar som (M)'}>{muted||volume===0?<VolumeX size={20}/>:<Volume2 size={20}/>}</button>
        <input type="range" min={0} max={1} step={.05} value={muted?0:volume} onChange={e=>changeVolume(Number(e.target.value))} aria-label="Volume"/></div>
       <span className="cinema-time">{clock(time)} / {clock(duration)}</span>
       <i/>
       <button className="cinema-theater" onClick={()=>setMode(mode==='theater'?'default':'theater')} aria-label={mode==='theater'?'Modo padrão':'Modo teatro'} title={mode==='theater'?'Modo padrão (T)':'Modo teatro (T)'} aria-pressed={mode==='theater'}><RectangleHorizontal size={20}/></button>
       <button onClick={fullscreen} aria-label={full||filled?'Sair da tela cheia':'Tela cheia'} title={full||filled?'Sair da tela cheia (F)':'Tela cheia (F)'}>{full||filled?<Minimize size={19}/>:<Maximize size={19}/>}</button>
      </div>
     </div>}
    </div>
    <aside className="cinema-info">
     <div className="cinema-meta">{meta}{source?.author&&<> · {source.author}</>}</div>
     <h2>{item.title}</h2>
     <p className="cinema-description">{item.description}</p>
     <div className="cinema-actions">
      <button onClick={onDetails}><PanelRight size={14}/> Ficha completa</button>
      {d?.prompt&&<button onClick={()=>copy(d.prompt!)}><Copy size={14}/> Copiar prompt</button>}
      {!isVideo&&<button onClick={()=>copy(item.url)}><Link size={14}/> Copiar link</button>}
      {source?.post&&<a href={source.post} target="_blank" rel="noreferrer"><ExternalLink size={14}/> Post do autor</a>}
     </div>
     {item.idea&&<section><h3>Ideia transferível</h3><p>{item.idea}</p></section>}
     {d?.how&&<section><h3>{isVideo?'Decupagem':'Como funciona'}</h3><p>{d.how}</p></section>}
     {!isVideo&&d?.html&&<section><h3>Como fazer em HTML</h3><p>{d.html}</p></section>}
     {!isVideo&&!!item.techniques?.length&&<section><h3>Conexões criativas</h3><div className="cinema-chips">{item.techniques.map(id=><span key={id}>{techniques.find(t=>t.id===id)?.nome||id}</span>)}</div></section>}
     {!isVideo&&!!item.intentions?.length&&<section><h3>Papel na história</h3><div className="cinema-chips">{item.intentions.map(id=><span key={id}>{id}</span>)}</div></section>}
     {d?.prompt&&<section><h3>{d.template?'Prompt do modelo':'Prompt original'}</h3><pre>{d.prompt}</pre></section>}
     {!!related.length&&<section className="cinema-next"><h3>Parecidos com este</h3>{related.map(r=><button key={r.id} onClick={()=>{setDirection(1);onOpen(r.id,r.workspace_id);}}>
      <span className="cinema-thumb">{r.thumbnail&&<img src={sized(r.thumbnail,512)} alt="" loading="lazy"/>}{r.motion?.duration&&<small>{clock(r.motion.duration)}</small>}</span>
      <span><strong>{r.title}</strong><em>{r.idea||r.description}</em></span></button>)}</section>}
     {sequence.length>1&&<nav className="cinema-pager" aria-label={'Trocar de '+noun}><span>{index>=0?`${index+1} de ${sequence.length}`:''}</span>
      <button onClick={()=>go(-1)} disabled={!previous} aria-label={isVideo?'Anterior':'Material anterior'} title={isVideo?'Anterior (←)':'Material anterior (↑)'}><ChevronLeft size={18}/></button>
      <button onClick={()=>go(1)} disabled={!following} aria-label={isVideo?'Próximo':'Próximo material'} title={isVideo?'Próximo (→)':'Próximo material (↓)'}><ChevronRight size={18}/></button></nav>}
    </aside>
   </div>
  </Dialog.Content></Dialog.Portal></Dialog.Root>;
}
