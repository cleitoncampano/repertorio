import {useId,useRef,useState} from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import {ArrowUpRight,BookOpen,BellRing,BookA,Bug,Check,ClipboardCheck,Code2,Copy,FileCode2,Gauge,Gem,GraduationCap,Handshake,Image,Layers,LayoutTemplate,Lightbulb,ListChecks,Mic,Package,Paintbrush,Palette,Presentation,ScanEye,Search,Shuffle,Smartphone,Sparkles,Target,Vibrate,WandSparkles,Waves,X} from 'lucide-react';
import {buildSkillRequest,searchSkills,skillCategories,type Skill} from './skillCatalog';
import {useQuery} from '@tanstack/react-query';
import {api} from './api';
import {useCatalog} from './catalog';
import {SkillMarkdown} from './skillMarkdown';
import type {Workspace} from './types';

type SkillContent={id:string;file:string;content:string;files:string[];location:string};

// O catálogo indica o ícone de cada skill pelo nome do Lucide; sem ícone conhecido, vale o padrão.
const icons:Record<string,typeof Sparkles>={Paintbrush,Code2,LayoutTemplate,Image,Presentation,Target,GraduationCap,ClipboardCheck,Mic,Handshake,Gem,Waves,Shuffle,Bug,Smartphone,Palette,WandSparkles,Vibrate,ScanEye,ListChecks,Lightbulb,Gauge,BookA,Package,BellRing,FileCode2};

