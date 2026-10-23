import {useId,useRef,useState} from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import {ArrowUpRight,BellRing,BookA,Bug,Check,Clapperboard,ClipboardCheck,Code2,Copy,FileCode2,Film,Gauge,Gem,GraduationCap,Image,Layers,LayoutTemplate,Lightbulb,ListChecks,Package,Paintbrush,Palette,Presentation,ScanEye,Search,Shuffle,Smartphone,Sparkles,Target,Vibrate,WandSparkles,Waves,X} from 'lucide-react';
import {buildSkillRequest,searchSkills,skills,type Skill,type SkillCategory} from './skillCatalog';
import type {Workspace} from './types';

const icons:Record<string,typeof Sparkles>={impeccable:Paintbrush,'frontend-design':Code2,'landing-page-design':LayoutTemplate,imagegen:Image,'presentations:Presentations':Presentation,hyperframes:Film,'hyperframes-creative':Clapperboard,'perestroika-tese':Target,'perestroika-experiencia':GraduationCap,'perestroika-revisao':ClipboardCheck,
 'emil-design-eng':Gem,'apple-design':Waves,prototype:Shuffle,'break-ui':Bug,'mobile-native':Smartphone,'design-taste-frontend':Palette,animate:WandSparkles,'animate-expo':Vibrate,'review-animations':ScanEye,'improve-animations':ListChecks,'find-animation-opportunities':Lightbulb,'animation-performance':Gauge,'animation-vocabulary':BookA,'pick-ui-library':Package,'ask-sonner':BellRing,'write-swift':FileCode2};
const categories:('Todas'|SkillCategory)[]=['Todas','Design','Animação','Imagens','Apresentações','Vídeo','Método','Código'];

export function Skills({workspace}:{workspace?:Workspace}){
 const [query,setQuery]=useState(''),[category,setCategory]=useState<SkillCategory|'Todas'>('Todas');
 const [selected,setSelected]=useState<Skill|null>(null),[goal,setGoal]=useState(''),[copied,setCopied]=useState(false),[copyError,setCopyError]=useState('');
 const preview=useRef<HTMLTextAreaElement>(null),returnFocus=useRef<HTMLButtonElement|null>(null),goalId=useId(),previewId=useId();
 const matches=searchSkills(query,category);
 const request=selected?buildSkillRequest(selected,goal,workspace):'';
 const open=(skill:Skill,trigger:HTMLButtonElement)=>{returnFocus.current=trigger;setSelected(skill);setGoal(skill.example);setCopied(false);setCopyError('');};
 const copy=async()=>{setCopied(false);setCopyError('');try{await navigator.clipboard.writeText(request);setCopied(true);}catch{preview.current?.focus();preview.current?.select();setCopyError('Selecionei o pedido. Use ⌘C ou Ctrl+C para copiar.');}};
 return <section className="collection-page skills-page" aria-label="Catálogo de skills">
  <div className="skills-intro"><div><span className="eyebrow"><Sparkles size={14}/> SKILLS</span><h1>O que vamos criar?</h1><p className="page-intro">Escolha uma habilidade, conte sua ideia e leve o pedido para a conversa com seu agente.</p></div><span className="skills-curated">{skills.length} skills escolhidas por você</span></div>
  <div className="skills-tools"><label className="skills-search"><Search size={17}/><input aria-label="Buscar skills" placeholder="O que você quer fazer?" value={query} onChange={e=>setQuery(e.target.value)}/>{query&&<button aria-label="Limpar busca de skills" onClick={()=>setQuery('')}><X size={15}/></button>}</label><div className="skill-categories" role="group" aria-label="Categorias de skills">{categories.map(item=><button key={item} aria-pressed={category===item} onClick={()=>setCategory(item)}>{item}</button>)}</div></div>
  <div className="skills-context"><Layers size={15}/><span>{workspace?<>Inspiração do espaço <strong>{workspace.name}</strong></>:'Escolha um espaço para definir o repertório de inspiração.'}</span><small>Você pode usar estas skills em qualquer espaço.</small></div>
  <div className="skills-grid">{matches.map(skill=>{const Icon=icons[skill.id];return <article key={skill.id} className="skill-card" aria-labelledby={'skill-'+skill.id}>
   <div className="skill-card-top"><Icon size={22} strokeWidth={1.5}/><span>{skill.category}</span></div><h2 id={'skill-'+skill.id}>{skill.name}</h2><p>{skill.description}</p><div className="skill-when"><span>QUANDO USAR</span><p>{skill.when}</p></div><button aria-label={'Montar pedido com '+skill.name} onClick={e=>open(skill,e.currentTarget)}>Montar pedido <ArrowUpRight size={16}/></button>
  </article>;})}</div>
  {!matches.length&&<div className="skills-empty"><Search size={24}/><h2>Nenhuma skill encontrada.</h2><p>Tente outro objetivo ou veja todas as categorias.</p><button onClick={()=>{setQuery('');setCategory('Todas');}}>Ver todas as skills</button></div>}
  <Dialog.Root open={!!selected} onOpenChange={value=>{if(!value)setSelected(null);}}><Dialog.Portal><Dialog.Overlay className="dialog-overlay"/><Dialog.Content className="skill-dialog" onCloseAutoFocus={e=>{e.preventDefault();returnFocus.current?.focus();}}>
   <Dialog.Close className="dialog-close" aria-label="Fechar pedido"><X size={20}/></Dialog.Close>
   <span className="eyebrow">MONTAR PEDIDO</span><Dialog.Title>{selected?.name}</Dialog.Title><Dialog.Description>Adapte a ideia, copie o pedido e cole na conversa com seu agente para acionar a skill.</Dialog.Description>
   <label htmlFor={goalId}>O que você quer criar ou melhorar?</label><textarea id={goalId} className="skill-goal" rows={3} value={goal} maxLength={4000} onChange={e=>{setGoal(e.target.value);setCopied(false);setCopyError('');}}/>
   <div className="skill-request-space"><Layers size={16}/><span>{workspace?<>Repertório de <strong>{workspace.name}</strong></>:'O agente vai perguntar qual espaço usar como inspiração.'}</span></div>
   <label htmlFor={previewId}>Seu pedido para o agente</label><textarea id={previewId} ref={preview} className="skill-request" rows={8} readOnly value={request}/>
   <div className="skill-dialog-actions"><span role="status">{copyError|| (copied?'Pedido copiado. Cole na conversa com seu agente.':'O pedido inclui a skill e o repertório de inspiração.')}</span><button disabled={!goal.trim()} onClick={()=>void copy()}>{copied?<Check size={16}/>:<Copy size={16}/>} {copied?'Copiado':'Copiar pedido'}</button></div>
  </Dialog.Content></Dialog.Portal></Dialog.Root>
 </section>;
}
