import {useEffect,useState} from 'react';
import {useQuery,useQueryClient} from '@tanstack/react-query';
import {BookOpen,Check,ListChecks,X} from 'lucide-react';
import {api,sized} from './api';
import {kindName} from './types';

type PackSummary={id:string;title:string;created:string;total:number;approved:number;cut:number};
export type Demand={id:string;demand:string;created:string;project_name:string;workspaces:{id:string;name:string}[];packs:PackSummary[]};
type Verdict='approved'|'cut';
type PackReference={workspace_ids:string[];id:string;title:string;idea?:string;description?:string;intentions?:string[];thumbnail:string|null;available:boolean;review:{verdict:Verdict;note:string}|null;kind?:string};
type PackDetail={id:string;demand:string;project_name:string;title:string;created:string;rationale:string;workspaces:{id:string;name:string}[];references:PackReference[]};

const when=(iso:string)=>new Date(iso).toLocaleString('pt-BR',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'});

// Escolhas: as referências que o agente separou para cada pedido. O usuário aprova ou corta antes da criação;
// o agente lê a revisão com get_pack.
export function Choices({demands,pack,onPack,onOpen,onError}:{demands:Demand[];pack:string|null;onPack:(id:string)=>void;onOpen:(id:string,workspaceId?:string)=>void;onError:(message:string)=>void}){
 const client=useQueryClient();
 const current=(pack&&demands.some(d=>d.packs.some(k=>k.id===pack))?pack:null)||demands[0]?.packs[0]?.id||null;
 const detail=useQuery({queryKey:['pack',current],queryFn:()=>api<PackDetail>('/packs/'+current),enabled:!!current});
 const [notes,setNotes]=useState<Record<string,string>>({});
 useEffect(()=>{setNotes(Object.fromEntries((detail.data?.references||[]).map(r=>[r.id,r.review?.note||''])));},[detail.data]);
 const decide=async(ref:PackReference,verdict:Verdict|null,note=notes[ref.id]||'')=>{
  try{
   const updated=await api<PackDetail>(`/packs/${current}/reviews`,{reference_id:ref.id,verdict,note});
   client.setQueryData(['pack',current],updated);client.invalidateQueries({queryKey:['demands']});
  }catch(e){onError((e as Error).message);}
 };
 if(!demands.length)return <div className="empty"><ListChecks/><h2>Nenhuma escolha por enquanto.</h2><p>Quando eu separar referências para um pedido seu, elas aparecem aqui para você aprovar ou cortar antes de eu criar.</p></div>;
 const d=detail.data,refs=d?.references||[];
 const approved=refs.filter(r=>r.review?.verdict==='approved').length,cut=refs.filter(r=>r.review?.verdict==='cut').length;
 return <div className="choices">
  <nav className="choice-list" aria-label="Pedidos">{demands.map(item=><div className="choice-demand" key={item.id}>
   <small>{item.project_name} · {when(item.packs[0]?.created||item.created)}</small><p>{item.demand}</p>
   {item.packs.map(k=>{const open=k.total-k.approved-k.cut;return <button key={k.id} className={k.id===current?'choice-pack current':'choice-pack'} aria-current={k.id===current} onClick={()=>onPack(k.id)}>
    <strong>{k.title}</strong><span>{open?`${open} para revisar`:'revisada'}</span></button>;})}
  </div>)}</nav>
  <section className="choice-detail" aria-label="Seleção">{detail.isPending?<p className="page-intro">Carregando…</p>:d&&<>
   <header className="choice-head"><small>{d.project_name} · {d.workspaces.map(w=>w.name).join(" + ")} · {when(d.created)}</small><h2>{d.title}</h2><p>{d.demand}</p>{d.rationale&&<p className="choice-rationale">{d.rationale}</p>}</header>
   <div className="choice-counts" role="status"><span><Check size={13}/> {approved} aprovadas</span><span><X size={13}/> {cut} cortadas</span><span>{refs.length-approved-cut} sem resposta</span></div>
   <div className="choice-grid">{refs.map(ref=>{const verdict=ref.review?.verdict;return <article key={ref.id} className={'choice-card'+(verdict?' '+verdict:'')}>
    <button className="choice-image" onClick={()=>onOpen(ref.id,ref.workspace_ids[0])} aria-label={'Ver detalhes de '+ref.title}>{ref.thumbnail?<img src={sized(ref.thumbnail,512)} alt="" loading="lazy"/>:<BookOpen size={28}/>}{ref.kind&&<span>{kindName[ref.kind]||ref.kind}</span>}</button>
    <div className="card-text"><h3>{ref.title}</h3><p>{ref.idea||ref.description}</p>{!ref.available&&<p className="status-note">Saiu da biblioteca depois da escolha.</p>}</div>
    <div className="verdicts">
     <button className={verdict==='approved'?'approve on':'approve'} aria-pressed={verdict==='approved'} onClick={()=>decide(ref,verdict==='approved'?null:'approved')}><Check size={14}/> Aprovar</button>
     <button className={verdict==='cut'?'cut on':'cut'} aria-pressed={verdict==='cut'} onClick={()=>decide(ref,verdict==='cut'?null:'cut')}><X size={14}/> Cortar</button>
    </div>
    {verdict&&<input className="choice-note" aria-label={'Comentário sobre '+ref.title} placeholder="Comentário para o Claude (opcional)" value={notes[ref.id]||''}
     onChange={e=>setNotes({...notes,[ref.id]:e.target.value})} onBlur={()=>{if((notes[ref.id]||'')!==(ref.review?.note||''))decide(ref,verdict);}}
     onKeyDown={e=>{if(e.key==='Enter')(e.target as HTMLInputElement).blur();}}/>}
   </article>;})}</div>
  </>}</section>
 </div>;
}
