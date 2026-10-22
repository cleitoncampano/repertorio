import {useEffect,useRef} from 'react';
import {Copy,ExternalLink} from 'lucide-react';
import {sized} from './api';
import type {Detail,Reference} from './types';

// Loop curto nas listas: toca enquanto o cartão está na tela e para ao sair, para não acumular decodificadores.
export function MotionThumb({item}:{item:Reference}){
 const video=useRef<HTMLVideoElement>(null);
 useEffect(()=>{
  const node=video.current;if(!node||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  const watch=new IntersectionObserver(([entry])=>{if(entry.isIntersecting)node.play().catch(()=>{/* fica a capa */});else node.pause();},{threshold:.35});
  watch.observe(node);return()=>watch.disconnect();
 },[item.motion?.loop]);
 return <video ref={video} src={item.motion?.loop} poster={sized(item.thumbnail,1024)} muted loop playsInline preload="none" aria-hidden="true"/>;
}

const clock=(seconds?:number)=>seconds==null?'':`${Math.floor(seconds/60)}:${String(Math.round(seconds%60)).padStart(2,'0')}`;
const ratio=(w?:number,h?:number)=>!w||!h?'':Math.abs(w/h-16/9)<.05?'16:9':Math.abs(w/h-9/16)<.05?'9:16':Math.abs(w/h-1)<.05?'1:1':Math.abs(w/h-4/5)<.05?'4:5':`${w}×${h}`;

export function motionSummary(d:Reference){
 const m=d.motion;if(!m)return '';
 return ['Vídeo',clock(m.duration),ratio(m.width,m.height),m.audio?'com som':m.audio===false?'sem som':''].filter(Boolean).join(' · ');
}

// Prompt que gerou o vídeo, skill usada e créditos do autor, como chegaram da fonte.
export function MotionInfo({detail:d,copy}:{detail:Detail;copy:(text:string)=>void}){
 const s=d.source;
 if(!d.prompt&&!s)return null;
 const facts=[s?.stack&&`Ferramenta: ${s.stack}`,s?.iterations&&`Rodadas: ${s.iterations==='One-shot'?'uma só':s.iterations==='A few rounds'?'algumas':s.iterations==='Many rounds'?'muitas':s.iterations}`,s?.effort&&`Esforço: ${s.effort}`,s?.model&&`Modelo: ${s.model}`].filter(Boolean);
 return <>
  {d.prompt&&<section className="detail-section"><h3>{d.template?'Prompt do modelo':'Prompt original'}</h3><div className="code-block motion-prompt"><pre>{d.prompt}</pre><button title="Copiar prompt" aria-label="Copiar prompt" onClick={()=>copy(d.prompt!)}><Copy size={15}/></button></div>{d.prompt_note&&<p>{d.prompt_note}</p>}</section>}
  {s?.skill&&<section className="detail-section"><h3>Skill usada</h3>{s.skill.about&&<p>{s.skill.about}</p>}{s.skill.install&&<div className="code-block"><pre>{s.skill.install}</pre><button title="Copiar" aria-label="Copiar instalação" onClick={()=>copy(s.skill!.install!)}><Copy size={15}/></button></div>}</section>}
  {s&&<section className="detail-section"><h3>Fonte</h3><p>{s.author&&<>Criado por {s.author}{s.handle&&` (@${s.handle})`}</>}{s.posted&&`, publicado em ${new Date(s.posted+'T12:00:00').toLocaleDateString('pt-BR')}`}{s.collection==='prompt-motion'&&', reunido no Prompt Motion'}.{s.title_original&&` Título original: “${s.title_original}”.`}</p>{!!facts.length&&<p>{facts.join(' · ')}</p>}
   <div className="detail-actions motion-links">{s.post&&<a href={s.post} target="_blank" rel="noreferrer"><ExternalLink size={14}/> Post do autor</a>}{s.page&&<a href={s.page} target="_blank" rel="noreferrer"><ExternalLink size={14}/> Prompt Motion</a>}{s.skill?.repo&&<a href={s.skill.repo} target="_blank" rel="noreferrer"><ExternalLink size={14}/> Repositório da skill</a>}</div></section>}
 </>;
}
