import {useEffect,useState} from 'react';
import {ArrowLeft,ArrowUpRight,ChevronRight,X} from 'lucide-react';
import {colors,terms,type GraphData} from './types';
import {sized} from './api';

export function TermPanel({data,palette=colors,operation,technique,referenceIds,onTechnique,onOperation,onSelect,onClose}:{data:GraphData;palette?:Record<string,string>;operation:string;technique:string;referenceIds:Set<string>;onTechnique:(id:string)=>void;onOperation:(id:string)=>void;onSelect:(id:string)=>void;onClose:()=>void}){
 const [limit,setLimit]=useState(48);
 useEffect(()=>setLimit(48),[operation,technique]);
 const ts=terms(data.vocabulary,'tecnicas'),ops=terms(data.vocabulary,'operacoes');
 const term=technique?ts.find(t=>t.id===technique):ops.find(o=>o.id===operation);
 if(!term)return null;
 const op=ops.find(o=>o.id===(technique?term.operacao:operation));
 const cue=terms(data.vocabulary,'pistas').find(c=>c.id===term.pista);
 const linkedTechniques=ts.filter(t=>t.operacao===op?.id);
 const refs=data.items.filter(i=>referenceIds.has(i.id)).sort((a,b)=>b.strength-a.strength);
 return <aside className="detail-panel term-panel" aria-label={technique?'Detalhes da técnica':'Detalhes do eixo'} style={{'--term-color':palette[op?.id||'']} as React.CSSProperties}>
  <div className="panel-heading"><span>{technique?'TÉCNICA VISUAL':'OPERAÇÃO DO OLHAR'}</span><button onClick={onClose} aria-label="Fechar eixo"><X size={18}/></button></div>
  <div className="term-body">
   {technique&&op&&<button className="term-back" onClick={()=>onOperation(op.id)}><ArrowLeft size={13}/>{op.nome}</button>}
   <h2><i/>{term.nome||term.id}</h2>
   {cue&&<p className="term-meta">Pista: {cue.nome}</p>}
   <p className="term-definition">{term.def}</p>
   <p className="term-count">{refs.length.toLocaleString('pt-BR')} referências conectadas no mapa</p>
   {technique?<>
    {term.html&&<section className="detail-section"><h3>Como fazer em HTML</h3><p>{term.html}</p></section>}
    <h3 className="term-section-title">Referências que usam esta técnica</h3>
    <div className="term-references">{refs.slice(0,limit).map(item=><button className="result-row" key={item.id} onClick={()=>onSelect(item.id)}>{item.thumbnail&&<img src={sized(item.thumbnail,256)} alt="" loading="lazy"/>}<span><strong>{item.title}</strong><small>{item.idea||item.description}</small></span><ArrowUpRight size={14}/></button>)}</div>
    {refs.length>limit&&<button className="more-references" onClick={()=>setLimit(limit+48)}>Mostrar mais referências <ChevronRight size={14}/></button>}
   </>:<><h3 className="term-section-title">{linkedTechniques.length} técnicas para explorar</h3><div className="technique-index">{linkedTechniques.map(t=><button key={t.id} onClick={()=>onTechnique(t.id)}><span><i/>{t.nome||t.id}<ChevronRight size={14}/></span><p>{t.def}</p></button>)}</div></>}
  </div>
 </aside>;
}
