import {useEffect,useState} from 'react';
import {ArrowLeft,ArrowUpRight,ChevronRight,X} from 'lucide-react';
import {colors,terms,type GraphData} from './types';
import {sized} from './api';

type Labels={operation:string;technique:string;techniques:(n:number)=>string;references:string;count?:string;operationPanel?:string;techniquePanel?:string};
const DEFAULT_LABELS:Labels={operation:'OPERAÇÃO DO OLHAR',technique:'TÉCNICA VISUAL',techniques:n=>`${n} técnicas para explorar`,references:'Referências que usam esta técnica'};
export function TermPanel({data,labels=DEFAULT_LABELS,palette=colors,operation,technique,referenceIds,onTechnique,onOperation,onSelect,onClose}:{data:GraphData;labels?:Labels;palette?:Record<string,string>;operation:string;technique:string;referenceIds:Set<string>;onTechnique:(id:string)=>void;onOperation:(id:string)=>void;onSelect:(id:string)=>void;onClose:()=>void}){
 const [limit,setLimit]=useState(48);
 useEffect(()=>setLimit(48),[operation,technique]);
 const ts=terms(data.vocabulary,'tecnicas'),ops=terms(data.vocabulary,'operacoes');
 const term=technique?ts.find(t=>t.id===technique):ops.find(o=>o.id===operation);
 if(!term)return null;
 const op=ops.find(o=>o.id===(technique?term.operacao:operation));
 const cue=terms(data.vocabulary,'pistas').find(c=>c.id===term.pista);
 const linkedTechniques=ts.filter(t=>t.operacao===op?.id);
 const refs=data.items.filter(i=>referenceIds.has(i.id)).sort((a,b)=>b.strength-a.strength);
 return <aside className="detail-panel term-panel" aria-label={technique?labels.techniquePanel||'Detalhes da técnica':labels.operationPanel||'Detalhes do eixo'} style={{'--term-color':palette[op?.id||'']} as React.CSSProperties}>
  <div className="panel-heading"><span>{technique?labels.technique:labels.operation}</span><button onClick={onClose} aria-label="Fechar eixo"><X size={18}/></button></div>
  <div className="term-body">
   {technique&&op&&<button className="term-back" onClick={()=>onOperation(op.id)}><ArrowLeft size={13}/>{op.nome}</button>}
   <h2><i/>{term.nome||term.id}</h2>
   {cue&&<p className="term-meta">Pista: {cue.nome}</p>}
   <p className="term-definition">{term.def}</p>
   <p className="term-count">{refs.length.toLocaleString('pt-BR')} {labels.count||'referências conectadas no mapa'}</p>
   {technique?<>
    {term.html&&<section className="detail-section"><h3>Como fazer em HTML</h3><p>{term.html}</p></section>}
    <h3 className="term-section-title">{labels.references}</h3>
    <div className="term-references">{refs.slice(0,limit).map(item=><button className="result-row" key={item.id} onClick={()=>onSelect(item.id)}>{item.thumbnail&&<img src={sized(item.thumbnail,256)} alt="" loading="lazy"/>}<span><strong>{item.title}</strong><small>{item.idea||item.description}</small></span><ArrowUpRight size={14}/></button>)}</div>
    {refs.length>limit&&<button className="more-references" onClick={()=>setLimit(limit+48)}>Mostrar mais referências <ChevronRight size={14}/></button>}
   </>:<><h3 className="term-section-title">{labels.techniques(linkedTechniques.length)}</h3><div className="technique-index">{linkedTechniques.map(t=><button key={t.id} onClick={()=>onTechnique(t.id)}><span><i/>{t.nome||t.id}<ChevronRight size={14}/></span><p>{t.def}</p></button>)}</div></>}
  </div>
 </aside>;
}
