export type Reference={id:string;kind:string;title:string;origin:string;state:string;revision:number;ready:number;parent_id?:string;updated:string;description:string;idea:string;techniques:string[];intentions:string[];movements:string[];aesthetics:string[];strength:number;reusable:boolean|null;thumbnail?:string;url:string;format?:string;unclassified?:boolean;number?:number|null;matched_by?:string[]};
export type Asset={id:string;role:string;mime:string;missing:number;url:string};
export type Detail=Reference & {assets:Asset[];children:Reference[];related:Reference[];usage_notes:string;how?:string;html?:string;good_for?:string[];project_name?:string;source_reference_ids?:string[];unavailable_by_parent?:boolean};
export type Term={id:string;nome?:string;def:string;operacao?:string;pista?:string;html?:string};
export type Vocabulary=Record<string,{itens:(Term|string)[]}>;
export type GraphData={items:Reference[];vocabulary:Vocabulary};
export const terms=(v:Vocabulary|undefined,key:string):Term[]=>(v?.[key]?.itens||[]).filter((x):x is Term=>typeof x!=='string');
export const colors:Record<string,string>={diferenciacao:'#FF5A3C',agrupamento:'#3E7BFF',sequencia:'#F5B400',previsao:'#B455FF'};
export const kindName:Record<string,string>={arquivo:'Apresentação',slide:'Slide',referencia:'Referência',midia:'Mídia',criacao:'Criação'};
