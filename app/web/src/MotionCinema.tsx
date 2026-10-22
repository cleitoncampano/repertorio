import {useEffect,useRef,useState} from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import {Copy,ExternalLink,Maximize,Minimize,PanelRight,Pause,Play,RectangleHorizontal,SkipForward,Volume2,VolumeX,X} from 'lucide-react';
import {sized} from './api';
import {motionSummary} from './MotionParts';
import type {Detail,Reference} from './types';

// Assistir um vídeo de motion como no YouTube: modo padrão (vídeo grande, detalhes e próximos ao lado),
// modo teatro (vídeo na largura toda, detalhes abaixo) e tela cheia. Atalhos: espaço ou K, F, T, M, setas, J e L.
type Mode='default'|'theater';
const MODE_KEY='repertorio-cinema-mode';
const clock=(s:number)=>!Number.isFinite(s)?'0:00':`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
type FullscreenDocument=Document&{webkitFullscreenElement?:Element;webkitExitFullscreen?:()=>void};
type FullscreenElement=HTMLElement&{webkitRequestFullscreen?:()=>void};

export function MotionCinema({item,detail,onClose,onOpen,onDetails,copy}:{item:Reference;detail?:Detail;onClose:()=>void;onOpen:(id:string,workspace?:string)=>void;onDetails:()=>void;copy:(text:string)=>void}){
 const [mode,setMode]=useState<Mode>(()=>{try{return localStorage.getItem(MODE_KEY)==='theater'?'theater':'default';}catch{return 'default';}});
 const [playing,setPlaying]=useState(false),[time,setTime]=useState(0),[duration,setDuration]=useState(item.motion?.duration||0);
 const [muted,setMuted]=useState(false),[volume,setVolume]=useState(1),[full,setFull]=useState(false),[filled,setFilled]=useState(false),[idle,setIdle]=useState(false);
 const video=useRef<HTMLVideoElement|null>(null),stage=useRef<HTMLDivElement>(null),idleTimer=useRef(0),pointer=useRef('mouse');
 // O diálogo monta o conteúdo depois do primeiro desenho: o vídeo começa quando o elemento existe.
 const [node,setNode]=useState<HTMLVideoElement|null>(null);
 const d=detail?.id===item.id?detail:undefined;
 const next=(d?.related||[]).filter(r=>r.motion?.video);
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
 const tap=()=>{if(pointer.current==='touch'&&idle&&playing){wake();return;}toggle();};
 const playNext=()=>{if(next[0])onOpen(next[0].id,next[0].workspace_id);};

 const onKey=(e:React.KeyboardEvent)=>{
  e.stopPropagation(); // atalhos do mapa ficam parados enquanto o vídeo está aberto
  const target=e.target as HTMLElement;
  if(target.tagName==='INPUT'&&e.key.startsWith('Arrow'))return; // a barra de tempo e o volume tratam as setas
  if(target.tagName==='BUTTON'&&(e.key===' '||e.key==='Enter'))return;
  const v=video.current,key=e.key.toLowerCase();
  const actions:Record<string,()=>void>={' ':toggle,k:toggle,f:fullscreen,t:()=>setMode(m=>m==='theater'?'default':'theater'),m:mute,
   arrowleft:()=>seek((v?.currentTime||0)-5),arrowright:()=>seek((v?.currentTime||0)+5),j:()=>seek((v?.currentTime||0)-10),l:()=>seek((v?.currentTime||0)+10),
   arrowup:()=>changeVolume(Math.min(1,(v?.volume||0)+.1)),arrowdown:()=>changeVolume(Math.max(0,(v?.volume||0)-.1)),n:playNext};
  if(/^[0-9]$/.test(key)&&v){seek(v.duration*Number(key)/10);e.preventDefault();return;}
  if(actions[key]&&!e.metaKey&&!e.ctrlKey&&!e.altKey){actions[key]();wake();e.preventDefault();}
 };

 const source=d?.source;
 const progress=duration?time/duration*100:0;
 return <Dialog.Root open onOpenChange={open=>{if(!open)onClose();}}><Dialog.Portal><Dialog.Overlay className="cinema-overlay"/>
  <Dialog.Content className={'cinema '+mode+(filled?' filled':'')} aria-describedby={undefined} onKeyDown={onKey}
   onEscapeKeyDown={e=>{e.stopPropagation();const doc=document as FullscreenDocument;if(doc.fullscreenElement||doc.webkitFullscreenElement){e.preventDefault();return;}if(filled){e.preventDefault();setFilled(false);}}}>
   <header className="cinema-bar"><Dialog.Title>{item.title}</Dialog.Title>
    <Dialog.Close aria-label="Fechar vídeo" title="Fechar (Esc)"><X size={21}/></Dialog.Close></header>
   <div className="cinema-body">
    <div ref={stage} className={'cinema-stage'+(idle&&playing?' idle':'')} onPointerDown={e=>{pointer.current=e.pointerType;}} onPointerMove={wake} onPointerLeave={()=>playing&&setIdle(true)}>
     <video ref={el=>{video.current=el;setNode(el);}} key={item.motion?.video} src={item.motion?.video} poster={sized(item.thumbnail,2048)} playsInline loop
      onClick={tap} onDoubleClick={fullscreen} onPlay={()=>{setPlaying(true);wake();}} onPause={()=>{setPlaying(false);setIdle(false);}}
      onTimeUpdate={e=>setTime(e.currentTarget.currentTime)} onLoadedMetadata={e=>setDuration(e.currentTarget.duration)}
      onVolumeChange={e=>{setMuted(e.currentTarget.muted);setVolume(e.currentTarget.volume);}} aria-label={'Vídeo: '+item.title}/>
     {!playing&&<button className="cinema-big-play" onClick={toggle} aria-label="Reproduzir"><Play size={34} fill="currentColor"/></button>}
     <div className="cinema-controls">
      <input className="cinema-progress" type="range" min={0} max={duration||0} step={.01} value={time} aria-label="Posição do vídeo"
       style={{'--progress':progress+'%'} as React.CSSProperties} onChange={e=>seek(Number(e.target.value))}/>
      <div className="cinema-row">
       <button onClick={toggle} aria-label={playing?'Pausar':'Reproduzir'} title={playing?'Pausar (K)':'Reproduzir (K)'}>{playing?<Pause size={20} fill="currentColor"/>:<Play size={20} fill="currentColor"/>}</button>
       {!!next.length&&<button onClick={playNext} aria-label="Próximo vídeo" title="Próximo (N)"><SkipForward size={19} fill="currentColor"/></button>}
       <div className="cinema-volume"><button onClick={mute} aria-label={muted?'Ativar som':'Desativar som'} title={muted?'Ativar som (M)':'Desativar som (M)'}>{muted||volume===0?<VolumeX size={20}/>:<Volume2 size={20}/>}</button>
        <input type="range" min={0} max={1} step={.05} value={muted?0:volume} onChange={e=>changeVolume(Number(e.target.value))} aria-label="Volume"/></div>
       <span className="cinema-time">{clock(time)} / {clock(duration)}</span>
       <i/>
       <button className="cinema-theater" onClick={()=>setMode(mode==='theater'?'default':'theater')} aria-label={mode==='theater'?'Modo padrão':'Modo teatro'} title={mode==='theater'?'Modo padrão (T)':'Modo teatro (T)'} aria-pressed={mode==='theater'}><RectangleHorizontal size={20}/></button>
       <button onClick={fullscreen} aria-label={full||filled?'Sair da tela cheia':'Tela cheia'} title={full||filled?'Sair da tela cheia (F)':'Tela cheia (F)'}>{full||filled?<Minimize size={19}/>:<Maximize size={19}/>}</button>
      </div>
     </div>
    </div>
    <aside className="cinema-info">
     <div className="cinema-meta">{motionSummary(item)}{source?.author&&<> · {source.author}</>}</div>
     <h2>{item.title}</h2>
     <p className="cinema-description">{item.description}</p>
     <div className="cinema-actions">
      <button onClick={onDetails}><PanelRight size={14}/> Ficha completa</button>
      {d?.prompt&&<button onClick={()=>copy(d.prompt!)}><Copy size={14}/> Copiar prompt</button>}
      {source?.post&&<a href={source.post} target="_blank" rel="noreferrer"><ExternalLink size={14}/> Post do autor</a>}
     </div>
     {item.idea&&<section><h3>Ideia transferível</h3><p>{item.idea}</p></section>}
     {d?.how&&<section><h3>Decupagem</h3><p>{d.how}</p></section>}
     {d?.prompt&&<section><h3>{d.template?'Prompt do modelo':'Prompt original'}</h3><pre>{d.prompt}</pre></section>}
     {!!next.length&&<section className="cinema-next"><h3>A seguir</h3>{next.map(r=><button key={r.id} onClick={()=>onOpen(r.id,r.workspace_id)}>
      <span className="cinema-thumb">{r.thumbnail&&<img src={sized(r.thumbnail,512)} alt="" loading="lazy"/>}{r.motion?.duration&&<small>{clock(r.motion.duration)}</small>}</span>
      <span><strong>{r.title}</strong><em>{r.idea||r.description}</em></span></button>)}</section>}
    </aside>
   </div>
  </Dialog.Content></Dialog.Portal></Dialog.Root>;
}