export function Skills({workspace}:{workspace?:Workspace}){
 const catalog=useCatalog(),skills=catalog.data?.skills||[],categories=skillCategories(skills);
 const [query,setQuery]=useState(''),[category,setCategory]=useState('Todas');
 const [selected,setSelected]=useState<Skill|null>(null),[goal,setGoal]=useState(''),[copied,setCopied]=useState(false),[copyError,setCopyError]=useState('');
 const preview=useRef<HTMLTextAreaElement>(null),returnFocus=useRef<HTMLButtonElement|null>(null),goalId=useId(),previewId=useId();
 const [reading,setReading]=useState<Skill|null>(null),[file,setFile]=useState('SKILL.md'),readId=useId(),body=useRef<HTMLDivElement>(null);
 const content=useQuery({queryKey:['skill-content',reading?.id,file],enabled:!!reading,staleTime:60000,retry:false,
  queryFn:()=>api<SkillContent>('/skills/'+encodeURIComponent(reading!.id)+'/content'+(file==='SKILL.md'?'':'?file='+encodeURIComponent(file)))});
 const matches=searchSkills(skills,query,category);
 const request=selected?buildSkillRequest(selected,goal,workspace):'';
 const open=(skill:Skill,trigger:HTMLButtonElement)=>{returnFocus.current=trigger;setSelected(skill);setGoal(skill.example);setCopied(false);setCopyError('');};
 const read=(skill:Skill,trigger:HTMLButtonElement)=>{returnFocus.current=trigger;setFile('SKILL.md');setReading(skill);};
 const openFile=(name:string)=>{setFile(name);body.current?.scrollTo({top:0});};
 // Da leitura para o pedido: o foco volta ao mesmo cartão quando o pedido fechar.
 const build=()=>{const skill=reading;setReading(null);if(skill){setSelected(skill);setGoal(skill.example);setCopied(false);setCopyError('');}};
 const copy=async()=>{setCopied(false);setCopyError('');try{await navigator.clipboard.writeText(request);setCopied(true);}catch{preview.current?.focus();preview.current?.select();setCopyError('Selecionei o pedido. Use ⌘C ou Ctrl+C para copiar.');}};
 return <section className="collection-page skills-page" aria-label="Catálogo de skills">
  <div className="skills-intro"><div><span className="eyebrow"><Sparkles size={14}/> SKILLS</span><h1>O que vamos criar?</h1><p className="page-intro">Escolha uma habilidade, conte sua ideia e leve o pedido para a conversa com seu agente.</p></div><span className="skills-curated">{catalog.isSuccess&&(skills.length===1?'1 skill':skills.length+' skills')+(catalog.data.personal?(skills.length===1?' escolhida por você':' escolhidas por você'):(skills.length===1?' sugerida':' sugeridas'))}</span></div>
  <div className="skills-tools"><label className="skills-search"><Search size={17}/><input aria-label="Buscar skills" placeholder="O que você quer fazer?" value={query} onChange={e=>setQuery(e.target.value)}/>{query&&<button aria-label="Limpar busca de skills" onClick={()=>setQuery('')}><X size={15}/></button>}</label><div className="skill-categories" role="group" aria-label="Categorias de skills">{categories.map(item=><button key={item} aria-pressed={category===item} onClick={()=>setCategory(item)}>{item}</button>)}</div></div>
  <div className="skills-grid">{matches.map(skill=>{const Icon=icons[skill.icon||'']||Sparkles;return <article key={skill.id} className="skill-card" aria-labelledby={'skill-'+skill.id}>
   <div className="skill-card-top"><Icon size={22} strokeWidth={1.5}/><span>{skill.category}</span></div><h2 id={'skill-'+skill.id}>{skill.name}</h2><p>{skill.description}</p><div className="skill-when"><span>QUANDO USAR</span><p>{skill.when}</p></div><div className="skill-card-actions"><button aria-label={'Montar pedido com '+skill.name} onClick={e=>open(skill,e.currentTarget)}>Montar pedido <ArrowUpRight size={16}/></button><button className="skill-read" aria-label={'Ler a skill '+skill.name} onClick={e=>read(skill,e.currentTarget)}><BookOpen size={15}/> Ler a skill</button></div>
  </article>;})}</div>
  {catalog.isError&&<div className="skills-empty" role="alert"><Search size={24}/><h2>Não consegui carregar as skills.</h2><p>Confira se o serviço do Repertório está ligado e recarregue a página.</p></div>}
  {catalog.isSuccess&&!matches.length&&<div className="skills-empty"><Search size={24}/><h2>Nenhuma skill encontrada.</h2><p>Tente outro objetivo ou veja todas as categorias.</p><button onClick={()=>{setQuery('');setCategory('Todas');}}>Ver todas as skills</button></div>}
  <Dialog.Root open={!!selected} onOpenChange={value=>{if(!value)setSelected(null);}}><Dialog.Portal><Dialog.Overlay className="dialog-overlay"/><Dialog.Content className="skill-dialog" onCloseAutoFocus={e=>{e.preventDefault();returnFocus.current?.focus();}}>
   <Dialog.Close className="dialog-close" aria-label="Fechar pedido"><X size={20}/></Dialog.Close>
   <span className="eyebrow">MONTAR PEDIDO</span><Dialog.Title>{selected?.name}</Dialog.Title><Dialog.Description>Adapte a ideia, copie o pedido e cole na conversa com seu agente para acionar a skill.</Dialog.Description>
   {selected?.source&&<p className="skill-source">Se o seu agente ainda não tem esta skill, instale pelo <a href={selected.source} target="_blank" rel="noreferrer">repositório da skill <ArrowUpRight size={13}/></a></p>}
   <label htmlFor={goalId}>O que você quer criar ou melhorar?</label><textarea id={goalId} className="skill-goal" rows={3} value={goal} maxLength={4000} onChange={e=>{setGoal(e.target.value);setCopied(false);setCopyError('');}}/>
   <div className="skill-request-space"><Layers size={16}/><span>{workspace?<>Repertório de <strong>{workspace.name}</strong></>:'O agente vai perguntar qual espaço usar como inspiração.'}</span></div>
   <label htmlFor={previewId}>Seu pedido para o agente</label><textarea id={previewId} ref={preview} className="skill-request" rows={8} readOnly value={request}/>
   <div className="skill-dialog-actions"><span role="status">{copyError|| (copied?'Pedido copiado. Cole na conversa com seu agente.':'O pedido inclui a skill e o repertório de inspiração.')}</span><button disabled={!goal.trim()} onClick={()=>void copy()}>{copied?<Check size={16}/>:<Copy size={16}/>} {copied?'Copiado':'Copiar pedido'}</button></div>
  </Dialog.Content></Dialog.Portal></Dialog.Root>
  <Dialog.Root open={!!reading} onOpenChange={value=>{if(!value)setReading(null);}}><Dialog.Portal><Dialog.Overlay className="dialog-overlay"/><Dialog.Content className="skill-dialog skill-reader" onCloseAutoFocus={e=>{e.preventDefault();returnFocus.current?.focus();}}>
   <Dialog.Close className="dialog-close" aria-label="Fechar leitura"><X size={20}/></Dialog.Close>
   <span className="eyebrow">CONTEÚDO DA SKILL</span><Dialog.Title>{reading?.name}</Dialog.Title><Dialog.Description>As instruções que o agente segue quando usa esta skill.</Dialog.Description>
   {content.data&&content.data.files.length>0&&<div className="skill-file"><label htmlFor={readId}>Arquivo</label><select id={readId} value={file} onChange={e=>openFile(e.target.value)}><option value="SKILL.md">Principal (SKILL.md)</option>{content.data.files.map(name=><option key={name} value={name}>{name}</option>)}</select></div>}
   <div className="skill-markdown" ref={body} tabIndex={0} aria-label={'Texto de '+(reading?.name||'')}>
    {content.isPending&&<p className="skill-reader-note" role="status">Abrindo a skill...</p>}
    {content.isError&&<div className="skill-reader-note" role="alert"><p>{(content.error as Error).message}</p>{reading?.source&&<p>Veja o texto no <a href={reading.source} target="_blank" rel="noreferrer">repositório da skill <ArrowUpRight size={13}/></a></p>}</div>}
    {content.data&&<SkillMarkdown text={content.data.content} file={content.data.file} files={content.data.files} onOpen={openFile}/>}
   </div>
   <div className="skill-dialog-actions"><span>{content.data?'Instalada em '+content.data.location:''}</span><button onClick={build}>Montar pedido <ArrowUpRight size={15}/></button></div>
  </Dialog.Content></Dialog.Portal></Dialog.Root>
 </section>;
}
